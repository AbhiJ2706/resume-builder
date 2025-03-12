from validator_collection import checkers, validators
from streamlit_tags import st_tags

import streamlit as st

from datetime import datetime

import json

from resume_builder.frontend.strings import date_to_string, internal_to_external


def validate_partial_form(partial_form, errors: list, key=None):
    if isinstance(partial_form, dict):
        for (section, item) in partial_form.items():
            validate_partial_form(item, errors, key=section)
    elif isinstance(partial_form, list):
        for item in partial_form:
            validate_partial_form(item, errors)
    elif isinstance(partial_form, str):
        external_key = internal_to_external(key)
        if external_key is None:
            return
        errors.append(safe_assert(
            checkers.is_not_empty(partial_form) or external_key.endswith("(Optional)"), f"{external_key} required."
        ))


def postprocess_partial_form(partial_form):
    if isinstance(partial_form, dict):
        return {section: postprocess_partial_form(item) for (section, item) in partial_form.items()}
    elif isinstance(partial_form, list):
        return [postprocess_partial_form(item) for item in partial_form]
    elif isinstance(partial_form, datetime):
        return date_to_string(partial_form)
    return partial_form


def safe_assert(condition, error_message):
    try:
        assert condition
    except AssertionError:
        return error_message


def validate_and_post_process(resume_data: dict):
    errors = []

    errors.append(
        safe_assert(
            (checkers.is_email(resume_data["info"]["email"]) and checkers.is_not_empty(resume_data["info"]["email"])) or
            not checkers.is_not_empty(resume_data["info"]["email"]), "Email is not valid.")
    )
    errors.append(
        safe_assert(
            (checkers.is_url(resume_data["info"]["linkedin"]) and checkers.is_not_empty(resume_data["info"]["linkedin"])) or
            not checkers.is_not_empty(resume_data["info"]["linkedin"]), "LinkedIn link is not valid.")
    )
    errors.append(
        safe_assert(
            (checkers.is_url(resume_data["info"]["profile"], allow_empty=True) and checkers.is_not_empty(resume_data["info"]["profile"]) or
            not checkers.is_not_empty(resume_data["info"]["profile"])), "Profile link is not valid.")
    )
    validate_partial_form(resume_data, errors)

    errors = list(filter(lambda x: x is not None, errors))

    if errors:
        st.warning(
            f"Invalid input detected. Errors found:\n {'\n'.join(list(map(lambda x: "- " + x, errors)))}"
        )
        return resume_data
    
    return postprocess_partial_form(resume_data)


def user_info_page():
    st.title("Dynamic Resume JSON Generator")
    
    st.header("Personal Information", divider="grey")

    st.session_state.user_info = {
        "firstname": "",
        "lastname": "",
        "phone": "",
        "email": "",
        "linkedin": "",
        "profile": "",
        "domains": []
    }

    st.session_state.user_info["firstname"] = st.text_input(internal_to_external("firstname"))
    st.session_state.user_info["lastname"] = st.text_input(internal_to_external("lastname"))
    st.session_state.user_info["phone"] = st.text_input(internal_to_external("phone"))
    st.session_state.user_info["email"] = st.text_input(internal_to_external("email"))
    st.session_state.user_info["linkedin"] = st.text_input(internal_to_external("linkedin"))
    st.session_state.user_info["profile"] = st.text_input(internal_to_external("profile"))
    st.session_state.user_info["domains"] = st_tags(label="What areas your areas of focus/interest? Examples include Software Engineering, AI/ML Research, etc.")

    st.header("Education Information", divider="grey")

    if 'education' not in st.session_state:
        st.session_state.education = []

    if st.button("Add Education"):
        st.session_state.education.append({
            "institution": "",
            "institution_location": "",
            "degree_name": "",
            "start": datetime.now(),
            "end": datetime.now(),
            "relevant_coursework": "",
        })

    for i in range(len(st.session_state.education)):
        st.subheader(f"Education {i + 1}")
        st.session_state.education[i]["institution"] = st.text_input(
            "Institution name", 
            key=f"institution_{i}", 
            value=st.session_state.education[i]["institution"]
        )
        st.session_state.education[i]["institution_location"] = st.text_input(
            "Institution location", 
            key=f"location_{i}",
            value=st.session_state.education[i]["institution_location"]
        )
        st.session_state.education[i]["degree_name"] = st.text_input(
            "Degree obtained/obtaining", 
            key=f"obtained_{i}",
            value=st.session_state.education[i]["degree_name"]
        )
        st.session_state.education[i]["start"] = st.date_input(
            "Start", 
            format="DD/MM/YYYY", 
            key=f"start_{i}",
            value=st.session_state.education[i]["start"]
        )
        st.session_state.education[i]["end"] = st.date_input(
            "End (Actual or Expected)", 
            format="DD/MM/YYYY", 
            key=f"end_{i}",
            value=st.session_state.education[i]["end"]
        )
        st.session_state.education[i]["relevant_coursework"] = st.text_input(
            "Relevant coursework", 
            key=f"coursework_{i}",
            value=st.session_state.education[i]["relevant_coursework"]
        )
        st.session_state.education[i]["completed"] = st.session_state.education[i]["end"] <= datetime.now().date()
        
    st.header("Additional Information")

    is_swe = st.checkbox("I am applying for software engineering (or adjacent) roles")

    st.session_state.user_info.update({
        "education": st.session_state.education,
        "core_skill_label": "Languages" if is_swe else "Skills",
        "extra_skill_label": "Technologies" if is_swe else None,
        "domain_label": "Domains" if is_swe else "Areas of Focus"
    })


