import numpy as np, librosa, json
from scipy.ndimage import gaussian_filter1d
HOP=160; SR=16000; FPS=SR/HOP
CUT=9.48; VLEN=librosa.get_duration(path='voice.mp3'); OFPS=24
def feat(y):
    m=librosa.feature.mfcc(y=y,sr=SR,n_mfcc=20,hop_length=HOP,n_fft=512)[1:]
    return (m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6)
def energy(y):
    return librosa.feature.rms(y=y,frame_length=512,hop_length=HOP)[0]
vy,_=librosa.load('voice.wav',sr=SR)
plan={'first':(0.0,CUT+0.6,['T1','M1','C2']),'second':(CUT-0.6,VLEN,['T2','M2','C1'])}
maps={}
for half,(va,vb,clips) in plan.items():
    seg=vy[int(va*SR):int(vb*SR)]; V=feat(seg); ve=energy(seg)
    for c in clips:
        cy,_=librosa.load(c+'.wav',sr=SR); X=feat(cy); ce=energy(cy)
        D,wp=librosa.sequence.dtw(V,X,metric='cosine'); wp=wp[::-1]
        vt=wp[:,0]/FPS+va; ct=wp[:,1]/FPS
        sp=(ve[np.minimum(wp[:,0],len(ve)-1)]>0.25*ve.max()*0.3)&(ce[np.minimum(wp[:,1],len(ce)-1)]>ce.max()*0.075)
        # raw map on output grid (speech anchors only)
        grid=np.arange(va,vb,1/OFPS)
        raw=np.interp(grid,vt[sp],ct[sp])
        sm=gaussian_filter1d(raw,sigma=0.3*OFPS)
        d=np.diff(sm,prepend=sm[0]-1/OFPS)*OFPS
        d=np.clip(d,0.8,1.25)
        m=np.cumsum(d)/OFPS; m+=np.median(raw-m)
        err=np.abs(m-raw)
        maps[c]=dict(grid=grid.tolist(),map=m.tolist())
        print(f'{c}: voice {va:.2f}-{vb:.2f}  clip@start {m[0]:.2f} clip@end {m[-1]:.2f}  speed min {d.min():.2f} max {d.max():.2f} | |map-raw| mean {err.mean()*1000:.0f}ms p95 {np.percentile(err,95)*1000:.0f}ms')
json.dump(maps,open('timemap.json','w'))
