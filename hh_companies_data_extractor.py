from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import time
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(
        description='Extracting companies database from hh.ru')
parser.add_argument('--driver', type=str, required=True,
                    help='Path to the Chrome driver)')
args = parser.parse_args()


def gogo(li, browser):
    dalee = True
    while dalee == True:
        c = browser.find_elements_by_tag_name('td')
        for e in c:
            d = e.find_elements_by_tag_name('div')
            for q in d:
                a = q.find_element_by_tag_name('a')
                tt = (a.text, a.get_attribute('href'))
                li.append(tt)
        try:
            dal = browser.find_element_by_css_selector('body > div.HH-MainContent'+
                                                       ' > div.g-row.m-row_content'+
                                                       ' > div.g-col1.m-colspan3'+
                                                       ' > div.bloko-gap.bloko-gap_top'+
                                                       ' > div > a.bloko-button.HH-Pager'+
                                                       '-Controls-Next.HH-Pager-Control')
            dal.click()
        except:
            dalee = False


def extr(li, l, r, browser, fl=None): 
    print(f'===== Creating list of companies from {l} to {r} =====')
    if fl=='chr':
        with tqdm(total=r-l) as pbar:
            for i in range(l, r):
                cr = chr(i)
                browser.get(f"https://hh.ru/employers_list?areaId=113&letter={cr}")
                gogo(li, browser)
                pbar.update()
    if fl==None:
        browser.get(f"https://hh.ru/employers_list?areaId=113&&letter=%23")
        gogo(li, browser)


browser = Chrome(executable_path=args.driver)
co_list = []

extr(co_list, 65, 91, browser, 'chr')
extr(co_list, 1040, 1072, browser, 'chr')
extr(co_list, 0, 9, browser)

fin = {}
f = open('hh_dump.tsv', 'w', encoding='utf-8')
with tqdm(total=len(co_list)) as pbar:
    print('===== Extracting data =====')
    for e in co_list:
        try: 
            browser.get(e[1])
            c = browser.find_element_by_class_name('HH-SidebarView-Industries')
            d = c.find_elements_by_tag_name('p')
            g = [j.text for j in d[1:]]
            fin[e[0]] = g
            f.write(e[0] + '\t' + ', '.join(g) + '\n')
        except:
            fin[e[0]] = []
            f.write(e[0] + '\t' + '' + '\n')
        pbar.update()
        
f.close()

with open('hh_dump0.json', 'w', encoding='utf-8') as f:
    json.dump(fin, f, ensure_ascii=False)
