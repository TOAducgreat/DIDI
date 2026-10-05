import cv2,sys
a=sys.argv; c=a[1]; fr=int(a[2]); x0,y0,x1,y1,step=map(int,a[3:8]); scale=float(a[8]); out=a[9]
cap=cv2.VideoCapture(c+'.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,fr); ok,f=cap.read()
im=f[y0:y1,x0:x1].copy(); im=cv2.resize(im,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
for x in range((x0//step+1)*step,x1,step):
    X=int((x-x0)*scale); cv2.line(im,(X,0),(X,im.shape[0]),(0,255,0),1); cv2.putText(im,str(x),(X+2,14),0,0.45,(0,255,0),1)
for y in range((y0//step+1)*step,y1,step):
    Y=int((y-y0)*scale); cv2.line(im,(0,Y),(im.shape[1],Y),(0,255,0),1); cv2.putText(im,str(y),(2,Y-2),0,0.45,(0,255,0),1)
cv2.imwrite(out,im)
