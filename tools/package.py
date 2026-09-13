"""Package self-contained viewer and import-only JSON archive. No fabrication data."""
from pathlib import Path
import re,json,base64,zipfile,hashlib,shutil
R=Path(__file__).resolve().parents[1];OUT=R.parent

def inline_html(embed_downloads=True):
 text=(R/'index.html').read_text()
 text=re.sub(r'<link rel="stylesheet" href="\./css/app.css">','<style>'+(R/'css/app.css').read_text()+'</style>',text)
 text=re.sub(r'<script defer src="\./js/[^\"]+"></script>','',text)
 text=text.replace('./assets/favicon.svg','data:image/svg+xml;base64,'+base64.b64encode((R/'assets/favicon.svg').read_bytes()).decode())
 text=text.replace('href="./index.html"','href="#"')
 embeds={}
 if embed_downloads:
  for typ,name,mime in [('pdf','Smart-Cart-Wiring-B1.pdf','application/pdf'),('eda','Smart-Cart-B1-EDA.zip','application/zip')]:
   p=R/'downloads'/name
   embeds[typ]={'name':name,'type':mime,'base64':base64.b64encode(p.read_bytes()).decode()}
 body='<script>window.CART_EMBEDDED_DOWNLOADS='+json.dumps(embeds)+';</script>' if embeds else ''
 for name in ['design.js','drawings.js','app.js']:
  js=(R/'js'/name).read_text().replace('</script','<\\/script');body+='<script>'+js+'</script>'
 return text.replace('</body>',body+'</body>')

def build():
 with zipfile.ZipFile(R/'downloads/Smart-Cart-B1-EDA.zip','w',zipfile.ZIP_DEFLATED) as z:
  p=R/'eda/easyeda/SmartCart-B1-Modules.json';z.write(p,p.name)
 (OUT/'Smart-Cart-Wiring-B1-Preview.html').write_text(inline_html())
 for name in ['Smart-Cart-Wiring-B1.pdf','Smart-Cart-B1-EDA.zip']:shutil.copy2(R/'downloads'/name,OUT/name)
 shutil.copy2(R/'eda/easyeda/SmartCart-B1-Modules.json',OUT/'SmartCart-B1-Modules.json')
 sha=[]
 for p in sorted(R.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt':sha.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R)))
 (R/'SHA256SUMS.txt').write_text('\n'.join(sha)+'\n')
 with zipfile.ZipFile(OUT/'Smart-Cart-Wiring-B1.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(R.rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:z.write(p,Path(R.name)/p.relative_to(R))
 print('Artifacts:',[(p.name,p.stat().st_size) for p in OUT.glob('Smart-Cart-*') if p.is_file()])
if __name__=='__main__':build()
