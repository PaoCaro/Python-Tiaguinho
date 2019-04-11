import sys
from cx_Freeze import setup, Executable

sys.argv.append("build")

setup(
    name = "",
    version = "1",
    description = "",
    executables = [Executable("flappyBird.py", base = "Win32GUI")]
    )
