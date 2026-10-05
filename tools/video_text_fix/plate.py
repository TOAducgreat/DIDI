import cv2, numpy as np, sys
def corners(img, box, thr=600, close=3):
    x0,y0,x1,y1=box; roi=img[y0:y1,x0:x1]
    m=(roi.astype(int).sum(2)>thr).astype(np.uint8)*255
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((close,close),np.uint8))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    c=max(cs,key=cv2.contourArea)
    hull=cv2.convexHull(c).reshape(-1,2).astype(float)
    # pick extreme corners: TL,TR,BR,BL via sums/diffs
    s=hull.sum(1); d=hull[:,0]-hull[:,1]
    q=np.array([hull[s.argmin()],hull[d.argmax()],hull[s.argmax()],hull[d.argmin()]])
    return q+[x0,y0], m
if __name__=='__main__':
    import fix
    fx=fix.load('C1'); cap=cv2.VideoCapture('C1.mp4'); ok,f=cap.read(); f=fx.apply(f,0)
    q,m=corners(f,(640,1680,1000,1795))
    print('C1 plate corners',q.round(1).tolist())
    x0,y0=int(q[:,0].min())-6,int(q[:,1].min())-6; x1,y1=int(q[:,0].max())+7,int(q[:,1].max())+7
    tpl=f[y0:y1,x0:x1].copy(); cv2.imwrite('plate_tpl.png',tpl)
    np.save('plate_tpl_q.npy',q-[x0,y0])
    v=tpl.copy(); cv2.polylines(v,[np.round((q-[x0,y0])).astype(np.int32)],True,(0,0,255),1)
    cv2.imwrite('plate_tpl_dbg.png',cv2.resize(v,None,fx=3,fy=3,interpolation=cv2.INTER_NEAREST))
