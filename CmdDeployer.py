import logging
import os
import ctypes
import sys
import uuid

import Handler
import Settings
import Utils


if __name__ == "__main__":

    # Check UAC elevation and restart if not elevated
    if Settings.elevated_cred and not Utils.is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
    else:

        # Create non existing directories
        if not os.path.exists(Settings.logdir):
            os.mkdir(Settings.logdir)
        if not os.path.exists(Settings.temp_cmd_loc):
            os.mkdir(Settings.temp_cmd_loc)

        # Create unique identifiers for cmd- and logfile
        Settings.instance_uid = f"{uuid.uuid1()}_{os.environ['COMPUTERNAME']}"
        Settings.instance_cmdfile = os.path.join(Settings.temp_cmd_loc, f"{Settings.instance_uid}.cmd")

        # Logger setup
        Settings.logfile = os.path.join(Settings.logdir, f"{Settings.instance_uid}.log")
        Settings.logger = logging.getLogger('CmdDeployer')
        Settings.logger.setLevel(Settings.log_level)
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')
        filehandler = logging.FileHandler(filename=Settings.logfile)
        streamhandler = logging.StreamHandler()
        filehandler.setLevel(logging.DEBUG)
        streamhandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        streamhandler.setFormatter(formatter)
        Settings.logger.addHandler(filehandler)
        Settings.logger.addHandler(streamhandler)
        sys.excepthook = Utils.sys_exceptions

        # For hiding console window during runtime
        if not Settings.hide_cmd or os.path.basename(os.path.dirname(os.getcwd())) == 'GitHub':
            Utils.cmd_visibility(show=True)
        else:
            Utils.cmd_visibility(show=False)

        # Tkinter root window setup
        root = Handler.FrameHandler()
        root.title("Command Deployer")
        root.iconbitmap(Settings.logo_loc)
        root.protocol("WM_DELETE_WINDOW", Utils.exit_app)
        root.minsize(Settings.min_width, Settings.min_height)
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)

        # Screen size and screen centering
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        width = Settings.width_perc * screenwidth
        height = Settings.height_perc * screenheight
        root.geometry("{:0.0f}x{:0.0f}+{:0.0f}+{:0.0f}".format(width, height,
                        (screenwidth / 2) - (width / 2), (screenheight / 2) - (height / 2)))
        
        # Start program
        root.start_frame('Selection')
        root.mainloop()
