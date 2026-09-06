from app.services.compatibility import compatible

def score_donor(donor, recipient_group, requested_city=None):
    if not donor.eligible() or not compatible(donor.blood_group, recipient_group):
        return 0
    score = 60
    if donor.blood_group == recipient_group:
        score += 20
    if requested_city and donor.city.lower() == requested_city.lower():
        score += 15
    if donor.last_donation is None:
        score += 5
    return min(score, 100)

def match_donors(donors, recipient_group, city=None):
    rows = []
    for donor in donors:
        score = score_donor(donor, recipient_group, city)
        if score:
            rows.append((donor, score))
    return sorted(rows, key=lambda x: x[1], reverse=True)
