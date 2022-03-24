from ursina import *

import random                           # Import the random library
from panda3d.core import CollisionRay
random_generator = random.Random()
move_mode = False
pan_cam_flag = False
rot_cam_flag = False
zoom_cam_flag = False
cam_rot_origin = Vec3(0,0,0)
origin = Vec3(0,0,0)
cam_origin = Vec3(0,0,0)
selected_objects = []
sensitivity = 10
scroll_sensitivity = 10
cube_selected = False


def input(key):
    global origin
    global cam_origin,cam_rot_origin
    global pan_cam_flag, rot_cam_flag
    global scroll_sensitivity
    global move_mode
    if key ==  'q':
        print('q')
        move_mode = True


    if key == Keys.right_mouse_down:
        print('left mouse down')
        # Get origin
        pan_cam_flag = True
        origin = Vec3(mouse.x, mouse.y, 0)

        cam_origin = camera.position




    if key == Keys.right_mouse_up:
        pan_cam_flag = False
        origin = Vec3(0,0,0) # Reset origin
        cam_origin =  Vec3(0,0,0) # Reset origin
        if key == Keys.right_mouse_down:
            print('left mouse down')
        # Get origin
        pan_cam_flag = False
        origin = Vec3(mouse.x, mouse.y, 0)

        cam_origin = camera.position
    if key == Keys.left_mouse_down:
        print('left mouse down')
        # Get origin
        rot_cam_flag = True
        origin = Vec3(mouse.x, mouse.y, 0)

        cam_rot_origin = camera.rotation

        CollisionNode

        # cube selected
        if cube.hovered:
            cube_selected = True
            cube.color = color.rgb(255, 0,0)
        else:
            cube.color = color.orange
            cube_selected = False

    if key == Keys.left_mouse_up:
        rot_cam_flag = False
        origin = Vec3(0,0,0) # Reset origin
        cam_rot_origin =  Vec3(0,0,0) # Reset origin

    if key in [Keys.scroll_up, Keys.scroll_down]:
        scroll_cam_origin = camera.position
    if key == Keys.scroll_up:
        camera.position = scroll_cam_origin + camera.forward*sensitivity
    if key == Keys.scroll_down:
        camera.position = scroll_cam_origin + camera.back*sensitivity



    print("end handler")
def update():
    """
    Update of every object
    :return:
    """
    # World Update
    # cube.rotation_y += time.dt * 100
    # red = random_generator.random() * 255
    # green = random_generator.random() * 255
    # blue = random_generator.random() * 255
    # cube.color= color.rgb(red,green,blue)
    #print(mouse.hovered_entity)

    if held_keys['q']:                  # If t is pressed
        pass
    if held_keys['z']:                  # If t is pressed
        pass

    global pan_cam_flag, sensitivity,rot_cam_flag, zoom_cam_flag
    if pan_cam_flag:
        print(f"PanCam Mode = {camera.position}\ncam_origin = {cam_origin}\norigin = {origin}\nmouse.position = {mouse.position}")
        change_in_pos = (origin - mouse.position)*sensitivity
        camera.position = cam_origin + camera.up*change_in_pos[1] + camera.right*change_in_pos[0]


    if rot_cam_flag:
        print(f"RotCam Mode = {camera.rotation}\ncam_origin = {cam_rot_origin}\norigin = {origin}\nmouse.position = {mouse.position}")
        change_in_pos = (origin - mouse.position)*sensitivity
        #camera.rotation = cam_rot_origin + origin - mouse.position*20
        camera.rotation_y = (cam_rot_origin.y + 1.0*change_in_pos[0]*sensitivity)%360
        camera.rotation_x = (cam_rot_origin.x + 1.0*change_in_pos[1]*10)%360
        camera.rotation_z = 0 # Never roll k thanks



def info():
    print("Information for the user")

app = Ursina()

camera_collision_node = CollisionNode


window.title = 'My Game'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = False      # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter
cube = Entity(model='wireframe_cube', color=color.orange, scale=(2,2,2))
cube.collider = BoxCollider(cube)
planey_plane = Entity(model='plane', color = color.green, scale=(20,20,20)) #Plane()
planey_plane.collider = MeshCollider(planey_plane, )
#planey_plane.coll
button = Button(text="Info!", scale = 0.25)
button.x = -0.5
button.y = 0.4
button.on_click = info
app.run()                       # opens a window and starts the game.

running = True
