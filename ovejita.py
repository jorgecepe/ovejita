#!/usr/bin/env python3.12
"""
eSheep Clone - Desktop Sheep Pet
A recreation of the classic 90s desktop pet where a sheep walks around your screen
"""

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random
import sys
import io
import ctypes
from ctypes import wintypes

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Windows API functions for window detection
    user32 = ctypes.windll.user32

    # Define structures
    class RECT(ctypes.Structure):
        _fields_ = [
            ('left', ctypes.c_long),
            ('top', ctypes.c_long),
            ('right', ctypes.c_long),
            ('bottom', ctypes.c_long)
        ]

# Global list to keep track of all sheep
sheep_list = []

def get_visible_windows():
    """Get list of visible window rectangles (Windows only)"""
    if sys.platform != 'win32':
        return []

    windows = []

    def enum_windows_callback(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            # Skip our own sheep windows
            class_name = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_name, 256)
            if 'Toplevel' in class_name.value or class_name.value == 'Tk':
                return True

            rect = RECT()
            if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                # Only consider windows with reasonable size
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                if width > 50 and height > 50 and rect.top > 0:
                    windows.append({
                        'left': rect.left,
                        'top': rect.top,
                        'right': rect.right,
                        'bottom': rect.bottom
                    })
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)

    return windows

