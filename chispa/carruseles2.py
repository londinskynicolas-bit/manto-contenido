"""Tanda de carruseles. python3 chispa/carruseles2.py [slug ...]  -> nuevos/<slug>/slide_N.jpg 1080x1350"""
import os,sys
sys.path.insert(0,os.path.dirname(__file__))
from render import font,cover,wrap,spaced,CREAM
from PIL import Image,ImageDraw
W,H=1080,1350
SAND=(217,201,168);BROWN=(138,111,77);DARK=(42,39,35);BODY=(74,66,58);FLOOR=(238,228,208);FURN=(150,134,114);GOOD=(94,128,92);BAD=(176,84,70)
M=lambda s,w=500:font('Montserrat[wght].ttf',s,w)
C=lambda s:font('CormorantGaramond-Italic[wght].ttf',s)
def mark(d,cx,cy,ok):
    col=GOOD if ok else BAD;d.ellipse((cx-22,cy-22,cx+22,cy+22),fill=col)
    if ok:d.line((cx-10,cy,cx-3,cy+8,cx+11,cy-8),fill='white',width=5)
    else:d.line((cx-9,cy-9,cx+9,cy+9),fill='white',width=5);d.line((cx-9,cy+9,cx+9,cy-9),fill='white',width=5)
def R(d,b,r,fill,out=None,rad=14,w=3):
    x,y,bw,bh=b;d.rounded_rectangle((x+r[0]*bw,y+r[1]*bh,x+(r[0]+r[2])*bw,y+(r[1]+r[3])*bh),radius=rad,fill=fill,outline=out,width=w)
def plan(d,b,kind):
    x,y,bw,bh=b;d.rounded_rectangle((x,y,x+bw,y+bh),radius=18,fill=FLOOR,outline=BROWN,width=3)
    pend=[]
    rug=lambda r,ok,lab:(R(d,b,r,SAND,BROWN),pend.append((x+(r[0]+r[2])*bw-52,y+(r[1]+r[3])*bh-52 if r[3]<.9 else y+(r[1]+r[3])*bh-90,ok)),d.text((x+bw/2,y+bh-30),lab,font=M(26,600),fill=DARK,anchor='mm'))
    if kind in('l_small','l_ok','l_big'):
        r={'l_small':((.34,.34,.32,.30),False,'Muy chica: queda flotando'),'l_ok':((.14,.19,.72,.62),True,'Justa: patas delanteras sobre la alfombra'),'l_big':((.02,.02,.96,.94),False,'Muy grande: sin borde de piso')}[kind]
        rug(*r);R(d,b,(.1,.04,.8,.17),FURN);R(d,b,(.02,.30,.12,.22),FURN);R(d,b,(.86,.30,.12,.22),FURN);R(d,b,(.38,.42,.24,.12),(120,104,88))
    elif kind=='comedor':
        rug((.1,.12,.8,.72),True,'Las sillas quedan siempre sobre la alfombra');R(d,b,(.3,.3,.4,.34),(120,104,88))
        for cx in(.36,.5,.64):R(d,b,(cx-.05,.22,.1,.07),FURN);R(d,b,(cx-.05,.65,.1,.07),FURN)
    elif kind=='dormi':
        rug((.1,.30,.8,.58),True,'Debajo de dos tercios de la cama');R(d,b,(.26,.04,.48,.46),FURN);R(d,b,(.26,.04,.48,.07),(110,94,78));R(d,b,(.14,.06,.09,.09),(120,104,88));R(d,b,(.77,.06,.09,.09),(120,104,88))
    elif kind=='pasillo':
        R(d,b,(.34,.04,.32,.84),SAND,BROWN);pend.append((x+bw*.5,y+bh*.45,True));R(d,b,(.3,.93,.4,.04),(120,104,88),rad=4);d.text((x+bw/2,y+bh-18),'Corredor: deja 10 cm de piso a cada lado',font=M(24,600),fill=DARK,anchor='mm')
    for a,b_,c in pend:mark(d,a,b_,c)
def _marks(d,pend):
    for a,b_,c in pend:mark(d,a,b_,c)
def base(n,tot,kicker):
    im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im);spaced(d,(80,70),'MANTO DECO',M(26),BROWN,8)
    t=f'{n}/{tot}';d.text((W-80-d.textlength(t,font=M(26)),70),t,font=M(26),fill=BROWN)
    if kicker:spaced(d,(80,150),kicker.upper(),M(28,600),BROWN,6)
    return im,d
