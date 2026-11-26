import json,os,random,urllib.request,urllib.error
EN=os.environ.get("MAKEFUN_ENV_URL","")
SF="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
P,N,B,R,Q,K=1,2,3,4,5,6
V=[0,100,320,330,500,900,0]
PR=(Q,R,B,N)
MT=100000
NF=MT+1
NB=100000
def z():
 T=[[0]*64 for _ in range(8)]
 ad=[0,2,6,12,20,32,48,0]
 ce=[0,0,0,12,18,12,6,0]
 km=[20,25,10,0,0,10,25,20]
 for r in range(8):
  for f in range(8):
   i=r*8+f
   c=min(f,7-f)+min(r,7-r)
   T[P][i]=ad[r]+(ce[r] if f in(3,4)else 0)
   T[N][i]=7*c-24
   T[B][i]=5*c-10
   T[R][i]=(20 if r==6 else 0)+(5 if r==0 and f in(3,4)else 0)
   T[Q][i]=3*c-8
   T[K][i]=km[f] if r==0 else max(-50,-15*r)
   T[7][i]=10*c-30
 return T
PST=z()
KM,KE=PST[K],PST[7]
_r=random.Random(7)
Z=[[_r.getrandbits(64)for _ in range(128)]for _ in range(16)]
ZS=_r.getrandbits(64)
ZC=[_r.getrandbits(64)for _ in range(16)]
ZE=[_r.getrandbits(64)for _ in range(8)]
S64=[s for s in range(128)if not s&0x88]
CR=[15]*128
CR[4]=12;CR[7]=14;CR[0]=13
CR[116]=3;CR[119]=11;CR[112]=7
BD=[0]*128
SD=CA=HM=HH=0
EP=-1
KP=[4,116]
U=[]
PS=set()
TT={}
KL=[0]*256
HI=[0]*16384
NN=0
AB=False
LM=0
def fen(f):
 global BD,SD,CA,EP,HM,HH
 BD=[0]*128
 w=f.split()
 for r,row in enumerate(w[0].split("/")):
  x=0
  for ch in row:
   if ch.isdigit():
    x+=int(ch)
   else:
    s=(7-r)*16+x
    t="pnbrqk".index(ch.lower())+1
    c=0 if ch.isupper()else 1
    BD[s]=t|(c<<3)
    if t==K:
     KP[c]=s
    x+=1
 SD=0 if w[1]=="w"else 1
 CA=0
 for i,ch in enumerate("KQkq"):
  if ch in w[2]:
   CA|=1<<i
 EP=-1
 if w[3]!="-":
  EP=(int(w[3][1])-1)*16+(ord(w[3][0])-97)
 HM=int(w[4])
 HH=0
 for s in S64:
  p=BD[s]
  if p:
   HH^=Z[p][s]
 if SD:
  HH^=ZS
 HH^=ZC[CA]
 if EP>=0:
  HH^=ZE[EP&7]
 del U[:]
def m2u(m):
 a=m&127
 b=(m>>7)&127
 s="abcdefgh"[a&7]+str((a>>4)+1)+"abcdefgh"[b&7]+str((b>>4)+1)
 p=(m>>14)&7
 return s+(" pnbrqk"[p] if p else "")
def u2m(u):
 a=(int(u[1])-1)*16+(ord(u[0])-97)
 b=(int(u[3])-1)*16+(ord(u[2])-97)
 p=" pnbrqk".index(u[4])if len(u)==5 else 0
 c=BD[a]
 if(c&7)==P:
  f=5 if b==EP and not BD[b]else(1 if BD[b]else 0)
  if abs(b-a)==32:
   f|=2
 else:
  f=(1 if BD[b]else 0)|(8 if(c&7)==K and abs(b-a)==2 else 0)
 return a|(b<<7)|(p<<14)|(f<<17)
def atk(s,by):
 bd=BD
 sg=1 if by else-1
 for dd in(15,17):
  t=s+sg*dd
  if not(t&0x88)and bd[t]==P|(by<<3):
   return True
 kn=N|(by<<3)
 for d in(-33,-31,-18,-14,14,18,31,33):
  t=s+d
  if not(t&0x88)and bd[t]==kn:
   return True
 kg=K|(by<<3)
 for d in(-17,-16,-15,-1,1,15,16,17):
  t=s+d
  if not(t&0x88)and bd[t]==kg:
   return True
 qu=Q|(by<<3)
 for d in(-17,-15,15,17,-16,-1,1,16):
  sl=B|(by<<3)if d in(-17,-15,15,17)else R|(by<<3)
  t=s+d
  while not(t&0x88):
   p=bd[t]
   if p:
    if p==sl or p==qu:
     return True
    break
   t+=d
 return False
