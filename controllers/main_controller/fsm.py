from config import *

class FSM:
    def __init__(self):
        self.state = "EXPLORE" # Current FSM state
        self._stuck_counter = 0 # Counter used to detect if robot is stuck
        self._recovery_counter = 0 # Counter used during recovery behaviour
        self._prev_enc_left = None   # Previous left encoder value for movement tracking

    def update(self, sensor, goal_detected):

        # -------------------------
        # GOAL STATE
        # -------------------------
        # If the goal has been detected, immediately switch to GOAL_REACHED
        if goal_detected:
            self.state = "GOAL_REACHED"
            self._stuck_counter = 0
            return

        # -------------------------
        # RECOVERY STATE
        # -------------------------
        # Recovery behaviour runs for a fixed number of steps
        if self.state == "RECOVERY":
            self._recovery_counter += 1

            # After recovery is complete, return to EXPLORE mode
            if self._recovery_counter >= RECOVERY_STEPS:
                self.state = "EXPLORE"
                self._recovery_counter = 0
                self._stuck_counter = 0

            # Update encoder reference
            self._prev_enc_left = sensor.get("enc_left", 0)
            return

        # Read sensor values
        front = sensor["front"]
        right = sensor["right"]

        # -------------------------
        # ENCODER STUCK CHECK
        # -------------------------
        # Detect whether the robot wheels are no longer moving
        curr_enc_left = sensor.get("enc_left", 0)

        # Store the first encoder value
        if self._prev_enc_left is None:
            self._prev_enc_left = curr_enc_left

        # If encoder change is extremely small, assume robot is stuck
        encoder_not_moving = abs(curr_enc_left - self._prev_enc_left) < 0.001

        # Save current encoder for next cycle
        self._prev_enc_left = curr_enc_left

        # -------------------------
        # OBSTACLE / STUCK
        # -------------------------
        # Trigger avoidance if:
        # 1. Front obstacle detected
        # 2. Robot appears stuck
        if front > FRONT_AVOID_ON or encoder_not_moving:
            self._stuck_counter += 1

            # If stuck for too long, enter RECOVERY state
            if self._stuck_counter >= STUCK_TIME_LIMIT:
                self.state = "RECOVERY"
                self._recovery_counter = 0
            
            # Otherwise perform simple avoidance
            else:
                self.state = "AVOID"

            return
        # Reset stuck counter if robot is moving normally
        self._stuck_counter = 0

        # -------------------------
        # WALL DETECTION
        # -------------------------
        # If a wall exists on the right, switch to wall following
        if right > WALL_THRESHOLD:
            self.state = "WALL_FOLLOW"

        # Otherwise continue exploring
        else:
            self.state = "EXPLORE"

    def get_action(self, sensor):

        # Read sensor values
        front = sensor["front"]
        right = sensor["right"]

        # -------------------------
        # GOAL
        # -------------------------
        # Stop robot when goal reached
        if self.state == "GOAL_REACHED":
            return ("STOP", 0)

        # -------------------------
        # RECOVERY
        # -------------------------
        # Turn left continuously during recovery
        if self.state == "RECOVERY":
            return ("TURN_LEFT", 0)

        # -------------------------
        # AVOID
        # -------------------------
        # Simple obstacle (corners or dead-ends) avoidance behaviour
        if self.state == "AVOID":
            return ("TURN_LEFT", 0)

        # -------------------------
        # WALL FOLLOW (FIXED CONTROL)
        # -------------------------
        if self.state == "WALL_FOLLOW":

            # emergency correction if too close
            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            # Calculate wall-following error
            # Positive = too close to wall
            # Negative = too far from wall
            error = right - DESIRED_RIGHT

            # -------------------------
            # PROPORTIONAL-LIKE CONTROL
            # -------------------------
            # Too close to wall
            if error > WALL_DIFF:
                return ("SLIGHT_LEFT", 0)
            # Too far from wall
            elif error < -WALL_DIFF:
                return ("SLIGHT_RIGHT", 0)
            # Correct distance maintained
            return ("MOVE_FORWARD", 0)

        # -------------------------
        # EXPLORE
        # -------------------------
        if self.state == "EXPLORE":
            
            # No wall detected on right, search for wall by turning right
            if right < WALL_THRESHOLD:
                return ("TURN_RIGHT", 0)

            # Avoid front obstacle
            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            # Continue moving forward
            return ("MOVE_FORWARD", 0)