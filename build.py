from pathlib import Path
from html import escape as e
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote
import yaml, shutil, zipfile, os, re

ROOT=Path(__file__).parent; DIST=ROOT/'dist'; AS=ROOT/'assets'; SLUG='just-pancake-simulator'; STORE='https://store.steampowered.com/app/5286420/Just_Pancake_Simulator/'
ORIGIN=os.environ.get('SITE_URL','https://ovov-games.seongeun52h.chatgpt.site').rstrip('/')
BASE=os.environ.get('SITE_BASE_PATH','').rstrip('/')
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir(); shutil.copytree(AS,DIST/'assets')

def read(path):
    raw=(ROOT/'content'/path).read_text(encoding='utf-8')
    _,front,body=raw.split('---',2)
    return yaml.safe_load(front) or {}, body.strip()

def data(lang,path):
    en,b_en=read('en/'+path)
    p=ROOT/'content'/lang/path
    if lang=='en' or not p.exists(): return en,b_en
    loc,b_loc=read(lang+'/'+path)
    return {**en,**{k:v for k,v in loc.items() if v not in (None,'')}}, b_loc or b_en

def sections(body):
    out={}; key=None
    for line in body.splitlines():
        if line.startswith('# '): key=line[2:].strip();out[key]=[]
        elif key and line.strip():out[key].append(line.strip())
    return {k:' '.join(v) for k,v in out.items()}

def features(body):
    items=[]; title=None; lines=[]; inside=False
    for line in body.splitlines():
        if line.startswith('# '):
            if inside: break
            inside=line[2:].strip()=='Key Features';continue
        if not inside: continue
        if line.startswith('## '):
            if title: items.append((title,' '.join(lines)))
            title=line[3:].strip();lines=[]
        elif line.strip():lines.append(line.strip())
    if title:items.append((title,' '.join(lines)))
    return items

def img(path,alt,cls='',loading='lazy'):
    return f'<img class="{cls}" src="/{path}" alt="{e(alt)}" loading="{loading}">'

def a(href,label,cls='button',target=''):
    return f'<a class="{cls}" href="{e(href,quote=True)}" {target}>{e(label)}</a>'

