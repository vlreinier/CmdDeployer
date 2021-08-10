from cx_Freeze import setup, Executable

build_exe_options = {}

setup(
    name = "CmdDeployer",
    version = "1.0",
    description = "Deploy commands locally and remotely",
    options = {"build_exe": build_exe_options},
    executables = [
        Executable(
            script = "CmdDeployer.py",
            base = None, #"Win32GUI",
            icon = "dependencies\\logo.ico"
        )
    ]
)