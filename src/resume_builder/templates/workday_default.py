import subprocess
from textwrap import dedent as td

from resume_builder.templates.template import LatexTemplate


class WorkdayDefault(LatexTemplate):
    def _build_header(self, info):
        name = f"{info['firstname']} {info['lastname']}"
        phone = info["phone"]
        email = info["email"]

        linkedin = info["linkedin"]
        if linkedin.startswith("https://"):
            linkedin_without_https = linkedin[8:]
        else:
            linkedin = "https://" + info["linkedin"]
            linkedin_without_https = info["linkedin"]

        profile = info["profile"]
        if profile.startswith("https://"):
            profile_without_https = profile[8:]
        else:
            profile = "https://" + info["profile"]
            profile_without_https = info["profile"]

        return td(
            fr"""
            \begin{{center}}
                \textbf{{\Huge \scshape {name}}} \\ \vspace{{1pt}}
                \small {phone} $|$ \href{{mailto:{email}}}{{\underline{{{email}}}}} $|$ 
                \href{{{linkedin}}}{{\underline{{{linkedin_without_https}}}}} $|$
                \href{{{profile}}}{{\underline{{{profile_without_https}}}}}
            \end{{center}}
            """
        )

    def _build_skills(self, info):
        return td(
            fr"""
            \begin{{itemize}}[leftmargin=0.15in, label={{}}]
                \small{{\item{{
                    \textbf{{Languages}}{{: {', '.join(info['languages']) + '.'}}} \\
                    \textbf{{Technologies}}{{: {', '.join(info['technologies']) + '.'}}} \\
                    \textbf{{Domains}}{{: {', '.join(info['domains']) + '.'}}} \\
                }}}}
            \end{{itemize}}
            """
        )

    def _build_education(self, info):
        return td(
            r"""
            \section{Education}
                \resumeSubHeadingListStart
                    \resumeSubheading
                    {University of Waterloo}{Waterloo, ON}
                    {Bachelor of Computer Science with AI Specialization (Honors, Co-op)}{Sep. 2020-- May 2025 (Expected)}
                \resumeSubHeadingListEnd
            """
        )
    
    def _build_experience_position(self, position):
        experience = td(
            fr"""
                    \resumeSubheading
                        {{{position['position']}}}{{{position['duration']}}}
                        {{{position['company']} | {position['location']}}}{{{', '.join(position['technologies'])}}}
            """
        )

        experience += td(
            r"""
                        \resumeItemListStart
            """
        )

        for point in position["description"]:
            experience += td(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        experience += td(
            r"""
                        \resumeItemListEnd
            """
        )

        return experience

    def _build_experiences(self, experience_json):
        experience = td(
            r"""
            \section{Experience}
                \resumeSubHeadingListStart
            """
        )

        for exp in experience_json:
            experience += self._build_experience_position(exp)
        
        experience += td(
            r"""
                    \resumeSubHeadingListEnd
            """
        )
        
        return experience
    
    def _build_extracurricular_position(self, position):
        extracurricular = td(
            fr"""
                    \resumeSubheading
                        {{{position['organization']}}}{{{position['duration']}}}
                        {{{position['location']}}}{{{', '.join(position['technologies'])}}}
            """
        )

        extracurricular += td(
            r"""
                        \resumeItemListStart
            """
        )

        for point in position["description"]:
            extracurricular += td(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        extracurricular += td(
            r"""
                        \resumeItemListEnd
            """
        )

        return extracurricular

    def _build_extracurriculars(self, extracurricular_json):
        extracurricular = td(
            r"""
            \section{Extracurriculars}
                \resumeSubHeadingListStart
            """
        )

        for exp in extracurricular_json:
            extracurricular += self._build_extracurricular_position(exp)
        
        extracurricular += td(
            r"""
                    \resumeSubHeadingListEnd
            """
        )
        
        return extracurricular
    
    def _build_projects(self, projects):
        return ""
    
    def _build_project_entry(self, project):
        return ""

    @property
    def preamble(self):
        with open("latex/preamble.tex", "r") as f:
            return f.read()
    
    @property
    def render_script(self):
        return td(
            """\
            #!/bin/sh
            pdflatex final_doc.tex
            """
        )

    def _build_doc(self, preamble, resume):
        doc = preamble

        doc += self.build_header(resume["info"])
        doc += self.build_skills({
            "languages": resume["languages"],
            "technologies": resume["frameworks"], 
            "domains": resume["info"]["domains"]
        })
        doc += self.build_experiences(resume["experience"])
        doc += self.build_extracurriculars(resume["extracurriculars"])
        doc += self.build_education(None)

        doc += r"\end{document}"

        return doc