def layout(lang,route,title,description,content,og=None):
    home,_=data(lang,'home.md'); ko=lang=='ko'; t=lambda x,y:y if ko else x
    nav=f'<a href="/" class="wordmark" aria-label="ovov games Home"><span class="mark">ovov</span><small>GAMES</small></a><nav id="site-nav" aria-label="Main"><a href="/" class="{("active" if route=="/" else "")}">{t("Home","홈")}</a><a href="/games/" class="{("active" if route.startswith("/games") else "")}">{t("Games","게임")}</a></nav>'
    switch=f'<div class="lang" aria-label="Language"><a href="{route}?lang=en" lang="en" class="{("current" if not ko else "")}">EN</a><span aria-hidden="true">/</span><a href="{route}?lang=ko" lang="ko" class="{("current" if ko else "")}">KO</a></div>'
    # Language selection uses a cookie for clean canonical URLs; the query selects the cookie before rendering via client code.
    icon=quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#D85A32"/><text x="32" y="43" text-anchor="middle" fill="#FDF8F1" font-family="Arial" font-weight="bold" font-size="27">ovo</text></svg>')
    canonical=ORIGIN+route
    metaimg=f'<meta property="og:image" content="{ORIGIN}/{og}"><meta name="twitter:image" content="{ORIGIN}/{og}">' if og else ''
    footer=f'<footer><div class="footer-inner"><div><a class="footer-brand" href="/">ovov games</a><p>{e(home["about"])}</p></div><div><b>{t("Contact","문의")}</b><a href="mailto:ovovgames@gmail.com">ovovgames@gmail.com</a><div class="social"><a href="https://x.com/ovoveuni" target="_blank" rel="noopener">Developer X ↗</a><a href="https://www.youtube.com/@ovoveuni" target="_blank" rel="noopener">Developer YouTube ↗</a></div></div><div class="footer-bottom"><span>© 2026 ovov games. All rights reserved.</span><a href="#top">{t("Back to top ↑","맨 위로 ↑")}</a></div></div></footer>'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title,quote=True)}"><meta name="twitter:description" content="{e(description,quote=True)}">{metaimg}<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{icon}"><link rel="stylesheet" href="/style.css"><script defer src="/site.js"></script></head><body id="top"><header><div class="header-inner">{nav}<button class="menu-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Menu"><span></span><span></span></button>{switch}</div></header><main>{content}</main>{footer}</body></html>'''

def write(route,lang,html):
    name='index.html' if lang=='en' else 'ko.html'
    p=DIST/route.strip('/')/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html,encoding='utf-8')

for lang in ('en','ko'):
    ko=lang=='ko'; t=lambda x,y:y if ko else x
    home,_=data(lang,'home.md'); games,_=data(lang,'games.md'); game,_=data(lang,f'games/{SLUG}.md'); press,body=data(lang,f'press/{SLUG}.md'); desc=sections(body); feats=features(body)
    homecontent=f'''<section class="home-hero"><div class="home-art" aria-hidden="true"></div><div class="home-overlay"></div><div class="home-copy wrap"><span class="eyebrow">INDEPENDENT GAME STUDIO · SOUTH KOREA</span><h1>our value,<br><em>our variety.</em></h1><p>{e(home['about'])}</p><a href="/games/" class="text-link">{t('Explore our games ↗','게임 살펴보기 ↗')}</a></div></section><section class="home-feature wrap"><div class="section-label"><span>01 / FEATURED GAME</span><span>2026</span></div><div class="feature-row"><div><span class="eyebrow">A LITTLE COOKING EXPERIMENT</span><h2>Just Pancake<br>Simulator</h2><p>{e(game['short'])}</p>{a('/games/'+SLUG+'/',t('Discover the game ↗','게임 소개 보기 ↗'),'text-link')}</div><a class="feature-image" href="/games/{SLUG}/">{img('assets/'+SLUG+'/keyart/capsule_portrait.png','Just Pancake Simulator key art')}</a></div></section>'''
    write('/',lang,layout(lang,'/','ovov games',home['seo_description'],homecontent))
    listing=f'''<section class="page-intro wrap"><span class="eyebrow">OVOV GAMES / 01</span><h1>{e(games['heading'])}<span class="accent-dot">.</span></h1><p>{e(games['intro'])}</p></section><section class="game-band"><div class="game-band-bg"></div><div class="game-band-inner wrap"><div class="game-band-copy"><span class="eyebrow">01 / COMING OCTOBER 20, 2026</span><h2>Just Pancake<br>Simulator</h2><p>{e(game['oneline'])}</p><p>{e(game['short'])}</p><div class="actions">{a('/games/'+SLUG+'/',t('View game','게임 보기'))}{a('/press/'+SLUG+'/',t('Press kit ↗','프레스킷 ↗'),'button button-outline')}</div></div><a href="/games/{SLUG}/" class="game-card">{img('assets/'+SLUG+'/keyart/capsule_portrait.png','Just Pancake Simulator capsule art')}</a></div></section>'''
    write('/games/',lang,layout(lang,'/games/',t('Games | ovov games','게임 | ovov games'),game['oneline'],listing,'assets/'+SLUG+'/keyart/capsule_landscape.png'))
    detail=f'''<section class="detail-hero"><div class="detail-bg"></div><div class="wrap detail-inner"><div><span class="eyebrow">OVOV GAMES / GAME 01</span><h1>Just Pancake<br>Simulator</h1><p>{e(game['oneline'])}</p><div class="actions">{a(STORE,t('Wishlist on Steam ↗','Steam에서 찜하기 ↗'),'button','target="_blank" rel="noopener"')}{a('/press/'+SLUG+'/',t('Press kit','프레스킷'),'button button-outline')}</div></div><div class="detail-poster">{img('assets/'+SLUG+'/keyart/capsule_portrait.png','Just Pancake Simulator artwork')}</div></div></section><section class="wrap detail-story"><div class="section-label"><span>ABOUT THE GAME</span><span>2026</span></div><h2>{e(game['short'])}</h2><div class="screenshot-grid">{img('assets/'+SLUG+'/screenshots/screenshot_00.jpg','Pancake cooking gameplay screenshot')}{img('assets/'+SLUG+'/screenshots/screenshot_01.png','Just Pancake Simulator game screen')}</div></section>'''
    write('/games/'+SLUG+'/',lang,layout(lang,'/games/'+SLUG+'/', 'Just Pancake Simulator | ovov games',game['oneline'],detail,press['og_image']))
    icons='';facts=[(t('Developer','개발사'),press['developer']),(t('Release date','출시일'), 'October 20, 2026' if not ko else '2026년 10월 20일'),(t('Platforms','플랫폼'),'<a href="'+STORE+'" target="_blank" rel="noopener">Steam ↗</a>'),(t('Genres','장르'),', '.join(press['genres'])),(t('Playtime','플레이타임'),press.get('playtime')),(t('Price','가격'),press.get('price',{}).get('krw' if ko else 'usd')),(t('Languages','지원 언어'),', '.join(press['languages'])),(t('Generative AI Usages','생성형 AI 사용처'),press.get('ai_usage'))]
    facts_html=''.join(f'<div class="fact"><dt>{e(k)}</dt><dd>{v if k==t("Platforms","플랫폼") else e(str(v))}</dd></div>' for k,v in facts if v)
    features_html=''.join(f'<article class="feature"><span class="feature-num">0{i+1}</span><h3>{e(head)}</h3><p>{e(value)}</p></article>' for i,(head,value) in enumerate(feats))
    imgroot='assets/'+SLUG+'/'; screenshots=[('screenshots/screenshot_00.jpg','Pancake cooking gameplay'),('screenshots/screenshot_01.png','Just Pancake Simulator game screen')]; arts=[('keyart/capsule_portrait.png','Portrait capsule'),('keyart/capsule_landscape.png','Landscape capsule'),('keyart/capsule_square.png','Square capsule')]
    def gallery(items):
        return ''.join(f'<figure class="asset"><button class="zoom" data-src="/{imgroot+path}" data-alt="{e(label,quote=True)}" aria-label="{e("Enlarge "+label,quote=True)}">{img(imgroot+path,label)}</button><figcaption><span>{e(label)}</span><a href="/{imgroot+path}" download>{t("Download original ↓","원본 다운로드 ↓")}</a></figcaption></figure>' for path,label in items)
    presscontent=f'''<section class="press-hero"><div class="press-hero-image">{img(imgroot+'hero.png','Just Pancake Simulator hero art','', 'eager')}</div><div class="wrap press-head"><div><span class="eyebrow">OVOV GAMES / PRESS KIT</span><h1>Just Pancake Simulator</h1><p>{e(desc.get('One-line Description',''))}</p></div><div class="actions">{a(STORE,'Steam ↗','button','target="_blank" rel="noopener"')}</div></div></section><div class="wrap press-columns"><div class="press-main"><section class="press-section"><div class="section-label"><span>01 / THE GAME</span></div><div class="copy-head"><h2>{t('About the game','게임 소개')}</h2><button class="copy" data-copy="short">{t('Copy text','텍스트 복사')}</button></div><p id="short" class="lead">{e(desc.get('Short Description',''))}</p></section><section class="press-section"><div class="section-label"><span>02 / HIGHLIGHTS</span><button class="copy" data-copy="feature-list">{t('Copy features','특징 복사')}</button></div><h2>{t('Key features','주요 특징')}</h2><div class="features" id="feature-list">{features_html}</div></section></div><aside class="facts"><div class="facts-title"><span>FACT SHEET</span><span>↘</span></div><dl>{facts_html}</dl></aside></div><section class="wrap asset-section"><div class="section-label"><span>03 / MEDIA</span><span>DOWNLOADABLE ASSETS</span></div><h2>{t('Screenshots','스크린샷')}</h2><div class="assets-grid">{gallery(screenshots)}</div><h2>{t('Logos & key art','로고 및 키 아트')}</h2><div class="assets-grid">{gallery(arts)}</div><a class="button download-all" href="/{imgroot}press.zip" download>{t('Download all press assets ↓','전체 프레스 에셋 다운로드 ↓')}</a></section><section class="press-about"><div class="wrap press-about-inner"><div><span class="eyebrow">ABOUT THE STUDIO</span><h2>our value,<br><em>our variety.</em></h2></div><div><p>{e(home['about'])}</p><h3>PRESS CONTACT</h3><p>ovov games<br><a href="mailto:ovovgames@gmail.com">ovovgames@gmail.com ↗</a></p></div></div></section><div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image preview"><button class="lightbox-close" aria-label="Close preview">×</button><img alt=""><a class="button" download>{t('Download Original ↓','원본 다운로드 ↓')}</a></div>'''
    write('/press/'+SLUG+'/',lang,layout(lang,'/press/'+SLUG+'/', 'Just Pancake Simulator | Press Kit | ovov games',desc.get('Short Description',''),presscontent,press['og_image']))

zip_path=DIST/'assets'/SLUG/'press.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for path in sorted((AS/SLUG).rglob('*')):
        if path.is_file(): z.write(path,path.relative_to(AS/SLUG))
shutil.copy(ROOT/'style.css',DIST/'style.css');shutil.copy(ROOT/'site.js',DIST/'site.js')
# Relocate root-relative paths for a GitHub Pages project repository.
if BASE:
    for path in DIST.rglob('*.html'):
        html=path.read_text(encoding='utf-8')
        html=html.replace('href="/',f'href="{BASE}/').replace('src="/',f'src="{BASE}/')
        html=html.replace('href="'+ORIGIN+'/', 'href="'+ORIGIN+BASE+'/')
        html=html.replace('content="'+ORIGIN+'/', 'content="'+ORIGIN+BASE+'/')
        path.write_text(html,encoding='utf-8')
    css=DIST/'style.css';css.write_text(css.read_text().replace("url('/assets/", f"url('{BASE}/assets/"),encoding='utf-8')
(DIST/'.nojekyll').touch()

print('Built 4 routes x 2 languages:',DIST)
