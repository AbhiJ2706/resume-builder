from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from abc import ABC, abstractmethod

import json
import os


class LatexTemplate(ABC):
    def build_header(self, info):
        return self._build_header(info)
    
    def build_skills(self, info):
        return self._build_skills(info)
    
    def build_education(self, info):
        return self._build_education(info)
    
    def build_experiences(self, experiences):
        return self._build_experiences(experiences)
    
    def build_extracurriculars(self, extracurriculars):
        return self._build_extracurriculars(extracurriculars)

    def build_projects(self, project):
        return self._build_projects(project)

    @abstractmethod
    def _build_header(self, info):
        pass

    @abstractmethod
    def _build_skills(self, info):
        pass

    @abstractmethod
    def _build_education(self, info):
        pass

    @abstractmethod
    def _build_experiences(self, experiences):
        pass
    
    @abstractmethod
    def _build_extracurriculars(self, extracurriculars):
        pass

    @abstractmethod
    def _build_projects(self, projects):
        pass

    @abstractmethod
    def _build_experience_position(self, position):
        pass

    @abstractmethod
    def _build_extracurricular_position(self, position):
        pass

    @abstractmethod
    def _build_project_entry(self, project):
        pass
    
    @abstractmethod
    def _build_doc(self, preamble, resume):
        pass

    # @property
    # @abstractmethod
    # def font_name(self):
    #     pass

    # @property
    # @abstractmethod
    # def font_path(self):
    #     pass

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
    
    def get_text_width(self, text):
        pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        return pdfmetrics.stringWidth(text, self.font_name, self.font_path)

    def points_to_inches(self, points):
        return points / 72.0

