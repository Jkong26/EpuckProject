from config import *


class FSM:
    def __init__(self):
        # Initial state of the robot
        self.state = "EXPLORE"

        # Counter to detect if robot is stuck
        self._stuck_counter = 0

        # Counter used during recovery behaviour
        self._recovery_counter = 0

        # Previous encoder value for movement detection
        self._prev_enc_left = None   # for encoder-based motion tracking

    def update(self, sensor, goal_detected):
        # GOAL CHECK (highest priority)
        if goal_detected:
            self.state = "GOAL_REACHED"
            self._stuck_counter = 0
            return

        # RECOVERY STATE HANDLING
        # If currently recovering, count down recovery steps
        if self.state == "RECOVERY":
            self._recovery_counter += 1

            # Stay in recovery for fixed number of steps
            if self._recovery_counter >= RECOVERY_STEPS:
                self.state = "EXPLORE"
                self._recovery_counter = 0
                self._stuck_counter = 0

            # Update encoder baseline to prevent false stuck detection
            self._prev_enc_left = sensor.get("enc_left", 0)
            return

        # SENSOR READINGS
        front = sensor["front"]
        right = sensor["right"]
        left = sensor["left"]

        ## ENCODER-BASED STUCK DETECTION
        curr_enc_left = sensor.get("enc_left", 0)

        # Initialise encoder reference if first run
        if self._prev_enc_left is None:
            self._prev_enc_left = curr_enc_left

        # Detect if robot is not moving (very small encoder change)
        encoder_not_moving = abs(curr_enc_left - self._prev_enc_left) < 0.01

        # Update encoder for next cycle
        self._prev_enc_left = curr_enc_left

        # STUCK / OBSTACLE HANDLING
        # If obstacle in front OR robot not moving -> consider stuck
        if front > FRONT_AVOID_ON or encoder_not_moving:
            self._stuck_counter += 1

            # If stuck too long -> enter recovery mode
            if self._stuck_counter >= STUCK_TIME_LIMIT:
                self.state = "RECOVERY"
                self._recovery_counter = 0
            else:
                # Temporary avoidance behaviour
                self.state = "AVOID"
            return
        
        # Reset stuck counter if movement is normal
        self._stuck_counter = 0

        # WALL DETECTION LOGIC
        # If wall exists on right side -> follow it
        if right > WALL_THRESHOLD:
            self.state = "WALL_FOLLOW"
        else:
            # Otherwise explore freely
            self.state = "EXPLORE"

    def get_action(self, sensor):
        front = sensor["front"]
        right = sensor["right"]
        left = sensor["left"]

        # --- GOAL REACHED: stop the robot ---
        if self.state == "GOAL_REACHED":
            return ("STOP", 0)

        # --- RECOVERY: turn left to escape stuck situation ---
        if self.state == "RECOVERY":
            return ("TURN_LEFT", 0)

        # --- AVOID: obstacle ahead, turn left ---
        if self.state == "AVOID":
            return ("TURN_LEFT", 0)

        # --- WALL FOLLOW: adjust direction using left-right sensor difference ---
        if self.state == "WALL_FOLLOW":
            # Gap opened on the right — turn to follow
            if right < RIGHT_OPEN_THRESHOLD:
                return ("TURN_RIGHT", 0)

            # Obstacle ahead while wall following
            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            # Use left-right difference to adjust balance in corridor
            diff = left - right

            if diff > WALL_DIFF_STRONG:
                return ("TURN_RIGHT", 0)
            elif diff < -WALL_DIFF_STRONG:
                return ("TURN_LEFT", 0)
            elif diff > WALL_DIFF_SMALL:
                return ("SLIGHT_RIGHT", 0)
            elif diff < -WALL_DIFF_SMALL:
                return ("SLIGHT_LEFT", 0)
            else:
                return ("MOVE_FORWARD", 0)

        # --- EXPLORE: move forward, drift toward right wall if one appears ---
        if self.state == "EXPLORE":

            # If no wall on right -> try to find one (right-hand rule)
            if right < WALL_THRESHOLD:
                return ("TURN_RIGHT", 0)

            # Avoid obstacle in front
            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            # Default forward movement
            return ("FORWARD", 0)