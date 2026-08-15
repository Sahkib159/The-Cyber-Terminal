from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import random
import math

# Give the USB port time to connect
time.sleep(1)

# Connect to the display
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# ==========================================
# THEME 1: SAHKIB'S BOUNCING NAME
# ==========================================
def theme_name_bounce(duration_ms):
    start_time = time.ticks_ms()
    # Starting coordinates and speed
    x, y = 10, 10
    dx, dy = 1, 1
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        # Stacked to fit the 128px screen width
        oled.text("Sahkib Ahad", x, y)
        oled.text("Chowdhury", x, y + 10)
        oled.text("IUB CSE", x, y + 20)
        oled.show()
        
        x += dx
        y += dy
        
        # Collision math (Screen is 128x64. Text box is ~88x28)
        if x <= 0 or x >= 36: dx = -dx
        if y <= 0 or y >= 36: dy = -dy
        time.sleep(0.01)

# ==========================================
# THEME 2: HYPERSPACE STARFIELD
# ==========================================
def theme_starfield(duration_ms):
    start_time = time.ticks_ms()
    stars = [[random.randint(-100, 100), random.randint(-100, 100), random.randint(50, 150)] for _ in range(40)]
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        for i in range(len(stars)):
            star = stars[i]
            old_z = star[2]
            star[2] -= 6
            
            if star[2] <= 1:
                stars[i] = [random.randint(-100, 100), random.randint(-100, 100), random.randint(50, 150)]
                continue
                
            x1 = int((star[0] * 64) / star[2]) + 64
            y1 = int((star[1] * 64) / star[2]) + 32
            x2 = int((star[0] * 64) / old_z) + 64
            y2 = int((star[1] * 64) / old_z) + 32
            
            if 0 <= x1 < 128 and 0 <= y1 < 64:
                oled.line(x1, y1, x2, y2, 1)
        oled.show()

# ==========================================
# THEME 3: THE MATRIX RAIN
# ==========================================
def theme_matrix(duration_ms):
    start_time = time.ticks_ms()
    drops = [random.randint(0, 64) for _ in range(16)]
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        for i in range(16):
            random_char = chr(random.randint(33, 126))
            oled.text(random_char, i * 8, drops[i])
            drops[i] += 8
            if drops[i] > 64 or random.random() > 0.9:
                drops[i] = 0
        oled.show()
        time.sleep(0.05)

# ==========================================
# THEME 4: 3D ROTATING CUBE
# ==========================================
def theme_3d_cube(duration_ms):
    start_time = time.ticks_ms()
    scale = 20
    vertices = [[-scale, -scale, -scale], [scale, -scale, -scale], [scale, scale, -scale], [-scale, scale, -scale],
                [-scale, -scale, scale], [scale, -scale, scale], [scale, scale, scale], [-scale, scale, scale]]
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    angle_x = angle_y = angle_z = 0
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        angle_x += 0.05
        angle_y += 0.03
        angle_z += 0.01
        
        projected = []
        for v in vertices:
            x, y, z = v[0], v[1], v[2]
            
            new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
            new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
            y, z = new_y, new_z
            
            new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
            new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
            x, z = new_x, new_z
            
            new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
            new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
            x, y = new_x, new_y
            
            perspective = scale * 1.5 / (z + 60)
            projected.append((int(x * perspective + 64), int(y * perspective + 32)))
            
        for edge in edges:
            p1, p2 = projected[edge[0]], projected[edge[1]]
            oled.line(p1[0], p1[1], p2[0], p2[1], 1)
            
        oled.show()
        time.sleep(0.01)

# ==========================================
# THEME 5: FIREWORKS
# ==========================================
def theme_fireworks(duration_ms):
    start_time = time.ticks_ms()
    particles = []
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        
        if random.random() < 0.1:
            origin_x, origin_y = random.randint(20, 108), random.randint(10, 40)
            for _ in range(15):
                angle = random.uniform(0, 6.28)
                speed = random.uniform(1, 4)
                particles.append([origin_x, origin_y, math.cos(angle)*speed, math.sin(angle)*speed, 10])
                
        for p in particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] <= 0:
                particles.remove(p)
            else:
                oled.pixel(int(p[0]), int(p[1]), 1)
                
        oled.show()
        time.sleep(0.05)

