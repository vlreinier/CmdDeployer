# CmdDeployer
Python Tkinter application for deploying Batch/CMD and Powershell commands to a local machine or multiple remote machines. This app uses Tkinter as a GUI and Psexec.exe and Python module subprocess to execute commands remotely, and redirect cmd output. No external libraries are required for running the app without compiling it to an standalone executable (at least when using Python 3.8).

This tool is not completely verified to be perfect, bugfree and threadsafe. A good advice would be to verify the source code when running this program. Suggestions for improvements or extensions are more than welcome :)

## Compiling CmdDeployer to .exe
The app can be compiled using a variety of modules. It is adviced to avoid compiling to one file since this increases startup time significantly, and it makes configuring and maintaining the app harder..

### pyinstaller
Install Pyinstaller and PyQt5. CD into the root CmdDeployer folder where CmdDeployer.py is located.<br>
From here, run the following command to create the exe installer:
```
pyinstaller --uac-admin --clean CmdDeployer.py --icon dependencies\logo.ico
```

### cx_freeze
Install cx_Freeze and PyQt5. CD into the root CmdDeployer folder where CmdDeployer.py is located.<br>
From here, run the following command to create the exe installer:
```
python Setup.py build
```

## Running CmdDeployer uncompiled
CD into the root CmdDeployer folder where CmdDeployer.py is located, and execute the following command:
```
python CmdDeployer.py
```

## Running CmdDeployer compiled
To run the app, place dependencies folder into the compilation output folder. The app CmdDeployer.exe can be run from this folder. The CmdDeployer folder within dist (or a different compilation output folder) can be moved to a different location.

## Configuring installation and deletion commands
For configuring the app the Excel file located at dependencies\Configuration.xlsx can be used. This file is used for storing Batch/CMD and Powershell commands used for installations and deletions. Always use 'call [app]' for starting a process from a command.
