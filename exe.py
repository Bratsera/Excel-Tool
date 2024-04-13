import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {"build_exe": {
    "include_files": ["Testdata", "Export"],
    "build_exe": "dist/Laboratory Export"
}}

executables = [Executable("main.py", base=base, target_name="Laboratory Export")]

setup(
    name="Laboratory Export Tool",
    version="0.1",
    description="Tool for extracting and exporting data from laboratory results",
    options=options,
    executables=executables,
)