# ==========================================
# THEME 6: THE RADAR SWEEP
# ==========================================
def theme_radar(duration_ms):
    start_time = time.ticks_ms()
    angle = 0
    targets = [{'r': random.randint(5, 28), 'theta': random.uniform(0, 6.28), 'life': 0} for _ in range(6)]
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        oled.hline(32, 32, 64, 1)
        oled.vline(64, 0, 64, 1)
        
        sweep_x = int(64 + 31 * math.cos(angle))
        sweep_y = int(32 + 31 * math.sin(angle))
        oled.line(64, 32, sweep_x, sweep_y, 1)
        
        for t in targets:
            if abs(angle - t['theta']) < 0.2 or abs(abs(angle - t['theta']) - 6.28) < 0.2:
                t['life'] = 15
                
            if t['life'] > 0:
                tx = int(64 + t['r'] * math.cos(t['theta']))
                ty = int(32 + t['r'] * math.sin(t['theta']))
                oled.fill_rect(tx-1, ty-1, 3, 3, 1)
                t['life'] -= 1
                
        oled.show()
        angle += 0.1
        if angle > 6.28: angle = 0

# ==========================================
# THEME 7: SCI-FI OSCILLOSCOPE
# ==========================================
def theme_oscilloscope(duration_ms):
    start_time = time.ticks_ms()
    offset = 0
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        for i in range(0, 128, 16):
            for j in range(0, 64, 16):
                oled.pixel(i, j, 1)
                
        old_x, old_y = 0, 32
        for x in range(128):
            y = int(32 + math.sin((x + offset) * 0.1) * 15 + math.sin((x + offset) * 0.05) * 10)
            oled.line(old_x, old_y, x, y, 1)
            old_x, old_y = x, y
            
        oled.show()
        offset += 3

# ==========================================
# THEME 8: SYNTHWAVE 3D FLOOR
# ==========================================
def theme_synthwave(duration_ms):
    start_time = time.ticks_ms()
    offset = 0
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        
        # Draw the horizon and a retro sun
        oled.hline(0, 20, 128, 1)
        oled.fill_rect(54, 8, 20, 12, 1)
        
        # Draw perspective lines coming from the center
        for i in range(-5, 6):
            x = 64 + i * 25
            oled.line(64, 20, x + (i * 20), 64, 1)
            
        # Draw horizontal scrolling lines to create 3D movement illusion
        for j in range(5):
            y = 20 + int(((j * 10 + offset) ** 1.4) / 4)
            if y < 64: oled.hline(0, y, 128, 1)
            
        oled.show()
        offset += 1.5
        if offset > 10: offset = 0

# ==========================================
# THEME 9: SPINNING DNA HELIX
# ==========================================
def theme_dna_helix(duration_ms):
    start_time = time.ticks_ms()
    phase = 0
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        
        # Step through the X axis to draw the helix waves
        for x in range(0, 128, 8):
            y1 = int(32 + math.sin(phase + x * 0.1) * 20)
            y2 = int(32 + math.sin(phase + math.pi + x * 0.1) * 20)
            
            # Draw the strands and the connecting bonds
            oled.pixel(x, y1, 1)
            oled.pixel(x, y2, 1)
            oled.line(x, y1, x, y2, 1)
            
        oled.show()
        phase += 0.2

# ==========================================
# THEME 10: EXPANDING HYPNO-RINGS
# ==========================================
def theme_hypno_rings(duration_ms):
    start_time = time.ticks_ms()
    radius_offset = 0
    
    while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
        oled.fill(0)
        
        # Draw expanding concentric rectangles
        for r in range(int(radius_offset) % 15, 80, 15):
            x = 64 - r
            y = 32 - int(r/2)
            w = r * 2
            h = r
            oled.rect(x, y, w, h, 1)
            
        oled.show()
        radius_offset += 1.5

# ==========================================
# THE MASTER PLAYLIST ENGINE
# ==========================================
# Play each theme for 10 seconds (10000 milliseconds)
DISPLAY_TIME = 10000 

while True:
    theme_name_bounce(DISPLAY_TIME)
    theme_synthwave(DISPLAY_TIME)
    theme_starfield(DISPLAY_TIME)
    theme_dna_helix(DISPLAY_TIME)
    theme_3d_cube(DISPLAY_TIME)
    theme_hypno_rings(DISPLAY_TIME)
    theme_matrix(DISPLAY_TIME)
    theme_fireworks(DISPLAY_TIME)
    theme_radar(DISPLAY_TIME)
    theme_oscilloscope(DISPLAY_TIME)