def gen(cp=False):
 ms=[]
 ap=ms.append
 bd=BD
 for s in S64:
  p=bd[s]
  if not p or(p>>3)!=SD:
   continue
  t=p&7
  if t==P:
   d=16 if SD==0 else-16
   r=s>>4
   st=1 if SD==0 else 6
   pr=6 if SD==0 else 1
   o=s+d
   if not(o&0x88)and bd[o]==0:
    if r==pr:
     for q in PR:
      ap(s|(o<<7)|(q<<14))
    elif not cp:
     ap(s|(o<<7))
     if r==st and bd[s+2*d]==0:
      ap(s|((s+2*d)<<7)|(2<<17))
   for dd in(d-1,d+1):
    to=s+dd
    if to&0x88:
     continue
    q=bd[to]
    if q and(q>>3)!=SD and(q&7)!=K:
     if r==pr:
      for x in PR:
       ap(s|(to<<7)|(x<<14)|(1<<17))
     else:
      ap(s|(to<<7)|(1<<17))
    elif to==EP and EP>=0:
     ap(s|(to<<7)|(5<<17))
  elif t==N or t==K:
   stp=(-33,-31,-18,-14,14,18,31,33)if t==N else(-17,-16,-15,-1,1,15,16,17)
   for dd in stp:
    to=s+dd
    if to&0x88:
     continue
    q=bd[to]
    if not q:
     if not cp:
      ap(s|(to<<7))
    elif(q>>3)!=SD and(q&7)!=K:
     ap(s|(to<<7)|(1<<17))
   if t==K:
    for ca,ks,k2,rs,em,pa in((1,4,6,7,(5,6),(4,5,6)),(2,4,2,0,(3,2,1),(4,3,2)),(4,116,118,119,(117,118),(116,117,118)),(8,116,114,112,(115,114,113),(116,115,114))):
     if CA&ca and s==ks and bd[rs]==(R|(SD<<3))and not any(bd[x]for x in em)and not any(atk(x,SD^1)for x in pa):
      ap(ks|(k2<<7)|(8<<17))
  else:
   ds=(-17,-15,15,17)if t==B else(-16,-1,1,16)if t==R else(-17,-16,-15,-1,1,15,16,17)
   for dd in ds:
    to=s+dd
    while not(to&0x88):
     q=bd[to]
     if not q:
      if not cp:
       ap(s|(to<<7))
     else:
      if(q>>3)!=SD and(q&7)!=K:
       ap(s|(to<<7)|(1<<17))
      break
     to+=dd
 return ms
def mk(m):
 global SD,CA,EP,HM,HH
 a=m&127
 b=(m>>7)&127
 p=(m>>14)&7
 f=m>>17
 c=BD[a]
 oh=HH
 cap=0
 cs=-1
 if f&1:
  if f&4:
   cs=b-16 if SD==0 else b+16
   cap=BD[cs]
   BD[cs]=0
  else:
   cs=b
   cap=BD[b]
 HH^=Z[c][a]
 if cap:
  HH^=Z[cap][cs]
 np=(p|(SD<<3))if p else c
 BD[b]=np
 BD[a]=0
 HH^=Z[np][b]
 if f&8:
  rf,rt=(b+1,b-1)if b in(6,118)else(b-2,b+1)
  rk=BD[rf]
  BD[rt]=rk
  BD[rf]=0
  HH^=Z[rk][rf]^Z[rk][rt]
 if(c&7)==K:
  KP[SD]=b
 oc=CA
 CA&=CR[a]&CR[b]
 if oc!=CA:
  HH^=ZC[oc]^ZC[CA]
 oe=EP
 EP=-1
 if f&2:
  if BD[b-1]==(P|((SD^1)<<3))or BD[b+1]==(P|((SD^1)<<3)):
   EP=(a+b)//2
 if oe>=0:
  HH^=ZE[oe&7]
 if EP>=0:
  HH^=ZE[EP&7]
 om=HM
 HM=0 if(c&7)==P or cap else HM+1
 HH^=ZS
 U.append((m,cap,cs,oc,oe,om,oh))
 SD^=1
 if atk(KP[SD^1],SD):
  un()
  return False
 return True
