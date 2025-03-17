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
    
    def build_education_section(self, info):
        return self._build_education_section(info)
    
    def build_major_section(self, name, info):
        return self._build_major_section(name, info)
    
    def build_minor_section(self, name, info):
        return self._build_minor_section(name, info)
    
    def get_major_sections(self):
        return ["experience"]
    
    def resolve_date(self, start, end):
        return start if start == end else f"{start} - {end}"


    @abstractmethod
    def _build_header(self, info):
        pass

    @abstractmethod
    def _build_skills(self, info):
        pass

    @abstractmethod
    def _build_education_section(self, info):
        pass

    @abstractmethod
    def _build_education_entry(self, info):
        pass

    @abstractmethod
    def _build_major_section(self, name, info):
        pass
    
    @abstractmethod
    def _build_minor_section(self, name, info):
        pass

    @abstractmethod
    def _build_major_position(self, position):
        pass

    @abstractmethod
    def _build_minor_position(self, position):
        pass
    
    @abstractmethod
    def _build_doc(self, resume):
        pass

    @property
    @abstractmethod
    def font_name(self):
        pass

    @property
    @abstractmethod
    def font_path(self):
        pass

    @property
    @abstractmethod
    def font_size(self):
        pass

    @property
    @abstractmethod
    def margin(self):
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
            doc = self._build_doc(resume_json)
            final_doc.write(doc)
            render_script.write(self.render_script)
        
        os.chmod(
            "artifacts/render.sh", 
            0o777
        )

    def truncate(self, l, fmt=lambda x: ' '.join(x)):
        while self.get_text_width(fmt(l)) > 8.5:
            del l[-1]
        return l
    
    def get_text_width(self, text):
        pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        return self.__points_to_inches(pdfmetrics.stringWidth(text, self.font_name, self.font_size)) + self.margin

    def __points_to_inches(self, points):
        return points / 72.0

