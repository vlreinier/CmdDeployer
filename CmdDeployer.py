import logging
import Container
import Settings
import os

if __name__ == "__main__":
    if not os.path.exists(Settings.logdir):
        os.mkdir(Settings.logdir)
    logfile = os.path.join(Settings.logdir, os.environ['COMPUTERNAME'] + ".log")
    if os.path.exists(logfile):
        os.remove(logfile)
    logging.basicConfig(
        filename=logfile,
        filemode='a',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO,
    )
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
