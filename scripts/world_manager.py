from ursina import Entity, Sky
from interaction.manager import interaction

def create_world():
    Sky()

    ground = Entity(
        model="plane",
        collider="box",
        scale=256,
        # color=color.blue,
        texture="../assets/textures/Grass.png",
        texture_scale=(64, 64))

    random_cube = Entity(
        model="cube",
        position=(5, 1, 5),
        collider="box",
        texture="../assets/textures/WindowGlass.png"
    )

    interaction.add_target(obj=random_cube)