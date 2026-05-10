class ResourceCSP:
    """Constraint Satisfaction Problem for ambulance allocation"""
    
    def __init__(self, ambulances, max_capacity=2, kits=10):
        self.ambulances = ambulances
        self.max_capacity = max_capacity
        self.kits = kits
        self.assignments = {}
        self.backtrack_count = 0
    
    def solve(self, patients):
        """Solve using backtracking + MRV heuristic"""
        unassigned = [p for p in patients if not getattr(p, 'assigned', False)]
        unassigned.sort(key=lambda p: self.count_options(p))
        return self.backtrack(unassigned)
    
    def count_options(self, patient):
        """MRV: Count valid ambulances for this patient"""
        count = 0
        for amb in self.ambulances:
            if len(getattr(amb, 'current_patients', [])) < self.max_capacity:
                count += 1
        return count
    
    def backtrack(self, unassigned):
        """Backtracking with forward checking"""
        self.backtrack_count += 1
        
        if not unassigned:
            return self.assignments
        
        patient = unassigned[0]
        
        for amb in self.ambulances:
            if self.is_valid(amb, patient):
                self.assignments[patient.id] = amb.id
                if hasattr(amb, 'current_patients'):
                    amb.current_patients.append(patient)
                if hasattr(patient, 'assigned'):
                    patient.assigned = True
                
                result = self.backtrack(unassigned[1:])
                if result is not None:
                    return result
                
                del self.assignments[patient.id]
                if hasattr(amb, 'current_patients'):
                    amb.current_patients.remove(patient)
                if hasattr(patient, 'assigned'):
                    patient.assigned = False
        
        return None
    
    def is_valid(self, amb, patient):
        """Check all constraints"""
        current_count = len(getattr(amb, 'current_patients', []))
        if current_count >= self.max_capacity:
            return False
        if self.kits < 1:
            return False
        return True