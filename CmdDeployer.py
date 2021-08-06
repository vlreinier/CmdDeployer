from os import path

from Utils import cmd_visibility
from Container import FrameContainer
from Settings import logo_loc, config_loc, width_perc, height_perc, min_width, min_height

if __name__ == "__main__":
    if path.isfile(config_loc):

        cmd_visibility()
        root = FrameContainer()
        root.title("Command Deployer")

        if path.isfile(logo_loc):
            root.iconbitmap(logo_loc)

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        width = width_perc * screenwidth
        height = height_perc * screenheight
        root.geometry("{:0.0f}x{:0.0f}+{:0.0f}+{:0.0f}".format(width, height,
                      (screenwidth / 2) - (width / 2), (screenheight / 2) - (height / 2)))

        root.minsize(min_width, min_height)

        root.mainloop()
