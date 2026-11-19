#!/usr/bin/env python3
"""Turn Guy's release build into the live index.html.

Usage: python3 tools/apply_web_edits.py guy/soul-shredder-release.html index.html [--platform android --version 1.0.0]

Gameplay is untouched. The script adds: a proper <head> (viewport, title, description,
link-preview tags, icons), the Press Start 2P font embedded (OFL licence), PostHog
analytics (cookieless, counts only), the real share address, and keeps RELEASE=true.
Every edit must match exactly once, so a new build from Guy that moved code fails loudly
instead of silently losing an event.
"""
import base64, pathlib, sys, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = 'https://soulshredder.oatmealmorning.com/'
PH_KEY = 'phc_qo4wiAUHZxUNwLi2nGGmHVEUX4cZxUcMNEMy5vxG6jBW'  # shared Oatmeal Morning project (public key)

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--platform', default='web'); ap.add_argument('--version', default='')
a = ap.parse_args()

s = pathlib.Path(a.src).read_text(encoding='utf-8')
font = base64.b64encode((ROOT / 'tools/press-start-2p-latin-400-normal.woff2').read_bytes()).decode()

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'EDIT FAILED ({n} matches): {old[:90]!r}')
    s = s.replace(old, new)

HEAD = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<title>Soul Shredder: a grim reaper quits his job to skate</title>
<meta name="description" content="A pixel-art skateboarding game told like a comic. Escape hell, learn to skate from five street skaters, win your first contest. Free, plays in your browser.">
<meta property="og:title" content="Soul Shredder">
<meta property="og:description" content="A grim reaper quits his job to skate. Escape hell. Shred the earth. Free, plays in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0b0710">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Soul Shredder">
<style>@font-face{{font-family:'Press Start 2P';font-style:normal;font-weight:400;font-display:block;src:url(data:font/woff2;base64,{font}) format('woff2')}}</style>
<script>
/* ---- analytics (PostHog, cookieless, no autocapture, no recordings, counts only) ---- */
const PH_KEY = '{PH_KEY}';
window.track = function(){{}};
if (PH_KEY) {{
  !function(t,e){{var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){{function g(t,e){{var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){{var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}},u.people.toString=function(){{return u.toString(1)+".people (stub)"}},o="init capture register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group identify setPersonProperties alias".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])}},e.__SV=1)}}(document,window.posthog||[]);
  const SS_BUILD = {{ platform: '{a.platform}', version: '{a.version}' }};
  let ssPid = null;   // app builds only: one random ID kept on the phone. The web game keeps no ID.
  if (SS_BUILD.platform !== 'web') {{ try {{ ssPid = localStorage.getItem('ss_pid'); if (!ssPid) {{ ssPid = 'ss-' + Array.from(crypto.getRandomValues(new Uint8Array(16)), x => ('0' + x.toString(16)).slice(-2)).join(''); localStorage.setItem('ss_pid', ssPid); }} }} catch (e) {{ ssPid = null; }} }}
  posthog.init(PH_KEY, Object.assign({{ api_host: 'https://us.i.posthog.com', persistence: 'memory', capture_pageview: true, autocapture: false, disable_session_recording: true }}, ssPid ? {{ bootstrap: {{ distinctID: ssPid }} }} : {{}}));
  posthog.register(Object.assign({{ app: 'soulshredder', platform: SS_BUILD.platform }}, SS_BUILD.version ? {{ app_version: SS_BUILD.version }} : {{}}));
  try {{ if (location.search.indexOf('tester=1') > -1) localStorage.setItem('om-tester', '1'); if (localStorage.getItem('om-tester') === '1') posthog.register({{ is_internal: true }}); }} catch (e) {{}}
  window.track = (ev, props, opts) => {{ try {{ posthog.capture(ev, props, opts); }} catch (e) {{}} }};
}}
/* one "run" = one attempt at a level, from game_start to level_win / game_over / game_quit */
let ssLv = 0, ssOn = false, ssT0 = 0;
function ssTrack(ev, p, o) {{ try {{ window.track(ev, p, o); }} catch (e) {{}} }}
function ssSec() {{ return Math.round((performance.now() - ssT0) / 1000); }}
function ssRun(lv) {{ ssLv = lv; ssOn = true; ssT0 = performance.now(); ssTrack('game_start', {{ level: lv }}); }}
function ssEnd(ev, p) {{ ssOn = false; p.seconds = ssSec(); ssTrack(ev, p); }}
function ssQuit(reason) {{ if (!ssOn) return; ssOn = false; ssTrack('game_quit', {{ level: ssLv, reason, seconds: ssSec() }}, {{ send_instantly: true, transport: 'sendBeacon' }}); }}
function ssComic() {{ try {{ return PANELS === PANELS1 ? ['intro', 1] : PANELS === PANELS2 ? ['level2', 2] : PANELS === PANELS3 ? ['level3', 3] : PANELS === PANELS3E ? ['ending', 3] : ['lesson', 2]; }} catch (e) {{ return ['other', ssLv]; }} }}
</script>
</head>
<body>
<title>Soul Shredder</title>'''

# 1. head, font, analytics (Guy's file starts with <title> and pulls the font from Google)
rep('''<title>Soul Shredder</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap">''', HEAD.replace('\n<title>Soul Shredder</title>', ''))

