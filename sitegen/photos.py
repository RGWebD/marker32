from PIL import Image
import os
R='/workspace/m32src/raw/'; O='/workspace/marker32/docs/img/'
def save(src,name,w,crop=None,q=78):
    im=Image.open(R+src).convert('RGB')
    if crop: # (l,t,r,b) fractions
        W,H=im.size; im=im.crop((int(crop[0]*W),int(crop[1]*H),int(crop[2]*W),int(crop[3]*H)))
    if im.width>w: im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    im.save(O+name+'.webp','WEBP',quality=q,method=6); return im.size
P={}
P['hero']=save('Marker32October2021-228-scaled.jpg','hero',2000,q=74)
P['hero-m']=save('Marker32October2021-228-scaled.jpg','hero-m',900,crop=(0.08,0,0.62,1),q=74)
P['owners']=save('groshells-1_367-1.jpg','owners',367,crop=(0,0.36,1,1),q=85)
P['dinner']=save('Marker32August2021-156-scaled.jpg','dinner',1100)
P['brunch']=save('MarkerBrunchNov2023-9-scaled.jpg','brunch',900)
P['bar']=save('Marker32Jan2024-219-scaled.jpg','bar',1100,crop=(0.1,0,0.9,1))
P['private']=save('Marker32-191-scaled.jpg','private',1000)
P['reserve']=save('Marker32May2021-116-scaled.jpg','reserve',1600)
P['visit']=save('Marker32October2021-226-scaled.jpg','visit',1600)
mq=[('0V2A1507-scaled.jpg','m-oysters'),('0V2A1617-scaled.jpg','m-crab'),('0V2A1663-1-scaled.jpg','m-tuna'),('0V2A1657-scaled.jpg','m-asparagus'),('0V2A1665-scaled.jpg','m-strip'),('Marker3-scaled.jpg','m-shrimp'),('0V2A1762-scaled.jpg','m-brulee'),('Marker32-135-scaled.jpg','m-broiled'),
('Marker32Jan2024-103-scaled.jpg','m-poke'),('Marker32Jan2024-63-scaled.jpg','m-beignets'),('0V2A1656-scaled.jpg','m-fettuccine'),('MarkerBrunchNov2023-4-scaled.jpg','m-frenchtoast'),('Marker32September2023-182-scaled.jpg','m-cappuccino'),('0V2A1798-scaled1.jpg','m-wine'),('Marker32-168-scaled.jpg','m-cocktail')]
for s,n in mq:
    im=Image.open(R+s).convert('RGB');W,H=im.size;m=min(W,H)
    im=im.crop(((W-m)//2,(H-m)//2,(W-m)//2+m,(H-m)//2+m)).resize((520,520),Image.LANCZOS)
    im.save(O+n+'.webp','WEBP',quality=74,method=6)
# logos
for src,n in [('Marker32_UPDATED_LOGO-03-12.png','logo-white'),('Marker32_UPDATED_LOGO-04-11.png','logo-blue')]:
    im=Image.open(R+src).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((900,900));im.save(O+n+'.png',optimize=True);im.save(O+n+'.webp','WEBP',quality=90)
    print(n,im.size)
# og image
im=Image.open(R+'Marker32October2021-228-scaled.jpg').convert('RGB');im=im.resize((1200,800));im=im.crop((0,85,1200,715))
lg=Image.open(O+'logo-white.png');lg.thumbnail((620,300));im.paste(lg,((1200-lg.width)//2,(630-lg.height)//2),lg);im.save(O+'og.jpg',quality=82)
# favicon: triangle crop from blue logo
lg=Image.open(R+'Marker32_UPDATED_LOGO-04-11.png').convert('RGBA');W,H=lg.size
px=lg.load()
# find red pixels bbox
xs=[];ys=[]
for y in range(0,H,2):
    for x in range(0,W,2):
        r,g,b,a=px[x,y]
        if a>128 and r>150 and g<80: xs.append(x);ys.append(y)
tri=lg.crop((min(xs)-4,min(ys)-4,max(xs)+4,max(ys)+4))
s=max(tri.size);c=Image.new('RGBA',(s,s),(0,0,0,0));c.paste(tri,((s-tri.width)//2,(s-tri.height)//2),tri)
for z in (32,180,512): c.resize((z,z),Image.LANCZOS).save(O+f'icon-{z}.png')
c.resize((64,64),Image.LANCZOS).save('/workspace/marker32/docs/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
print(P)
