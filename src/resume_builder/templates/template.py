from abc import ABC, abstractmethod

import json
import os
import stat


class LatexTemplate(ABC):
    @abstractmethod
    def build_header(self, info):
        pass

    @abstractmethod
    def build_skills(self, info):
        pass

    @abstractmethod
    def build_education(self, info):
        pass

    @abstractmethod
    def build_experiences(self, experiences):
        pass
    
    @abstractmethod
    def build_extracurriculars(self, extracurriculars):
        pass

    @abstractmethod
    def build_projects(self, projects):
        pass

    @abstractmethod
    def build_experience_position(self, position):
        pass

    @abstractmethod
    def build_extracurricular_position(self, position):
        pass

    @abstractmethod
    def build_project_entry(self, project):
        pass
    
    @abstractmethod
    def _build_doc(self, preamble, resume):
        pass

    @property
    @abstractmethod
    def preamble(self):
        pass

    @property
    @abstractmethod
    def render_script(self):
        pass

    def __init__(self, resume_json_path, final_doc_path):
        self.resume_json_path = resume_json_path
        self.final_doc_path = final_doc_path

    def build_doc(self):
        with open(self.resume_json_path, "r") as resume, \
                open(self.final_doc_path, "w+") as final_doc, \
                open("artifacts/render.sh", "w+") as render_script:
            
            resume_json = json.loads(resume.read())
            doc = self._build_doc(self.preamble, resume_json)
            final_doc.write(doc)
            render_script.write(self.render_script)
        
        os.chmod(
            "artifacts/render.sh", 
            0o777
        )
