import PyInstaller.__main__
import platform

IS_WINDOWS = platform.system() == "Windows"
DATA_SEP = ";" if IS_WINDOWS else ":"
ICON = "ui/assets/img/logo_ico.ico" if IS_WINDOWS else "ui/assets/img/logo.icns"

PyInstaller.__main__.run([
    "--noconfirm",
    "--onefile",
    "--console",
    "--clean",
    "--name=ISCGraph",
    f"--icon={ICON}",
    f"--add-data=ui{DATA_SEP}ui",
    "main.py",
])



# pyinstaller --noconfirm --onefile --console ^
# --icon "E:\projects\TemperatureGraphMacProgramm\ui\assets\img\logo_ico.ico" ^
# --name "ISCGraph" --clean ^
# --add-data "E:\projects\TemperatureGraphMacProgramm\ui;ui/" ^
# "E:\projects\TemperatureGraphMacProgramm\main.py"
