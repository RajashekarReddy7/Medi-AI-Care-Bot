def map_triage_to_specialist(structured, triage_level):
    """
    Decide doctor type based on extracted symptoms and triage level
    """

    symptoms = structured.get("symptoms", [])
    symptoms_text = " ".join(symptoms).lower()

    if "chest pain" in symptoms_text or "heart" in symptoms_text:
        return "Cardiologist"

    if "skin" in symptoms_text or "rash" in symptoms_text:
        return "Dermatologist"

    if "fracture" in symptoms_text or "bone" in symptoms_text:
        return "Orthopedic"

    if "pregnancy" in symptoms_text:
        return "Gynecologist"

    if "child" in symptoms_text or "baby" in symptoms_text:
        return "Pediatrician"

    if triage_level == "Emergency":
        return "Emergency Hospital"

    return "General Physician"
