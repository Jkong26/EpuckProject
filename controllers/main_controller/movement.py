from config import *

# -------------------------
# PREVIOUS MOTOR SPEEDS
# -------------------------
# Stores previous wheel speeds for smoothing and acceleration limiting
_prev_left = 0.0
_prev_right = 0.0

# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def clamp(x):
    """
    Clamp motor speed within safe limits.

    Prevents motor speeds from exceeding
    the robot's maximum allowed speed.
    """
    return max(-MAX_SPEED, min(MAX_SPEED, x))

def smooth(target, prev):
    """
    Apply exponential smoothing.

    Reduces sudden speed changes to make
    robot movement smoother and more stable.
    """
    return SMOOTHING_ALPHA * target + (1 - SMOOTHING_ALPHA) * prev

def accel_limit(target, prev):
    """
    Limit acceleration/deceleration.

    Ensures wheel speeds change gradually
    instead of instantly jumping.
    """
    # Limit positive acceleration
    diff = target - prev
    if diff > MAX_ACCEL:
        return prev + MAX_ACCEL
    
    # Limit negative acceleration
    elif diff < -MAX_ACCEL:
        return prev - MAX_ACCEL
    return target

# -------------------------
# CORE DRIVE FUNCTION
# -------------------------
def drive(left_motor, right_motor, left_target, right_target):
    """
    Main drive controller.  
    Steps:
    1. Smooth target speeds
    2. Limit acceleration
    3. Clamp to safe motor range
    4. Send final speed to motors
    """
    global _prev_left, _prev_right

    # SPEED SMOOTHING
    left = smooth(left_target, _prev_left)
    right = smooth(right_target, _prev_right)

    # ACCELERATION LIMITING
    left = accel_limit(left, _prev_left)
    right = accel_limit(right, _prev_right)

    # SAFETY CLAMPING
    left = clamp(left)
    right = clamp(right)

    # SAVE CURRENT SPEEDS
    _prev_left = left
    _prev_right = right

    # APPLY TO MOTORS
    left_motor.setVelocity(left)
    right_motor.setVelocity(right)

# -------------------------
# MOVEMENTS 
# -------------------------
def forward(left_motor, right_motor):
    """
    Move robot straight forward.
    """
    drive(left_motor, right_motor, FORWARD_SPEED, FORWARD_SPEED)

def slight_left(left_motor, right_motor):
    """
    Perform a gentle left correction.

    Left wheel moves slower than right wheel.
    Used for wall-following adjustments.
    """
    drive(left_motor, right_motor,
          FORWARD_SPEED - SLIGHT_SPEED,
          FORWARD_SPEED)

def slight_right(left_motor, right_motor):
    """
    Perform a gentle right correction.

    Right wheel moves slower than left wheel.
    Used for wall-following adjustments.
    """
    drive(left_motor, right_motor,
          FORWARD_SPEED,
          FORWARD_SPEED - SLIGHT_SPEED)

# -------------------------
# ARC TURNS 
# -------------------------
def turn_left(left_motor, right_motor):
    """
    Perform a left arc turn.

    Right wheel moves faster than left wheel.
    """
    drive(left_motor, right_motor, 1.58, 3.64)

def turn_right(left_motor, right_motor):
    """
    Perform a right arc turn.

    Left wheel moves faster than right wheel.
    """
    drive(left_motor, right_motor, 3.64, 1.58)

# -------------------------
# STOP FUNCTION
# -------------------------
def stop(left_motor, right_motor):
    """
    Stop both robot wheels.
    """
    drive(left_motor, right_motor, 0.0, 0.0)