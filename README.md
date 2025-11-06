# 🐑 Ovejita - Desktop Pet

Una recreación del clásico programa de los años 90 "eSheep", donde una ovejita camina por tu escritorio.

## Descripción

Este programa crea una ovejita animada que:
- Camina libremente por tu pantalla
- Cae con gravedad cuando está en el aire
- Salta aleatoriamente y cuando choca con otras ovejas
- Cambia de dirección en los bordes de la pantalla
- Puede ser arrastrada con el mouse
- Cada oveja tiene un color aleatorio (blanco a gris suave)
- Múltiples ovejas pueden coexistir en la pantalla
- Siempre permanece visible sobre todas las demás ventanas
- En Windows, camina sobre las ventanas abiertas

## 🚀 Inicio Rápido

### Para usuarios de Windows (sin Python)

Si no tienes Python instalado, puedes usar el ejecutable:

1. **Descarga** `Ovejita.exe` (ver sección Releases)
2. **Doble clic** en el archivo
3. **¡Listo!** La ovejita aparecerá en tu escritorio

**Nota**: Windows puede mostrar una advertencia la primera vez. Click en "Más información" → "Ejecutar de todas formas"

### Para desarrolladores (con Python)

Continúa leyendo las secciones de instalación y uso más abajo.

---

## Requisitos

### Para ejecutar el código fuente:
- Python 3.12 (recomendado, incluye Tkinter)
- Tkinter (incluido con Python 3.12)
- Pillow (PIL)

### Para crear el ejecutable .exe:
- Todo lo anterior, más:
- PyInstaller (`pip install pyinstaller`)

## Instalación

1. Verifica que tienes Python 3.12 instalado:
```bash
python3.12 --version
```

2. Instala las dependencias:
```bash
python3.12 -m pip install --break-system-packages Pillow
```

O si tienes permisos de sistema:
```bash
pip install -r requirements.txt
```

**Nota para sistemas Linux**: Si no tienes Python 3.12, puedes instalarlo con:
```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-tk
```

## Uso

### Ejecutar el programa:

```bash
python3.12 ovejita.py
```

O hazlo ejecutable y ejecútalo directamente:
```bash
chmod +x ovejita.py
./ovejita.py
```

### Controles:

- **Arrastrar**: Haz clic y arrastra la ovejita para moverla
- **Doble clic**: Crea una nueva ovejita
- **Ctrl+C** en la terminal: Cierra el programa

## 📦 Crear Ejecutable de Windows (.exe)

¿Quieres compartir el programa con alguien que no tiene Python? Puedes crear un archivo `.exe`:

### Método Rápido (Recomendado)

```bash
# 1. Instalar dependencias
pip install -r requirements-build.txt

# 2. Crear el ícono (opcional)
python create_icon.py

# 3. Construir el ejecutable
python build_exe.py
```

El archivo `Ovejita.exe` estará en la carpeta `dist/`.

### Método Manual

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ícono (opcional)
python create_icon.py

# Construir ejecutable
pyinstaller --onefile --windowed --icon=sheep_icon.ico --name=Ovejita ovejita.py
```

### Distribución

El archivo `.exe` resultante:
- **Tamaño**: ~15-25 MB (incluye Python y todas las dependencias)
- **Funciona en cualquier Windows** sin necesidad de instalar Python
- **Portable**: Un solo archivo, fácil de compartir

**Para instrucciones detalladas**, consulta [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## Características

- **Animación fluida**: La ovejita tiene diferentes animaciones para caminar y caer
- **Diseño realista**: Patas visibles con pezuñas, ojos negros grandes, proporción de oveja real
- **Física realista**: Implementa gravedad y detección de colisiones
- **Colisiones entre ovejas**: Las ovejas saltan sobre otras ovejas manteniendo su inercia lateral
- **Múltiples ovejas**: Crea tantas ovejas como quieras con doble clic
- **Colores variados**: Cada oveja tiene un color aleatorio entre blanco y gris suave
- **Comportamiento aleatorio**: Las ovejas toman decisiones aleatorias (cambiar dirección, saltar)
- **Detección de ventanas** (Windows): Las ovejas caminan sobre las ventanas abiertas
- **Ventana transparente**: Solo se ve la ovejita, sin bordes de ventana
- **Siempre visible**: Las ovejas permanecen sobre todas las demás ventanas
- **Tamaño optimizado**: 96x96 píxeles (50% más grande que la versión original)

## Cómo funciona

El programa usa:
- **Tkinter**: Para crear la ventana flotante y transparente
- **PIL/Pillow**: Para generar los sprites de la ovejita
- **Canvas**: Para dibujar y animar la ovejita

Los sprites se generan dinámicamente al iniciar el programa, creando:
- 2 frames de animación para caminar a la derecha
- 2 frames de animación para caminar a la izquierda
- 1 sprite para cuando está cayendo

## Personalización

Puedes modificar el comportamiento editando las siguientes variables en `ovejita.py`:

- `velocity_x`: Velocidad de caminata (línea 30)
- `gravity`: Fuerza de gravedad (línea 32)
- Frecuencia de comportamientos aleatorios (línea 222)
- Altura del salto (línea 230)

## Notas

- La ovejita respeta la barra de tareas (no cae por debajo de la pantalla visible)
- El programa consume muy pocos recursos del sistema
- Compatible con Linux, Windows y macOS (con algunas diferencias visuales)

## Problemas conocidos

- En algunos gestores de ventanas de Linux, la transparencia puede no funcionar perfectamente
- En sistemas con múltiples monitores, la ovejita solo se mueve en el monitor principal

## Créditos

Inspirado en el clásico "eSheep" de los años 90.

---

¡Disfruta de tu nueva mascota de escritorio! 🐑
