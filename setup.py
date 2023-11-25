from cx_Freeze import setup, Executable
import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("main.py", base=base, icon="static/icons/galaxy.ico")]

includefiles = [
    "README.md",
    "README.txt",
    "static"
]

packages = [
    "pygame",
    "random",
    "math",
    "sys"
]

options = {
    "build_exe": {
        "packages": packages,
        "include_files": includefiles
    }
}

setup(
    name="space_invaders",
    version="1.0",
    options=options,
    executables=executables,
    icon="static/icons/galaxy.ico",
    author="Ilay",
    description="Space Invaders is a classic arcade game where players control a spaceship to shoot down the galactic aliens.",
    long_description=open("README.txt", encoding="utf-8").read()
)