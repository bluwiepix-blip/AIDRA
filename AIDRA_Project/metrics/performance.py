def compute_metrics(paths, grid, bfs_paths):
    victims_saved = sum(1 for p in paths if p is not None)

    # ✅ Avg time (ignore None)
    valid_paths = [p for p in paths if p]
    avg_time = sum(len(p) for p in valid_paths) / len(valid_paths) if valid_paths else 0

    # ✅ Risk exposure
    risk_exposure = 0
    for path in valid_paths:
        for x, y in path:
            if grid[x][y] == 'R':
                risk_exposure += 1

    # ✅ Optimality ratio (FIXED)
    ratios = []
    for p, bfs_p in zip(paths, bfs_paths):
        if p and bfs_p and len(bfs_p) > 0:
            ratios.append(len(p) / len(bfs_p))

    optimality_ratio = sum(ratios) / len(ratios) if ratios else 1

    # ✅ Resource utilization
    resource_utilization = victims_saved / len(paths) if paths else 0

    return {
        "victims_saved": victims_saved,
        "avg_time": round(avg_time, 2),
        "risk_exposure": risk_exposure,
        "optimality_ratio": round(optimality_ratio, 2),
        "resource_utilization": round(resource_utilization, 2)
    }
def calculate_all_kpis(patients, ambulances, grid, all_paths, bfs_paths):
    """Calculate all required KPIs"""
    
    # Victims saved
    victims_saved = sum(1 for p in patients if p.in_hospital)
    
    # Average rescue time
    rescue_times = [p.rescue_time for p in patients if p.rescue_time]
    avg_time = sum(rescue_times) / len(rescue_times) if rescue_times else 0
    
    # Path optimality ratio
    optimality_ratios = []
    for path, bfs_path in zip(all_paths, bfs_paths):
        if path and bfs_path:
            optimality_ratios.append(len(path) / len(bfs_path))
    optimality_ratio = sum(optimality_ratios) / len(optimality_ratios) if optimality_ratios else 0
    
    # Risk exposure
    risk_exposure = 0
    for path in all_paths:
        if path:
            risk_exposure += sum(1 for x, y in path if grid[x][y] == 'R')
    
    # Resource utilization
    total_ambulances = len(ambulances)
    used_ambulances = sum(1 for a in ambulances if not a.available)
    resource_utilization = used_ambulances / total_ambulances if total_ambulances > 0 else 0
    
    # Medical kit usage
    kits_used = sum(1 for p in patients if p.in_hospital)
    
    # Survival estimates using ML
    survival_estimates = {}
    for p in patients:
        # Simple survival probability based on severity and rescue time
        if p.severity == "critical":
            survival_prob = max(0.3, 1.0 - (p.rescue_time or 20) * 0.05)
        elif p.severity == "moderate":
            survival_prob = max(0.6, 1.0 - (p.rescue_time or 15) * 0.03)
        else:
            survival_prob = max(0.8, 1.0 - (p.rescue_time or 10) * 0.02)
        survival_estimates[p.id] = survival_prob
    
    kpis = {
        "victims_saved": victims_saved,
        "avg_rescue_time": round(avg_time, 2),
        "optimality_ratio": round(optimality_ratio, 2),
        "risk_exposure": risk_exposure,
        "resource_utilization": round(resource_utilization, 2),
        "kits_used": kits_used,
        "survival_estimates": survival_estimates
    }
    
    # Print KPI report
    print("\n" + "="*50)
    print("📊 KEY PERFORMANCE INDICATORS")
    print("="*50)
    print(f"✅ Victims Saved: {victims_saved}/{len(patients)}")
    print(f"⏱️ Average Rescue Time: {kpis['avg_rescue_time']}")
    print(f"📏 Path Optimality Ratio: {kpis['optimality_ratio']}")
    print(f"⚠️ Risk Exposure Score: {risk_exposure}")
    print(f"🚑 Resource Utilization: {kpis['resource_utilization']*100}%")
    print(f"💊 Medical Kits Used: {kits_used}/10")
    print(f"\n📈 Survival Estimates:")
    for pid, prob in survival_estimates.items():
        print(f"  {pid}: {prob*100:.0f}% survival probability")
    
    return kpis