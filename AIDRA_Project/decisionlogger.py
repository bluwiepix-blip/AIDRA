# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:49:14 2026

@author: DELL
"""

import time

class DecisionLogger:
    """Logs all agent decisions with justifications"""
    
    def __init__(self):
        self.logs = []
        
    def log_route_choice(self, ambulance_id, algorithm, path, reason):
        """Log route selection with trade-off justification"""
        log_entry = {
            "time": time.time(),
            "type": "ROUTE_SELECTION",
            "ambulance": ambulance_id,
            "algorithm": algorithm,
            "path_length": len(path) if path else 0,
            "risk_exposure": sum(1 for x,y in path if grid_at(x,y) == 'R'),
            "decision": reason,
            "trade_off": self._analyze_trade_off(path)
        }
        self.logs.append(log_entry)
        print(f"[DECISION] {ambulance_id}: {reason}")
        print(f"[TRADE-OFF] {log_entry['trade_off']}")
    
    def log_prioritization(self, patient_id, priority_score, reason):
        """Log why a patient was prioritized"""
        log_entry = {
            "time": time.time(),
            "type": "PRIORITIZATION",
            "patient": patient_id,
            "priority_score": priority_score,
            "reason": reason
        }
        self.logs.append(log_entry)
        print(f"[PRIORITY] {patient_id}: {reason} (Score: {priority_score})")
    
    def log_replanning(self, ambulance_id, trigger_event, old_path, new_path):
        """Log replanning events"""
        log_entry = {
            "time": time.time(),
            "type": "REPLANNING",
            "ambulance": ambulance_id,
            "trigger": trigger_event,
            "old_path_length": len(old_path),
            "new_path_length": len(new_path),
            "reason": f"Replanned due to {trigger_event}"
        }
        self.logs.append(log_entry)
        print(f"[REPLAN] {ambulance_id}: {trigger_event}")
    
    def _analyze_trade_off(self, path):
        """Analyze time vs risk trade-off"""
        if not path:
            return "No path"
        
        risk_count = sum(1 for x,y in path if grid[x][y] == 'R')
        if risk_count > 0:
            return f"PRIORITIZED SPEED (Accepting risk in {risk_count} cells)"
        else:
            return "PRIORITIZED SAFETY (Avoiding all risk zones)"
    
    def get_summary(self):
        """Get decision summary report"""
        summary = "DECISION LOG SUMMARY\n"
        summary += "="*50 + "\n"
        for log in self.logs:
            summary += f"[{log['type']}] {log.get('decision', log.get('reason', ''))}\n"
        return summary

# Global grid reference for risk checking
def grid_at(x, y):
    """Helper to check grid cell type"""
    try:
        from environment.grid import current_grid
        return current_grid[x][y]
    except:
        return '.'