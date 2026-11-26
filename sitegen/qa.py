import asyncio, sys, json, re
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8765/'
TAG = sys.argv[2] if len(sys.argv)>2 else 'r1'
PAGES = ['', 'menu.html', '404.html'] if 'github.io' in BASE else ['', 'menu.html']
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h,lab in [(1440,900,'d'),(390,844,'m')]:
            for rm in ['no-preference','reduce']:
                ctx = await b.new_context(viewport={'width':w,'height':h}, reduced_motion=rm, device_scale_factor=1)
                for path in PAGES:
                    pg = await ctx.new_page(); errs=[]
                    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
                    pg.on('pageerror', lambda e: errs.append(str(e)))
                    await pg.goto(BASE+path, wait_until='load')
                    await pg.wait_for_timeout(1800)
                    nm = (path or 'index').replace('.html','')
                    if rm=='no-preference':
                        await pg.screenshot(path=f'/workspace/marker32/qa/{TAG}-{nm}-{lab}-hero.png')
                    # scroll through
                    H = await pg.evaluate('document.body.scrollHeight')
                    for y in range(0, H, 600):
                        await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                    await pg.wait_for_timeout(1300)
                    r = await pg.evaluate('''()=>{
                      const ow=document.documentElement.scrollWidth>window.innerWidth+1;
                      const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>window.innerWidth+1 && !e.closest('.mq-row') && getComputedStyle(e).position!=='fixed'}).slice(0,5).map(e=>e.className||e.tagName);
                      const broken=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src);
                      const hidden=[...document.querySelectorAll('.rv')].filter(e=>getComputedStyle(e).opacity<0.5).length;
                      const srcs=[...document.images].filter(i=>!i.closest('[aria-hidden=true]')&&!/logo|icon/.test(i.src)).map(i=>i.currentSrc||i.src);
                      const dup=srcs.filter((s,i)=>srcs.indexOf(s)!==i);
                      const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{JSON.parse(s.textContent);return 'ok'}catch(e){return 'BAD'}});
                      const ph=(document.body.innerText.match(/\\{[A-Z_]+\\}/g)||[]);
                      const small=[...document.querySelectorAll('p,li,td')].filter(e=>e.offsetParent&&parseFloat(getComputedStyle(e).fontSize)<15&&!e.closest('.hero-meta,.creds,.demo,.ft-legal,.crumbs,.mq')).length;
                      const res=[...document.querySelectorAll('a[href*="resy.com"]')].length;
                      return {ow,wide,broken,hidden,dup,ld,ph,small,res,status:(document.getElementById('live')||{}).textContent}}''')
                    if rm=='no-preference' and lab=='m' and path=='':
                        await pg.screenshot(path=f'/workspace/marker32/qa/{TAG}-index-m-full.png', full_page=True)
                    if rm=='no-preference' and lab=='d':
                        await pg.screenshot(path=f'/workspace/marker32/qa/{TAG}-{nm}-d-full.png', full_page=True)
                    print(lab, rm, path or 'index', json.dumps(r), 'ERR:', [e for e in errs if 'opentable' not in e][:4])
                    await pg.close()
                await ctx.close()
        await b.close()
asyncio.run(run())
