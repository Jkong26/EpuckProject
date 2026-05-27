# SPEEDS
FORWARD_SPEED = 5.0 # Normal forward movement speed
SLIGHT_SPEED = 2.8 # Reduced speed used for gentle turns/corrections
MAX_SPEED = 6.28 # Maximum wheel speed allowed for the e-puck robot

# WALL FOLLOWING
DESIRED_RIGHT = 70 # Distance to maintain from the right wall

# THRESHOLDS
WALL_DIFF = 5 # Acceptable error range from desired wall distance
FRONT_AVOID_ON = 75 # Front sensor threshold to trigger obstacle avoidance
WALL_THRESHOLD = 75 # Minimum right sensor value required to detect a wall
RIGHT_OPEN_THRESHOLD = 45 # If right sensor drops below this, the right side is open / no wall detected

# GOAL SETTINGS 
GOAL_CONFIRM_TIME = 5 # Number of consecutive checks needed to confirm goal
GOAL_TOUCH_THRESHOLD = 130 # Sensor threshold used to detect contact with green wall
 
# RECOVERY
STUCK_TIME_LIMIT = 30 # Number of steps before robot is considered stuck
RECOVERY_STEPS = 15 # Number of recovery movements performed when stuck

# Smoothing factor (0 = no change, 1 = instant change)
SMOOTHING_ALPHA = 0.35
MAX_ACCEL = 0.2 # Maximum change in wheel speed per control cycle