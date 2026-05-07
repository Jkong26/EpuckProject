from controller import Robot
from sensors import Sensors
from fsm import FSM
import movement
from config import *

# GOAL DETECTION FUNCTION
def detect_goal(camera):
    """
    Detect green goal area using camera image.
    Checks pixels near the center of the screen.
    """
    # Get image from camera
    image = camera.getImage()

    # Camera dimensions
    width = camera.getWidth()
    height = camera.getHeight()

    green_count = 0
    total = 0

    # Scan small center region
    for dx in range(-5, 6):
        for dy in range(-4, 5):

            # Current pixel coordinates
            cx = width // 2 + dx
            cy = height // 2 + dy

            # Get RGB values
            r = camera.imageGetRed(image, width, cx, cy)
            g = camera.imageGetGreen(image, width, cx, cy)
            b = camera.imageGetBlue(image, width, cx, cy)

            total += 1

            # Check if pixel is mostly green
            if g > r + 15 and g > b + 15:
                green_count += 1
    # Safety check
    if total == 0:
        return False

    # Goal detected if enough green pixels found
    return (green_count / total) > 0.65

# MAIN FUNCTION
def main():
    # Create robot object
    robot = Robot()

    # Simulation timestep
    timestep = int(robot.getBasicTimeStep())

    # Camera
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # Wheel motors
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # Wheel encoders (position sensors) for motion tracking
    left_encoder = robot.getDevice("left wheel sensor")
    right_encoder = robot.getDevice("right wheel sensor")
    left_encoder.enable(timestep)
    right_encoder.enable(timestep)

    # Distance sensors
    ps = []
    for i in range(8):
        # Get proximity sensor
        sensor = robot.getDevice(f"ps{i}")
        # Enable sensor
        sensor.enable(timestep)
        ps.append(sensor)

    # Create sensor manager
    sensors = Sensors(robot, ps, encoders=(left_encoder, right_encoder))
    # Create finite state machine
    fsm = FSM()
    # Counter for stable goal detection
    goal_counter = 0

    # MAIN ROBOT LOOP
    while robot.step(timestep) != -1:
        # Read all sensor values
        sensor_data = sensors.read()

        
        # GREEN DETECTION
        if detect_goal(camera):
            # Increase counter if green is seen
            goal_counter += 1
        else:
            # Reset counter if green disappears
            goal_counter = 0

        # Confirm goal after several frames
        green_seen = goal_counter >= GOAL_CONFIRM_TIME

        
        # WALL / OBJECT TOUCH DETECTION
        # Detect if front sensors are very close
        touching_wall = (
            sensor_data["front_left"] > GOAL_TOUCH_THRESHOLD or
            sensor_data["front_right"] > GOAL_TOUCH_THRESHOLD
        )

        # Goal reached only if:
        # 1. Green goal confirmed
        # 2. Robot touches wall/object
        goal_detected = green_seen and touching_wall

       
        # STOP WHEN GOAL IS REACHED
        if goal_detected:
            print("GOAL REACHED")
            # Stop robot movement
            movement.stop(left_motor, right_motor)

            # Wait a few steps to fully stop robot
            for _ in range(20):
                robot.step(timestep)

            break

        
        # FSM DECISION MAKING

        # Update FSM state
        fsm.update(sensor_data, goal_detected)

        # Get movement action from FSM
        action, value = fsm.get_action(sensor_data)
        
        # Debug output
        print(f"{fsm.state} -> {action}", sensor_data)

        # ROBOT MOVEMENT
        if action == "MOVE_FORWARD":
            movement.forward(left_motor, right_motor)

        elif action == "SLIGHT_RIGHT":
            movement.slight_right(left_motor, right_motor)

        elif action == "SLIGHT_LEFT":
            movement.slight_left(left_motor, right_motor)

        elif action == "FORWARD":
            movement.forward(left_motor, right_motor)

        elif action == "TURN_LEFT":
            movement.turn_left(left_motor, right_motor)

        elif action == "TURN_RIGHT":
            movement.turn_right(left_motor, right_motor)

        elif action == "STOP":
            movement.stop(left_motor, right_motor)

# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()