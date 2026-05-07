from config import *


class FSM:
    def __init__(self):
        self.state = "EXPLORE"
        self._stuck_counter = 0
        self._recovery_counter = 0
        self._prev_enc_left = None   # for encoder-based motion tracking

    def update(self, sensor, goal_detected):
        if goal_detected:
            self.state = "GOAL_REACHED"
            self._stuck_counter = 0
            return

        # If currently recovering, count down recovery steps
        if self.state == "RECOVERY":
            self._recovery_counter += 1
            if self._recovery_counter >= RECOVERY_STEPS:
                self.state = "EXPLORE"
                self._recovery_counter = 0
                self._stuck_counter = 0
            # Update encoder baseline so we don't immediately re-trigger
            self._prev_enc_left = sensor.get("enc_left", 0)
            return

        front = sensor["front"]
        right = sensor["right"]
        left = sensor["left"]

        # --- Encoder-based motion tracking ---
        curr_enc_left = sensor.get("enc_left", 0)
        if self._prev_enc_left is None:
            self._prev_enc_left = curr_enc_left

        encoder_not_moving = abs(curr_enc_left - self._prev_enc_left) < 0.01
        self._prev_enc_left = curr_enc_left

        # Obstacle directly ahead OR encoder shows no movement — increment stuck counter
        if front > FRONT_AVOID_ON or encoder_not_moving:
            self._stuck_counter += 1
            # If stuck too long, trigger recovery (fail-safe)
            if self._stuck_counter >= STUCK_TIME_LIMIT:
                self.state = "RECOVERY"
                self._recovery_counter = 0
            else:
                self.state = "AVOID"
            return

        self._stuck_counter = 0

        # Wall detected on the right — follow it
        if right > WALL_THRESHOLD:
            self.state = "WALL_FOLLOW"
        else:
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
            if right < WALL_THRESHOLD:
                return ("TURN_RIGHT", 0)

            if front > FRONT_AVOID_ON:
                return ("TURN_LEFT", 0)

            return ("FORWARD", 0)