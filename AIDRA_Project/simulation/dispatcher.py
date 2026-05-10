import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from search.astar import astar
from search.bfs import bfs
from search.greedy import greedy
from search.hill_climbing import hill_climbing
from search.dfs import dfs
from uncertainty.fuzzy import fuzzy_route_score
from utils.comparison import print_algorithm_table

# ==========================================
# SIMPLE KNN MODEL
# ==========================================
class SimpleKNN:
    def __init__(self, k=3):
        self.k = k
        self.X = None
        self.y = None
    
    def fit(self, X, y):
        self.X = X
        self.y = y
    
    def predict(self, X_test):
        preds = []
        for xt in X_test:
            distances = [sum((a-b)**2 for a,b in zip(xt,x))**0.5 for x in self.X]
            k_idx = sorted(range(len(distances)), key=lambda i: distances[i])[:self.k]
            k_labels = [self.y[i] for i in k_idx]
            preds.append(max(set(k_labels), key=k_labels.count))
        return preds

# ==========================================
# SIMPLE NAIVE BAYES MODEL
# ==========================================
class SimpleNaiveBayes:
    def __init__(self):
        self.cp = {}
        self.fp = {}
        self.cls = set()
    
    def fit(self, X, y):
        self.cls = set(y)
        n = len(y)
        nf = len(X[0]) if X else 0
        for c in self.cls:
            self.cp[c] = sum(1 for l in y if l==c)/n
            self.fp[c] = {}
            cs = [X[i] for i in range(n) if y[i]==c]
            for fi in range(nf):
                fv = [s[fi] for s in cs]
                uv = set(fv)
                self.fp[c][fi] = {}
                for v in uv:
                    cnt = sum(1 for vv in fv if vv==v)
                    self.fp[c][fi][v] = (cnt+1)/(len(cs)+len(uv))
    
    def predict(self, X_test):
        preds = []
        for xt in X_test:
            scores = {}
            for c in self.cls:
                s = self.cp[c]
                for fi, fv in enumerate(xt):
                    if fv in self.fp[c][fi]:
                        s *= self.fp[c][fi][fv]
                    else:
                        s *= 0.01
                scores[c] = s
            preds.append(max(scores, key=scores.get))
        return preds

# ==========================================
# TRAIN MODELS
# ==========================================
def train_models():
    X = [[2,12,4],[2,10,3],[2,8,2],[1,10,3],[1,6,1],[1,4,0],[0,8,2],[0,4,0],[0,2,0],[2,15,5]]
    y = [0,0,0,1,1,1,1,1,1,0]
    knn = SimpleKNN(3)
    nb = SimpleNaiveBayes()
    knn.fit(X,y)
    nb.fit(X,y)
    return knn, nb

knn_model, nb_model = train_models()

# ==========================================
# PREDICTION FUNCTIONS
# ==========================================
def predict_path_risk(knn, path, grid):
    if not path: return 1
    rc = sum(1 for x,y in path if grid[x][y]=='R')
    return 0 if knn.predict([[2 if rc>3 else 1 if rc>0 else 0, len(path), rc]])[0]==1 else 1

def predict_survival(nb, patient, te):
    sm = {"critical":2,"moderate":1,"minor":0}
    return nb.predict([[sm.get(patient.severity,1), te, 1]])[0]

def get_survival_probability(patient, rt):
    if patient.severity=="critical": return max(0.20, 0.92-rt*0.025)
    elif patient.severity=="moderate": return max(0.35, 0.96-rt*0.015)
    else: return max(0.55, 0.99-rt*0.008)

# ==========================================
# PATH ANALYSIS
# ==========================================
def analyze_path(path, grid):
    if not path: return {"length":999,"risk":999,"time":999,"cost":999}
    l = len(path)
    r = sum(1 for x,y in path if grid[x][y]=='R')
    return {"length":l,"risk":r,"time":l+r*2,"cost":l*1.5+r*4}

# ==========================================
# FUZZY LOGIC SCORE
# ==========================================
def fuzzy_score(m, ml_risk=0, survival_probability=0.5):
    return fuzzy_route_score(m, ml_risk, survival_probability)



# ==========================================
# ALGORITHM SELECTION - BEST FUZZY SCORE WINS
# ==========================================
algo_tracker = {"A*":0,"BFS":0,"Greedy":0,"DFS":0,"Hill":0}


def reset_algorithm_tracker():
    for algorithm in algo_tracker:
        algo_tracker[algorithm] = 0

def _severity_number(patient):
    severity = getattr(patient, "severity", "moderate") if patient else "moderate"
    return {"critical": 2, "moderate": 1, "minor": 0}.get(severity, 1)


def _survival_probability_from_prediction(prediction, patient, path_time):
    base = get_survival_probability(patient, path_time) if patient else max(0.2, 0.75 - path_time * 0.02)
    if prediction == 1:
        return min(0.99, base + 0.10)
    return max(0.05, base - 0.15)