def txt(d,y,title,body,tsize=92):
    f=C(tsize)
    for l in wrap(d,title,f,W-160):d.text((80,y),l,font=f,fill=DARK);y+=int(tsize*1.06)
    if body:
        y+=34;fb=M(34,400)
        for l in wrap(d,body,fb,W-160):d.text((80,y),l,font=fb,fill=BODY);y+=52
    return y
def s_photo(n,tot,k,t,b,photo,fy=.5,fx=.5,out=None):
    im,d=base(n,tot,k);y=txt(d,220 if k else 150,t,b);ph=min(H-y-90,620)
    if ph>220:im.paste(cover(Image.open(photo).convert('RGB'),W-160,ph,fx,fy),(80,H-ph-70))
    im.save(out,quality=93)
def s_plan(n,tot,k,t,b,kind,out):
    im,d=base(n,tot,k);y=txt(d,220,t,b);ph=H-y-90
    bb=(80,y+10,W-160,ph-10);plan(d,bb,kind);im.save(out,quality=93)
POOL=['n6-autito-nene-rayas.jpg','n6-vidriera-gris-noche.jpg','ia-real-azul-trabajo.png','n6-dormitorio-rosa-min.jpg','n6-vidriera-sillon-beige.jpg','n6-living-silla-rayas.jpg','n6-gato-siesta-beige.jpg','n6-dormitorio-maleta-gris.jpg']
def s_list(n,tot,k,t,items,out,photo=None):
    im,d=base(n,tot,k);y=txt(d,220,t,'');y+=14
    if len(items)==1:
        h,c=items[0];d.rounded_rectangle((80,y,300,y+60),radius=30,fill=BROWN);d.text((190,y+31),h.upper(),font=M(28,700),fill=CREAM,anchor='mm');y+=96
        for l in wrap(d,c,M(38,400),W-160):d.text((80,y),l,font=M(38,400),fill=BODY);y+=56
        items=[]
    for i,(h,c) in enumerate(items):
        d.ellipse((80,y,132,y+52),fill=BROWN);d.text((106,y+27),str(i+1),font=M(28,700),fill=CREAM,anchor='mm')
        d.text((160,y+4),h,font=M(38,700),fill=DARK);y+=58
        for l in wrap(d,c,M(32,400),W-240):d.text((160,y),l,font=M(32,400),fill=BODY);y+=46
        y+=30
    ph=H-y-80
    if ph>260:
        ph=min(ph,560);im.paste(cover(Image.open('fotos/'+(photo or POOL[n%len(POOL)])).convert('RGB'),W-160,ph,.5,.6),(80,H-ph-70))
    im.save(out,quality=93)
def s_cover(n,tot,t,sub,photo,fy=.55,fx=.5,out=None):
    im=cover(Image.open(photo).convert('RGB'),W,H,fx,fy).convert('RGBA');ov=Image.new('RGBA',(W,H),(0,0,0,0))
    g=Image.new('L',(1,H))
    for yy in range(H):g.putpixel((0,yy),int(min(230,230*max(0,(yy/H-.35)/.65)**1.2)))
    ov.paste(Image.new('RGBA',(W,H),(24,18,12,255)),(0,0),g.resize((W,H)));ov.paste(Image.new('RGBA',(W,H),(24,18,12,255)),(0,0),Image.linear_gradient('L').rotate(180).resize((W,260)).crop((0,0,W,260)).resize((W,H),box=None).point(lambda v:0) if False else Image.new('L',(W,H),0));d=ImageDraw.Draw(ov)
    spaced(d,(80,70),'MANTO DECO',M(26),CREAM,8);f=C(104);L=wrap(d,t,f,W-160);y=H-120-len(L)*108-(70 if sub else 0)
    for l in L:d.text((80,y),l,font=f,fill=CREAM);y+=108
    if sub:spaced(d,(80,y+14),sub.upper(),M(26,600),(240,230,212),5)
    d.text((W-80,H-70),'Deslizá  →',font=M(26,500),fill=CREAM,anchor='rm')
    Image.alpha_composite(im,ov).convert('RGB').save(out,quality=93)
def s_end(n,tot,t,sub,photo,out,b2b=False):
    im,d=base(n,tot,None);y=txt(d,200,t,sub)
    ph=min(H-y-300,520)
    if ph>200:im.paste(cover(Image.open(photo).convert('RGB'),W-160,ph,.5,.6),(80,y+20))
    d.rounded_rectangle((80,H-230,W-80,H-110),radius=60,fill=DARK)
    d.text((W/2,H-170),'Escribinos por WhatsApp · link en bio',font=M(32,600),fill=CREAM,anchor='mm');im.save(out,quality=93)
