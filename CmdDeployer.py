import logging
import os
import ctypes
import sys
import datetime

import Container
import Settings
import Utils

if __name__ == "__main__":

    # Check UAC elevation
    if not Utils.is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
    else:
        # Init actions and variables
        if not os.path.exists(Settings.logdir):
            os.mkdir(Settings.logdir)
        if not os.path.exists(Settings.temp_cmd_loc):
            os.mkdir(Settings.temp_cmd_loc)
        Settings.instance_uid = f"{datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')}_{os.environ['COMPUTERNAME']}"
        Settings.instance_cmdfile = os.path.join(Settings.temp_cmd_loc, f"{Settings.instance_uid}.cmd")

        # Logger setup
        Settings.logfile = os.path.join(Settings.logdir, f"{Settings.instance_uid}.log")
        Settings.logger = logging.getLogger('CmdDeployer')
        sys.excepthook = Utils.sys_exceptions
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
        handler = logging.FileHandler(Settings.logfile, mode='a', level=logging.INFO, formatter=formatter)
        Settings.logger.addHandler(handler)

        # For hiding CMD window
        if os.path.basename(os.path.dirname(os.getcwd())) == 'GitHub':
            Utils.cmd_visibility(show=True)
        else:
            Utils.cmd_visibility(show=False)

        # Tkinter root window
        root = Container.FrameContainer()
        root.title("Command Deployer")
        root.iconbitmap(Settings.logo_loc)
        root.protocol("WM_DELETE_WINDOW", Utils.exit_app)
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
