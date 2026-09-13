"""Render the exact local assets in Chromium without navigation when managed policy blocks file/HTTP."""
from pathlib import Path
import sys,json,re,zipfile,threading,urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from package import inline_html
checks=[]
def ck(name,ok,detail=''):
 checks.append(dict(name=name,pass_=bool(ok),detail=detail));print('PASS' if ok else 'FAIL',name)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1050},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(inline_html(),wait_until='load');page.evaluate('document.fonts.ready');page.wait_for_timeout(400)
 ck('4 drawing tabs',page.locator('.tab').count()==4)
 ck('initial SVG drawing loaded',page.locator('#svg-host>svg').count()==1)
 ck('initial overview contains battery module',page.locator('g.component[data-ref="BT1"]').count()==1)
 page.locator('g.component[data-ref="BT1"]').click(force=True)
 ck('actual pointer component selection',page.locator('#inspector').is_visible() and 'LiFePO4' in page.locator('#inspect-content').inner_text())
 page.locator('#inspect-content tr[data-net="BAT_POS"]').click()
 ck('net inspector traverses real members','F0' in page.locator('#inspect-content').inner_text())
 page.locator('#close-inspector').click();ck('inspector can close',not page.locator('#inspector').is_visible())
 before=page.evaluate('CartWiringViewer.getState().view.w');page.locator('#zoom-in').click();after=page.evaluate('CartWiringViewer.getState().view.w')
 ck('zoom in changes actual viewBox',after<before)
 page.locator('#fit').click();ck('fit restores width',page.evaluate('CartWiringViewer.getState().view.w')==2040)
 page.mouse.move(850,680);page.mouse.down();page.mouse.move(950,740,steps=8);page.mouse.up();ck('pointer pan changes viewBox',page.evaluate('CartWiringViewer.getState().view.x')!=30)
 page.locator('#fit').click();page.mouse.move(850,650);page.mouse.wheel(0,-200);page.wait_for_timeout(150);ck('wheel zoom changes viewBox',page.evaluate('CartWiringViewer.getState().view.w')<2040)
 page.locator('#fit').click()
 for i in range(4):
  page.locator('.tab').nth(i).click();ck('switch drawing '+str(i+1),page.evaluate('CartWiringViewer.getState().sheet')==i and page.locator('#svg-host>svg').count()==1)
 ck('breadboard renders 400 holes',page.locator('.hole').count()==400)
 page.locator('[data-hole="e3"]').click(force=True)
 ck('breadboard contact shows U2 pin1','U2.1' in page.locator('#inspect-content').inner_text())
 page.locator('#close-inspector').click();page.locator('[data-hole="T+23"]').click(force=True)
 ck('rail uses independent 1-25 count','1-25' in page.locator('#inspect-content').inner_text() and 'TOF1.VIN' in page.locator('#inspect-content').inner_text())
 page.locator('#close-inspector').click()
 with page.expect_download() as dinfo:page.locator('#save-svg').click()
 download=dinfo.value;out=R/'tests/tmp-export.svg';download.save_as(out)
 ck('SVG export is real vector drawing',out.read_text().startswith('<svg') and 'SN74AHCT125N' in out.read_text());out.unlink()
 for key,name in [('pdf','Smart-Cart-Wiring-B1.pdf'),('eda','Smart-Cart-B1-EDA.zip')]:
  with page.expect_download() as di:page.locator(f'a[data-download="{key}"]').click()
  dest=R/'tests'/('tmp-'+name);di.value.save_as(dest)
  ck('embedded '+key+' download byte-identical',dest.read_bytes()==(R/'downloads'/name).read_bytes());dest.unlink()
 page.locator('.tab').nth(0).click();page.screenshot(path=str(R/'tests/desktop.png'))
 page.locator('.tab').nth(3).click();page.screenshot(path=str(R/'tests/breadboard-view.png'))
 ck('desktop no document overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 # mobile same assets and pointer-based event handlers
 mobile=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1)
 mobile.set_content(inline_html(False),wait_until='load');mobile.evaluate('document.fonts.ready')
 ck('mobile no horizontal page overflow',mobile.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 mobile.locator('.tab').nth(2).tap();ck('mobile tab selection',mobile.evaluate('CartWiringViewer.getState().sheet')==2)
 mobile.evaluate("CartWiringViewer.select('U1')")
 ck('mobile inspector within viewport',mobile.locator('#inspector').bounding_box()['x']>=0 and mobile.locator('#inspector').bounding_box()['width']<=390)
 mobile.screenshot(path=str(R/'tests/mobile.png'))
 ck('no JavaScript runtime errors',not errors,str(errors))
 # Check all printed page bodies fit above footer. Excludes drawings which use viewBox.
 pr=b.new_page();pr.set_content((R/'docs/print.html').read_text(),wait_until='load');pr.evaluate('document.fonts.ready')
 result=pr.evaluate("""Array.from(document.querySelectorAll('.appendix')).map((p,i)=>({page:i+5,body:p.querySelector('article').getBoundingClientRect().bottom,footer:p.querySelector('footer').getBoundingClientRect().top}))""")
 for q in result:ck('PDF content clear of footer page '+str(q['page']),q['body']<q['footer']-3,str(q))
 b.close()
# Check static files over local HTTP independently (Chromium navigation was policy blocked).
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
paths=['index.html','css/app.css','js/app.js','js/design.js','js/drawings.js','downloads/Smart-Cart-Wiring-B1.pdf','downloads/Smart-Cart-B1-EDA.zip']
for path in paths:
 with urllib.request.urlopen(base+path) as resp:ck('HTTP static resource '+path,resp.status==200 and len(resp.read())>0)
server.shutdown()
report={'environment':'Chromium 144, 1600x1050 desktop / 390x844 mobile','load_method':'Exact local HTML/CSS/JS inlined using page.set_content. Native file:// and local HTTP browser navigation are blocked by environment policy; not claimed as browser transport tests. Local HTTP file responses tested separately.','passed':sum(c['pass_'] for c in checks),'total':len(checks),'checks':checks,'not_executed':['EasyEDA Pro import','Native KiCad load / ERC','Hardware tests','Safari / Firefox / real mobile device']}
(R/'tests/browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Result',report['passed'],'/',report['total']);sys.exit(0 if report['passed']==report['total'] else 1)
