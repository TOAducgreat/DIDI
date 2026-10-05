"""Per-frame text replacement: erase old text inside tracked zones, draw new text."""
import cv2, numpy as np, json
import textfx


class Fixer:
    def __init__(self, cfg, trk):
        self.cfg = cfg
        self.trk = {k: [np.array(a) for a in v] for k, v in trk.items()}
        win = cfg.get('smooth', 5)
        for k in self.trk:
            a = np.array(self.trk[k]); s = a.copy(); h = win // 2
            for i in range(len(a)):
                s[i] = a[max(0, i - h):i + h + 1].mean(0)
            self.trk[k] = list(s)
        self.patches = []
        for ov in cfg.get('overlays', []):
            if ov['type'] == 'plate':
                self.patches.append((ov, self._plate(ov)))
            else:
                self.patches.append((ov, textfx.render(ov, ov['bbox'])))

    @staticmethod
    def _plate(ov):
        tpl = cv2.imread(ov.get('tpl', 'plate_tpl.png')).astype(np.float32)
        qt = np.load(ov.get('tpl_q', 'plate_tpl_q.npy'))
        qr = np.array(ov['quad'], float)
        side = lambda q: (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2
        sc = min(1.0, side(qr) / side(qt) * 1.5)  # pre-shrink, keep 1.5x for the warp
        tpl = cv2.resize(tpl, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        qt = qt * sc
        a = np.zeros(tpl.shape[:2], np.float32)
        cv2.fillPoly(a, [np.round(qt * 8).astype(np.int32)], 1.0, lineType=cv2.LINE_AA, shift=3)
        e = ov.get('expand', 0.6) * 1.5
        if e > 0:
            a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=max(1, int(round(e))))
        a = cv2.GaussianBlur(a, (0, 0), 0.6)
        tpl = tpl * ov.get('gain', 1.0)
        rgba = np.dstack([tpl * a[..., None], a])
        H0 = cv2.getPerspectiveTransform(qt.astype(np.float32), qr.astype(np.float32))
        return (rgba, H0, qt)

    @staticmethod
    def _warp_roi(A, bbox, shape, pad=4):
        x0, y0, x1, y1 = bbox
        pts = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)
        q = pts @ A[:, :2].T + A[:, 2]
        fx0 = max(0, int(np.floor(q[:, 0].min())) - pad); fy0 = max(0, int(np.floor(q[:, 1].min())) - pad)
        fx1 = min(shape[1], int(np.ceil(q[:, 0].max())) + pad); fy1 = min(shape[0], int(np.ceil(q[:, 1].max())) + pad)
        return fx0, fy0, fx1, fy1

    def apply(self, frame, i):
        f = frame
        for er in self.cfg.get('erase', []):
            A = self.trk[er['track']][i]
            poly = np.array(er['zone'], float)
            q = poly @ A[:, :2].T + A[:, 2]
            bb = (int(poly[:, 0].min()), int(poly[:, 1].min()), int(poly[:, 0].max()) + 1, int(poly[:, 1].max()) + 1)
            fx0, fy0, fx1, fy1 = self._warp_roi(A, bb, f.shape, pad=er.get('inpaint_r', 5) * 3)
            roi = f[fy0:fy1, fx0:fx1]
            zone = np.zeros(roi.shape[:2], np.uint8)
            cv2.fillPoly(zone, [np.round((q - [fx0, fy0]) * 8).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=3)
            zone = (zone > 127).astype(np.uint8) * 255
            if er.get('thr') is not None:
                lum = roi.astype(np.int32).sum(2)
                if er.get('mode', 'bright') == 'bright':
                    m = (lum > er['thr']).astype(np.uint8) * 255
                else:
                    m = (lum < er['thr']).astype(np.uint8) * 255
                d = er.get('dilate', 2)
                if d:
                    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * d + 1, 2 * d + 1)))
                m &= zone
            else:
                m = zone
            if er.get('fill') == 'plane':
                # fit a smooth colour plane to a ring just inside/around the zone, fill + grain
                k = er.get('ring', 4)
                ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))
                gap = er.get('ring_gap', 2)
                ring = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * (k + gap) + 1,) * 2)) & ~cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * gap + 1,) * 2))
                if er.get('ring_mask') is not None:
                    pass
                ys, xs = np.where(ring > 0)
                X = np.stack([np.ones_like(xs), xs, ys, xs * ys, xs ** 2, ys ** 2], 1).astype(np.float64)
                X[:, 1:] /= 100.0; X[:, 3:] /= 100.0
                vals = roi[ys, xs].astype(np.float64)
                lum = vals.sum(1); med = np.median(lum); mad = np.median(abs(lum - med)) + 1
                keep = abs(lum - med) < 2.5 * mad
                X, vals = X[keep], vals[keep]
                coef, *_ = np.linalg.lstsq(X, vals, rcond=None)
                resid = (vals - X @ coef).std(0)
                yy, xx = np.where(m > 0)
                Xf = np.stack([np.ones_like(xx), xx, yy, xx * yy, xx ** 2, yy ** 2], 1).astype(np.float64)
                Xf[:, 1:] /= 100.0; Xf[:, 3:] /= 100.0
                g = er.get('grain', 0.8)
                noise = cv2.GaussianBlur(np.random.normal(0, 1, roi.shape[:2]).astype(np.float32), (0, 0), 0.8)
                noise = noise / (noise.std() + 1e-6)
                fillv = Xf @ coef + noise[yy, xx][:, None] * g
                soft = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1.0)
                new = roi.astype(np.float32).copy(); new[yy, xx] = fillv
                roi[:] = np.clip(new * soft[..., None] + roi * (1 - soft[..., None]), 0, 255).astype(np.uint8)
            else:
                roi[:] = cv2.inpaint(roi, m, er.get('inpaint_r', 5), cv2.INPAINT_TELEA)
        for ov, patch in self.patches:
            A = self.trk[ov['track']][i]
            if ov['type'] == 'plate':
                rgba, H0, qt = patch
                M = np.vstack([A, [0, 0, 1]]) @ H0
                q = cv2.perspectiveTransform(qt.reshape(-1, 1, 2).astype(np.float32), M).reshape(-1, 2)
                fx0 = max(0, int(q[:, 0].min()) - 4); fy0 = max(0, int(q[:, 1].min()) - 4)
                fx1 = min(f.shape[1], int(q[:, 0].max()) + 5); fy1 = min(f.shape[0], int(q[:, 1].max()) + 5)
                T = np.array([[1, 0, -fx0], [0, 1, -fy0], [0, 0, 1]], float)
                w = cv2.warpPerspective(rgba, T @ M, (fx1 - fx0, fy1 - fy0), flags=cv2.INTER_LINEAR)
                s_ = ov.get('blur', 0.6)
                if s_ > 0:
                    w = cv2.GaussianBlur(w, (0, 0), s_)
                roi = f[fy0:fy1, fx0:fx1].astype(np.float32)
                roi = w[..., :3] + roi * (1 - w[..., 3:4])
                f[fy0:fy1, fx0:fx1] = np.clip(roi, 0, 255).astype(np.uint8)
                continue
            x0, y0, x1, y1 = ov['bbox']
            fx0, fy0, fx1, fy1 = self._warp_roi(A, ov['bbox'], f.shape)
            M = A @ np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], float)
            M[:, 2] -= [fx0, fy0]
            w = cv2.warpAffine(patch, M, (fx1 - fx0, fy1 - fy0), flags=cv2.INTER_LINEAR)
            s = ov.get('blur', 0.7)
            if s > 0:
                w = cv2.GaussianBlur(w, (0, 0), s)
            roi = f[fy0:fy1, fx0:fx1].astype(np.float32)
            a = w[..., 3:4]
            roi = w[..., :3] + roi * (1 - a)
            if ov.get('noise', 0):
                n = np.random.normal(0, ov['noise'], roi.shape[:2])[..., None] * a
                roi += n
            f[fy0:fy1, fx0:fx1] = np.clip(roi, 0, 255).astype(np.uint8)
        return f


