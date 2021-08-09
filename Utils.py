import os
import ctypes
import sys
import shutil
import Settings

def obj_bg(obj, bg):
    obj.config(bg=bg)


def lambdaf_event(func, *args):
    return lambda e: func(*args)


def lambdaf(func, *args):
    return lambda: func(*args)


def pingable(target, test_pings=4):
    return os.system("ping " + f"-n {test_pings} " + target + '| find "TTL=" > nul') == 0


def cmd_visibility(option=0):
    hWnd = ctypes.WinDLL('kernel32').GetConsoleWindow()
    if hWnd:
        ctypes.WinDLL('user32').ShowWindow(hWnd, option)


def yview(canvas, *args):
    if canvas.yview() == (0.0, 1.0):
        return
    canvas.yview(*args)


def _on_mousewheel(event, canvas):
    yview(canvas, 'scroll', int(-1 * (event.delta / 120)), "units")


def exit_app():
    dir_name = os.path.dirname(Settings.temp_cmd_loc)
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name, ignore_errors=True)
    sys.exit()