def un():
 global SD,CA,EP,HM,HH
 m,cap,cs,oc,oe,om,oh=U.pop()
 SD^=1
 a=m&127
 b=(m>>7)&127
 p=(m>>14)&7
 f=m>>17
 BD[a]=(P|(SD<<3))if p else BD[b]
 BD[b]=0
 if cap:
  BD[cs]=cap
 if f&8:
  rf,rt=(b+1,b-1)if b in(6,118)else(b-2,b+1)
  BD[rf]=BD[rt]
  BD[rt]=0
 if not p and(BD[a]&7)==K:
  KP[SD]=a
 CA=oc
 EP=oe
 HM=om
 HH=oh
def ev():
 s=0
 np=0
 b0=b1=k0=k1=0
 pf=[[0]*8,[0]*8]
 hi=[[-1]*8,[-1]*8]
 lo=[[9]*8,[9]*8]
 pw=[[],[]]
 bd=BD
 for q in S64:
  p=bd[q]
  if not p:
   continue
  t=p&7
  if t==K:
   if p<8:
    k0=(q>>4)*8+(q&7)
   else:
    k1=(7-(q>>4))*8+(q&7)
   continue
  r=(q>>4)*8+(q&7)if p<8 else(7-(q>>4))*8+(q&7)
  v=V[t]+PST[t][r]
  if p<8:
   s+=v
  else:
   s-=v
  if t==P:
   c=0 if p<8 else 1
   f=q&7
   rw=q>>4
   pf[c][f]+=1
   if rw>hi[c][f]:
    hi[c][f]=rw
   if rw<lo[c][f]:
    lo[c][f]=rw
   pw[c].append((f,rw))
  else:
   np+=V[t]
   if t==B:
    if p<8:
     b0+=1
    else:
     b1+=1
 ph=np if np<6400 else 6400
 eg=6400-ph
 s+=(KM[k0]*ph+KE[k0]*eg)//6400
 s-=(KM[k1]*ph+KE[k1]*eg)//6400
 s+=30*((b0>=2)-(b1>=2))
 for c in(0,1):
  sg=1 if c==0 else-1
  for f,rw in pw[c]:
   if pf[c][f]>1:
    s-=8*sg
   if(f==0 or pf[c][f-1]==0)and(f==7 or pf[c][f+1]==0):
    s-=10*sg
   ps=True
   for g in(f-1,f,f+1):
    if 0<=g<8 and(hi[1][g]>rw if c==0 else lo[0][g]<rw):
     ps=False
     break
   if ps:
    s+=(12+8*(rw if c==0 else 7-rw))*sg
 return s if SD==0 else-s
def srt(ms,pl,tm):
 k0=KL[pl*2]
 k1=KL[pl*2+1]
 sc=[]
 bd=BD
 for m in ms:
  s=0
  f=m>>17
  if f&1:
   vt=P if f&4 else bd[(m>>7)&127]&7
   s=100000+10*V[vt]-V[bd[m&127]&7]
  p=(m>>14)&7
  if p:
   s+=200000+V[p]
  if not s:
   s=50000 if m==k0 else 40000 if m==k1 else min(HI[m&16383],30000)
  if m==tm:
   s=1000000
  sc.append((s,m))
 sc.sort(reverse=True)
 return[m for _,m in sc]
def qs(al,be,pl):
 global NN,AB
 NN+=1
 if LM and NN>=LM:
  AB=True
  return 0
 if AB:
  return 0
 if pl>=120:
  return ev()
 ck=atk(KP[SD],SD^1)
 if not ck:
  s=ev()
  if s>=be:
   return s
  best=s
  if s>al:
   al=s
 else:
  best=-NF
 ms=srt(gen(cp=not ck),pl,0)
 lg=0
 for m in ms:
  if not mk(m):
   continue
  lg+=1
  s=-qs(-be,-al,pl+1)
  un()
  if AB:
   return 0
  if s>best:
   best=s
  if s>=be:
   return s
  if s>al:
   al=s
 if ck and lg==0:
  return-MT+pl
 return best