def load(name):
    cfg = json.load(open(f'cfg_{name}.json'))
    trk = json.load(open(f'trk_{name}.json'))
    return Fixer(cfg, trk)


if __name__ == '__main__':
    import sys
    name = sys.argv[1]; times = [float(t) for t in sys.argv[2].split(',')]
    crop = [int(v) for v in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
    fx = load(name)
    cap = cv2.VideoCapture(fx.cfg['video'])
    rows = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * 24)); ok, fr = cap.read()
        i = int(t * 24)
        before = fr.copy(); after = fx.apply(fr, i)
        if crop:
            # crop follows the first track
            A = fx.trk[sys.argv[4] if len(sys.argv) > 4 else list(fx.trk)[0]][i]
            cx, cy = A[:, :2] @ np.array([(crop[0] + crop[2]) / 2, (crop[1] + crop[3]) / 2]) + A[:, 2]
            w, h = crop[2] - crop[0], crop[3] - crop[1]
            xa, ya = int(cx - w / 2), int(cy - h / 2)
            before = before[ya:ya + h, xa:xa + w]; after = after[ya:ya + h, xa:xa + w]
            sc = 3 if w < 400 else 1
            before = cv2.resize(before, None, fx=sc, fy=sc, interpolation=cv2.INTER_CUBIC)
            after = cv2.resize(after, None, fx=sc, fy=sc, interpolation=cv2.INTER_CUBIC)
        row = np.hstack([before, after])
        cv2.putText(row, f'{name} t={t}', (8, 30), 0, 1, (0, 255, 255), 2)
        rows.append(row)
    cv2.imwrite(f'prev_{name}_{sys.argv[4] if len(sys.argv)>4 else "full"}.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
