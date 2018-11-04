import sys
import pythoncom, pyHook
import threading
import os
import requests


from rslib import *
chars = ""
name = ""

paused = False


VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}


import time
import random



pause_key = '`'


event_binds = {
    'b': ['bag'],
    #'z': ['bag', 'bag_1', 0.5, 'bag_2', 'bag_2', 'bag_3'],
    #'m': ['settings', 'controls' , 'left_click_attack'],
    # 'n': ['settings', 'controls' , 'right_click_attack'],
    #'c': ['bag', 'bag_1', 0.08, 'bag_5', 0.08, 'bag_9'],
    #'g': ['food'],
    '2': ['prayer', 0.08, 'protect_melee', 0.08, 'bag'],
    '1': ['prayer', 0.08, 'protect_range', 0.08, 'bag'],
    '3': ['prayer', 0.08, 'protect_magic', 0.08, 'bag'],
    #'e': ['bag', 'bag', 'bag_25', 'bag_26', 'bag_27', 'magic', 'ice_blitz'],
    'e': ['magic', 'ice_barrage'],
    's': ['magic', 'ice_blitz'],
    'v': ['bag_8'],
    'q': ['bag_1'],
    'w': ['bag_2'],
    #'e': ['bag_3'],
    'x': ['prayer', 0.08, 'piety', 0.08, 'bag'],

    'z': ['run'],
    #'a': ['bag', 'bag_3', 0.15, 'combat_tab', 0.25, 'special_box'],

    ##'a': ['combat_tab', 0.25, 'special_box'],

    #'w': ['up_arrow'],
    #'s': ['down_arrow'],
    #'a': ['left_arrow'],
    #'d': ['right_arrow'],


    #'t': ['food'],
    #'l': ['reset_food_index'],
    #';': ['empty_inventory']
}

food_bag_index_start = 9
food_bag_index_end = 19
current_food_bag_index = food_bag_index_start

quick_mage_bind = 'e'
mage_set_on = False
reset_gear_bind = 'c'



tab_bottom_right_offsets = {
    'magic': (-20, -320),
        'smoke_burst': (-54, -255),
        'snare': (-145, -180),
        'fire_strike': (-170, -260),
        'ice_blitz': (-150 , -175),
        'ice_barrage': (-190, -115),

    'bag': (-110, -320),
        'bag_1': (-186 , -279),

    'combat_tab': (-215, -320),
        'special_box': (-170,-74),


    'run': (-175, 180),

    'prayer': (-55, -320),
        'protect_magic': (-160, -174),
        'protect_range': (-135, -174),
        'protect_melee': (-90, -174),
        'piety': (-160, -96),

    'settings': (-90, -30),
        'controls': (-40, -290),
            'left_click_attack': (-60, -140),
            'right_click_attack': (-100, -115),


    'q': ['bag_1'],
}


top_left_bag_x = -186
top_left_bag_y = -279


bag_spacing_x = 45
bag_spacing_y = 36


bag_number = 1


for bag_row_index in xrange(0, 7):
    for bag_column_index in xrange(0, 4):
        bag_key = 'bag_' + str(bag_number)

        if bag_key not in tab_bottom_right_offsets:
            this_bag_x = top_left_bag_x + (bag_spacing_x * bag_column_index)
            this_bag_y = top_left_bag_y + (bag_spacing_y * bag_row_index)

            tab_bottom_right_offsets[bag_key] = (this_bag_x, this_bag_y)

        bag_number += 1


import traceback
import multiprocessing
from multiprocessing import Process, Value, Array, freeze_support, Manager
lock = threading.Lock()



def press_key(key_name):
    win32api.keybd_event(VK_CODE[key_name], 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE[key_name],0 ,win32con.KEYEVENTF_KEYUP ,0)
    time.sleep(random.uniform(0.0, 0.5))




