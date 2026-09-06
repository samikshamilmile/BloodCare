from datetime import date
def eligibility_reasons(donor):
    reasons = []
    if donor.age < 18 or donor.age > 65:
        reasons.append("Age must be between 18 and 65.")
    if donor.weight < 50:
        reasons.append("Weight must be at least 50 kg.")
    if donor.medical_restriction:
        reasons.append("Medical restriction is active.")
    if not donor.available:
        reasons.append("Donor is currently unavailable.")
    if donor.last_donation and (date.today() - donor.last_donation).days < 90:
        reasons.append("Minimum donation interval has not passed.")
    return reasons
