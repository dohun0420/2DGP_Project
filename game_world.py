world = [[], [], []]

def add_object(o, depth = 0):
    while depth >= len(world):
        world.append([])
    world[depth].append(o)

def add_objects(ol, depth = 0):
    while depth >= len(world):
        world.append([])
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError('Cannot delete non existing object')

def update():
    for layer in world:
        for o in world:
            o.update()

def render():
    for layer in world:
        for o in world:
            o.draw()