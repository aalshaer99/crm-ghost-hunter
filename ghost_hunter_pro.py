import json
from datetime import datetime

class RevenueEngineer:
    def __init__(self, crm_seat_cost=150): # $150 per user/month avg
        self.crm_seat_cost = crm_seat_cost
        self.audit_results = []

    def calculate_decay_score(self, last_touch_days, title_change=False):
        """
        Calculates a 'Ghost Score'. 100 = Totally Dead, 0 = High Intent.
        """
        score = min(last_touch_days / 10, 80)
        if title_change:
            score -= 40  # A title change is a HUGE positive signal (Promotion)
        return max(score, 0)

    def run_audit(self, data):
        total_waste = 0
        for record in data:
            # Real-world logic: Days since last engagement
            last_date = datetime.strptime(record['last_contact'], "%Y-%m-%d")
            days_since = (datetime.now() - last_date).days
            
            # Genius Feature: Title Evolution check
            title_evolved = record['current_title'] != record['original_title']
            
            ghost_score = self.calculate_decay_score(days_since, title_evolved)
            
            # Calculate "Zombie Seat Cost" (Estimated waste of CRM resources)
            waste_contribution = 0
            if ghost_score > 70:
                waste_contribution = self.crm_seat_cost * 0.15 # 15% of seat value wasted
            
            total_waste += waste_contribution
            
            self.audit_results.append({
                "name": record['name'],
                "ghost_score": ghost_score,
                "is_promotion": title_evolved,
                "action": "PRIORITY: RE-ENGAGE" if title_evolved else "PURGE/ARCHIVE" if ghost_score > 75 else "NURTURE"
            })
        return total_waste

# --- THE SIMULATION ---
if __name__ == "__main__":
    # Realistic CRM Snapshot
    crm_data = [
        {"name": "Alice Chen", "last_contact": "2025-11-01", "original_title": "Director", "current_title": "VP of Ops"},
        {"name": "Mark Slobodan", "last_contact": "2023-04-12", "original_title": "Manager", "current_title": "Manager"},
        {"name": "Sarah Jenkins", "last_contact": "2024-08-30", "original_title": "Lead Eng", "current_title": "Director"}
    ]

    engineer = RevenueEngineer()
    waste_total = engineer.run_audit(crm_data)

    print(f"🚀 CRM REVENUE AUDIT COMPLETE")
    print(f"Estimated Monthly 'Data Tax' (Waste): ${waste_total:.2f}")
    print("-" * 30)
    for res in engineer.audit_results:
        status = "🔥" if res['is_promotion'] else "💀" if res['ghost_score'] > 70 else "⏳"
        print(f"{status} {res['name']}: Score {res['ghost_score']} -> {res['action']}")
