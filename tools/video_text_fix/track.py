import cv2, numpy as np, json, sys
def track(video, regions, ref=0, scale=1.0, iters=100):
    """regions: {name: (x0,y0,x1,y1)} in ref-frame full-res coords.
    returns {name: [2x3 affine ref->frame, ...]} for every frame."""
    cap=cv2.VideoCapture(video); frames=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        frames.append(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY))
    g=lambda i: cv2.resize(frames[i],None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA) if scale!=1 else frames[i]
    out={}; scores={}
    R=g(ref).astype(np.float32)
    for name,(x0,y0,x1,y1) in regions.items():
        o=np.array([x0,y0],float)
        T=R[int(y0*scale):int(y1*scale),int(x0*scale):int(x1*scale)]
        res=[None]*len(frames); sc=[0]*len(frames)
        crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,iters,1e-5)
        for direction in (range(ref,len(frames)),range(ref,-1,-1)):
            W=np.array([[1,0,x0*scale],[0,1,y0*scale]],np.float32)
            for i in direction:
                I=g(i).astype(np.float32)
                try:
                    cc,W=cv2.findTransformECC(T,I,W.copy(),cv2.MOTION_AFFINE,crit,None,5)
                except cv2.error as e:
                    cc=-1
                L=W[:,:2].astype(float); t=W[:,2].astype(float)/scale
                A=np.hstack([L,(t-L@o)[:,None]])
                res[i]=A; sc[i]=cc
        out[name]=res; scores[name]=sc
    return out,scores
def smooth(As,win=5):
    a=np.array(As); k=win//2; o=a.copy()
    for i in range(len(a)):
        o[i]=a[max(0,i-k):i+k+1].mean(0)
    return list(o)
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1])); 
    out,sc=track(cfg['video'],{k:tuple(v) for k,v in cfg['regions'].items()},cfg.get('ref',0),cfg.get('scale',1.0))
    for k in out: print(k,'min cc %.3f mean %.3f'%(min(sc[k]),np.mean(sc[k])), 'worst frames',np.argsort(sc[k])[:5])
    json.dump({k:[a.tolist() for a in v] for k,v in out.items()},open(sys.argv[2],'w'))