def choose_best_path(grid, start, goal, patient=None, show_table=True, context="Route selection"):
    algorithms = {
        "A*": astar(grid,start,goal),
        "BFS": bfs(grid,start,goal),
        "DFS": dfs(grid,start,goal),
        "Greedy": greedy(grid,start,goal),
        "Hill": hill_climbing(grid,start,goal)
    }

    rows = []
    best = None
    severity_num = _severity_number(patient)

    for name, path in algorithms.items():
        metrics = analyze_path(path, grid)
        if not path:
            row = {
                "algorithm": name, "length": "N/A", "time": "N/A", "risk": "N/A",
                "knn_risk": "N/A", "nb_survival": "N/A", "fuzzy": "N/A",
                "selected": False, "path": None, "score": 9999,
            }
        else:
            knn_risk = predict_path_risk(knn_model, path, grid)
            nb_prediction = nb_model.predict([[severity_num, metrics["time"], metrics["risk"]]])[0]
            survival_probability = _survival_probability_from_prediction(nb_prediction, patient, metrics["time"])
            score = fuzzy_score(metrics, knn_risk, survival_probability)
            row = {
                "algorithm": name,
                "length": metrics["length"],
                "time": metrics["time"],
                "risk": metrics["risk"],
                "knn_risk": "HIGH" if knn_risk else "LOW",
                "nb_survival": f"{survival_probability * 100:.0f}%",
                "fuzzy": f"{score:.2f}",
                "selected": False,
                "path": path,
                "score": score,
            }
            if best is None or score < best["score"]:
                best = row
        rows.append(row)

    if not best:
        if show_table:
            print_algorithm_table(rows, f"ALGORITHM COMPARISON - {context.upper()} - NO ROUTE FOUND")
        return None, None, rows

    best["selected"] = True
    algo_tracker[best["algorithm"]] = algo_tracker.get(best["algorithm"], 0) + 1

    if show_table:
        target = getattr(patient, "id", goal)
        print_algorithm_table(rows, f"ALGORITHM COMPARISON - {context.upper()}")
        print(f"Selected by lowest fuzzy score: {best['algorithm']} | score={best['fuzzy']} | target={target}")

    return best["algorithm"], best["path"], rows

# ==========================================
# PATIENT PRIORITY SCORE
# ==========================================
def patient_score(patient, ambulance, grid):
    algo, path, _ = choose_best_path(
        grid,
        ambulance.position,
        patient.position,
        patient,
        context=f"{ambulance.id} to {patient.id}"
    )
    if not path: return -999, None, None
    
    metrics = analyze_path(path, grid)
    risk_pred = predict_path_risk(knn_model, path, grid)
    survival_pred = predict_survival(nb_model, patient, metrics['time'])
    sp = get_survival_probability(patient, metrics['time'])
    
    # Severity-based base score (ensures critical first)
    severity_base = {"critical": 1000, "moderate": 500, "minor": 100}
    severity = patient.severity if hasattr(patient, 'severity') else "moderate"
    base = severity_base.get(severity, 500)
    
    # Secondary score for tie-breaking
    secondary = patient.incident_time * 3 - metrics['cost']*0.5 - metrics['risk']*2 - (1-survival_pred)*50
    
    total = base + secondary
    
    print(f"  {patient.id} ({severity.upper()}): Algo={algo} | Risk={'HIGH' if risk_pred else 'LOW'} | Survival={sp*100:.0f}% | Score={total:.1f}")
    
    # Explicit trade-off justification
    if severity == "critical":
        print(f"     🎯 DECISION: PRIORITIZE SPEED - Critical condition, time-critical")
    elif severity == "moderate":
        print(f"     ⚖️ DECISION: BALANCED - Moderate condition, balance speed/safety")
    else:
        print(f"     🛡️ DECISION: PRIORITIZE SAFETY - Minor condition, safety first")
    
    return total, algo, path

# ==========================================
# ASSIGN PATIENTS (CRITICAL FIRST - GUARANTEED)
# ==========================================
def assign_patients(ambulances, patients, grid):
    # SEPARATE by severity
    criticals = [p for p in patients if not p.rescued and not p.assigned and p.severity == "critical"]
    moderates = [p for p in patients if not p.rescued and not p.assigned and p.severity == "moderate"]
    minors = [p for p in patients if not p.rescued and not p.assigned and p.severity == "minor"]
    
    # FORCE ORDER: Critical FIRST, then moderate, then minor
    unassigned = criticals + moderates + minors
    
    if unassigned:
        print(f"\n📋 PRIORITY QUEUE (Critical First):")
        for i, p in enumerate(unassigned):
            e = "🔴" if p.severity=="critical" else "🟠" if p.severity=="moderate" else "🟢"
            print(f"   {i+1}. {e} {p.id} ({p.severity.upper()}) at {p.position}")
    
    for ambulance in ambulances:
        if not ambulance.available:
            continue
        
        # ONLY assign critical if any available (HARD RULE)
        available_critical = [p for p in criticals if not p.assigned]
        available_moderate = [p for p in moderates if not p.assigned]
        available_minor = [p for p in minors if not p.assigned]
        
        if available_critical:
            candidates = available_critical
            print(f"\n🔴 {ambulance.id}: ONLY considering CRITICAL patients")
        elif available_moderate:
            candidates = available_moderate
            print(f"\n🟠 {ambulance.id}: Considering MODERATE patients (no criticals)")
        elif available_minor:
            candidates = available_minor
            print(f"\n🟢 {ambulance.id}: Considering MINOR patients (only remaining)")
        else:
            continue
        
        best_patient = None
        best_score = -999999
        best_path = None
        best_algo = None
        
        for patient in candidates:
            score, algo, path = patient_score(patient, ambulance, grid)
            if score > best_score:
                best_score = score
                best_patient = patient
                best_path = path
                best_algo = algo
        
        if best_patient:
            best_patient.assigned = True
            ambulance.target = best_patient
            ambulance.path = best_path
            ambulance.algorithm = best_algo
            ambulance.available = False
            
            sev_emoji = "🔴" if best_patient.severity=="critical" else "🟠" if best_patient.severity=="moderate" else "🟢"
            print(f"   🚑 {ambulance.id} → {sev_emoji} {best_patient.id} ({best_patient.severity.upper()}) | 🧠 {best_algo}")
            
            remaining_crit = [p.id for p in patients if not p.rescued and not p.assigned and p.severity=="critical"]
            if remaining_crit:
                print(f"   ⚠️ CRITICAL STILL WAITING: {remaining_crit}")
