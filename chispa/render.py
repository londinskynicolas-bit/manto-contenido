"""Genera piezas de Manto con fotos reales. Uso: python render.py spec.json
spec = {"salida":"semana-N","piezas":[{"tipo":"post|story","foto":"fotos/x.jpg","titulo":"...","sub":"...","fx":.5,"fy":.5,"zoom":1.0,"archivo":"1.jpg"},
        {"tipo":"reel","foto":"fotos/x.jpg","titulo":"...","sub":"...","segundos":8,"archivo":"3.mp4"}]}"""
import json,os,subprocess,sys,urllib.request
from PIL import Image,ImageDraw,ImageFont
FD=os.path.join(os.path.dirname(__file__),'fonts');os.makedirs(FD,exist_ok=True)
BASE='https://raw.githubusercontent.com/google/fonts/main/ofl/'
FILES={'CormorantGaramond-Italic[wght].ttf':'cormorantgaramond/','Montserrat[wght].ttf':'montserrat/'}
def font(n,s,w=500):
    p=os.path.join(FD,n)
    if not os.path.exists(p): urllib.request.urlretrieve(BASE+FILES[n]+n.replace('[','%5B').replace(']','%5D'),p)
    f=ImageFont.truetype(p,s)
    try:f.set_variation_by_axes([w])
    except Exception:pass
    return f
CREAM=(251,246,236)
def cover(im,W,H,fx=.5,fy=.5,z=1.0):
    sw,sh=im.size;sc=max(W/sw,H/sh)*z;nw,nh=int(sw*sc),int(sh*sc);im=im.resize((nw,nh),Image.LANCZOS)
    x=int(min(max(fx*nw-W/2,0),nw-W));y=int(min(max(fy*nh-H/2,0),nh-H));return im.crop((x,y,x+W,y+H))
def shade(W,H,top=True):
    g=Image.new('L',(1,H))
    for y in range(H):
        t=y/H;v=190*max(0,(t-.55)/.45)**1.3
        if top and y<320:v+=130*(1-y/320)**1.5
        g.putpixel((0,y),int(min(v,255)))
    return g.resize((W,H))
def spaced(d,xy,t,f,fill,sp):
    x,y=xy
    for c in t:d.text((x,y),c,font=f,fill=fill);x+=d.textlength(c,font=f)+sp
def wrap(d,t,f,mw):
    L=[];c=''
    for w in t.split():
        x=(c+' '+w).strip()
        if d.textlength(x,font=f)<=mw:c=x
        else:L.append(c);c=w
    L.append(c);return L
def capa(W,H,titulo,sub,size,pad):
    ov=Image.new('RGBA',(W,H),(0,0,0,0));ov.paste(Image.new('RGBA',(W,H),(24,18,12,255)),(0,0),shade(W,H))
    d=ImageDraw.Draw(ov);spaced(d,(pad,int(H*.05)),'MANTO DECO',font('Montserrat[wght].ttf',int(W*.026)),CREAM,8)
    f=font('CormorantGaramond-Italic[wght].ttf',size);L=wrap(d,titulo,f,W-2*pad);lh=int(size*1.04)
    y=H-int(H*.085)-lh*len(L)-(int(W*.065) if sub else 0)
    for l in L:d.text((pad,y),l,font=f,fill=CREAM);y+=lh
    if sub:spaced(d,(pad,y+30),sub.upper(),font('Montserrat[wght].ttf',int(W*.023)),(240,230,212),5)
    return ov
def pieza(p,out):
    story=p['tipo'] in('story','reel');W,H=(1080,1920) if story else (1080,1350)
    im=cover(Image.open(p['foto']).convert('RGB'),W,H,p.get('fx',.5),p.get('fy',.5),p.get('zoom',1.0)).convert('RGBA')
    ov=capa(W,H,p['titulo'],p.get('sub'),p.get('size',120 if story else 92),80)
    path=os.path.join(out,p['archivo'])
    if p['tipo']!='reel':
        Image.alpha_composite(im,ov).convert('RGB').save(path,quality=92);return
    base=path+'.base.jpg';over=path+'.ov.png';cover(Image.open(p['foto']).convert('RGB'),W,H,p.get('fx',.5),p.get('fy',.5)).save(base,quality=92);ov.save(over)
    n=int(p.get('segundos',8)*30)
    subprocess.run(['ffmpeg','-v','error','-y','-i',base,'-loop','1','-framerate','30','-t',str(p.get('segundos',8)),'-i',over,'-filter_complex',
      f"[0:v]scale=2160:3840,zoompan=z='1+0.18*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30[v];[1:v]format=rgba,fade=t=in:st=0.6:d=1:alpha=1[o];[v][o]overlay=shortest=1,format=yuv420p",
      '-c:v','libx264','-preset','veryfast','-crf','22','-an',path],check=True);os.remove(base);os.remove(over)
if __name__=='__main__':
    s=json.load(open(sys.argv[1]));os.makedirs(s['salida'],exist_ok=True)
    for p in s['piezas']:pieza(p,s['salida'])
