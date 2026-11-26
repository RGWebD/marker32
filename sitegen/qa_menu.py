import asyncio, sys, json, time
from playwright.async_api import async_playwright
TAG=sys.argv[1]; BASE=sys.argv[2] if len(sys.argv)>2 else 'https://rgwebd.github.io/marker32/'
JS='''()=>{const vis=e=>e&&e.offsetParent!==null&&getComputedStyle(e).visibility!=='hidden'&&parseFloat(getComputedStyle(e).opacity)>0.1;
 const items=[...document.querySelectorAll('.mn-i')];return {secs:[...document.querySelectorAll('.mn-sec')].map(s=>s.id+':'+(vis(s)?'v':'h')),
 visItems:items.filter(vis).length,total:items.length,ow:document.documentElement.scrollWidth>innerWidth+1,y:Math.round(scrollY),
 chips:document.querySelectorAll('.chip').length,bodyH:document.body.scrollHeight,hd:getComputedStyle(document.getElementById('hd')).position}}'''
async def one(p,bt,w,h):
    import os; b=await getattr(p,bt).launch(**({'env':{**os.environ,'LD_LIBRARY_PATH':'/workspace/wkdeps/root/usr/lib/x86_64-linux-gnu'}} if bt=='webkit' else {}))
    ctx=await b.new_context(viewport={'width':w,'height':h},has_touch=(w<500),is_mobile=(w<500 and bt=='chromium'))
    if bt=='webkit':
        async def h(route):
            try:
                r=await route.fetch(); await route.fulfill(response=r)
            except Exception as e: await route.abort()
        await ctx.route('**/*',h)
    pg=await ctx.new_page(); errs=[]
    pg.on('console',lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.on('pageerror',lambda e: errs.append('PAGEERROR: '+str(e)))
    pg.on('requestfailed',lambda r: errs.append('REQFAIL: '+r.url))
    lab=f'{bt}-{w}'
    await pg.goto(BASE+'menu.html?cb='+str(time.time()),wait_until='load'); await pg.wait_for_timeout(1500)
    print(lab,'load',json.dumps(await pg.evaluate(JS)))
    await pg.screenshot(path=f'/workspace/marker32/qa/{TAG}-{lab}-menu.png')
    # search
    await pg.fill('#q','oyster'); await pg.wait_for_timeout(300)
    print(lab,'search oyster',(await pg.evaluate(JS))['visItems'])
    await pg.fill('#q',''); await pg.wait_for_timeout(200)
    for f in ['brunch','cocktails','all']:
        await pg.click(f'.chip[data-f={f}]'); await pg.wait_for_timeout(250)
        print(lab,'chip',f,(await pg.evaluate(JS))['secs'])
    # anchors
    for a in ['dinner','brunch','cocktails']:
        await pg.goto(BASE+f'menu.html?cb={time.time()}#{a}',wait_until='load'); await pg.wait_for_timeout(1200)
        r=await pg.evaluate(f"(()=>{{const t=document.getElementById('{a}').getBoundingClientRect().top;return [Math.round(t),Math.round(scrollY)]}})()")
        print(lab,'anchor',a,'secTop',r)
    # deep chip / search while scrolled down
    await pg.goto(BASE+'menu.html?cb='+str(time.time()),wait_until='load'); await pg.wait_for_timeout(800)
    await pg.evaluate('scrollTo(0,3200)'); await pg.wait_for_timeout(300)
    if w>700:
        await pg.click('.chip[data-f=cocktails]'); await pg.wait_for_timeout(500)
        r=await pg.evaluate("(()=>{const t=document.getElementById('cocktails').getBoundingClientRect();return [Math.round(t.top),Math.round(t.bottom),innerHeight]})()")
        print(lab,'deep chip cocktails rect',r,'OK' if r[0]<r[2] and r[1]>0 else 'BROKEN')
        await pg.screenshot(path=f'/workspace/marker32/qa/{TAG}-{lab}-deepchip.png')
        await pg.click('.chip[data-f=all]'); await pg.evaluate('scrollTo(0,3200)'); await pg.wait_for_timeout(300)
        await pg.fill('#q','crab'); await pg.wait_for_timeout(400)
        r=await pg.evaluate("(()=>{const v=[...document.querySelectorAll('.mn-i')].filter(l=>!l.hidden&&l.offsetParent);const t=v[0].getBoundingClientRect();return [v.length,Math.round(t.top),innerHeight]})()")
        print(lab,'deep search crab first hit',r,'OK' if 0<r[1]<r[2] else 'BROKEN')
    # from homepage
    await pg.goto(BASE+'?cb='+str(time.time()),wait_until='load'); await pg.wait_for_timeout(800)
    links=await pg.evaluate("[...document.querySelectorAll('a[href*=menu]')].map(a=>a.getAttribute('href')+'|'+(a.offsetParent!==null))")
    print(lab,'home menu links',links)
    sel='.hd-nav a[href="menu.html"]'
    await pg.click(sel); await pg.wait_for_load_state('load'); await pg.wait_for_timeout(1200)
    print(lab,'clicked',sel,'->',pg.url,json.dumps(await pg.evaluate(JS)))
    print(lab,'ERRS',errs[:8])
    await b.close()
async def main():
    async with async_playwright() as p:
        for bt in ['webkit','chromium']:
            for w,h in [(390,844),(1024,700),(1440,900)]:
                try: await one(p,bt,w,h)
                except Exception as e: print(bt,w,'FAILED',str(e)[:600])
asyncio.run(main())
