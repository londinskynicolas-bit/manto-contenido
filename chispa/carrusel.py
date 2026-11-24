"""Carrusel educativo: python3 chispa/carrusel.py  -> nuevos/errores/slide_N.jpg (1080x1350)"""
import os,sys
sys.path.insert(0,os.path.dirname(__file__))
from render import font,cover,wrap,spaced,CREAM
from PIL import Image,ImageDraw
W,H=1080,1350
SAND=(217,201,168);BROWN=(138,111,77);DARK=(42,39,35)
def slide(n,kicker,titulo,cuerpo,foto,out,fx=.5,fy=.5):
    im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im)
    spaced(d,(80,70),'MANTO DECO',font('Montserrat[wght].ttf',26),BROWN,8)
    d.text((W-80-d.textlength(f'{n}/6',font=font('Montserrat[wght].ttf',26)),70),f'{n}/6',font=font('Montserrat[wght].ttf',26),fill=BROWN)
    y=150
    if kicker: spaced(d,(80,y),kicker.upper(),font('Montserrat[wght].ttf',28,600),BROWN,6);y+=70
    f=font('CormorantGaramond-Italic[wght].ttf',96);lh=100
    for l in wrap(d,titulo,f,W-160):d.text((80,y),l,font=f,fill=DARK);y+=lh
    if cuerpo:
        y+=40;fb=font('Montserrat[wght].ttf',34,400)
        for l in wrap(d,cuerpo,fb,W-160):d.text((80,y),l,font=fb,fill=(74,66,58));y+=52
    ph=H-y-90
    if ph>200:
        ph=min(ph,600);ph_y=H-ph-70
        im.paste(cover(Image.open(foto).convert('RGB'),W-160,ph,fx,fy),(80,ph_y))
    im.save(out,quality=93)
S=[(0,'Guía rápida','5 errores al elegir tu alfombra','Y cómo evitarlos.','fotos/n6-living-silla-rayas.jpg',.5,.5),
(1,'Error 1','Que sea muy chica.','Si flota en el medio, el living se ve más chico. Que al menos las patas delanteras del sillón queden sobre ella.','fotos/n6-vidriera-sillon-beige.jpg',.5,.5),
(2,'Error 2','Elegir solo por la foto.','La luz cambia el color. Mirala de día y de noche en tu ambiente antes de decidir.','fotos/ia-living-azul.jpg',.5,.5),
(3,'Error 3','No pensar en el uso.','Con chicos o mascotas, pensá en una trama fácil de limpiar. La alfombra se vive, no se mira.','fotos/n6-autito-nene-rayas.jpg',.5,.55),
(4,'Error 4','Tapar todo el piso.','Dejá un borde de piso a la vista: ordena el espacio y la alfombra se luce más.','fotos/n6-dormitorio-rosa-min.jpg',.5,.5),
(5,'Error 5','Olvidarse de la base.','Una base antideslizante evita que se corra y cuida tu piso.','fotos/n6-vidriera-gris-noche.jpg',.5,.55)]
os.makedirs('nuevos/errores',exist_ok=True)
for i,k,t,c,f,fx,fy in S: slide(i+1,k,t,c,f,f'nuevos/errores/slide_{i+1}.jpg',fx,fy)
