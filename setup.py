import sys
from cx_Freeze import setup, Executable
import GUI

includeFiles = ["beep.wav"]
bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\LockCalc',
    }
setup(
    name = "LockCalc",
    version = GUI.version,
    description = "Easily organize fleet send schedule.",
    executables = [Executable("GUI.py", base = "Win32GUI")],
    options={'bdist_msi': bdist_msi_options,'build_exe':{'include_files':includeFiles}})
