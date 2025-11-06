#!/usr/bin/env python3.12
"""
Generate a simple sheep icon for the Windows executable
Creates a .ico file with multiple sizes
"""

from PIL import Image, ImageDraw

def create_sheep_icon():
    """Create a simple sheep icon at various sizes"""

    # Icon sizes for Windows
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    for size in sizes:
        # Create new image
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Scale factor based on size
        w, h = size
        scale = w / 64.0  # Base design is for 64x64

        # Body color - white/light gray
        body_color = (240, 240, 240)

        # Body (oval)
        body_margin = int(8 * scale)
        body_height = int(20 * scale)
        draw.ellipse([body_margin, int(h/2 - body_height/2),
                     w - body_margin, int(h/2 + body_height/2)],
                    fill=body_color, outline='gray', width=max(1, int(2 * scale)))

        # Head (circle on right)
        head_size = int(18 * scale)
        head_x = w - body_margin - int(5 * scale)
        head_y = int(h/2)
        draw.ellipse([head_x - head_size, head_y - head_size,
                     head_x + head_size, head_y + head_size],
                    fill=body_color, outline='gray', width=max(1, int(2 * scale)))

        # Face (lighter)
        face_size = int(8 * scale)
        draw.ellipse([head_x - face_size, head_y - face_size//2,
                     head_x + head_size, head_y + face_size],
                    fill=(255, 255, 255), outline='gray', width=max(1, int(scale)))

        # Eye (black dot)
        eye_size = max(2, int(3 * scale))
        draw.ellipse([head_x + int(5 * scale), head_y - int(2 * scale),
                     head_x + int(5 * scale) + eye_size, head_y - int(2 * scale) + eye_size],
                    fill='black')

        # Ears (pink)
        ear_size = int(5 * scale)
        draw.ellipse([head_x - int(8 * scale), head_y - head_size - int(2 * scale),
                     head_x - int(8 * scale) + ear_size, head_y - head_size - int(2 * scale) + ear_size],
                    fill='pink', outline='gray', width=1)
        draw.ellipse([head_x + int(3 * scale), head_y - head_size - int(2 * scale),
                     head_x + int(3 * scale) + ear_size, head_y - head_size - int(2 * scale) + ear_size],
                    fill='pink', outline='gray', width=1)

        # Legs (4 small rectangles at bottom)
        if w >= 32:  # Only draw legs for larger sizes
            leg_width = max(2, int(3 * scale))
            leg_height = int(10 * scale)
            leg_y = int(h/2 + body_height/2)

            # Draw 4 legs
            for i, x_pos in enumerate([15, 25, 35, 45]):
                leg_x = int(x_pos * scale)
                draw.rectangle([leg_x, leg_y, leg_x + leg_width, leg_y + leg_height],
                              fill='black')
                # Hoof
                draw.ellipse([leg_x - 1, leg_y + leg_height - 2,
                             leg_x + leg_width + 1, leg_y + leg_height + 2],
                            fill='black')

        images.append(img)

    # Save as .ico file
    images[0].save('sheep_icon.ico', format='ICO', sizes=[(img.width, img.height) for img in images])
    print("✓ Ícono creado: sheep_icon.ico")
    print(f"  Tamaños incluidos: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")

if __name__ == "__main__":
    print("🐑 Generando ícono de oveja...")
    create_sheep_icon()
    print("✅ ¡Ícono creado exitosamente!")
