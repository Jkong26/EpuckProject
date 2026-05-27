from controller import Robot
from sensors import Sensors
from fsm import FSM
import movement
from config import *

# -------------------------
# GOAL DETECTION FUNCTION
# -------------------------
# Detects whether the camera is currently seeing the green goal area
def detect_goal(camera):
    # Capture image from camera
    image = camera.getImage()

    # Get camera dimensions
    width = camera.getWidth()
    height = camera.getHeight()

    # Counters for green pixel detection
    green_count = 0
    total = 0

    # Scan a small region around the image center, instead of checking the whole image
    for dx in range(-5, 6):
        for dy in range(-4, 5):

            # Pixel coordinates near image center
            cx = width // 2 + dx
            cy = height // 2 + dy

            # Extract RGB colour values from the current pixel
            r = camera.imageGetRed(image, width, cx, cy)
            g = camera.imageGetGreen(image, width, cx, cy)
            b = camera.imageGetBlue(image, width, cx, cy)

            total += 1
            
            # Detect "green-dominant" pixels
            if g > r + 15 and g > b + 15:
                green_count += 1
    # Stop if no pixels are detected
    if total == 0:
        return False
    # Goal confirmed if most center pixels are green
    return (green_count / total) > 0.65

# -------------------------
# MAIN ROBOT PROGRAM
# -------------------------
def main():
    # Create robot instance
    robot = Robot()

    # Get simulation timestep
    timestep = int(robot.getBasicTimeStep())

    # -------------------------
    # Camera
    # -------------------------
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # -------------------------
    # MOTOR SETUP
    # -------------------------
    # Access wheel motors
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    # Enable velocity control mode
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # -------------------------
    # ENCODER SETUP
    # -------------------------
    # Used for detecting whether the robot is stuck
    left_encoder = robot.getDevice("left wheel sensor")
    right_encoder = robot.getDevice("right wheel sensor")

    left_encoder.enable(timestep)
    right_encoder.enable(timestep)

    # -------------------------
    # Distance sensors
    # -------------------------
    ps = []
    # Enable all 8 proximity sensors
    for i in range(8):
        sensor = robot.getDevice(f"ps{i}")
        sensor.enable(timestep)
        ps.append(sensor)

    # -------------------------
    # SYSTEM INITIALISATION
    # -------------------------
    # Sensor processing class
    sensors = Sensors(robot, ps, encoders=(left_encoder, right_encoder))
    # Finite State Machine
    fsm = FSM()

    # Counter used for stable goal confirmation
    goal_counter = 0
    
    # -------------------------
    # MAIN CONTROL LOOP
    # -------------------------
    while robot.step(timestep) != -1:
        # Read all sensor values
        sensor_data = sensors.read()

        # -------------------------
        # GREEN DETECTION
        # -------------------------
        # Check if green goal is visible
        if detect_goal(camera):
            goal_counter += 1
        else:
            goal_counter = 0

        # Goal only confirmed if seen continuously for several frames
        green_seen = goal_counter >= GOAL_CONFIRM_TIME

        # -------------------------
        # TOUCH DETECTION 
        # -------------------------
        # Detect whether robot has physically, reached the wall/goal
        touching_wall = (
            sensor_data["front_left"] > GOAL_TOUCH_THRESHOLD or
            sensor_data["front_right"] > GOAL_TOUCH_THRESHOLD
        )

        # Goal is only confirmed when:
        # 1. Green goal is visible
        # 2. Robot touches the goal wall
        goal_detected = green_seen and touching_wall

        # -------------------------
        # HARD STOP AT GOAL
        # -------------------------
        if goal_detected:
            print("GOAL REACHED")

            # Immediately stop motors
            movement.stop(left_motor, right_motor)

            # Allow robot to fully stop and prevent sliding
            for _ in range(20):
                robot.step(timestep)

            break

        # -------------------------
        # FSM UPDATE
        # -------------------------
        # Update FSM state
        fsm.update(sensor_data, goal_detected)

        # Get next action from FSM
        action, _ = fsm.get_action(sensor_data)

        # Print debugging information
        print(f"{fsm.state} -> {action}", sensor_data)

        # -------------------------
        # ACTION EXECUTION
        # -------------------------
        if action == "MOVE_FORWARD":
            movement.forward(left_motor, right_motor)

        elif action == "SLIGHT_RIGHT":
            movement.slight_right(left_motor, right_motor)

        elif action == "SLIGHT_LEFT":
            movement.slight_left(left_motor, right_motor)

        elif action == "TURN_LEFT":
            movement.turn_left(left_motor, right_motor)

        elif action == "TURN_RIGHT":
            movement.turn_right(left_motor, right_motor)

        elif action == "STOP":
            movement.stop(left_motor, right_motor)

if __name__ == "__main__":
    main()