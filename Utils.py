from os import system
from os.path import exists, dirname
from ctypes import WinDLL
from Settings import temp_cmd_loc
from sys import exit
from shutil import rmtree

def obj_bg(obj, bg):
    obj.config(bg=bg)


def lambdaf_event(func, *args):
    return lambda e: func(*args)


def lambdaf(func, *args):
    return lambda: func(*args)


def pingable(target, test_pings=4):
    return system("ping " + f"-n {test_pings} " + target + '| find "TTL=" > nul') == 0


def cmd_visibility(option=0):
    hWnd = WinDLL('kernel32').GetConsoleWindow()
    if hWnd:
        WinDLL('user32').ShowWindow(hWnd, option)


def yview(canvas, *args):
    if canvas.yview() == (0.0, 1.0):
        return
    canvas.yview(*args)


def _on_mousewheel(event, canvas):
    yview(canvas, 'scroll', int(-1 * (event.delta / 120)), "units")


def exit_app():
    dir_name = dirname(temp_cmd_loc)
    if exists(dir_name):
        rmtree(dir_name, ignore_errors=True)
    exit()
