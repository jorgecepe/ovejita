#!/usr/bin/env python3.12
"""
Build script to create Windows executable for Ovejita Desktop Pet
Uses PyInstaller to bundle Python and all dependencies into a single .exe file
"""

import os
import sys
import subprocess
import shutil

def main():
    print("🐑 Ovejita - Build Script para Windows .exe")
    print("=" * 50)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("\nInstalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado")

    # Check if Pillow is installed
    try:
        import PIL
        print("✓ Pillow encontrado")
    except ImportError:
        print("❌ Pillow no está instalado")
        print("\nInstalando Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✓ Pillow instalado")

    print("\n" + "=" * 50)
    print("Construyendo ejecutable...")
    print("=" * 50 + "\n")

    # PyInstaller command
    # --onefile: Create a single executable file
    # --windowed: Don't show console window (GUI app)
    # --name: Name of the executable
    # --clean: Clean PyInstaller cache before building
    # --noconfirm: Replace output directory without asking

    cmd = [
        "pyinstaller",
        "--onefile",           # Single .exe file
        "--windowed",          # No console window
        "--name=Ovejita",      # Name of the exe
        "--clean",             # Clean cache
        "--noconfirm",         # Don't ask to replace
        "ovejita.py"
    ]

    # Add icon if it exists
    if os.path.exists("sheep_icon.ico"):
        cmd.insert(2, "--icon=sheep_icon.ico")
        print("✓ Usando ícono personalizado")

    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 50)
        print("✅ ¡Construcción exitosa!")
        print("=" * 50)
        print("\nEl ejecutable se encuentra en:")
        print("  📁 dist/Ovejita.exe")
        print("\nPuedes copiar este archivo a cualquier PC con Windows")
        print("y ejecutarlo sin necesidad de instalar Python.")
        print("\n⚠️  Nota: Algunos antivirus pueden marcar falsos positivos.")
        print("    Esto es normal con ejecutables creados por PyInstaller.")

        # Get file size
        exe_path = os.path.join("dist", "Ovejita.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n📊 Tamaño del archivo: {size_mb:.1f} MB")

    except subprocess.CalledProcessError as e:
        print("\n❌ Error durante la construcción")
        print(f"Código de error: {e.returncode}")
        sys.exit(1)

    # Clean up build artifacts (optional)
    print("\n¿Deseas limpiar archivos temporales? (build/, *.spec)")
    cleanup = input("Presiona 'y' para sí, cualquier otra tecla para no: ").lower()

    if cleanup == 'y':
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("✓ Carpeta 'build' eliminada")

        if os.path.exists("Ovejita.spec"):
            os.remove("Ovejita.spec")
            print("✓ Archivo 'Ovejita.spec' eliminado")

        print("\n✓ Limpieza completada")

    print("\n🐑 ¡Proceso completado!")

if __name__ == "__main__":
    main()
