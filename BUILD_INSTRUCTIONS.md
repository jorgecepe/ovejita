# 🔨 Instrucciones para Crear el Ejecutable .exe

Esta guía te explica cómo convertir el programa Python en un archivo `.exe` que puede ejecutarse en cualquier PC con Windows **sin necesidad de tener Python instalado**.

## 📋 Requisitos Previos

1. **Windows** (para crear el .exe)
2. **Python 3.12** instalado
3. **Conexión a Internet** (para descargar dependencias)

## 🚀 Método Rápido (Recomendado)

### Paso 1: Instalar dependencias

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements-build.txt
```

Esto instalará:
- `Pillow` (para las imágenes)
- `PyInstaller` (para crear el .exe)

### Paso 2: Crear el ícono (opcional)

```bash
python create_icon.py
```

Esto generará `sheep_icon.ico` que se usará como ícono del ejecutable.

### Paso 3: Construir el ejecutable

```bash
python build_exe.py
```

El script automáticamente:
- Verifica las dependencias
- Construye el ejecutable
- Lo coloca en la carpeta `dist/`

**¡Listo!** El archivo `Ovejita.exe` estará en la carpeta `dist/`.

## 🔧 Método Manual (Avanzado)

Si prefieres más control sobre el proceso:

### 1. Instalar PyInstaller

```bash
pip install pyinstaller pillow
```

### 2. Crear el ícono (opcional)

```bash
python create_icon.py
```

### 3. Construir con PyInstaller

**Versión simple (sin ícono):**
```bash
pyinstaller --onefile --windowed --name=Ovejita ovejita.py
```

**Versión con ícono:**
```bash
pyinstaller --onefile --windowed --icon=sheep_icon.ico --name=Ovejita ovejita.py
```

**Parámetros explicados:**
- `--onefile`: Crea un solo archivo .exe (en lugar de múltiples archivos)
- `--windowed`: No muestra ventana de consola (para aplicaciones GUI)
- `--icon`: Especifica el ícono del ejecutable
- `--name`: Nombre del archivo ejecutable

### 4. Encontrar el ejecutable

El archivo `Ovejita.exe` estará en:
```
dist/Ovejita.exe
```

## 📦 Distribución

### Tamaño del archivo
El ejecutable tendrá aproximadamente **15-25 MB** porque incluye:
- Python runtime
- Tkinter
- Pillow
- Todas las dependencias necesarias

### Compartir el ejecutable

Simplemente copia `dist/Ovejita.exe` y compártelo. El receptor puede:
1. Descargar el archivo
2. Doble clic para ejecutar
3. **No necesita instalar Python ni nada más**

## ⚠️ Advertencias Importantes

### Antivirus / Windows Defender

**Problema común**: Los antivirus pueden marcar el .exe como sospechoso.

**¿Por qué?**
- Los ejecutables creados con PyInstaller son "nuevos" y no tienen firma digital
- Windows SmartScreen no reconoce el archivo
- Esto es un **falso positivo** normal

**Soluciones:**
1. **Para ti**: Añade excepción en tu antivirus
2. **Para distribuir**:
   - Firma digitalmente el ejecutable (requiere certificado de código)
   - Comparte el código fuente también
   - Explica que es código abierto y seguro

### Windows SmartScreen

Al ejecutar por primera vez, Windows puede mostrar:
> "Windows protegió su PC"

**Para ejecutar:**
1. Click en "Más información"
2. Click en "Ejecutar de todas formas"

## 🧹 Limpiar Archivos Temporales

Después de crear el .exe, puedes eliminar:

```bash
rmdir /s build
del Ovejita.spec
```

O deja que el script `build_exe.py` lo haga automáticamente.

## 📂 Estructura de Archivos

Después del build:

```
ovejita/
├── ovejita.py              # Código fuente
├── build_exe.py            # Script de construcción
├── create_icon.py          # Generador de ícono
├── sheep_icon.ico          # Ícono (generado)
├── requirements-build.txt  # Dependencias para build
│
├── build/                  # Archivos temporales (puede eliminarse)
├── dist/
│   └── Ovejita.exe        # ⭐ TU EJECUTABLE FINAL
└── Ovejita.spec           # Configuración PyInstaller (puede eliminarse)
```

## 🐛 Solución de Problemas

### Error: "PyInstaller no está instalado"
```bash
pip install pyinstaller
```

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### El .exe no funciona en otro PC
- Asegúrate de usar `--onefile`
- Verifica que sea Windows de 64 bits
- Comparte también `README.md` para instrucciones

### El .exe es muy grande
- Es normal (15-25 MB)
- Incluye todo Python y dependencias
- No se puede reducir significativamente sin perder funcionalidad

### Error al construir
1. Elimina las carpetas `build/` y `dist/`
2. Elimina `Ovejita.spec`
3. Intenta de nuevo

## 💡 Consejos

1. **Prueba el .exe antes de distribuir**: Ejecútalo en tu PC primero
2. **Incluye un README**: Explica cómo usar el programa
3. **Versiona tus builds**: Nombra como `Ovejita-v1.0.exe`
4. **Comparte el código fuente**: Para que otros confíen en tu ejecutable

## 🎯 Alternativas a PyInstaller

Si PyInstaller te da problemas, prueba:

1. **cx_Freeze**: Similar a PyInstaller
   ```bash
   pip install cx_Freeze
   ```

2. **Nuitka**: Compila a código nativo (más rápido, más complejo)
   ```bash
   pip install nuitka
   ```

3. **Auto-py-to-exe**: GUI para PyInstaller (más fácil para principiantes)
   ```bash
   pip install auto-py-to-exe
   auto-py-to-exe
   ```

## 📞 Soporte

Si tienes problemas, verifica:
1. Versión de Python: `python --version` (debe ser 3.12+)
2. Versión de PyInstaller: `pyinstaller --version`
3. Los mensajes de error completos

---

**¡Eso es todo!** Con estos pasos deberías tener tu `Ovejita.exe` listo para compartir. 🐑✨
