# -*- encoding=utf8 -*-

from airtest.core.api import *

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

import time
import logging
logging.getLogger("airtest").setLevel(logging.WARNING)


RESULT = ''                    


def get_count_of_products(path):
    global RESULT
    
    count = -1

    try:
        filter_btn = poco('com.alibaba.aliexpresshd:id/search_btn_filter')
        filter_btn.click()
        
        count = poco('com.alibaba.aliexpresshd:id/refine_title_count').get_text()
        count = int(count.split()[0])

        wait(Template(r"tpl1526641312751.png", record_pos=(0.379, -0.753), resolution=(1080, 1920)))
        touch(Template(r"tpl1526641312751.png", record_pos=(0.379, -0.753), resolution=(1080, 1920)))

        wait(Template(r"tpl1526641468706.png", record_pos=(-0.421, -0.742), resolution=(1080, 1920)))
        touch(Template(r"tpl1526641468706.png", record_pos=(-0.421, -0.742), resolution=(1080, 1920)))
    except:
        pass
        
    if count == 0:
        RESULT += '\nZERO RESULT in Android app! {0}\n'.format(path)
    
    return count


def get_menu_items(element):
    menu_elements = []
    try:
        for menu in element.offspring('android.view.View'):
            title = menu.get_text().strip()
            if title > '':
                Y = menu.get_position()[1] * poco.device.display_info['height']
                menu_elements.append({'element': menu, 'Y': Y + 1, 'title': title})
    except:
        print('Can not get menu elements')
        print('- - - - - -')
        raise

    return menu_elements[::-1]


def click(item):
    title = item['title']
            
    print('\n\n-----\n{0}\n------\n\n'.format(title))
            
    swipe([10, 200], [10, 800])
    if item['Y'] > poco.device.display_info['height']:
        swipe([10, 700], [10, 100])
        item['Y'] = item['element'].get_position()[1] * poco.device.display_info['height']
        
    touch([100, item['Y']])
    time.sleep(0.5)

    
def check(element, path):
    
    count = get_count_of_products(path)
    
    if count < 0:
        menu_elements = get_menu_items(element)

        for item in menu_elements:
            click(item)
            
            if item['title'] != 'Назад':
                check(item['element'].sibling('android.widget.ListView'),
                      '{0} > {1}'.format(path, item['title'].strip()))

                
from datetime import datetime
start = datetime.now()

start_app("com.alibaba.aliexpresshd")                
touch(Template(r"tpl1527144269466.png", record_pos=(-0.189, -0.113), resolution=(1080.0, 1920.0)))
touch(Template(r"tpl1527144298312.png", record_pos=(0.377, 0.159), resolution=(1080, 1920)))
wait(Template(r"tpl1527144638838.png", record_pos=(-0.081, -0.737), resolution=(1080, 1920)))

poco = AndroidUiautomationPoco(force_restart=False)

try:
    init_e = [i for i in poco(resourceId="tmallmobilemenu", type='android.view.View')]
    check(init_e[0], '')
except Exception as e:
    print(e)
    pass    # we need to print results even in case of some exceptions

print(RESULT)

# Report time which required to perform full verification:
print('\n\n Full run took:')
print(datetime.now() - start)
