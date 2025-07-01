import json
import os
from datetime import datetime

def consolidate_donors():
    donors = []
    donors_dir = "donors"
    
    if not os.path.exists(donors_dir):
        return []
    
    for filename in os.listdir(donors_dir):
        if filename.endswith(".json"):
            with open(os.path.join(donors_dir, filename), "r") as f:
                try:
                    donor_data = json.load(f)
                    donors.append(donor_data)
                except json.JSONDecodeError:
                    continue
    
    # Sort by timestamp (newest first)
    donors.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Save consolidated file
    with open("donors/consolidated_donors.json", "w") as f:
        json.dump(donors, f, indent=2)
    
    return donors

if __name__ == "__main__":
    donors = consolidate_donors()
    print(f"Consolidated {len(donors)} donor records")