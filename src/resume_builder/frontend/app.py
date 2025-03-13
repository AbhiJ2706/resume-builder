import copy
from validator_collection import checkers, validators
from streamlit_tags import st_tags

import streamlit as st

from datetime import datetime

import json

from resume_builder.frontend.strings import date_to_string, internal_to_external


class ListInputController:
    def __init__(self, key, data_model):
        self.data_model = data_model
        self.key = key
        if self.key not in st.session_state:
            st.session_state[self.key] = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def add_item(self):
        st.session_state[self.key].append(copy.deepcopy(self.data_model))
    
    def delete_item(self, index):
        del st.session_state[self.key][index]
        st.rerun()


def validate_partial_form(partial_form, errors: list, key=None, idx=None, name=None):
    if isinstance(partial_form, dict):
        new_name = name if name is not None else partial_form.get("name")
        for (section, item) in partial_form.items():
            validate_partial_form(item, errors, key=section, idx=idx, name=new_name)
    elif isinstance(partial_form, list):
        for i, item in enumerate(partial_form):
            validate_partial_form(item, errors, idx=i, name=name)
    elif isinstance(partial_form, str):
        external_key = internal_to_external(key)
        if external_key is None:
            return
        errors.append(safe_assert(
            checkers.is_not_empty(partial_form) or external_key.endswith("(Optional)"), 
            (f"{external_key} required." if idx is None or name is None else f"{external_key} required for entry {idx + 1} in {name}.")
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
            "domains": [],
            "is_swe": False
        }

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

        with ListInputController("education", {
            "institution": "",
            "institution_location": "",
            "degree_name": "",
            "start": datetime.now(),
            "end": datetime.now(),
            "relevant_coursework": "",
        }) as education_controller:
            
            if st.button("Add Education"):
                education_controller.add_item()

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
                        education_controller.delete_item(i)

             
        st.header("Additional Information")

        is_swe = st.checkbox(
            "I am applying for software engineering (or adjacent) roles", 
            key="is_swe", 
            value=st.session_state.user_info["is_swe"]
        )

        st.session_state.user_info.update({
            "education": st.session_state.education,
            "core_skill_label": "Languages" if is_swe else "Skills",
            "extra_skill_label": "Technologies" if is_swe else None,
            "domain_label": "Domains" if is_swe else "Areas of Focus",
            "is_swe": is_swe
        })

        st.divider()
        col1, col2 = st.columns([1, 9])

        with col1:
            if st.button("Save", use_container_width=True):
                pass
        with col2:
            if st.button("Save & Continue", type="primary"):
                st.session_state.user_info.update({
                    "education": st.session_state.education,
                    "core_skill_label": "Languages" if is_swe else "Skills",
                    "extra_skill_label": "Technologies" if is_swe else None,
                    "domain_label": "Domains" if is_swe else "Areas of Focus",
                    "is_swe": is_swe
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
            with ListInputController(name, {
                "organization": "",
                "location": "",
                "position": "",
                "start": datetime.now(),
                "end": datetime.now(),
                "core_skills": [],
                "extra_skills": [],
                "description": [],
                "still_working": False
            }) as section_controller:
                
                if st.button("Add Item", key=f"add_item_{name}"):
                    section_controller.add_item()
                
                for i in range(len(st.session_state[name])):
                    with st.expander(f"**{name.capitalize()} Item {i + 1}**", expanded=True):
                        st.session_state[name][i]["organization"] = st.text_input(
                            internal_to_external("organization"), 
                            key=f"org_{name}_{i}",
                            value=st.session_state[name][i]["organization"]
                        )
                        st.session_state[name][i]["location"] = st.text_input(
                            internal_to_external("location"), 
                            key=f"loc_{name}_{i}",
                            value=st.session_state[name][i]["location"]
                        )
                        st.session_state[name][i]["position"] = st.text_input(
                            internal_to_external("position"), 
                            key=f"pos_{name}_{i}",
                            value=st.session_state[name][i]["position"]
                        )
                        st.session_state[name][i]["start"] = st.date_input(
                            internal_to_external("start"), 
                            key=f"start_{name}_{i}",
                            value=st.session_state[name][i]["start"]
                        )
                        st.session_state[name][i]["end"] = st.date_input(
                            internal_to_external("end"), 
                            key=f"end_{name}_{i}",
                            value=st.session_state[name][i]["end"],
                            disabled=st.checkbox(
                                "I am currently working here", 
                                key=f"working_{name}_{i}",
                                value=st.session_state[name][i]["still_working"]
                            )
                        )
                        st.session_state[name][i]["core_skills"] = st_tags(
                            label=internal_to_external("core_skills", fmt=core_skills_label), 
                            key=f"core_{name}_{i}",
                            value=st.session_state[name][i]["core_skills"]
                        )

                        if extra_skills_label is not None:
                            st.session_state[name][i]["extra_skills"] = st_tags(
                                label=internal_to_external("extra_skills", fmt=extra_skills_label), 
                                key=f"extra_{name}_{i}",
                                value=st.session_state[name][i]["extra_skills"]
                            )

                        st.text(f"{name.capitalize()} Item {i + 1} Description")

                        with ListInputController(f"{name}_{i}_description", {
                            "summary": "",
                            "required_skills": [],
                            "group": 0
                        }) as description_controller:
                            st.session_state[f"{name}_{i}_description"] = st.session_state[name][i]["description"]
                            if st.button("Add Point", key=f"add_item_{name}_{i}"):
                                description_controller.add_item()

                            for j in range(len(st.session_state[f"{name}_{i}_description"])):
                                col1, col2 = st.columns([0.9, 0.1], vertical_alignment="bottom")
                                with col1:
                                    st.session_state[f"{name}_{i}_description"][j]["summary"] = st.text_input(
                                        f"Point {j + 1}", 
                                        key=f"sum_{name}_{i}_{j}",
                                        value=st.session_state[f"{name}_{i}_description"][j]["summary"]
                                    )
                                with col2:
                                    if st.button("", icon=":material/delete:", key=f"{name}_{i}_{j}_description_delete"):
                                        description_controller.delete_item(j)
                        
                        st.session_state[name][i]["description"] = copy.deepcopy(st.session_state[f"{name}_{i}_description"])
                        del st.session_state[f"{name}_{i}_description"]

                        st.divider()
                        if st.button("Delete", key=f"{name}_{i}_delete"):
                            section_controller.delete_item(i)
                            
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 8])

        with col1:
            if st.button("Back", use_container_width=True):
                st.session_state.page = 1
                st.rerun()
        
        with col2:
            if st.button("Save", use_container_width=True):
                pass
        
        with col3:
            if st.button("Submit 🚀", type="primary"):
                resume_data = {
                    "info": copy.deepcopy(st.session_state.user_info),
                    "sections": copy.deepcopy(list(st.session_state.get("sections", []).values()))
                }
                for section in resume_data["sections"]:
                    section["items"] = st.session_state[section["name"]]
                resume_data = validate_and_post_process(resume_data)
                st.json(resume_data)


if __name__ == "__main__":
    main()
