@echo off
REM Build script for Windows - Creates Ovejita.exe
REM Double-click this file to build the executable

echo ========================================
echo    Ovejita - Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.12 desde python.org
    pause
    exit /b 1
)

echo [1/4] Verificando Python... OK
echo.

REM Install dependencies
echo [2/4] Instalando dependencias...
pip install -q pyinstaller pillow
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo       Dependencias instaladas correctamente
echo.

REM Create icon
echo [3/4] Creando icono...
if exist create_icon.py (
    python create_icon.py
    echo       Icono creado
) else (
    echo       create_icon.py no encontrado, omitiendo...
)
echo.

REM Build executable
echo [4/4] Construyendo ejecutable...
echo       Esto puede tomar varios minutos...
echo.

if exist sheep_icon.ico (
    pyinstaller --onefile --windowed --icon=sheep_icon.ico --name=Ovejita ovejita.py --noconfirm --clean
) else (
    pyinstaller --onefile --windowed --name=Ovejita ovejita.py --noconfirm --clean
)

if errorlevel 1 (
    echo.
    echo ERROR: Fallo la construccion del ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================
echo          BUILD EXITOSO!
echo ========================================
echo.
echo El ejecutable esta en: dist\Ovejita.exe
echo.
echo Puedes copiar este archivo a cualquier PC con Windows
echo y ejecutarlo sin necesidad de tener Python instalado.
echo.
echo Tamano del archivo:
dir dist\Ovejita.exe | find "Ovejita.exe"
echo.
echo ========================================
pause
