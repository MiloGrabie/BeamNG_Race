from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from beamngpy import BeamNGpy, Scenario, Vehicle, setup_logging
from beamngpy.sensors import Lidar
from beamngpy.visualiser import LidarVisualiser

SIZE = 1024


def lidar_resize(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)


def open_window(width, height):
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(width, height)
    window = glutCreateWindow(b'Lidar Tour')
    lidar_resize(width, height)
    return window


# homePath = r'C:\Users\Milo\Documents\BeamNG.drive\0.22\mods'
# homePath = r'C:\Program Files (x86)\BeamNG DRIVE'
bng = BeamNGpy('localhost', 64256)
# Launch BeamNG.tech
bng.open()
scenario = Scenario('hirochi_raceway', 'default')
vehicle = Vehicle('ego_vehicle', model='etk800', licence='PYTHON')
lidar = Lidar()
scenario.make(bng)

# Load and start our scenario
bng.load_scenario(scenario)
# bng.start_scenario()
# Make the vehicle's AI span the map
# vehicle.ai_set_mode('span')
vehicle.attach_sensor('lidar', lidar)
scenario.add_vehicle(vehicle, pos=(-408, 259, 25.5), rot=(0.000523, -0.000577, 0.9999696))

window = open_window(SIZE, SIZE)
lidar_vis = LidarVisualiser(Lidar.max_points)
lidar_vis.open(SIZE, SIZE)

bng.set_steps_per_second(60)
bng.set_deterministic()

# bng.hide_hud()

# bng.load_scenario(scenario)
# bng.start_scenario()

# bng.pause()
vehicle.ai_set_mode('span')


def update():
    vehicle.poll_sensors()
    points = lidar.data['points']
    bng.step(3, wait=False)

    lidar_vis.update_points(points, vehicle.state)
    glutPostRedisplay()


glutReshapeFunc(lidar_resize)
glutIdleFunc(update)
glutMainLoop()