def rs_binds_loop():
    key_press_index = 0
    global paused
    global chars

    global mage_set_on
    global quick_mage_bind
    global reset_gear_bind

    rs_binds = None
    while True:

        try:
            active_window = get_active_window()
            active_window_name = get_window_name(active_window)


            if contains_any(active_window_name,['Konduit', 'RS', 'rs', 'runescape']):

                # print "RS IS ACTIVE"
                original_mouse_x, original_mouse_y = get_mouse_position()


                active_window_x, active_window_y  = get_window_position(active_window)
                active_window_width, active_window_height = get_window_size(active_window)

                def click_rs_item(item_name):
                    try:
                        rs_click_x = active_window_width + tab_bottom_right_offsets[item_name][0]
                        rs_click_y = active_window_height + tab_bottom_right_offsets[item_name][1]


                        if item_name == 'run':
                            rs_click_x = active_window_width + tab_bottom_right_offsets[item_name][0]
                            rs_click_y = tab_bottom_right_offsets[item_name][1]


                        active_window_x, active_window_y = get_window_position(active_window)
                        screen_click_x = active_window_x + rs_click_x
                        screen_click_y = active_window_y + rs_click_y
                        click(screen_click_x, screen_click_y)
                    except:
                        traceback.print_exc()


                def execute_command_list(command_list):
                    print "EXECUTING COMMAND LIST: " + str(command_list)

                    for command_index in xrange(0, len(command_list)):
                        command = command_list[command_index]

                        global current_food_bag_index
                        if type(command) == type(float()):
                            time.sleep(command)
                        elif command == 'food':
                            click_rs_item('bag_' + str(current_food_bag_index))
                            current_food_bag_index += 1
                            if current_food_bag_index > food_bag_index_end:
                                current_food_bag_index = food_bag_index_start
                        elif command == 'reset_food_index':
                            current_food_bag_index = food_bag_index_start
                        elif command == 'empty_inventory':
                            for x in xrange(8,29):
                                print x
                        elif command == 'up_arrow' or command == 'down_arrow' or command == 'left_arrow' or command == 'right_arrow':
                            print command
                            press_key(command)


                        else:
                            click_rs_item(command)


                        if command_index < len(command_list) - 1:
                            #dont sleep after the last command
                            time.sleep(0.03)


                key_list_json = get_key_list_json_from_file()

                if len(key_list_json['key_list']) > 0:

                    while key_press_index < len(key_list_json['key_list']):
                        key_string = key_list_json['key_list'][key_press_index]
                        print key_string

                        if key_string == "oem_3`":
                            paused = not paused
                            print "paused: ```" + str(paused)

                        if not paused:
                            if key_string in event_binds:
                                command_list = event_binds[key_string]

                                if key_string == quick_mage_bind:
                                    print 'keystring == quick mage bind'
                                    print 'mage_set_on ' + str(mage_set_on)

                                    if mage_set_on:
                                        print 'mage set is on, exectuing [-2::]'
                                        execute_command_list(command_list[-2::])
                                    else:
                                        print 'setting mage_set_on to true'
                                        mage_set_on = True
                                        print 'executing command list'
                                        print command_list
                                        execute_command_list(command_list)
                                else:

                                    if key_string == reset_gear_bind:
                                        print 'RESETTING GEAR'
                                        global mage_set_on
                                        mage_set_on = False

                                    execute_command_list(command_list)


                                move_mouse(original_mouse_x, original_mouse_y)
                            else:
                                pass

                        key_press_index += 1

        except:
            print traceback.print_exc()
            continue

import json

key_press_list_json_file_name = 'key_presses.txt'


def clear_json_file():
    f = open(key_press_list_json_file_name, 'w')
    f.write('{"key_list":[]}')
    f.close()



def save_key_list_json_to_file(file_json):
    f = open(key_press_list_json_file_name, 'w')

    file_json_string = json.dumps(file_json)
    f.write(json.dumps(file_json))
    f.close()


def add_key_press_to_file(key_string):
    f = open(key_press_list_json_file_name, 'r+')
    file_text = f.read()
    file_json = json.loads(file_text)


    key_string = key_string.lower()
    file_json['key_list'].append(key_string)

    save_key_list_json_to_file(file_json)
    f.close()


def get_key_list_json_from_file():
    f = open(key_press_list_json_file_name, 'r+')
    try:
        file_text = f.read()
        file_json = json.loads(file_text)

        f.close()
        return file_json
    except:
        return {'key_list': []}



def OnKeyboardEvent(event):
    active_window = get_active_window()
    active_window_name = get_window_name(active_window)


    if contains_any(active_window_name,['Konduit']):
        try:
            global paused
            global chars

            char = ""

            if event.Ascii == 8:
                print "Backspace was pressed"
                char = ""
                chars = chars[:-1]

            elif event.Ascii == 13:
                char = "\n"
            else:

                if event.Ascii != 0:
                    char = chr(event.Ascii)
                else:
                    char = event.Key


            char = char.lower()

            global event_binds

            if not paused:
                if char in event_binds and 'arrow' in event_binds[char][0]:
                    #win32api.keybd_event(VK_CODE[event_binds[char][0]], 0,0,0)
                    pass
                else:
                    add_key_press_to_file(char)

        except:
            print "Error, skipping this char"


        return True

def use_special():
    print 'using spec'




def OnKeyUp(event):

    try:
        global paused
        global chars

        #Check for backspace
        char = ""

        if event.Ascii == 8:
            print "Backspace was pressed"
            char = ""
            chars = chars[:-1]

        elif event.Ascii == 13:
            char = "\n"
        else:
            if event.Ascii != 0:
                char = chr(event.Ascii)

        # print "ascii value: " + str(event.Ascii)
        # print "ascii: " + char

        global event_binds

        if not paused:
            if char in event_binds and 'arrow' in event_binds[char][0]:
                win32api.keybd_event(VK_CODE[event_binds[char][0]],0 ,win32con.KEYEVENTF_KEYUP ,0)



        # managed_dict['event_queue'].append(char)
        #
        # print managed_dict['event_queue']



    except:
        print "Error, skipping this char"


    return True

from multiprocessing import Queue

if __name__ == '__main__':
    clear_json_file()
    multiprocessing.freeze_support()
    hm = pyHook.HookManager()

    hm.KeyDown = OnKeyboardEvent
    hm.KeyUp = OnKeyUp
    hm.HookKeyboard()

    p = Process(target=rs_binds_loop, args=())
    p.start()

    try:
        pythoncom.PumpMessages()   #This call will block forever unless interrupted,
                               # so get everything ready before you execute this.

    except (KeyboardInterrupt, SystemExit) as e: #We will exit cleanly if we are told
        print(e)
        os._exit()

    p.join()