F='fotos/'
def build(slug,slides):
    o=f'nuevos/{slug}';os.makedirs(o,exist_ok=True);tot=len(slides)
    for i,(fn,a) in enumerate(slides,1):fn(i,tot,*a,out=f'{o}/slide_{i}.jpg')
CAR={
'medidas':[(s_cover,('Guía de medidas: qué alfombra para cada ambiente','Guardala',F+'living-gris-1.png',.6)),
 (s_plan,('Living','El punto de partida','Con sillón y mesa ratona, la de 200 × 300 cm deja las patas delanteras sobre la alfombra. Para livings más chicos: 160 × 230 cm.','l_ok')),
 (s_plan,('Comedor','La mesa y las sillas','Mesa de 4 personas: 160 × 230 cm. Mesa de 6: 200 × 300 cm. Que las sillas queden sobre la alfombra al correrlas.','comedor')),
 (s_plan,('Dormitorio','Pensá en la cama','Cama de 2 plazas: 200 × 300 cm debajo de dos tercios de la cama. Cama de 1 plaza: 160 × 230 cm.','dormi')),
 (s_list,('Resumen','Dos medidas, mil usos',[('160 × 230 cm','Dormitorios, cuartos de chicos, home office y livings chicos.'),('200 × 300 cm','Livings amplios, comedores y debajo de la cama.')])),
 (s_end,('¿Dudas con la medida?','Tenemos 160 × 230 y 200 × 300 cm. Te asesoramos.',F+'n6-living-silla-rayas.jpg'))],
'achica':[(s_cover,('¿Tu alfombra hace que el living se vea más chico?','Mirá el antes y el después',F+'n6-vidriera-sillon-beige.jpg',.6)),
 (s_plan,('Antes','Muy chica','Flota en el medio y corta el espacio en pedazos.','l_small')),
 (s_plan,('Después','Justa','Con 200 × 300 cm, conecta los muebles y el living se ve más amplio. Si es chico, 160 × 230 cm.','l_ok')),
 (s_plan,('Ojo','Muy grande','Sin borde de piso, el ambiente pierde aire.','l_big')),
 (s_end,('La medida correcta cambia todo.','Tenemos 160 × 230 y 200 × 300 cm. Contanos tu ambiente.',F+'ia-living-azul.jpg'))],
'combinar':[(s_cover,('Cómo combinar tu alfombra con el living','4 ideas simples',F+'living-ondas-3.png',.55)),
 (s_photo,('Idea 1','Tono sobre tono','Sillón claro y alfombra clara: ambiente calmo, luminoso y amplio.',F+'n6-vidriera-sillon-beige.jpg',.5)),
 (s_photo,('Idea 2','Contraste suave','Sillón oscuro y alfombra clara para dar luz sin perder carácter.',F+'living-azul-5.png',.55)),
 (s_photo,('Idea 3','Un toque de color','Si todo es neutro, que la alfombra sea la que sume el color.',F+'ia-living-azul.jpg',.55)),
 (s_photo,('Idea 4','Textura sobre todo','En ambientes neutros, la trama hace el trabajo: suma calidez y profundidad.',F+'n6-living-silla-rayas.jpg',.55)),
 (s_end,('Guardalo para cuando elijas.','Disponibles en 160 × 230 y 200 × 300 cm.',F+'living-rosa-2.png'))],
'cuidado':[(s_cover,('Cómo cuidar tu alfombra para que dure','Tips simples',F+'n6-gato-siesta-beige.jpg',.55)),
 (s_list,('Rutina','Lo básico',[('Aspirá seguido','Evitá que se acumule polvo en la trama.'),('Rotala de vez en cuando','Así se desgasta parejo.'),('Cuidá el sol directo','Mucha exposición puede apagar los colores.')])),
 (s_list,('Manchas','Si se cae algo',[('Actuá rápido','Absorbé con un paño limpio, sin frotar.'),('Probá en un rincón','Antes de usar cualquier producto.'),('Dudas con el material','Consultanos y te decimos qué conviene.')])),
 (s_list,('Hogar','Pensando en el día a día',[('Base antideslizante','Evita corrimientos y cuida el piso.'),('Muebles pesados','Usá protectores para no marcar la trama.'),('Mascotas y chicos','Una trama fácil de limpiar ayuda muchísimo.')])),
 (s_end,('Una alfombra bien cuidada dura más.','Escribinos y te asesoramos.',F+'n6-autito-nene-rayas.jpg'))],
'mitos':[(s_cover,('Mitos y verdades sobre las alfombras','Sin vueltas',F+'n6-gato-caja-rayas.jpg',.5)),
 (s_list,('Mito 1','"Achican el ambiente"',[('Verdad','Una alfombra muy chica sí. Con la medida correcta (160 × 230 o 200 × 300 cm), el ambiente se ve más grande.')])),
 (s_list,('Mito 2','"Son solo para el living"',[('Verdad','Quedan bien en dormitorio, comedor, home office, cuarto de chicos y entrada.')])),
 (s_list,('Mito 3','"Todas son iguales"',[('Verdad','Cambian el diseño, la trama, el tamaño y cómo se sienten al pisar.')])),
 (s_list,('Mito 4','"Las claras no se pueden usar"',[('Verdad','Se pueden. Elegir bien la trama y cuidarla es la clave.')])),
 (s_end,('¿Qué otro mito escuchaste?','Contanos en los comentarios.',F+'n6-dormitorio-rosa-min.jpg'))],
'ambientes':[(s_cover,('Una alfombra para cada ambiente','Ideas para toda la casa',F+'n6-dormitorio-maleta-gris.jpg',.55)),
 (s_photo,('Living','El centro de la casa','Define el espacio y reúne los muebles. Medida sugerida: 200 × 300 cm.',F+'n6-living-silla-rayas.jpg',.55)),
 (s_photo,('Dormitorio','Suave al despertar','El primer paso del día, resuelto. Medida sugerida: 160 × 230 cm (1 plaza) o 200 × 300 cm (2 plazas).',F+'n6-dormitorio-rosa-min.jpg',.55)),
 (s_photo,('Cuarto de chicos','Para jugar en el piso','Un lugar blando para el autito, el cuento y la siesta. Medida sugerida: 160 × 230 cm.',F+'n6-autito-nene-rayas.jpg',.7)),
 (s_photo,('Home office','Donde se trabaja mejor','Amortigua el sonido y le da calidez al escritorio. Medida sugerida: 160 × 230 cm.',F+'ia-real-azul-trabajo.png',.55)),
 (s_photo,('Entrada','La primera impresión','Una bienvenida con textura. Si hay lugar, 160 × 230 cm.',F+'n6-vidriera-gris-noche.jpg',.6)),
 (s_end,('¿Cuál es el tuyo?','Disponibles en 160 × 230 y 200 × 300 cm.',F+'n6-vidriera-sillon-beige.jpg'))],
'checklist':[(s_cover,('Antes de comprar tu alfombra','Checklist para guardar',F+'ia-lectura-rayas.jpg',.55)),
 (s_list,('Paso a paso','Antes de elegir',[('Medí el ambiente','Marcá con cinta el borde: 160 × 230 o 200 × 300 cm.'),('Mirá la luz','Fijate cómo cambia el color de día y de noche.'),('Pensá en el uso','¿Chicos, mascotas, mucho tránsito?')])),
 (s_list,('Paso a paso','Al decidir',[('Elegí la trama','Que te guste al verla y al pisarla.'),('Sumá la base','Antideslizante para que no se corra.'),('Consultá tamaños','Pedinos opciones y te asesoramos.')])),
 (s_end,('¿Lista la medida?','Escribinos con las medidas del ambiente y te ayudamos a elegir entre 160 × 230 y 200 × 300 cm.',F+'n6-vidriera-gris-noche.jpg'))],
'locales':[(s_cover,('¿Tenés un local de decoración, muebles o bazar?','Sumá alfombras importadas',F+'n6-ventanal-beige-noche.jpg',.55)),
 (s_list,('Para locales','Por qué sumar alfombras',[('Completan el ambiente','Quien compra un sillón suele necesitar una alfombra.'),('Se lucen en vidriera','Una alfombra transforma cualquier exhibición.'),('Variedad de diseños','En 160 × 230 y 200 × 300 cm, con distintos colores y texturas.')])),
 (s_list,('Con Manto Deco','Trabajamos con vos',[('Alfombras importadas','Para decoración, muebleras y bazares.'),('Catálogo por WhatsApp','Pedilo y te lo mandamos.'),('Atención directa','Te asesoramos según tu local.')])),
 (s_end,('Pedí el catálogo.','Trabajamos con locales de todo el país.',F+'n6-revista-dos-alfombras.jpg'))],
}
if __name__=='__main__':
    for s in (sys.argv[1:] or CAR):build(s,CAR[s])
