import json,os,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL")
T="__TABLES__"
L=[[0]*64 for _ in range(7)]
e=[[0]*64 for _ in range(7)]
for p in range(1,7):
 b=(p-1)*128
 for s in range(64):
  L[p][s]=16*(ord(T[b+s])-64)
  e[p][s]=L[p][s]+16*(ord(T[b+64+s])-64)
m=[0,82,337,365,477,1025,0]
v=[0,94,281,297,512,936,0]
h=[0,0,1,1,2,4,0]
w=[0,0,10,20,40,70,110,160,0]
y={21:2,28:1,91:8,98:4}
n=[-21,-19,-12,-8,8,12,19,21]
P=[-11,-9,9,11]
J=[-10,-1,1,10]
M=P+J
I=1000000
W=[0,0]
V=[0,0]
B=[7]*120
S=0
C=0
E=-1
Z=0
A=0
D=0
Y=0
K=[0,0]
_x=0x9e3779b97f4a7c15
def rnd():
 global _x
 _x=(_x*6364136223846793005+1442695040888963407)&((1<<64)-1)
 return _x
H=[[rnd() for _ in range(120)] for _ in range(13)]
Q=rnd()
X=[rnd() for _ in range(4)]
G=[rnd() for _ in range(8)]
def g(i):
 return (i//10-2)*8+(i%10-1)
q={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':-1,'n':-2,'b':-3,'r':-4,'q':-5,'k':-6}
def upd(p,sq,sgn):
 global A,D,Y
 pt=abs(p);sg=sgn if p>0 else -sgn;q=sq if p>0 else sq^56
 Y+=sgn*h[pt]
 A+=sg*(m[pt]+L[pt][q]);D+=sg*(v[pt]+e[pt][q])
def setup(fen):
 global B,S,C,E,Z,A,D,Y,K,W,V
 B=[7]*120
 for i in range(21,99):
  if 0<i%10<9:B[i]=0
 Z=0;A=0;D=0;Y=0;K=[0,0];W=[0,0];V=[0,0]
 parts=fen.split()
 rows=parts[0].split('/')
 for ri,row in enumerate(rows):
  r=9-ri
  f=1
  for ch in row:
   if ch.isdigit():
    f+=int(ch)
   else:
    p=q[ch]
    i=r*10+f
    B[i]=p
    s=g(i)
    upd(p,s,1)
    if abs(p)==6:K[p<0]=i
    if p==1:W[0]|=1<<s
    elif p==-1:W[1]|=1<<s
    elif p==3:V[0]+=1
    elif p==-3:V[1]+=1
    Z^=H[p+6][i]
    f+=1
 S=parts[1]!='w'
 if S:Z^=Q
 C=0
 if len(parts)>2:
  for ch in parts[2]:C|={'K':1,'Q':2,'k':4,'q':8}.get(ch,0)
 for b in range(4):
  if C>>b&1:Z^=X[b]
 E=-1
 if len(parts)>3 and parts[3]!='-':
  E=k(parts[3])
  Z^=G[(E%10)-1]
def l(sq,w):
 if w:
  if B[sq-9]==1 or B[sq-11]==1:return 1
 else:
  if B[sq+9]==-1 or B[sq+11]==-1:return 1
 for o in n:
  if B[sq+o]==(2 if w else -2):return 1
 for o in M:
  if B[sq+o]==(6 if w else -6):return 1
 for o in P:
  i=sq+o
  while B[i]!=7:
   if B[i]!=0:
    if B[i]==(3 if w else -3) or B[i]==(5 if w else -5):return 1
    break
   i+=o
 for o in J:
  i=sq+o
  while B[i]!=7:
   if B[i]!=0:
    if B[i]==(4 if w else -4) or B[i]==(5 if w else -5):return 1
    break
   i+=o
 return 0
i=[]
R={}
def make(m):
 global S,C,E,Z,A,D,Y,K,W,V
 okp=K[:]
 oE,oZ,oA,oD,oY,oPB=E,Z,A,D,Y,W[:]
 f=m&127;t=(m>>7)&127;p=(m>>14)&7
 pc=B[f];cap=B[t];epc=0;epc_sq=-1
 if abs(pc)==1 and cap==0 and (t-f) in (9,11,-9,-11):
  epc_sq=t-10 if pc>0 else t+10
  epc=B[epc_sq]
 Z^=H[pc+6][f];Z^=H[pc+6][t]
 if cap:Z^=H[cap+6][t]
 if epc:Z^=H[epc+6][epc_sq]
 Z^=Q
 oc=C
 s1=g(f);s2=g(t);pt=abs(pc)
 upd(pc,s1,-1)
 if cap:upd(cap,s2,-1)
 if epc:upd(epc,g(epc_sq),-1)
 if pt==1:
  W[pc<0]&=~(1<<s1)
  if not p:W[pc<0]|=1<<s2
 if abs(cap)==1:W[cap<0]&=~(1<<s2)
 if epc:W[epc<0]&=~(1<<g(epc_sq))
 if abs(cap)==3:V[cap<0]-=1
 if p==3:V[pc<0]+=1
 B[f]=0;B[t]=pc
 if epc:B[epc_sq]=0
 np=pc
 if p:
  np=p if pc>0 else -p
  B[t]=np
  upd(np,s2,1)
 else:
  upd(pc,s2,1)
 if pt==6:
  K[pc<0]=t
  if abs(t-f)==2:
   d=t-f
   rf,rt=(t+1,t-1) if d==2 else (t-2,t+1)
   rp=B[rf];B[rf]=0;B[rt]=rp
   Z^=H[rp+6][rf];Z^=H[rp+6][rt]
   upd(rp,g(rf),-1);upd(rp,g(rt),1)
  if pc>0:C&=~3
  else:C&=~12
 C&=~y.get(f,0);C&=~y.get(t,0)
 for b in range(4):
  if (oc>>b&1)!=(C>>b&1):Z^=X[b]
 if E!=-1:Z^=G[(E%10)-1]
 E=-1
 if pt==1 and abs(t-f)==20:
  E=f+10 if pc>0 else f-10
  Z^=G[(E%10)-1]
 S=1-S
 R[Z]=R.get(Z,0)+1
 i.append((m,cap,epc,epc_sq,oc,oE,oZ,oA,oD,oY,pc,okp,oPB))
def z():
 global S,C,E,Z,A,D,Y,K,W,V
 m,cap,epc,epc_sq,oc,oE,oZ,oA,oD,oY,pc,okp,oPB=i.pop()
 R[Z]-=1
 f=m&127;t=(m>>7)&127;p=(m>>14)&7
 S=1-S
 B[f]=pc;B[t]=cap
 if epc:B[epc_sq]=epc
 if abs(pc)==6 and abs(t-f)==2:
  if t>f:
   B[t+1]=B[t-1];B[t-1]=0
  else:
   B[t-2]=B[t+1];B[t+1]=0
 C=oc;E=oE;Z=oZ;A=oA;D=oD;Y=oY;K[:]=okp;W[:]=oPB
 if abs(cap)==3:V[cap<0]+=1
 if p==3:V[pc<0]-=1
def k(s):
 return (int(s[1])+1)*10+'abcdefgh'.index(s[0])+1
def uci_mv(u):
 f=k(u[:2]);t=k(u[2:4]);p=0
 if len(u)==5:p=q[u[4].upper()]
 return f|(t<<7)|(p<<14)
def mv_uci(m):
 f=m&127;t=(m>>7)&127;p=(m>>14)&7
 return 'abcdefgh'[f%10-1]+str(f//10-1)+'abcdefgh'[t%10-1]+str(t//10-1)+('nbrq'[p-2] if p else '')
def gen():
 ms=[];w=(S==0)
 for i in range(21,99):
  p=B[i]
  if p==0 or p==7 or (p>0)!=w:continue
  pt=abs(p)
  if pt==1:
   d=10 if w else -10;lr=9 if w else 2
   t=i+d
   if B[t]==0:
    if t//10==lr:
     for q in (5,4,3,2):ms.append(i|(t<<7)|(q<<14))
    else:
     ms.append(i|(t<<7))
     t2=i+2*d
     if i//10==(3 if w else 8) and B[t2]==0:ms.append(i|(t2<<7))
   for dd in (9,11) if w else (-9,-11):
    t=i+dd
    if B[t]==7:continue
    if B[t]!=0 and (B[t]>0)!=w:
     if t//10==lr:
      for q in (5,4,3,2):ms.append(i|(t<<7)|(q<<14))
     else:ms.append(i|(t<<7))
    elif t==E and B[t]==0:
     ms.append(i|(t<<7))
  elif pt==2:
   for o in n:
    j=i+o
    if B[j]!=7 and (B[j]==0 or (B[j]>0)!=w):ms.append(i|(j<<7))
  elif pt in (3,4,5):
   for o in P if pt==3 else J if pt==4 else M:
    j=i+o
    while B[j]!=7:
     if B[j]==0:ms.append(i|(j<<7))
     else:
      if (B[j]>0)!=w:ms.append(i|(j<<7))
      break
     j+=o
  elif pt==6:
   for o in M:
    j=i+o
    if B[j]!=7 and (B[j]==0 or (B[j]>0)!=w):ms.append(i|(j<<7))
   k=25 if w else 95;r=4 if w else -4;e=1-w
   if C&(1 if w else 4) and not B[k+1] and not B[k+2] and B[k+3]==r and not l(k,e) and not l(k+1,e) and not l(k+2,e):ms.append(k|((k+2)<<7))
   if C&(2 if w else 8) and not B[k-1] and not B[k-2] and not B[k-3] and B[k-4]==r and not l(k,e) and not l(k-1,e) and not l(k-2,e):ms.append(k|((k-2)<<7))
 return ms
O={}
N=0
F=0
x=150000
def ev():
 pm=0;pe=0
 for X,sg in ((W[0],1),(W[1],-1)):
  x=X
  while x:
   b=x&-x;s=b.bit_length()-1;x^=b
   r=s//8+1
   i=(s//8)*10+(s%8)+21
   j=i+9 if sg>0 else i-11;ok=1
   while (j<99 if sg>0 else j>=20):
    if B[j]==-sg or B[j+1]==-sg or B[j+2]==-sg:ok=0;break
    j+=10*sg
   if ok:
    bb=w[r] if sg>0 else w[9-r]
    if B[i+10*sg]:bb//=2
    pe+=sg*bb;pm+=sg*(bb//2)
 if V[0]>1:pm+=35;pe+=50
 if V[1]>1:pm-=35;pe-=50
 s=((A+pm)*Y+(D+pe)*(24-Y))//24
 return s if S==0 else -s
def qs(a,b):
 global N,F
 N+=1
 if N>=x:
  F=1;return 0
 s=ev()
 if s>=b:return b
 if s>a:a=s
 if s+900<a:return a
 ms=[]
 for m in gen():
  t=(m>>7)&127
  if B[t]!=0 or (abs(B[m&127])==1 and t==E):
   ms.append(m)
 def sc(m):
  t=(m>>7)&127;v=B[t] or 1
  return abs(v)*10-abs(B[m&127])
 ms.sort(key=sc,reverse=True)
 for m in ms:
  make(m)
  if l(K[1-S],S==0):
   z();continue
  v=-qs(-b,-a)
  z()
  if F:return 0
  if v>=b:return b
  if v>a:a=v
 return a
def f(a,b,d,ply,pv):
 global N,F
 if F:return 0
 N+=1
 if N>=x:
  F=1;return 0
 if R.get(Z,0)>=2:
  return -40
 bm=0
 if Z in O:
  de,sc,fl,bm=O[Z]
  if de>=d and not pv:
   if sc>90000:sc-=ply
   elif sc<-90000:sc+=ply
   if fl==0:return sc
   if fl==1 and sc>=b:return b
   if fl==2 and sc<=a:return a
 inchk=l(K[S],S==1)
 if inchk:d+=1
 if d<=0:
  return qs(a,b)
 s=ev()
 if not pv and not inchk and d<=3 and abs(b)<90000:
  if s-85*d>=b:return s
 ms=gen()
 def mo(m):
  t=(m>>7)&127;v=B[t];p=abs(B[m&127])
  return abs(v)*10-p+10000 if v else 9000 if m==KL[ply][0] else 8000 if m==KL[ply][1] else HS[p][t]
 ms.sort(key=lambda m:(m==bm,mo(m)),reverse=True)
 best=-I;bm=0;fl=2;cnt=0;oa=a
 for m in ms:
  t=(m>>7)&127
  cap=B[t]!=0 or (abs(B[m&127])==1 and t==E)
  if not cap and not ((m>>14)&7) and not inchk and d<=2 and cnt>1 and s+120*d<=a:
   continue
  make(m)
  if l(K[1-S],S==0):
   z();continue
  cnt+=1
  nd=d-1
  rd=0
  if cnt>3 and d>=3 and not cap and not inchk:
   nd=d-2;rd=1
  if cnt==1:
   v=-f(-b,-a,nd,ply+1,1)
  else:
   v=-f(-a-1,-a,nd,ply+1,0)
   if v>a and v<b:
    v=-f(-b,-a,nd,ply+1,1)
  if rd and v>a:
   v=-f(-b,-a,d-1,ply+1,1)
  z()
  if F:return 0
  if v>best:
   best=v;bm=m
   if v>a:
    a=v
    if v>=b:
     fl=1
     if not cap:
      if m!=KL[ply][0]:
       KL[ply][1]=KL[ply][0];KL[ply][0]=m
      HS[abs(B[m&127])][(m>>7)&127]+=d*d
     break
 if cnt==0:
  if inchk:return -100000+ply
  return -40
 sb=best
 if sb>90000:sb+=ply
 elif sb<-90000:sb-=ply
 if fl==2 and best>oa:fl=0
 O[Z]=(d,sb,fl,bm)
 return best
j="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
def post(p,b):
 q=u.Request(U+p,data=json.dumps(b).encode())
 with u.urlopen(q,timeout=30) as r:
  return json.load(r)
def o(moves):
 global R
 setup(j)
 R={Z:1}
 for u in moves:
  make(uci_mv(u))
def root(legal_uci):
 global N,F,KL,HS
 N=0;F=0
 if len(O)>250000:O.clear()
 KL=[[0,0] for _ in range(128)];HS=[[0]*128 for _ in range(13)]
 cands=[uci_mv(u) for u in legal_uci]
 best=cands[0]
 for d in range(1,64):
  a=-I;bb=I;cb=best;cs=-I
  cands.remove(best);cands.insert(0,best)
  for i,m in enumerate(cands):
   make(m)
   v=-f(-bb,-a,d-1,1,1) if i==0 else -f(-a-1,-a,d-1,1,0)
   if i and v>a:v=-f(-bb,-a,d-1,1,1)
   z()
   if F:return best
   if v>cs:
    cs=v;cb=m
   if v>a:a=v
  best=cb
 return best
def main():
 while True:
  g=post("/game",{})
  if g["status"]=="done":break
  o(g["moves"])
  while g["status"]=="your_move":
   mv=root(g["legal_moves"])
   if mv is None:
    g=post("/resign",{"game":g["game"]})
    break
   g=post("/move",{"game":g["game"],"move":mv_uci(mv)})
   if g["status"]!="done":
    o(g["moves"])
if __name__=="__main__":
 main()
