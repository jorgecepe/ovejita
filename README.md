# 🐑 Ovejita - Desktop Pet

Una recreación del clásico programa de los años 90 "eSheep", donde una ovejita camina por tu escritorio.

## Descripción

Este programa crea una ovejita animada que:
- Camina libremente por tu pantalla
- Cae con gravedad cuando está en el aire
- Salta aleatoriamente
- Cambia de dirección en los bordes de la pantalla
- Puede ser arrastrada con el mouse
- Siempre permanece visible sobre otras ventanas

## Requisitos

- Python 3.12 (recomendado, incluye Tkinter)
- Tkinter (incluido con Python 3.12)
- Pillow (PIL)

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
- **Doble clic**: Cierra el programa
- **Ctrl+C** en la terminal: También cierra el programa

## Características

- **Animación fluida**: La ovejita tiene diferentes animaciones para caminar y caer
- **Física realista**: Implementa gravedad y detección de colisiones con los bordes
- **Comportamiento aleatorio**: La ovejita toma decisiones aleatorias (cambiar dirección, saltar)
- **Ventana transparente**: Solo se ve la ovejita, sin bordes de ventana
- **Siempre visible**: La ovejita permanece sobre todas las demás ventanas

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
