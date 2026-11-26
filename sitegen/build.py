import json, html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from menudata import DINNER, BRUNCH, COCKTAILS
OUT = '/workspace/marker32/docs'
BASE = 'https://rgwebd.github.io/marker32/'
NAME = 'Marker 32'
PHONE = '(904) 223-1534'; TEL = '+19042231534'
ADDR1 = '14549 Beach Blvd'; CITY = 'Jacksonville'; REGION = 'FL'; ZIP = '32250'
ADDR = f'{ADDR1}, {CITY}, {REGION} {ZIP}'
RESY = 'https://resy.com/cities/jacksonville-fl/venues/marker-32'
MAPS = 'https://www.google.com/maps/place/?q=place_id:ChIJFb1blStK5IgR1lRqO310FF0'
MAPS_DIR = 'https://www.google.com/maps/dir/?api=1&destination=Marker+32%2C+14549+Beach+Blvd%2C+Jacksonville%2C+FL+32250&destination_place_id=ChIJFb1blStK5IgR1lRqO310FF0'
FB = 'https://www.facebook.com/marker32'; IG = 'https://www.instagram.com/_marker32/'
EV_NAME = 'Laura Hayes'; EV_PHONE = '(904) 654-9877'; EV_TEL = '+19046549877'; EV_MAIL = 'laura@southerntablehospitality.com'
RATING = '4.6'; RCOUNT = '1,697'
HOURS = [('Monday','5–10 PM'),('Tuesday','5–10 PM'),('Wednesday','5–10 PM'),('Thursday','5–10 PM'),('Friday','5–10 PM'),('Saturday','5–10 PM'),('Sunday','Brunch 10:30 AM–2:30 PM · Dinner 5–9 PM')]
e = html.escape

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">'

def head(title, desc, path, extra=''):
    url = BASE + path
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="restaurant.restaurant"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/og.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}img/og.jpg">
<meta name="theme-color" content="#14233a"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="img/icon-32.png"><link rel="apple-touch-icon" href="img/icon-180.png">
{FONTS}<link rel="stylesheet" href="style.css">{extra}</head>'''

def header(home=True):
    p = '' if home else 'index.html'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hd{' solid' if not home else ''}" id="hd"><div class="hd-in">
<a class="hd-logo" href="{p or '#top'}" aria-label="Marker 32 home"><img class="lw" src="img/logo-white.webp" alt="Marker 32" width="900" height="293"><img class="lb" src="img/logo-blue.webp" alt="" aria-hidden="true" width="900" height="293"></a>
<nav class="hd-nav" aria-label="Main"><a href="{p}#story">Story</a><a href="{p}#dining">Dining</a><a href="menu.html">Menu</a><a href="{p}#private">Private Dining</a><a href="{p}#visit">Visit</a></nav>
<div class="hd-cta"><a class="hd-tel" href="tel:{TEL}">{PHONE}</a><a class="btn btn-sm" href="{RESY}" target="_blank" rel="noopener">Reserve</a></div>
</div></header>'''

def mbar():
    return f'''<nav class="mbar" id="mbar" aria-label="Quick actions"><a href="tel:{TEL}">Call</a><a href="menu.html">Menu</a><a class="mb-res" href="{RESY}" target="_blank" rel="noopener">Reserve</a></nav>
<div class="demo" id="demo">Design preview by RGWebD <button type="button" aria-label="Dismiss design preview note" onclick="this.parentNode.remove()">×</button></div>'''

def hours_rows():
    return ''.join(f'<tr data-d="{i}"><th scope="row">{d}</th><td>{h}</td></tr>' for i,(d,h) in enumerate(HOURS))

