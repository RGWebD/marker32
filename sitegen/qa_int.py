import asyncio,sys
from playwright.async_api import async_playwright
BASE=sys.argv[1];TAG=sys.argv[2]
async def run():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,has_touch=True,is_mobile=True)
        pg=await c.new_page()
        await pg.goto(BASE+'menu.html',wait_until='load');await pg.wait_for_timeout(800)
        await pg.screenshot(path=f'qa/{TAG}-menu-m-top.png')
        await pg.fill('#q','oyster');await pg.wait_for_timeout(300)
        n=await pg.evaluate("[...document.querySelectorAll('.mn-i')].filter(l=>!l.hidden&&l.offsetParent).length");print('oyster hits',n)
        await pg.fill('#q','gluten free');await pg.wait_for_timeout(300)
        print('gf hits',await pg.evaluate("[...document.querySelectorAll('.mn-i')].filter(l=>!l.hidden&&l.offsetParent).length"))
        await pg.fill('#q','zzzz');print('empty shown',await pg.is_visible('#empty'))
        await pg.fill('#q','');await pg.click('.chip[data-f=brunch]');await pg.wait_for_timeout(200)
        print('visible secs',await pg.evaluate("[...document.querySelectorAll('.mn-sec')].filter(s=>!s.hidden).map(s=>s.id)"))
        await pg.goto(BASE,wait_until='load');await pg.wait_for_timeout(500)
        await pg.evaluate("document.querySelector('.mq').scrollIntoView()");await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'qa/{TAG}-mq-m.png')
        t1=await pg.evaluate("getComputedStyle(document.querySelector('.mq-track')).transform");await pg.wait_for_timeout(1000)
        t2=await pg.evaluate("getComputedStyle(document.querySelector('.mq-track')).transform");print('marquee moving',t1!=t2)
        await pg.touchscreen.tap(195,(await pg.evaluate("document.querySelector('.mq-row').getBoundingClientRect().top+60")));t1=await pg.evaluate("getComputedStyle(document.querySelector('.mq-track')).transform");await pg.wait_for_timeout(800)
        t2=await pg.evaluate("getComputedStyle(document.querySelector('.mq-track')).transform");print('tap paused',t1==t2)
        print('mbar visible after scroll',await pg.evaluate("document.getElementById('mbar').classList.contains('show')"))
        r=await pg.evaluate("(()=>{const a=document.querySelector('.mbar .mb-res').getBoundingClientRect();return [a.bottom<=innerHeight,a.right<=innerWidth]})()");print('reserve in viewport',r)
        await b.close()
asyncio.run(run())
