class Sensors:
    def __init__(self, robot, ps, encoders=None):
        """
        Sensor class for reading distance sensors
        and wheel encoder values from the robot.
        """
        self.robot = robot

        # Proximity sensors array
        self.ps = ps

        #This is the wheel encoder values from the robot
        self.encoders = encoders  # wheel encoders for motion tracking

    def read(self):
        """
        Read all proximity sensor values and
        return important sensor data in a dictionary.
        """

        # Get raw values from all proximity sensors
        values = [p.getValue() for p in self.ps]

        # Print raw sensor values for debugging
        print("RAW:", values)

        # Front sensors
        front_left = values[7]
        front_right = values[0]


        # Average front distance
        # Gives a more stable front reading
        # Front distance: average of the two forward-facing sensors
        front = (values[7] + values[0]) * 0.5

        # Side sensors
        left = values[6]
        right = values[1]

        # Store processed sensor data
        data = {
            "front_left": front_left,
            "front_right": front_right,
            "front": front,
            "left": left,
            "right": right
        }

        # If wheel encoders exist,
        # also read encoder positions
        # Read encoder positions if available (used for motion tracking)
        if self.encoders:
            left_enc, right_enc = self.encoders
            data["enc_left"] = left_enc.getValue()
            data["enc_right"] = right_enc.getValue()

        return data