def footer():
    return f'''<footer class="ft"><div class="ft-in">
<div class="ft-brand"><img src="img/logo-white.webp" alt="Marker 32" width="900" height="293" loading="lazy"><p>Waterfront seafood on the Intracoastal Waterway since 1992.</p><a class="btn btn-light" href="{RESY}" target="_blank" rel="noopener">Reserve on Resy</a></div>
<div><h2 class="ft-h">Find us</h2><p><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}<br>{CITY}, {REGION} {ZIP}</a></p><p><a href="tel:{TEL}">{PHONE}</a></p></div>
<div><h2 class="ft-h">Hours</h2><p>Monday–Saturday 5–10 PM<br>Sunday Brunch 10:30 AM–2:30 PM<br>Sunday Dinner 5–9 PM</p></div>
<div><h2 class="ft-h">Follow</h2><p><a href="{FB}" target="_blank" rel="noopener">Facebook</a><br><a href="{IG}" target="_blank" rel="noopener">Instagram</a></p><p class="ft-sm">A Southern Table Hospitality restaurant</p></div>
</div><p class="ft-legal">© {NAME}. Design preview by RGWebD. Photos from marker32.com.</p></footer>'''

def jsonld_restaurant():
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    d = {"@context":"https://schema.org","@type":"Restaurant","@id":BASE+"#restaurant","name":NAME,
      "description":"Waterfront fine-dining seafood restaurant on the Intracoastal Waterway in Jacksonville, Florida, open since 1992.",
      "url":BASE,"image":[BASE+"img/og.jpg",BASE+"img/hero.webp"],"logo":BASE+"img/logo-blue.png","telephone":TEL,
      "address":{"@type":"PostalAddress","streetAddress":ADDR1,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":30.2892379,"longitude":-81.4321476},
      "servesCuisine":["Seafood","New American"],"acceptsReservations":True,"menu":BASE+"menu.html","hasMenu":BASE+"menu.html",
      "potentialAction":{"@type":"ReserveAction","target":{"@type":"EntryPoint","urlTemplate":RESY},"result":{"@type":"FoodEstablishmentReservation","name":"Table at Marker 32"}},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":days,"opens":"17:00","closes":"22:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"10:30","closes":"14:30"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"17:00","closes":"21:00"}],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":4.6,"reviewCount":1697,"bestRating":5},
      "founder":[{"@type":"Person","name":"Ben Groshell"},{"@type":"Person","name":"Liza Groshell"}],"foundingDate":"1992-07",
      "parentOrganization":{"@type":"Organization","name":"Southern Table Hospitality","url":"https://southerntablehospitality.com/"},
      "sameAs":[FB,IG,"https://marker32.com/",RESY,"https://maps.google.com/?cid=6707113826278069462"]}
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'

MQ1 = [('m-oysters','Oysters on the half shell'),('m-crab','North Carolina blue crab'),('m-tuna','Yellowfin tuna'),('m-asparagus','Grilled asparagus'),('m-strip','Prime New York strip'),('m-shrimp','Wild caught shrimp'),('m-brulee','Tahitian vanilla crème brûlée'),('m-broiled','M32 broiled oysters')]
MQ2 = [('m-poke','Tuna poke'),('m-beignets','Sunday beignets'),('m-fettuccine','Shrimp fettuccine'),('m-frenchtoast','Sunday brunch'),('m-cappuccino','Cappuccino'),('m-wine','By the bottle'),('m-cocktail','Cocktail hour')]

def mq_row(items, rev=False):
    AH=' aria-hidden="true"'
    cards = lambda hid: ''.join(f'<li class="mq-c"{AH if hid else ""}><img src="img/{f}.webp" alt="{"" if hid else e(l)}" width="520" height="520" loading="lazy" decoding="async"><span>{e(l)}</span></li>' for f,l in items)
    return f'<div class="mq-row{" rev" if rev else ""}"><ul class="mq-track">{cards(False)}{cards(True)}</ul></div>'

