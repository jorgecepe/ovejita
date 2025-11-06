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

        # Sheep properties - 50% larger (64 -> 96)
        self.sheep_width = 96
        self.sheep_height = 96
        self.x = random.randint(100, self.screen_width - 200)
        self.y = 100
        self.velocity_x = 2
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.current_window = None  # Track which window sheep is on

        # Random color between white and soft gray
        gray_value = random.randint(200, 255)  # Range from gray to white
        self.body_color = (gray_value, gray_value, gray_value)

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

        # Scale factor for the new size (96 vs 64)
        s = 1.5

        # Create walking right animation (2 frames)
        for frame in range(2):
            img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Body (larger, more oval)
            body_y = int(35 * s) + (3 if frame == 1 else 0)
            draw.ellipse([int(15 * s), body_y, int(55 * s), body_y + int(25 * s)],
                        fill=self.body_color, outline='gray', width=2)

            # Head (more defined)
            head_x = int(50 * s)
            draw.ellipse([head_x, int(25 * s), head_x + int(20 * s), int(45 * s)],
                        fill=self.body_color, outline='gray', width=2)

            # Snout/Face (lighter color)
            face_color = tuple(min(c + 30, 255) for c in self.body_color)
            draw.ellipse([head_x + int(8 * s), int(32 * s), head_x + int(18 * s), int(42 * s)],
                        fill=face_color, outline='gray')

            # Ears (more visible)
            draw.ellipse([head_x + int(2 * s), int(22 * s), head_x + int(8 * s), int(30 * s)],
                        fill='pink', outline='gray', width=1)
            draw.ellipse([head_x + int(12 * s), int(22 * s), head_x + int(18 * s), int(30 * s)],
                        fill='pink', outline='gray', width=1)

            # Eye (bigger and more visible)
            draw.ellipse([head_x + int(13 * s), int(33 * s), head_x + int(17 * s), int(37 * s)],
                        fill='black')

            # Legs with hooves (more realistic, wider)
            leg_offset = 5 if frame == 0 else -5
            leg_color = 'black'

            # Front left leg
            leg_x = int(25 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) + leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) + leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) + leg_offset + int(16 * s)],
                        fill=leg_color)

            # Front right leg
            leg_x = int(35 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) - leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) - leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) - leg_offset + int(16 * s)],
                        fill=leg_color)

            # Back left leg
            leg_x = int(45 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) + leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) + leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) + leg_offset + int(16 * s)],
                        fill=leg_color)

            # Back right leg
            leg_x = int(55 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) - leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) - leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) - leg_offset + int(16 * s)],
                        fill=leg_color)

            # Fluffy tail
            tail_color = self.body_color
            draw.ellipse([int(8 * s), body_y + int(8 * s), int(18 * s), body_y + int(18 * s)],
                        fill=tail_color, outline='gray')

            sprites['walk_right'].append(ImageTk.PhotoImage(img))

        # Create walking left animation (mirror of right)
        for frame in range(2):
            img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Body
            body_y = int(35 * s) + (3 if frame == 1 else 0)
            draw.ellipse([int(15 * s), body_y, int(55 * s), body_y + int(25 * s)],
                        fill=self.body_color, outline='gray', width=2)

            # Head (on left side)
            head_x = int(5 * s)
            draw.ellipse([head_x, int(25 * s), head_x + int(20 * s), int(45 * s)],
                        fill=self.body_color, outline='gray', width=2)

            # Snout/Face
            face_color = tuple(min(c + 30, 255) for c in self.body_color)
            draw.ellipse([head_x + int(2 * s), int(32 * s), head_x + int(12 * s), int(42 * s)],
                        fill=face_color, outline='gray')

            # Ears
            draw.ellipse([head_x + int(2 * s), int(22 * s), head_x + int(8 * s), int(30 * s)],
                        fill='pink', outline='gray', width=1)
            draw.ellipse([head_x + int(12 * s), int(22 * s), head_x + int(18 * s), int(30 * s)],
                        fill='pink', outline='gray', width=1)

            # Eye
            draw.ellipse([head_x + int(3 * s), int(33 * s), head_x + int(7 * s), int(37 * s)],
                        fill='black')

            # Legs with hooves
            leg_offset = 5 if frame == 0 else -5
            leg_color = 'black'

            # Legs (mirrored positions)
            leg_x = int(20 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) - leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) - leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) - leg_offset + int(16 * s)],
                        fill=leg_color)

            leg_x = int(30 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) + leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) + leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) + leg_offset + int(16 * s)],
                        fill=leg_color)

            leg_x = int(40 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) - leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) - leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) - leg_offset + int(16 * s)],
                        fill=leg_color)

            leg_x = int(50 * s)
            draw.rectangle([leg_x - 2, body_y + int(25 * s), leg_x + 2, body_y + int(25 * s) + leg_offset + int(12 * s)],
                          fill=leg_color)
            draw.ellipse([leg_x - 3, body_y + int(25 * s) + leg_offset + int(10 * s),
                         leg_x + 3, body_y + int(25 * s) + leg_offset + int(16 * s)],
                        fill=leg_color)

            # Tail
            draw.ellipse([int(52 * s), body_y + int(8 * s), int(62 * s), body_y + int(18 * s)],
                        fill=self.body_color, outline='gray')

            sprites['walk_left'].append(ImageTk.PhotoImage(img))

        # Create falling animation
        img = Image.new('RGBA', (self.sheep_width, self.sheep_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Body (rotated look)
        draw.ellipse([int(25 * s), int(30 * s), int(55 * s), int(55 * s)],
                    fill=self.body_color, outline='gray', width=2)

        # Head
        draw.ellipse([int(32 * s), int(18 * s), int(52 * s), int(38 * s)],
                    fill=self.body_color, outline='gray', width=2)

        # Face
        face_color = tuple(min(c + 30, 255) for c in self.body_color)
        draw.ellipse([int(36 * s), int(24 * s), int(48 * s), int(36 * s)],
                    fill=face_color, outline='gray')

        # Ears
        draw.ellipse([int(34 * s), int(16 * s), int(40 * s), int(24 * s)],
                    fill='pink', outline='gray', width=1)
        draw.ellipse([int(44 * s), int(16 * s), int(50 * s), int(24 * s)],
                    fill='pink', outline='gray', width=1)

        # Eyes (surprised, both visible)
        draw.ellipse([int(37 * s), int(26 * s), int(41 * s), int(30 * s)], fill='black')
        draw.ellipse([int(43 * s), int(26 * s), int(47 * s), int(30 * s)], fill='black')

        # Legs (flailing)
        draw.rectangle([int(28 * s), int(45 * s), int(32 * s), int(58 * s)], fill='black')
        draw.ellipse([int(26 * s), int(56 * s), int(34 * s), int(62 * s)], fill='black')

        draw.rectangle([int(38 * s), int(48 * s), int(42 * s), int(62 * s)], fill='black')
        draw.ellipse([int(36 * s), int(60 * s), int(44 * s), int(66 * s)], fill='black')

        draw.rectangle([int(48 * s), int(48 * s), int(52 * s), int(62 * s)], fill='black')
        draw.ellipse([int(46 * s), int(60 * s), int(54 * s), int(66 * s)], fill='black')

        draw.rectangle([int(58 * s), int(45 * s), int(62 * s), int(58 * s)], fill='black')
        draw.ellipse([int(56 * s), int(56 * s), int(64 * s), int(62 * s)], fill='black')

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

    def check_collision_with_sheep(self):
        """Check if this sheep collides with any other sheep"""
        global sheep_list

        my_rect = {
            'left': self.x,
            'right': self.x + self.sheep_width,
            'top': self.y,
            'bottom': self.y + self.sheep_height
        }

        for other_sheep in sheep_list:
            if other_sheep is self:
                continue

            other_rect = {
                'left': other_sheep.x,
                'right': other_sheep.x + other_sheep.sheep_width,
                'top': other_sheep.y,
                'bottom': other_sheep.y + other_sheep.sheep_height
            }

            # Check if rectangles overlap
            if (my_rect['left'] < other_rect['right'] and
                my_rect['right'] > other_rect['left'] and
                my_rect['top'] < other_rect['bottom'] and
                my_rect['bottom'] > other_rect['top']):

                # Collision detected! Return the other sheep
                return other_sheep

        return None

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

                # Check collision with other sheep
                colliding_sheep = self.check_collision_with_sheep()
                if colliding_sheep is not None:
                    # Jump over the other sheep, maintaining lateral inertia
                    self.velocity_y = -15  # Strong jump
                    self.on_ground = False
                    # Keep velocity_x as is (maintain direction/inertia)
                    self.state = "fall"  # Show falling/jumping animation

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
                # Falling - maintain horizontal movement (inertia)
                self.x += self.velocity_x
                self.state = "fall"

                # Still respect screen boundaries while in air
                if self.x <= 0:
                    self.x = 0
                    self.velocity_x = abs(self.velocity_x)
                elif self.x >= self.screen_width - self.sheep_width:
                    self.x = self.screen_width - self.sheep_width
                    self.velocity_x = -abs(self.velocity_x)

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
