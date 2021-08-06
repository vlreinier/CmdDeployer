# CmdDeployer
Python Tkinter application for deploying Batch/CMD and Powershell commands to a local machine or multiple remote machines.<br>
This app uses Tkinter as a GUI and Psexec.exe and Python module subprocess to execute commands remotely, and redirect cmd output.<br>
No external libraries are required for running the app without compiling it to an standalone executable (at least when using Python 3.8).

## Compiling CmdDeployer to .exe
The app can be compiled using a multitude of modules.<br>
Before compiling, make sure cmd_visibility() in CmdDeployer.py is uncommented.<br>
Here the process for Pyinstaller is described:

Install Pyinstaller and PyQt5. CD into the root CmdDeployer folder where CmdDeployer.py is located.<br>
From here, run the following command to create the exe installer:

```
pyinstaller --uac-admin --clean CmdDeployer.py --icon images\cmdlogo.ico
```

It is adviced to avoid the --onefile option using Pyinstaller, since this increases startup time significantly.

## Running CmdDeployer uncompiled
First make sure cmd_visibility() in CmdDeployer.py is commented out, or the app will hide the terminal used to start the app.<br>
CD into the root CmdDeployer folder where CmdDeployer.py is located, and execute the following command:
```
python CmdDeployer.py
```

## Running CmdDeployer compiled
To run the app, place the images, dependencies and configuration folder into the compilation output folder.<br>
The app CmdDeployer.exe can be run from this folder.<br>
The CmdDeployer folder within dist (or a different compilation output folder) can be moved to a different desired location.<br>
Startup credentials used to open the app are also used for remote excecution with Psexec.<br>

## Configuring installation and deletion commands
For configuring the app the Excel file located at configuration\Configuration.xlsx can be used.<br>
This file is used form storing Batch/CMD and Powershell commands used for installations and deletions.<br>
Always use 'call [app]' for starting a process from a command.<br>
Also software groups and layout for placing these packages can be configured.<br>
Settings.ini is also for configuring certain app features and layouts.<br>

*This software is not created and verified to be perfect, bugfree and threadsafe. A good advice would be to verify the source code when running this program.*