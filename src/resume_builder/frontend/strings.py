import datetime


def date_to_string(date: datetime.date):
    return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ][date.month - 1] + f" {str(date.year)}"


def internal_to_external(key, fmt=None):
    field_names = {
        "firstname": "First Name",
        "lastname": "Last Name",
        "phone": "Phone Number",
        "email": "Email Address",
        "linkedin": "LinkedIn Profile",
        "profile": "Website/Portfolio/GitHub (Optional)",
        "domains": "Areas of Focus",
        "organization": "Organization",
        "location": "Location",
        "position": "Job Title",
        "start": "Start Date",
        "end": "End Date",
        "core_skills": f"{fmt} used",
        "extra_skills": f"{fmt} used",
        "description": "Resume Points"
    }

    return field_names.get(key)
