import copy
from validator_collection import checkers, validators
from streamlit_tags import st_tags

import streamlit as st

from datetime import datetime

import json

from resume_builder.frontend.strings import date_to_string, internal_to_external


class Deletable:
    def __init__(self, to_delete):
        self.to_delete = to_delete
    
    def __enter__(self):
        self.delete_ledger = []
    
    def delete(self, i):
        del self.to_delete[i]
        st.rerun()
    
    def __exit__(self, _, _1, _2):
        pass


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
    
    return postprocess_partial_form(resume_data)


def main():
    st.title("Let's build a resume.")

    if "page" not in st.session_state:
        st.session_state.page = 1

    if "user_info" not in st.session_state:
        st.session_state.user_info = {
            "firstname": "",
            "lastname": "",
            "phone": "",
            "email": "",
            "linkedin": "",
            "profile": "",
            "domains": []
        }
    
    if "education_marked_for_deletion" not in st.session_state:
        st.session_state.education_marked_for_deletion = []

    if "education" not in st.session_state:
        st.session_state.education = []

    if "sections" not in st.session_state:
        st.session_state.sections = dict()

    if st.session_state.page == 1:
        st.header("Personal Information", divider="grey")

        st.session_state.user_info["firstname"] = st.text_input(
            internal_to_external("firstname"), 
            key="firstname",
            value=st.session_state.user_info["firstname"]
        )
        st.session_state.user_info["lastname"] = st.text_input(
            internal_to_external("lastname"), 
            key="lastname",
            value=st.session_state.user_info["lastname"]
        )
        st.session_state.user_info["phone"] = st.text_input(
            internal_to_external("phone"), 
            key="phone",
            value=st.session_state.user_info["phone"]
        )
        st.session_state.user_info["email"] = st.text_input(
            internal_to_external("email"), 
            key="email",
            value=st.session_state.user_info["email"]
        )
        st.session_state.user_info["linkedin"] = st.text_input(
            internal_to_external("linkedin"), 
            key="linkedin",
            value=st.session_state.user_info["linkedin"]
        )
        st.session_state.user_info["profile"] = st.text_input(
            internal_to_external("profile"), 
            key="profile",
            value=st.session_state.user_info["profile"]
        )
        st.session_state.user_info["domains"] = st_tags(
            label="What areas your areas of focus/interest? Examples include Software Engineering, AI/ML Research, etc.",
            key="domains",
            value=st.session_state.user_info["domains"]
        )

        st.header("Education Information", divider="grey")

        if st.button("Add Education"):
            st.session_state.education.append({
                "institution": "",
                "institution_location": "",
                "degree_name": "",
                "start": datetime.now(),
                "end": datetime.now(),
                "relevant_coursework": "",
            })

        with Deletable(st.session_state.education) as education_controller:
            for i in range(len(st.session_state.education)):
                with st.expander(f"**Education Item {i + 1}**", expanded=True):
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

                    if st.button("Delete", key=f"education_delete_{i}"):
                        st.session_state.education_marked_for_deletion.append(i)
                        # education_controller.delete(i)

        for index in sorted(st.session_state.education_marked_for_deletion, reverse=True):
            del st.session_state.education[index]
            st.session_state.education_marked_for_deletion = st.session_state.education_marked_for_deletion[:-1]
            st.rerun()
             
        st.header("Additional Information")

        is_swe = st.checkbox("I am applying for software engineering (or adjacent) roles")

        st.session_state.user_info.update({
            "education": st.session_state.education,
            "core_skill_label": "Languages" if is_swe else "Skills",
            "extra_skill_label": "Technologies" if is_swe else None,
            "domain_label": "Domains" if is_swe else "Areas of Focus"
        })

        st.divider()
        col1, col2 = st.columns([1, 9])

        with col1:
            if st.button("Save"):
                pass
        with col2:
            if st.button("Save & Continue", type="primary"):
                st.session_state.user_info.update({
                    "education": st.session_state.education,
                    "core_skill_label": "Languages" if is_swe else "Skills",
                    "extra_skill_label": "Technologies" if is_swe else None,
                    "domain_label": "Domains" if is_swe else "Areas of Focus"
                })
                st.session_state.page = 2
                st.rerun()

    elif st.session_state.page == 2:
        core_skills_label = st.session_state.user_info["core_skill_label"]
        extra_skills_label = st.session_state.user_info["extra_skill_label"]

        section_titles = {"Experience": "experience", "Extracurriculars": "extracurriculars", "Projects": "projects"}
        
        st.header("Add Sections")
        st.text(f"These are the parts of your resume where you add the details of all the past work. Please add as much information as possible.")
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
                    "description": [],
                    "still_working": False
                })
            
            for i in range(len(section["items"])):
                with st.expander(f"**{name.capitalize()} Item {i + 1}**", expanded=True):
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
                        disabled=st.checkbox(
                            "I am currently working here", 
                            key=f"working_{name}_{i}",
                            value=st.session_state.sections[name]["items"][i]["still_working"]
                        )
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

                    st.text(f"{name.capitalize()} Item {i + 1} Description")
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
        
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 8])

        with col1:
            if st.button("Back"):
                st.session_state.page = 1
                st.rerun()
        
        with col2:
            if st.button("Save"):
                pass
        
        with col3:
            if st.button("Submit 🚀", type="primary"):
                resume_data = {
                    "info": copy.deepcopy(st.session_state.user_info),
                    "sections": copy.deepcopy(list(st.session_state.get("sections", []).values()))
                }
                resume_data = validate_and_post_process(resume_data)
                st.json(resume_data)


if __name__ == "__main__":
    main()
