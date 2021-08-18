import os
import ctypes
import sys
import shutil
import traceback
import time

import Settings


def obj_bg(obj, bg):
    obj.config(bg=bg)


def lambdaf_event(func, *args):
    return lambda e: func(*args)


def lambdaf(func, *args):
    return lambda: func(*args)


def pingable(target, test_pings=4):
    return os.system("ping " + f"-n {test_pings} " + target + '| find "TTL=" > nul') == 0


def cmd_visibility(show=True):
    hWnd = ctypes.WinDLL('kernel32').GetConsoleWindow()
    if hWnd:
        ctypes.WinDLL('user32').ShowWindow(hWnd, int(show))


def yview(canvas, *args):
    if canvas.yview() == (0.0, 1.0):
        return
    canvas.yview(*args)


def _on_mousewheel(event, canvas):
    yview(canvas, 'scroll', int(-1 * (event.delta / 120)), "units")


def exit_app():
    for handler in Settings.logger.handlers[:]:
        handler.close()
        Settings.logger.removeHandler(handler)
    if os.path.exists(Settings.logfile):
        os.remove(Settings.logfile)
    if os.path.exists(Settings.instance_cmdfile):
        os.remove(Settings.instance_cmdfile)
    if len(os.listdir(Settings.temp_cmd_loc)) == 0:
        shutil.rmtree(Settings.temp_cmd_loc)
    Settings.logger.info("PROGRAM WILL BE SHUT DOWN")
    sys.exit()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def sys_exceptions(type, value, tb):
    message = ''.join(traceback.format_exception(type, value, tb))
    Settings.logger.error(f'Caught {type} with value {value}\n' + message)


def thread_exceptions(args):
    Settings.logger.exception(f'Caught {args.exc_type} with value {args.exc_value} in thread {args.thread}')
