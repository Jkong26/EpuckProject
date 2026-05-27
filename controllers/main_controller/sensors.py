class Sensors:
    def __init__(self, robot, ps, encoders=None):

        # Reference to robot instance (Webots controller)
        self.robot = robot

        # List of proximity sensors (ps0–ps7)
        self.ps = ps

        # wheel encoders for motion tracking / stuck detection
        self.encoders = encoders  

    def read(self):
        # Read all proximity sensor values into a list
        values = [p.getValue() for p in self.ps]

        # -------------------------
        # SENSOR MAPPING
        # -------------------------

        # Front-left sensor (e-puck sensor index 7)
        front_left = values[7]

        # Front-right sensor (e-puck sensor index 0)
        front_right = values[0]

        # Combined front distance (average of front sensors)
        front = (values[7] + values[0]) * 0.5

        # Left side sensor
        left = values[6]
        # Right side sensor
        right = values[1]

        # Group the main sensor readings
        data = {    
            "front_left": front_left,
            "front_right": front_right,
            "front": front,
            "left": left,
            "right": right
        }

        # Read encoder positions if available (used for motion tracking)
        # Used for detecting movement / stuck conditions
        if self.encoders:
            left_enc, right_enc = self.encoders
            data["enc_left"] = left_enc.getValue()
            data["enc_right"] = right_enc.getValue()

        return data