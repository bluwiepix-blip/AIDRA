class Patient:
    def __init__(self, pid, position, incident_time):
        self.id = pid
        self.position = position
        self.incident_time = incident_time
        self.rescued = False
        self.in_hospital = False
        self.assigned = False
        self.rescue_time = None  # Track when rescued
        self.severity = self._calculate_severity()
    
    def _calculate_severity(self):
        """Calculate severity based on incident time"""
        if self.incident_time >= 12:
            return "critical"
        elif self.incident_time >= 6:
            return "moderate"
        else:
            return "minor"

class Ambulance:
    def __init__(self, aid, position, color, capacity=2):
        self.id = aid
        self.position = position
        self.color = color
        self.capacity = capacity
        self.current_patients = []
        self.available = True
        self.path = []
        self.target = None
        self.algorithm = None
        self.mission_log = []  # Track decisions
    
    def reset_mission(self):
        """Reset ambulance after completing mission"""
        self.path = []
        self.target = None
        self.algorithm = None
        self.current_patients.clear()
        self.available = True

class Hospital:
    def __init__(self, hid, position):
        self.id = hid
        self.position = position
        self.patients_treated = []