def index():
    h = head(f'{NAME} | Waterfront Seafood Fine Dining in Jacksonville, FL since 1992',
             'Marker 32: fine-dining seafood on the Intracoastal Waterway in Jacksonville, FL since 1992. Second-floor sunset dining room, Sunday brunch, private events. Reserve on Resy.',
             '', jsonld_restaurant())
    body = f'''<body id="top">{header(True)}
<main id="main">
<section class="hero" aria-label="Marker 32">
 <picture><source media="(max-width:700px)" srcset="img/hero-m.webp"><img class="hero-img" src="img/hero.webp" alt="Sunset over the marina docks on the Intracoastal Waterway beside Marker 32" width="2000" height="1333" fetchpriority="high"></picture>
 <div class="hero-shade"></div>
 <div class="hero-in">
  <img class="hero-logo" src="img/logo-white.webp" alt="Marker 32" width="900" height="293">
  <h1 class="hero-h1"><span>Waterfront seafood</span><span class="hs" aria-hidden="true"> · </span><span>Jacksonville, Florida</span><span class="hs" aria-hidden="true"> · </span><span>Since 1992</span></h1>
  <div class="hero-cta"><a class="btn btn-light" href="{RESY}" target="_blank" rel="noopener">Reserve a table</a><a class="hero-tel" href="tel:{TEL}">or call {PHONE}</a></div>
 </div>
 <p class="hero-meta"><span id="status" class="status">Mon–Sat 5–10 PM · Sun brunch & dinner</span><span class="sep" aria-hidden="true">·</span><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}</a></p>
</section>

<section class="sec about" id="story">
 <div class="wrap about-grid">
  <div class="about-tx rv">
   <p class="eyebrow"><span class="num">I</span> Our story</p>
   <h2 class="h2">Leave the world behind.</h2>
   <p class="lead">Ben Groshell grew up fishing and crabbing on these waters. After graduating from the Culinary Institute of America in 1989, he came home, and in July 1992 he and his wife Liza opened Marker 32 in a second-floor dining room above the marina on the Intracoastal Waterway.</p>
   <p>Over thirty years later it is still family owned. Sauces, stocks, soups and bread are made from scratch every day, with local seafood and produce.</p>
  </div>
  <figure class="about-q rv">
   <img class="disc" src="img/owners.webp" alt="Ben and Liza Groshell, owners of Marker 32" width="367" height="251" loading="lazy">
   <blockquote>“I enjoy the back of the house with all the chefs. The camaraderie with those guys, having walked in their shoes, I can see what they need.”</blockquote>
   <figcaption>Ben Groshell, chef and proprietor, to <a href="https://arbus.com/the-milestone-at-marker-32/" target="_blank" rel="noopener">Arbus Magazine</a>, 2023</figcaption>
  </figure>
 </div>
</section>

<section class="mq" aria-label="From the kitchen">
 <p class="mq-lab">From the kitchen <span>· hover or tap to pause</span></p>
 {mq_row(MQ1)}
 {mq_row(MQ2, True)}
</section>

<section class="sec dining" id="dining">
 <div class="wrap">
  <header class="sec-hd rv"><p class="eyebrow"><span class="num">II</span> The evening</p><h2 class="h2">Three ways to spend it.</h2></header>
  <div class="fmt">
   <article class="fmt-c rv"><img src="img/dinner.webp" alt="A window table set for dinner overlooking the marina" width="1100" height="733" loading="lazy"><div class="fmt-tx"><h3>Dinner</h3><p class="fmt-when">Mon–Sat 5–10 PM · Sun 5–9 PM</p><p>The second-floor dining room looks over the marina and the Intracoastal. Oysters, blue crab, New Bedford scallops and prime steaks; plates run $19 to $45, plus a nightly seafood special at market price.</p><a class="lnk" href="menu.html#dinner">Dinner menu</a></div></article>
   <article class="fmt-c rv"><img src="img/brunch.webp" alt="Brunch plates and coffee on a wooden table, seen from above" width="900" height="1349" loading="lazy"><div class="fmt-tx"><h3>Sunday Brunch</h3><p class="fmt-when">Sundays 10:30 AM–2:30 PM</p><p>Beignets with espresso caramel, shrimp &amp; grits, crab cake Benedict and a Bloody Mary garnished with prosciutto-wrapped shrimp.</p><a class="lnk" href="menu.html#brunch">Brunch menu</a></div></article>
   <article class="fmt-c rv"><img src="img/bar.webp" alt="Two cocktails on the ledge with the waterway behind" width="1100" height="916" loading="lazy"><div class="fmt-tx"><h3>Cocktails at sunset</h3><p class="fmt-when">Specialty cocktails $12–$14</p><p>A Nolet’s cucumber basil gimlet, an Old Fashioned with 1792, or the house Valley Girl, poured while the sun goes down over the water.</p><a class="lnk" href="menu.html#cocktails">Cocktail list</a></div></article>
  </div>
 </div>
</section>

<section class="creds" aria-label="Recognition">
 <ul class="wrap creds-row">
  <li><b>1992</b><span>Family owned<br>since July 1992</span></li>
  <li><b>{RATING}<i aria-hidden="true">★</i></b><span>{RCOUNT} Google<br>reviews</span></li>
  <li><b>Best Chefs</b><span>Ben Groshell, named one of America’s best chefs · <a href="http://www.bizjournals.com/jacksonville/blog/retail_radar/2013/03/19-local-chefs-make-the-cut-for-best.html?page=all" target="_blank" rel="noopener">JBJ, 2013</a></span></li>
  <li><b>Longest-standing</b><span>fine dining restaurant in the city · <a href="https://arbus.com/the-milestone-at-marker-32/" target="_blank" rel="noopener">Arbus, 2023</a></span></li>
 </ul>
</section>

<section class="sec private" id="private">
 <div class="wrap pv-grid">
  <img class="pv-img rv" src="img/private.webp" alt="A dining room lined with a floor-to-ceiling wine wall, tables set with white linen" width="1000" height="1499" loading="lazy">
  <div class="pv-tx rv">
   <p class="eyebrow"><span class="num">III</span> Private dining</p>
   <h2 class="h2">Gather the whole table.</h2>
   <p class="lead">For parties of 12 or more, or to book a room for a special occasion, speak with {EV_NAME}, Director of Events and Catering.</p>
   <dl class="facts"><div><dt>Room capacity</dt><dd><span class="ph">[ROOM CAPACITY]</span></dd></div><div><dt>Occasions</dt><dd>Birthdays, anniversaries and wedding showers</dd></div></dl>
   <div class="row-cta"><a class="btn" href="tel:{EV_TEL}">Call {EV_PHONE}</a><a class="lnk" href="mailto:{EV_MAIL}?subject=Private%20event%20at%20Marker%2032">Email {EV_MAIL}</a></div>
  </div>
 </div>
</section>

<section class="reserve" id="reserve">
 <img class="rs-img" src="img/reserve.webp" alt="Dinner on the table by the window, boats in the marina beyond" width="1600" height="1066" loading="lazy">
 <div class="rs-card rv">
  <p class="eyebrow"><span class="num">IV</span> Reservations</p>
  <h2 class="h2">Your table awaits.</h2>
  <p>Marker 32 books on Resy, and tables are known to fill up fast. Parties of up to 8 can book online; for larger groups, call us.</p>
  <p class="small">Running late? Please call. Tables are held for a 15-minute grace period before they go to the waitlist. Booking window: <span class="ph">[HOW FAR AHEAD RESERVATIONS OPEN]</span></p>
  <div class="row-cta center"><a class="btn" href="{RESY}" target="_blank" rel="noopener">Reserve on Resy</a><a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></div>
 </div>
</section>

<section class="sec visit" id="visit">
 <div class="wrap vs-grid">
  <div class="vs-tx rv">
   <p class="eyebrow"><span class="num">V</span> Visit</p>
   <h2 class="h2">On the water at Beach &amp; San Pablo.</h2>
   <p class="addr"><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}<br>{CITY}, {REGION} {ZIP}</a></p>
   <p><a class="lnk" href="{MAPS_DIR}" target="_blank" rel="noopener">Get directions</a> &nbsp; <a class="lnk" href="tel:{TEL}">{PHONE}</a></p>
   <p class="live" id="live" aria-live="polite"></p>
   <table class="hours"><caption class="vh">Opening hours</caption><tbody>{hours_rows()}</tbody></table>
   <p class="small">Holiday hours may differ. Please call ahead around Thanksgiving and other holidays.</p>
   <h3 class="h3">Good to know</h3>
   <ul class="policies">
    <li><b>Dress code</b> <span class="ph">[DRESS CODE]</span></li>
    <li><b>Parking</b> <span class="ph">[PARKING DETAILS]</span></li>
    <li><b>Corkage</b> <span class="ph">[CORKAGE POLICY]</span></li>
    <li><b>Dietary</b> Gluten-free dishes are marked on the menu, with a vegan plate and a kids’ menu.</li>
   </ul>
  </div>
  <img class="vs-img rv" src="img/visit.webp" alt="Marker 32 at dusk: the entrance stairs and the red channel-marker sign" width="1600" height="1066" loading="lazy">
 </div>
</section>
</main>
{footer()}{mbar()}
<script src="site.js" defer></script></body></html>'''
    return h + body

