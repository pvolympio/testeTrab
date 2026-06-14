from Rendering.Elements.Square import draw_square
import time

cloud_offset_x = 0.0
last_time = None
CLOUD_SPEED = 5.0

def draw_cloud(position, scene_width):
    global cloud_offset_x, last_time

    now = time.time()
    if last_time is None:
        last_time = now

    delta_time = now - last_time
    last_time = now

    cloud_offset_x += CLOUD_SPEED * delta_time
    if cloud_offset_x >= scene_width:
        cloud_offset_x -= scene_width

    raw_x = position[0] + cloud_offset_x
    wrapped_x = (raw_x % scene_width) - scene_width / 2

    animated_position = (wrapped_x, position[1], position[2])
    draw_square(animated_position, (1, 1, 1), 10)