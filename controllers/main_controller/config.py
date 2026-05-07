# SPEEDS
# Default forward movement speed
FORWARD_SPEED = 5.0

# Speed difference used for slight turns
# Higher value = sharper correction
SLIGHT_SPEED = 1.5

# Maximum wheel speed allowed by robot
MAX_SPEED = 6.28


# WALL FOLLOWING
# Desired distance from right wall
# Robot tries to maintain this value
DESIRED_RIGHT = 75


# THRESHOLDS
# Strong wall difference threshold
# Used for bigger turning corrections
WALL_DIFF_STRONG = 30

# Small wall difference threshold
# Used for smoother wall corrections
WALL_DIFF_SMALL = 10

# Front obstacle detection threshold
# Robot avoids object if front sensor exceeds this value
FRONT_AVOID_ON = 80

# Minimum value to consider wall detected
WALL_THRESHOLD = 70

# Detects open space on the right side
# Helps robot decide when to turn right
RIGHT_OPEN_THRESHOLD = 40


# GOAL SETTINGS
# Number of continuous frames required
# before confirming goal detection
GOAL_CONFIRM_TIME = 5

# Sensor threshold for touching the goal wall/object
GOAL_TOUCH_THRESHOLD = 130


# RECOVERY
# Number of steps before robot is considered stuck
STUCK_TIME_LIMIT = 30

# Number of recovery movement steps
# used to escape from stuck situations
RECOVERY_STEPS = 15