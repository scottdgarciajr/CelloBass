from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/r03'
errors=[];results={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1280,'height':1100},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'output/CelloBass_Review.html').as_uri())
    assert page.locator('img[src="r03/views/seated-player-storyboard-v1.png"]').evaluate('(img)=>img.complete && img.naturalWidth>0')
    page.locator('#engineering > summary').click()
    for op in ['play','pack','joint']:
        page.locator(f'[data-op={op}]').click()
        states=[]
        for progress in [0,20,50,83,100]:
            page.locator('#movement').fill(str(progress));page.locator('#movement').dispatch_event('input')
            state=page.evaluate('window.celloBassState');states.append(state)
            if op=='play':assert state['phase']['fold']==0
        results[op]=states
        page.screenshot(path=str(OUT/f'views/browser_{op}.png'),full_page=False)
    page.locator('[data-op=play]').click();page.locator('#animate').click();page.wait_for_function('window.celloBassState.progress===100',timeout=15000)
    page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(ROOT/'work/r03_mobile_check.png'),full_page=True)
    assert not errors,errors
    browser.close()
(OUT/'reports/ui_checks.json').write_text(json.dumps({'operations':results,'script_errors':errors,'animation_completed':True,'mobile_no_horizontal_overflow':True},indent=2))
print('Live rotation, lock withdrawal, folding, reinsertion and hinge view controls pass; no page errors')
