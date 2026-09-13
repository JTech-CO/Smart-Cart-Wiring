"""Render local print source through Chromium. Requires Playwright and Chromium."""
from pathlib import Path
import argparse,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
def main():
 out=R/'downloads/Smart-Cart-Wiring-B1.pdf';exe=shutil.which('chromium') or shutil.which('chromium-browser')
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
  page=browser.new_page();page.set_content((R/'docs/print.html').read_text(),wait_until='load');page.evaluate('document.fonts.ready');page.emulate_media(media='print')
  size=page.locator('.page').count();page.pdf(path=str(out),format='A3',landscape=True,print_background=True,prefer_css_page_size=True)
  browser.close()
 print('PDF pages requested:',size,'bytes:',out.stat().st_size)
if __name__=='__main__':main()
