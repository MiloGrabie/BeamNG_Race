# from beamngpy import *
from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import GForces, Electrics, Ultrasonic

bng = BeamNGpy('localhost', 64256)
bng.open()
scenario = Scenario('hirochi_raceway', 'default')
vehicle = Vehicle('ego_vehicle', model='etk800', licence='PYTHON')
scenario.add_vehicle(vehicle, pos=(-408, 259, 25.5), rot=(0.000523, -0.000577, 0.9999696))
scenario.make(bng)

# Load and start our scenario
bng.load_scenario(scenario)
bng.start_scenario()
# Make the vehicle's AI span the map
# vehicle.ai_set_mode('span')

gforces = GForces()
electrics = Electrics()
ultrasonic = Ultrasonic((20, 20, 20), (0, 0, 0))
ultrasonic.startVisualization(bng, vehicle.vid, (255, 0, 0, 255))

vehicle.attach_sensor('gforces', gforces)
vehicle.attach_sensor('electrics', electrics)
vehicle.attach_sensor('ultrasonic', ultrasonic)

while True:
    vehicle.poll_sensors()

    print()
