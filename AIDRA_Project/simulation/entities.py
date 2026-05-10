class Patient:

    def __init__(
        self,
        pid,
        position,
        incident_time
    ):

        self.id = pid

        self.position = position

        self.incident_time = incident_time

        self.rescued = False

        self.in_hospital = False

        self.assigned = False
        
        self.rescue_time = None

        self.pickup_step = None

        self.delivery_step = None

        # Auto-calculate severity based on incident time
        if incident_time >= 12:
            self.severity = "critical"
        elif incident_time >= 6:
            self.severity = "moderate"
        else:
            self.severity = "minor"


class Ambulance:

    def __init__(
        self,
        aid,
        position,
        color,
        capacity=2
    ):

        self.id = aid

        self.position = position

        self.color = color

        self.capacity = capacity

        self.current_patients = []

        self.available = True

        self.path = []

        self.target = None

        self.algorithm = None


class Hospital:

    def __init__(
        self,
        hid,
        position
    ):

        self.id = hid

        self.position = position
