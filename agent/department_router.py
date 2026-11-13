
DEPARTMENT_MAPPING = {
    "Street Condition": "Roads and Public Works Department",
    "Missed Collection": "Sanitation and Waste Management Department",
    "Noise - Commercial": "Noise Control Department",
    "WATER LEAK": "Water Supply Department",
    "Street Light Condition": "Electrical Maintenance Department",
    "Illegal Parking": "Traffic Enforcement Department",
    "Encampment": "Homeless Outreach and Social Services",
    "Illegal Fireworks": "Police and Fire Enforcement Department"
}


def recommend_department(category):

    department = DEPARTMENT_MAPPING.get(category)

    if department is None:
        return "Department not identified. Human review required."

    return department


if __name__ == "__main__":
    category = "Street Condition"

    department = recommend_department(category)

    print("Complaint Category:", category)
    print("Recommended Department:", department)
