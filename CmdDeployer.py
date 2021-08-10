import logging
import os
import ctypes
import sys

import Container
import Settings
import Utils

if __name__ == "__main__":
    if not Utils.is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
    else:
        if os.path.basename(os.path.dirname(os.getcwd())) == 'GitHub':
            Utils.cmd_visibility(show=True)
        else:
            Utils.cmd_visibility(show=False)
        if not os.path.exists(Settings.logdir):
            os.mkdir(Settings.logdir)
        Settings.logfile = os.path.join(Settings.logdir, os.environ['COMPUTERNAME'] + ".log")
        if os.path.exists(Settings.logfile):
            os.remove(Settings.logfile)
        logging.basicConfig(filename=Settings.logfile, filemode='a', format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S', level=logging.INFO)
        Settings.logger = logging.getLogger()
        root = Container.FrameContainer()
        root.title("Command Deployer")
        root.iconbitmap(Settings.logo_loc)
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        width = Settings.width_perc * screenwidth
        height = Settings.height_perc * screenheight
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)
        root.geometry("{:0.0f}x{:0.0f}+{:0.0f}+{:0.0f}".format(width, height,
                        (screenwidth / 2) - (width / 2), (screenheight / 2) - (height / 2)))
        root.minsize(Settings.min_width, Settings.min_height)
        root.mainloop()
