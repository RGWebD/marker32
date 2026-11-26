document.documentElement.classList.add('js');
(function(){
 var hd=document.getElementById('hd'),mbar=document.getElementById('mbar'),hero=document.querySelector('.hero');
 function onScroll(){var y=window.scrollY,h=hero?hero.offsetHeight:0;
  if(hero&&hd)hd.classList.toggle('solid',y>h-90);
  if(mbar)mbar.classList.toggle('show',hero?y>h*0.6:true);}
 window.addEventListener('scroll',onScroll,{passive:true});onScroll();
 // reveals
 var rv=document.querySelectorAll('.rv');
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(el){io.observe(el)});}
 else rv.forEach(function(el){el.classList.add('in')});
 // marquee: tap to pause on touch
 var mq=document.querySelector('.mq');
 if(mq){mq.addEventListener('click',function(){mq.classList.toggle('paused')});
  if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(en){mq.querySelectorAll('.mq-track').forEach(function(t){t.style.animationPlayState=en.isIntersecting?'':'paused'})})}).observe(mq);}}
 // live status, America/New_York
 var live=document.getElementById('live'),st=document.getElementById('status');
 var HOL={'2026-11-26':'Thanksgiving','2026-11-27':'Black Friday','2026-12-24':'Christmas Eve','2026-12-25':'Christmas Day','2026-12-31':'New Year’s Eve','2027-01-01':'New Year’s Day'};
 // [day 0=Sun..6] -> list of [openMin,closeMin,label]
 var H={0:[[630,870,'brunch'],[1020,1260,'dinner']],1:[[1020,1320,'dinner']],2:[[1020,1320,'dinner']],3:[[1020,1320,'dinner']],4:[[1020,1320,'dinner']],5:[[1020,1320,'dinner']],6:[[1020,1320,'dinner']]};
 function fmt(m){var h=Math.floor(m/60),mm=m%60,ap=h>=12?'PM':'AM';h=h%12||12;return h+(mm?':'+String(mm).padStart(2,'0'):'')+' '+ap}
 function nowNY(){var p={};new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23',weekday:'short'}).formatToParts(new Date()).forEach(function(x){p[x.type]=x.value});
  var wd={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[p.weekday];return{d:wd,m:+p.hour*60+ +p.minute,key:p.year+'-'+p.month+'-'+p.day}}
 function keyPlus(key,n){var d=new Date(key+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10)}
 function status(){var n=nowNY(),txt,open=false,today=H[n.d],hol=HOL[n.key];
  for(var i=0;i<today.length;i++){var s=today[i];if(n.m>=s[0]&&n.m<s[1]){open=true;txt='Open now · '+s[2]+' until '+fmt(s[1]);break;}}
  if(!open){var nx=null;for(var j=0;j<today.length;j++){if(n.m<today[j][0]){nx='Closed now · opens today at '+fmt(today[j][0]);break;}}
   if(!nx){var t=(n.d+1)%7,tk=keyPlus(n.key,1);nx='Closed now · opens tomorrow at '+fmt(H[t][0][0])+(HOL[tk]?' ('+HOL[tk]+': hours may differ)':'');}txt=nx;}
  if(hol)txt+=' · '+hol+': hours may differ, please call';
  if(live){live.textContent=txt;live.className='live '+(open?'open':'closed');}
  if(st)st.textContent=txt;
  var rows=document.querySelectorAll('.hours tr');rows.forEach(function(r){r.classList.toggle('today',+r.dataset.d===(n.d+6)%7)});}
 if(live||st){status();setInterval(status,60000);}
 // menu filter + search
 var chips=document.querySelectorAll('.chip'),q=document.getElementById('q');
 if(chips.length){var cur='all';
  document.querySelectorAll('.mn-i').forEach(function(li){li._n=li.querySelector('.mn-n').textContent;var d=li.querySelector('.mn-d');li._d=d?d.textContent:'';});
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function hl(t,w){if(!w)return esc(t);var i=t.toLowerCase().indexOf(w);if(i<0)return esc(t);return esc(t.slice(0,i))+'<mark>'+esc(t.slice(i,i+w.length))+'</mark>'+esc(t.slice(i+w.length))}
  function apply(){var w=(q&&q.value||'').trim().toLowerCase(),any=false;
   document.querySelectorAll('.mn-sec').forEach(function(sec){var showSec=cur==='all'||sec.dataset.cat===cur,secAny=false;
    sec.querySelectorAll('.mn-grp').forEach(function(g){var gAny=false;
     g.querySelectorAll('.mn-i').forEach(function(li){var w2=w==='gluten free'||w==='gf'?'(gf)':w;var hit=!w||(li._n+' '+li._d).toLowerCase().indexOf(w2)>=0||(w2==='(gf)'&&/gluten free/i.test(li._d));
      li.hidden=!hit;li.querySelector('.mn-n').innerHTML=hl(li._n,w);var d=li.querySelector('.mn-d');if(d)d.innerHTML=hl(li._d,w);if(hit)gAny=true;});
     g.hidden=!gAny;if(gAny)secAny=true;});
    sec.hidden=!(showSec&&secAny);if(!sec.hidden)any=true;});
   document.getElementById('empty').hidden=any;}
  // keep the results in view: if the reader is scrolled below the top of the menu, jump back to it after filtering
  var start=document.getElementById('mn-start');
  function jump(){var hdH=(hd?hd.offsetHeight:0),y=Math.max(0,start.getBoundingClientRect().top+window.scrollY-hdH-8);if(window.scrollY>y+4)window.scrollTo(0,y);}
  function toTop(){if(!start)return;jump();requestAnimationFrame(jump);setTimeout(jump,60);}
  chips.forEach(function(c){c.addEventListener('click',function(){cur=c.dataset.f;chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});apply();toTop();})});
  if(q)q.addEventListener('input',function(){apply();toTop();});
  // web fonts can swap in after the browser jumps to #dinner/#brunch/#cocktails; land on the section again once they are ready
  var h=location.hash.slice(1),tgt=h&&document.getElementById(h);
  if(tgt&&document.fonts&&document.fonts.ready){var moved=false,mark=function(){moved=true};window.addEventListener('wheel',mark,{once:true,passive:true});window.addEventListener('touchstart',mark,{once:true,passive:true});
   var land=function(){if(!moved)tgt.scrollIntoView();};
   window.addEventListener('load',function(){document.fonts.ready.then(function(){land();setTimeout(land,700);});});}
 }
})();