class Sheep:
    def __init__(self, main_root):
        self.main_root = main_root

        # Create a new Toplevel window for this sheep
        self.root = tk.Toplevel(main_root)
        self.root.title("Ovejita")

        # Make window transparent and always on top
        self.root.attributes('-transparentcolor', 'black')
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # Remove window decorations

        # Get screen dimensions
        self.screen_width = self.main_root.winfo_screenwidth()
        self.screen_height = self.main_root.winfo_screenheight()

        # Sheep properties
        self.sheep_width = 64
        self.sheep_height = 64
        self.x = random.randint(100, self.screen_width - 200)
        self.y = 100
        self.velocity_x = 2
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.current_window = None  # Track which window sheep is on

        # Animation state
        self.state = "walk_right"  # walk_right, walk_left, fall
        self.animation_frame = 0
        self.frame_count = 0

        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.sheep_width,
            height=self.sheep_height,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()

        # Create sprites
        self.sprites = self.create_sprites()

        # Current image on canvas
        self.image_on_canvas = self.canvas.create_image(
            self.sheep_width // 2,
            self.sheep_height // 2,
            image=self.sprites[self.state][0]
        )

        # Update window position
        self.update_position()

        # Bind click to drag
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Double-Button-1>', self.on_double_click)

        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Start animation loop
        self.animate()

    def create_sprites(self):
        """Create sheep sprites for different animations"""
        sprites = {
            'walk_right': [],
            'walk_left': [],
            'fall': []
        }

        # Create walking right animation (2 frames)
        for frame in range(2):
            img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Body
            body_y = 25 + (2 if frame == 1 else 0)
            draw.ellipse([15, body_y, 50, body_y + 20], fill='white', outline='gray')

            # Head
            head_x = 45
            draw.ellipse([head_x, 20, head_x + 15, 35], fill='white', outline='gray')

            # Ears
            draw.ellipse([head_x + 2, 18, head_x + 6, 24], fill='pink', outline='gray')
            draw.ellipse([head_x + 9, 18, head_x + 13, 24], fill='pink', outline='gray')

            # Eye
            draw.ellipse([head_x + 10, 25, head_x + 12, 27], fill='black')

            # Legs (alternate for walking animation)
            leg_offset = 3 if frame == 0 else -3
            draw.line([20, body_y + 20, 20 + leg_offset, body_y + 30], fill='black', width=2)
            draw.line([30, body_y + 20, 30 - leg_offset, body_y + 30], fill='black', width=2)
            draw.line([35, body_y + 20, 35 + leg_offset, body_y + 30], fill='black', width=2)
            draw.line([45, body_y + 20, 45 - leg_offset, body_y + 30], fill='black', width=2)

            # Tail
            draw.arc([10, body_y + 5, 20, body_y + 15], 0, 180, fill='white', width=3)

            sprites['walk_right'].append(ImageTk.PhotoImage(img))

        # Create walking left animation (mirror of right)
        for frame in range(2):
            img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Body
            body_y = 25 + (2 if frame == 1 else 0)
            draw.ellipse([15, body_y, 50, body_y + 20], fill='white', outline='gray')

            # Head (on left side)
            head_x = 5
            draw.ellipse([head_x, 20, head_x + 15, 35], fill='white', outline='gray')

            # Ears
            draw.ellipse([head_x + 2, 18, head_x + 6, 24], fill='pink', outline='gray')
            draw.ellipse([head_x + 9, 18, head_x + 13, 24], fill='pink', outline='gray')

            # Eye
            draw.ellipse([head_x + 3, 25, head_x + 5, 27], fill='black')

            # Legs
            leg_offset = 3 if frame == 0 else -3
            draw.line([20, body_y + 20, 20 - leg_offset, body_y + 30], fill='black', width=2)
            draw.line([30, body_y + 20, 30 + leg_offset, body_y + 30], fill='black', width=2)
            draw.line([35, body_y + 20, 35 - leg_offset, body_y + 30], fill='black', width=2)
            draw.line([45, body_y + 20, 45 + leg_offset, body_y + 30], fill='black', width=2)

            # Tail
            draw.arc([45, body_y + 5, 55, body_y + 15], 0, 180, fill='white', width=3)

            sprites['walk_left'].append(ImageTk.PhotoImage(img))

        # Create falling animation
        img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Body (rotated look)
        draw.ellipse([20, 25, 45, 45], fill='white', outline='gray')

        # Head
        draw.ellipse([25, 15, 40, 30], fill='white', outline='gray')

        # Ears
        draw.ellipse([27, 13, 31, 19], fill='pink', outline='gray')
        draw.ellipse([34, 13, 38, 19], fill='pink', outline='gray')

        # Eyes (surprised)
        draw.ellipse([28, 20, 31, 23], fill='black')
        draw.ellipse([34, 20, 37, 23], fill='black')

        # Legs (flailing)
        draw.line([22, 35, 15, 40], fill='black', width=2)
        draw.line([28, 40, 22, 50], fill='black', width=2)
        draw.line([37, 40, 43, 50], fill='black', width=2)
        draw.line([43, 35, 50, 40], fill='black', width=2)

        sprites['fall'].append(ImageTk.PhotoImage(img))

        return sprites

    def update_position(self):
        """Update window position on screen"""
        self.root.geometry(f'{self.sheep_width}x{self.sheep_height}+{int(self.x)}+{int(self.y)}')

    def on_click(self, event):
        """Handle mouse click to start dragging"""
        self.dragging = True
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y

    def on_drag(self, event):
        """Handle dragging the sheep"""
        if self.dragging:
            self.x = self.root.winfo_pointerx() - self.drag_offset_x
            self.y = self.root.winfo_pointery() - self.drag_offset_y
            self.velocity_y = 0
            self.update_position()

    def on_release(self, event):
        """Handle mouse release to stop dragging"""
        self.dragging = False

    def on_double_click(self, event):
        """Double click to spawn a new sheep"""
        global sheep_list
        new_sheep = Sheep(self.main_root)
        sheep_list.append(new_sheep)
        print(f"🐑 Nueva ovejita! Total: {len(sheep_list)} ovejitas")

    def find_surface_below(self):
        """Find the surface (window top or ground) below the sheep"""
        sheep_bottom = self.y + self.sheep_height
        sheep_center_x = self.x + self.sheep_width // 2

        ground_level = self.screen_height - self.sheep_height - 40  # Default ground
        self.current_window = None  # Track which window we're on

        if sys.platform == 'win32':
            windows = get_visible_windows()

            # Find windows that could be below the sheep
            for win in windows:
                # Check if sheep's center is horizontally over the window
                if win['left'] <= sheep_center_x <= win['right']:
                    # Check if window top is below sheep bottom
                    if win['top'] >= sheep_bottom - 10:  # Small tolerance
                        # Check if this is closer than current ground
                        if win['top'] < ground_level + self.sheep_height:
                            ground_level = win['top'] - self.sheep_height
                            self.current_window = win

        return ground_level

    def check_window_edge(self):
        """Check if sheep is at the edge of a window"""
        if not hasattr(self, 'current_window') or self.current_window is None:
            return False

        sheep_center_x = self.x + self.sheep_width // 2

        # Check if we're about to walk off the edge
        if self.velocity_x > 0:  # Moving right
            return sheep_center_x + 10 >= self.current_window['right']
        else:  # Moving left
            return sheep_center_x - 10 <= self.current_window['left']

    def animate(self):
        """Main animation loop"""
        if not self.dragging:
            self.frame_count += 1

            # Apply gravity
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            # Find the surface below (could be window or ground)
            surface_level = self.find_surface_below()

            # Check collision with surface
            if self.y >= surface_level:
                self.y = surface_level
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False

            # Move horizontally when on ground
            if self.on_ground:
                self.x += self.velocity_x

                # Check if at window edge and turn around
                if self.check_window_edge():
                    self.velocity_x = -self.velocity_x
                    self.state = "walk_right" if self.velocity_x > 0 else "walk_left"

                # Change direction at screen edges
                if self.x <= 0:
                    self.x = 0
                    self.velocity_x = abs(self.velocity_x)
                    self.state = "walk_right"
                elif self.x >= self.screen_width - self.sheep_width:
                    self.x = self.screen_width - self.sheep_width
                    self.velocity_x = -abs(self.velocity_x)
                    self.state = "walk_left"

                # Random behavior changes
                if self.frame_count % 120 == 0:  # Every ~2 seconds
                    action = random.choice(['continue', 'turn', 'jump'])

                    if action == 'turn':
                        self.velocity_x = -self.velocity_x
                        self.state = "walk_right" if self.velocity_x > 0 else "walk_left"
                    elif action == 'jump':
                        self.velocity_y = -12
                        self.on_ground = False
            else:
                # Falling
                self.state = "fall"

            # Update sprite
            if self.state == "fall":
                current_sprite = self.sprites[self.state][0]
            else:
                # Animate walking (change frame every 10 updates)
                frame_index = (self.frame_count // 10) % 2
                current_sprite = self.sprites[self.state][frame_index]

            self.canvas.itemconfig(self.image_on_canvas, image=current_sprite)
            self.update_position()

        # Schedule next frame
        self.root.after(33, self.animate)  # ~30 FPS

def main():
    global sheep_list

    print("🐑 Ovejita Desktop Pet")
    print("=" * 40)
    print("La ovejita caminará por tu pantalla!")
    print("")
    print("Controles:")
    print("  • Arrastra la oveja para moverla")
    print("  • Doble clic para crear más ovejitas")
    print("  • Ctrl+C para cerrar")
    print("=" * 40)

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create first sheep
    first_sheep = Sheep(root)
    sheep_list.append(first_sheep)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n¡Adiós ovejitas! 🐑")
        sys.exit(0)

if __name__ == "__main__":
    main()
