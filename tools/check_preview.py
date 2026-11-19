from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto((ROOT/'output/CelloBass_Review.html').as_uri())
    captions={}
    for name in ['cello','bass','transition','travel']:
        page.locator(f'button[data-state="{name}"]').click()
        captions[name]=page.locator('#caption').inner_text()
        assert captions[name]
    page.locator('button[data-state="cello"]').click()
    page.screenshot(path=str(ROOT/'output/views/review_browser_check.png'),full_page=False)
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.screenshot(path=str(ROOT/'work/review_mobile_check.png'),full_page=True)
    assert not errors,errors
    browser.close()
(ROOT/'output/reports/review_ui_check.json').write_text(json.dumps({'browser':'headless Chromium, existing installation','state_buttons':captions,'desktop_and_mobile_no_horizontal_overflow':True,'page_errors':errors},indent=2))
print('Four states rendered; desktop/mobile layout checks pass; no JavaScript errors')