def sr(dp,al,be,pl,nn=0):
 global NN,AB,SD,EP,HM,HH
 if pl>0 and(HM>=100 or HH in PS):
  return 0
 if dp<=0 or pl>=120:
  return qs(al,be,pl)
 NN+=1
 if LM and NN>=LM:
  AB=True
  return 0
 if AB:
  return 0
 e=TT.get(HH)
 tm=0
 if e:
  d,f,s,m=e
  if d>=dp:
   if s>MT-1000:
    s-=pl
   elif s<-(MT-1000):
    s+=pl
   if f==0:
    return s
   if f==1 and s>=be:
    return s
   if f==2 and s<=al:
    return s
  tm=m
 ck=atk(KP[SD],SD^1)
 if ck:
  dp+=1
 if dp==1 and not ck:
  fe=ev()
  if fe+250<=al:
   return fe
 if dp>=3 and not ck and not nn and pl>0:
  oe=EP
  om=HM
  oh=HH
  HH^=ZS
  if oe>=0:
   HH^=ZE[oe&7]
  EP=-1
  HM+=1
  SD^=1
  s=-sr(dp-3,-be,-be+1,pl+1,1)
  SD^=1
  EP=oe
  HM=om
  HH=oh
  if AB:
   return 0
  if s>=be:
   return s
 a0=al
 PS.add(HH)
 ms=srt(gen(),pl,tm)
 lg=0
 best=-NF
 bm=0
 for i,m in enumerate(ms):
  if not mk(m):
   continue
  lg+=1
  if i>=3 and dp>=3 and not ck and not(m>>17)&1 and not(m>>14)&7 and m!=KL[pl*2]and m!=KL[pl*2+1]:
   s=-sr(dp-2,-be,-al,pl+1)
   if not AB and s>al:
    s=-sr(dp-1,-be,-al,pl+1)
  else:
   s=-sr(dp-1,-be,-al,pl+1)
  un()
  if AB:
   PS.discard(HH)
   return 0
  if s>best:
   best=s
   bm=m
  if s>al:
   al=s
  if al>=be:
   if not(m>>17)&1 and not(m>>14)&7:
    HI[m&16383]+=dp*dp
    if KL[pl*2]!=m:
     KL[pl*2+1]=KL[pl*2]
     KL[pl*2]=m
   break
 PS.discard(HH)
 if lg==0:
  return-MT+pl if atk(KP[SD],SD^1)else 0
 sc=best
 if sc>MT-1000:
  sc+=pl
 elif sc<-(MT-1000):
  sc-=pl
 f=2 if best<=a0 else(1 if best>=be else 0)
 TT[HH]=(dp,f,sc,bm)
 return best
def root(lg):
 global TT,KL,NN,AB,LM,HI
 TT={}
 KL=[0]*256
 HI=[0]*16384
 if len(lg)==1:
  return u2m(lg[0])
 ms=[u2m(u)for u in lg]
 sc={}
 best=ms[0]
 NN=0
 AB=False
 for d in range(1,40):
  LM=0 if d==1 else NB
  ms.sort(key=lambda m:-sc.get(m,0))
  al=-NF
  cur=best
  cs=-NF
  for m in ms:
   if not mk(m):
    continue
   s=-sr(d-1,-NF,-al,1)
   un()
   if AB:
    break
   sc[m]=s
   if s>cs:
    cs=s
    cur=m
   if s>al:
    al=s
  if AB:
   break
  best=cur
  if cs>=MT-100:
   break
 return best
def po(pa,bo):
 try:
  with urllib.request.urlopen(EN+pa,json.dumps(bo).encode())as r:
   return json.load(r)
 except urllib.error.HTTPError as e:
  raise SystemExit(pa)
def rep(mv):
 fen(SF)
 h={HH}
 for u in mv:
  if not mk(u2m(u)):
   break
  h.add(HH)
 return h
if __name__=="__main__":
 while True:
  g=po("/game",{})
  if g["status"]=="done":
   break
  while g["status"]=="your_move":
   gh=rep(g["moves"])
   fen(g["fen"])
   PS=set(gh)
   m=root(g["legal_moves"])
   g=po("/move",{"game":g["game"],"move":m2u(m)})