# 2. share the real address
rep("const SHARE_URL='https://oatmealmorning.com/'", f"const SHARE_URL='{URL}'")

# 3. release mode stays on (dev menu off)
if "const RELEASE=/*__RELEASE__*/true;" not in s:
    sys.exit('RELEASE is not true in this build')

# 4. events
# level 1
rep("function beginPlay(){setState('play');", "function beginPlay(){ssRun(1);setState('play');")
rep("if(h.dead>2&&state==='play'){setState('over');saveBest()}",
    "if(h.dead>2&&state==='play'){setState('over');saveBest();ssEnd('game_over',{level:1,score:G.score,kills:G.kills,tricks:G.tricks})}")
rep("if(g.exiting>3.4&&state==='play'){setState('clear');saveBest();",
    "if(g.exiting>3.4&&state==='play'){setState('clear');saveBest();ssEnd('level_win',{level:1,score:g.score,kills:g.kills,tricks:g.tricks,hits:g.hits});")
# level 2 (five lessons, no game over)
rep("function l2Chapter(i){", "function l2Chapter(i){if(i===0)ssRun(2);else ssTrack('level_progress',{level:2,chapter:i+1});")
rep("L2DONE=true;try{localStorage.setItem('ss_l2done','1')}catch(e){}L.mode='clear';",
    "L2DONE=true;try{localStorage.setItem('ss_l2done','1')}catch(e){}ssEnd('level_win',{level:2,tries:L.tries,bails:L.bails});L.mode='clear';")
# level 3 (three sessions, then win or lose)
rep("function l3Contest(){", "function l3Contest(){ssRun(3);")
rep("function l3Session(i){", "function l3Session(i){if(i>0)ssTrack('level_progress',{level:3,session:i+1});")
rep("function l3Win(){", "function l3Win(){ssEnd('level_win',{level:3,score:L.total});")
rep("else{L.mode='lose';L.t=0;SFX.hit()}", "else{ssEnd('game_over',{level:3,score:L.total});L.mode='lose';L.t=0;SFX.hit()}")
# leaving a run: pause menu, or app put away / phone locked
rep("if(inR(p,B.menu)){paused=false;", "if(inR(p,B.menu)){ssQuit('quit_button');paused=false;")
rep("function appBG(hide){if(hide){", "function appBG(hide){if(hide){ssQuit('app_hidden');")
# locked levels, share, skipped comics
rep("lockMsg=2;lockWhich=2;SFX.hit();return", "lockMsg=2;lockWhich=2;ssTrack('locked_level_tap',{level:2});SFX.hit();return")
rep("lockMsg=2;lockWhich=3;SFX.hit();return", "lockMsg=2;lockWhich=3;ssTrack('locked_level_tap',{level:3});SFX.hit();return")
rep("function shareGame(){SFX.page();", "function shareGame(){SFX.page();ssTrack('share_click',{where:state==='title'?'title':'pause',level:state==='title'?0:ssLv});")
rep("if(state==='comic'){if(inR(p,CB().skip)){comicEnd();return}",
    "if(state==='comic'){if(inR(p,CB().skip)){const c=ssComic();ssTrack('cutscene_skip',{cutscene:c[0],level:c[1],panel:cp+1});comicEnd();return}")
rep("if(e.code==='Escape'&&state==='comic'){comicEnd();return}",
    "if(e.code==='Escape'&&state==='comic'){const c=ssComic();ssTrack('cutscene_skip',{cutscene:c[0],level:c[1],panel:cp+1});comicEnd();return}")

s = s.rstrip() + '\n</body>\n</html>\n'
pathlib.Path(a.dst).write_text(s, encoding='utf-8')
print('ok', a.dst, len(s))
