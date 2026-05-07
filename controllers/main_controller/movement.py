from config import FORWARD_SPEED, SLIGHT_SPEED

# Maximum wheel speed of the robot
MAX_SPEED = 6.28


# Smoothing factor for low-pass filter
# Smaller value = smoother movement but slower reaction
SMOOTHING_ALPHA = 0.25   # lower = smoother but slower response

# Limits how much the speed can change each step
# Helps reduce shaking / sudden jerks
MAX_ACCEL = 0.15         # max speed change per step (removes shaking)

# Small dead zones to ignore tiny movements/errors
DEAD_ZONE_DIST = 0.02
DEAD_ZONE_ANGLE = 1.0


# Maximum correction allowed while turning
CORRECTION_LIMIT = 1.5


# Store previous motor values for smoothing
_prev_left = 0.0
_prev_right = 0.0


# UTILITY FUNCTIONS
def clamp(speed):
    """
    Keep speed within robot motor limits.
    """
    return max(-MAX_SPEED, min(MAX_SPEED, speed))


def low_pass(new, prev):
    """
    Apply low-pass filtering for smoother movement.
    Blends new speed with previous speed.
    """
    return (SMOOTHING_ALPHA * new) + ((1 - SMOOTHING_ALPHA) * prev)


def apply_accel_limit(target, prev):
    """
    Prevent sudden speed changes.
    Makes acceleration/deceleration smoother.
    """
    delta = target - prev
    if delta > MAX_ACCEL:
        delta = MAX_ACCEL
    elif delta < -MAX_ACCEL:
        delta = -MAX_ACCEL
    return prev + delta


# MOVEMENT FUNCTIONS
def forward(left_motor, right_motor):
    """
    Move robot straight forward smoothly.
    """
    global _prev_left, _prev_right

    target = FORWARD_SPEED

    _prev_left = low_pass(target, _prev_left)
    _prev_right = low_pass(target, _prev_right)

    left_motor.setVelocity(clamp(_prev_left))
    right_motor.setVelocity(clamp(_prev_right))


def slight_right(left_motor, right_motor):
    """
    Slightly turn robot to the right.
    Right wheel moves slower than left wheel.
    """
    global _prev_left, _prev_right

    left_target = FORWARD_SPEED
    right_target = FORWARD_SPEED - (SLIGHT_SPEED * 0.7)

    _prev_left = low_pass(left_target, _prev_left)
    _prev_right = low_pass(right_target, _prev_right)

    left_motor.setVelocity(clamp(_prev_left))
    right_motor.setVelocity(clamp(_prev_right))


def slight_left(left_motor, right_motor):
    """
    Slightly turn robot to the left.
    Left wheel moves slower than right wheel.
    """
    global _prev_left, _prev_right

    left_target = FORWARD_SPEED - (SLIGHT_SPEED * 0.7)
    right_target = FORWARD_SPEED

    _prev_left = low_pass(left_target, _prev_left)
    _prev_right = low_pass(right_target, _prev_right)

    left_motor.setVelocity(clamp(_prev_left))
    right_motor.setVelocity(clamp(_prev_right))


def turn_left(left_motor, right_motor):
    """
    Rotate robot left on the spot.
    """
    global _prev_left, _prev_right

    left_target = -1.0
    right_target = 1.2

    _prev_left = low_pass(left_target, _prev_left)
    _prev_right = low_pass(right_target, _prev_right)

    left_motor.setVelocity(clamp(_prev_left))
    right_motor.setVelocity(clamp(_prev_right))


def turn_right(left_motor, right_motor):
    """
    Rotate robot right on the spot.
    """
    global _prev_left, _prev_right

    left_target = 1.2
    right_target = -1.0

    _prev_left = low_pass(left_target, _prev_left)
    _prev_right = low_pass(right_target, _prev_right)

    left_motor.setVelocity(clamp(_prev_left))
    right_motor.setVelocity(clamp(_prev_right))


def stop(left_motor, right_motor):
    """
    Stop both motors immediately.
    """
    global _prev_left, _prev_right

    _prev_left = 0
    _prev_right = 0

    left_motor.setVelocity(0)
    right_motor.setVelocity(0)