def sections_page():
    core_skills_label = st.session_state.user_info["core_skill_label"]
    extra_skills_label = st.session_state.user_info["extra_skill_label"]

    section_titles = {"Experience": "experience", "Extracurriculars": "extracurriculars", "Projects": "projects"}
    
    st.header("Add Sections")
    section_type = st.selectbox("Select Section Type", list(section_titles.keys()))

    if "sections" not in st.session_state:
        st.session_state.sections = dict()
    
    if st.button("Add Section"):
        st.session_state.sections[section_titles[section_type]] = {
            "name": section_titles[section_type], 
            "items": [],
            "include": False
        }
    
    for name, section in st.session_state.sections.items():
        st.subheader(f"{section['name'].capitalize()}", divider="grey")
        
        st.session_state.sections[name]["include"] = st.checkbox(
            "Include all entries in this section on my resume", 
            key=f"include_{name}",
            value=st.session_state.sections[name]["include"]
        )
        
        if st.button("Add Item", key=f"add_item_{name}"):
            section["items"].append({
                "organization": "",
                "location": "",
                "position": "",
                "start": datetime.now(),
                "end": datetime.now(),
                "core_skills": [],
                "extra_skills": [],
                "description": []
            })
        
        for i in range(len(section["items"])):
            st.subheader(f"{section['name'].capitalize()} Item {i + 1}")

            st.session_state.sections[name]["items"][i]["organization"] = st.text_input(
                internal_to_external("organization"), 
                key=f"org_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["organization"]
            )
            st.session_state.sections[name]["items"][i]["location"] = st.text_input(
                internal_to_external("location"), 
                key=f"loc_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["location"]
            )
            st.session_state.sections[name]["items"][i]["position"] = st.text_input(
                internal_to_external("position"), 
                key=f"pos_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["position"]
            )
            st.session_state.sections[name]["items"][i]["start"] = st.date_input(
                internal_to_external("start"), 
                key=f"start_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["start"]
            )
            st.session_state.sections[name]["items"][i]["end"] = st.date_input(
                internal_to_external("end"), 
                key=f"end_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["end"],
                disabled=st.checkbox("I am currently working here")
            )
            st.session_state.sections[name]["items"][i]["core_skills"] = st_tags(
                label=internal_to_external("core_skills", fmt=core_skills_label), 
                key=f"core_{name}_{i}",
                value=st.session_state.sections[name]["items"][i]["core_skills"]
            )

            if extra_skills_label is not None:
                st.session_state.sections[name]["items"][i]["extra_skills"] = st_tags(
                    label=internal_to_external("extra_skills", fmt=extra_skills_label), 
                    key=f"extra_{name}_{i}",
                    value=st.session_state.sections[name]["items"][i]["extra_skills"]
                )

            if st.button("Add Point", key=f"add_item_{name}_{i}"):
                st.session_state.sections[name]["items"][i]["description"].append({
                    "summary": "",
                    "group": 0
                })

            for j in range(len(st.session_state.sections[name]["items"][i]["description"])):
                col1, col2 = st.columns([0.01, 0.99])
                with col1:
                    st.markdown(f"•", unsafe_allow_html=True)
                with col2:
                    st.session_state.sections[name]["items"][i]["description"][j]["summary"] = st.text_input(
                        f"Point {j + 1}", 
                        key=f"sum_{name}_{i}_{j}",
                        value=st.session_state.sections[name]["items"][i]["description"][j]["summary"]
                    )
    
    if st.button("Generate JSON"):
        resume_data = {
            "info": st.session_state.user_info,
            "sections": list(st.session_state.get("sections", []).values())
        }

        resume_data = validate_and_post_process(resume_data)

        st.json(resume_data)
        
        json_str = json.dumps(resume_data, indent=4)
        st.download_button("Download JSON", json_str, "resume.json", "application/json")


def main():
    page = st.sidebar.radio("Navigate", ["User Info", "Sections"])
    if page == "User Info":
        user_info_page()
    else:
        sections_page()


if __name__ == "__main__":
    main()
