from Rendering.Elements.Pyramid import draw_pyramid
from Rendering.Elements.Cube import draw_cube   

def draw_tree(position):
    #Desenha um cubo (caule) e uma piramide em cima para formar uma arvore
    draw_cube(position, (0.55, 0.27, 0.07))

    position = (
        position[0],
        position[1] + 2,
        position[2]
    )

    draw_pyramid(position, (0, 0.9, 0))