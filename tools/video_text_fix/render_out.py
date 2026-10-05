import cv2, numpy as np, json, subprocess, sys, librosa
import fix
OFPS=24; CUT=9.48
VLEN=librosa.get_duration(path='voice.mp3')
N=int(round(VLEN*OFPS))
shots={'Toan':('T1','T2'),'Trung':('M1','M2'),'Can':('C2','C1')}
name=sys.argv[1]; first,second=shots[name]
maps=json.load(open('timemap.json'))
def src_index(c,t):
    g=np.array(maps[c]['grid']); m=np.array(maps[c]['map'])
    st=np.interp(t,g,m,left=m[0]+(t-g[0]),right=m[-1]+(t-g[-1]))
    return int(np.clip(round(st*OFPS),0,239))
plan=[]
for k in range(N):
    t=k/OFPS; c=first if t<CUT else second
    plan.append((c,src_index(c,t)))
# enforce monotonic per clip
for c in (first,second):
    idx=[i for i,(cc,_) in enumerate(plan) if cc==c]; last=-1
    for i in idx:
        s=max(plan[i][1],last); plan[i]=(c,s); last=s
out=f'../out/S07_{name}.mp4'
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','3840x2160','-r',str(OFPS),'-i','-',
    '-i','voice.mp3','-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','192k','-ar','48000','-t',f'{VLEN:.3f}','-movflags','+faststart',out],stdin=subprocess.PIPE)
fixers={c:fix.load(c) for c in (first,second)}
caps={c:cv2.VideoCapture(c+'.mp4') for c in (first,second)}
cur={c:-1 for c in (first,second)}; frm={c:None for c in (first,second)}
dups=0
for k,(c,s) in enumerate(plan):
    if cur[c]==s: dups+=1
    while cur[c]<s:
        ok,f=caps[c].read(); cur[c]+=1
        if cur[c]==s:
            frm[c]=fixers[c].apply(f,s)
    ff.stdin.write(frm[c].tobytes())
ff.stdin.close(); ff.wait()
used={c:sorted(set(s for cc,s in plan if cc==c)) for c in (first,second)}
print(name,'frames',N,'dups',dups,{c:(u[0],u[-1]) for c,u in used.items()},'->',out)
json.dump(plan,open(f'plan_{name}.json','w'))
