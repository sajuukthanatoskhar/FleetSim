from ursina import *

if __name__ == '__main__':
    app = Ursina()

    '''
    Casts a ray from *origin*, in *direction*, with length *distance* and returns
    a HitInfo containing information about what it hit. This ray will only hit entities with a collider.

    Use optional *traverse_target* to only be able to hit a specific entity and its children/descendants.
    Use optional *ignore* list to ignore certain entities.
    Setting debug to True will draw the line on screen.

    Example where we only move if a wall is not hit:
    '''


    class Player(Entity):

        def update(self):
            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()  # get the direction we're trying to walk in.

            origin = self.world_position + (self.up*.5) # the ray should start slightly up from the ground so we can walk up slopes or walk over small objects.
            hit_info = raycaster.raycast(origin , self.direction, ignore=(self,), distance=.5, debug=False)
            print(hit_info.hits)
            if not hit_info.hit:
                self.position += self.direction * 5 * time.dt

    Player(model='cube', origin_y=-.5, color=color.orange)
    wall_left = Entity(model='cube', collider='box', scale_y=3, origin_y=-.5, color=color.azure, x=-4)
    wall_right = duplicate(wall_left, x=4)
    camera.y = 2
    app.run()

    # test
    breakpoint()
    d = Entity(parent=scene, position=(0,0,2), model='cube', color=color.orange, collider='box', scale=2)
    e = Entity(model='cube', color=color.lime)

    camera.position = (0, 15, -15)
    camera.look_at(e)
    # camera.reparent_to(e)
    speed = .01
    rotation_speed = 1
    intersection_marker = Entity(model='cube', scale=.2, color=color.red)

    def update():

        e.position += e.forward * held_keys['w'] * speed
        e.position += e.left * held_keys['a'] * speed
        e.position += e.back * held_keys['s'] * speed
        e.position += e.right * held_keys['d'] * speed

        e.rotation_y -= held_keys['q'] * rotation_speed
        e.rotation_y += held_keys['e'] * rotation_speed

        #ray = raycast(e.world_position, e.forward, 3, debug=True)
        ray = raycast(e.world_position, e.forward, 3, debug=True)
        #ray = boxcast(e.world_position, e.right, 3, debug=True)
        print(ray.distance, ray2.distance)
        intersection_marker.world_position = ray.world_point
        intersection_marker.visible = ray.hit
        if ray.hit:
            d.color = color.azure
        else:
            d.color = color.orange

    t = time.time()
    # ray = raycast(e.world_position, e.forward, 3, debug=True)
    print(time.time() - t)
    # raycast((0,0,-2), (0,0,1), 5, debug=False)

    EditorCamera()
    app.run()