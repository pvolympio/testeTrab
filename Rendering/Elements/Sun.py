from Rendering.Elements.Sphere import draw_sphere
import time
import math

pulse_speed = 2.0      # velocidade da pulsação
min_radius = 5       # tamanho mínimo
max_radius = 8      # tamanho máximo

def draw_sun(pos):
    t = time.time()

    pulse = (math.sin(t * pulse_speed) + 1) / 2
    
    radius = min_radius + pulse * (max_radius - min_radius)

    draw_sphere(pos, radius)