def menu_page():
    def sec(sid, title, groups):
        out = [f'<section class="mn-sec" id="{sid}" data-cat="{sid}"><h2 class="mn-h2">{title}</h2>']
        for g, items in groups:
            out.append(f'<div class="mn-grp"><h3 class="mn-h3">{e(g)}</h3><ul class="mn-list">')
            for n, p, d in items:
                pr = f'<span class="mn-p">{"$" + p if p and p[0].isdigit() else e(p)}</span>' if p else ''
                out.append(f'<li class="mn-i"><div class="mn-top"><span class="mn-n">{e(n)}</span><span class="mn-dots" aria-hidden="true"></span>{pr}</div>{f"<p class=mn-d>{e(d)}</p>" if d else ""}</li>')
            out.append('</ul></div>')
        out.append('</section>'); return ''.join(out)
    secs = []
    for sid, groups in [('dinner', DINNER), ('brunch', BRUNCH), ('cocktails', COCKTAILS)]:
        sm = {"@type":"Menu","name":sid.title(),"hasMenuSection":[{"@type":"MenuSection","name":g,"hasMenuItem":[{"@type":"MenuItem","name":n, **({"description":d} if d else {})} for n,p,d in it]} for g,it in groups]}
        secs.append(sm)
    ld = {"@context":"https://schema.org","@graph":[{"@type":"Restaurant","@id":BASE+"#restaurant","name":NAME,"url":BASE,"telephone":TEL,"address":{"@type":"PostalAddress","streetAddress":ADDR1,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},"hasMenu":secs},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Menu","item":BASE+"menu.html"}]}]}
    h = head(f'Menu | {NAME}, Waterfront Seafood in Jacksonville, FL',
             'The Marker 32 dinner, Sunday brunch and cocktail menus: oysters, blue crab cakes, New Bedford scallops, prime steaks and more on the Intracoastal in Jacksonville, FL.',
             'menu.html', '<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
    chips = ''.join(f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{l}</button>' for k,l in [('all','All'),('dinner','Dinner'),('brunch','Sunday Brunch'),('cocktails','Cocktails')])
    body = f'''<body class="pg-menu">{header(False)}
<main id="main" class="wrap mn">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> <span aria-hidden="true">/</span> Menu</nav>
 <header class="mn-hd"><p class="eyebrow">Marker 32 · Jacksonville</p><h1 class="h1">Menu</h1>
 <p class="lead">Made from scratch daily, with local seafood and produce. The menu follows the season and the nightly seafood special is market price, so call <a href="tel:{TEL}">{PHONE}</a> for tonight’s offerings.</p>
 <div class="row-cta"><a class="btn" href="{RESY}" target="_blank" rel="noopener">Reserve on Resy</a></div></header>
 <div class="mn-tools"><div class="chips" role="group" aria-label="Filter menu">{chips}</div>
 <label class="mn-search"><span class="vh">Search the menu</span><input id="q" type="search" placeholder="Search: oysters, crab, gluten free…" autocomplete="off"></label></div>
 <p class="mn-empty" id="empty" hidden>Nothing matches that search. Try “shrimp” or “oyster”.</p>
 {''.join(sec(s,t,g) for s,t,g in [('dinner','Dinner',DINNER),('brunch','Sunday Brunch · 10:30 AM–2:30 PM',BRUNCH),('cocktails','Cocktails',COCKTAILS)])}
 <p class="mn-note">Prices as published on marker32.com in November 2026 and subject to change. (GF) gluten free. *Consuming raw or undercooked meats, poultry, seafood, shellfish or eggs may increase your risk of foodborne illness, especially if you have medical conditions. Wine and beer lists are available at the restaurant.</p>
</main>
{footer()}{mbar()}
<script src="site.js" defer></script></body></html>'''
    return h + body

def page404():
    h = head(f'Page not found | {NAME}', 'This page could not be found. Return to Marker 32, waterfront seafood in Jacksonville, FL.', '404.html')
    h = h.replace('href="style.css"','href="/marker32/style.css"').replace('href="favicon.ico"','href="/marker32/favicon.ico"').replace('href="img/','href="/marker32/img/')
    return h + f'''<body class="pg-404"><main id="main" class="nf"><img src="/marker32/img/logo-blue.webp" alt="Marker 32" width="900" height="293"><h1 class="h1">Off the channel.</h1><p class="lead">This page drifted away. The marina is right where we left it.</p><div class="row-cta center"><a class="btn" href="/marker32/">Back to Marker 32</a><a class="btn btn-ghost" href="{RESY}">Reserve on Resy</a></div></main></body></html>'''

def misc():
    open(f'{OUT}/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    open(f'{OUT}/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url><url><loc>{BASE}menu.html</loc></url></urlset>\n')
    open(f'{OUT}/llms.txt','w').write(f'''# Marker 32
> Family-owned fine-dining seafood restaurant on the Intracoastal Waterway in Jacksonville, Florida, open since July 1992. Second-floor dining room overlooking the marina. Owned by Ben Groshell (chef and proprietor, Culinary Institute of America 1989) and Liza Groshell, part of Southern Table Hospitality.

- Address: {ADDR} (Beach Blvd at San Pablo Rd S)
- Phone: {PHONE}
- Hours: Monday–Saturday 5–10 PM; Sunday brunch 10:30 AM–2:30 PM; Sunday dinner 5–9 PM
- Reservations: Resy, {RESY} (online up to 8 guests; 15-minute grace period)
- Private events (12+ guests): {EV_NAME}, Director of Events and Catering, {EV_PHONE}, {EV_MAIL}
- Google rating: {RATING} from {RCOUNT} reviews (November 2026)
- Cuisine: seafood, New American; made from scratch daily with local seafood and produce

## Pages
- [Home]({BASE}): story, dining formats, private dining, reservations, hours and location
- [Menu]({BASE}menu.html): dinner, Sunday brunch and cocktail menus
''')
    open(f'{OUT}/.nojekyll','w').write('')

os.makedirs(OUT, exist_ok=True)
open(f'{OUT}/index.html','w').write(index())
open(f'{OUT}/menu.html','w').write(menu_page())
open(f'{OUT}/404.html','w').write(page404())
misc()
print('built')
