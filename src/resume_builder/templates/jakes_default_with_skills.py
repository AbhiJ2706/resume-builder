from textwrap import dedent as td

from resume_builder.templates.template import LatexTemplate


class JakesDefaultWithSkills(LatexTemplate):
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
        core_skills = self.truncate(info['core_skills'], fmt=lambda x: ', '.join(x) + '.')
        extra_skills = self.truncate(info['extra_skills'], fmt=lambda x: ', '.join(x) + '.')
        domains = self.truncate(info['domains'], fmt=lambda x: ', '.join(x) + '.')
        return td(
            fr"""
            \begin{{itemize}}[leftmargin=0.15in, label={{}}]
                \small{{\item{{
                    \textbf{{{info['core_skill_label']}}}{{: {', '.join(core_skills) + '.'}}} \\
                    \textbf{{{info['extra_skill_label']}}}{{: {', '.join(extra_skills) + '.'}}} \\
                    \textbf{{{info['domain_label']}}}{{: {', '.join(domains) + '.'}}} \\
                }}}}
            \end{{itemize}}
            """
        )

    def _build_education(self, info):
        degree_finished = " (Expected)" if not info['education']['completed'] else ""
        relevant_coursework = td(fr"""\
                    \resumeItemListStart
                        \resumeItem{{Relevant Coursework: {info['education']['relevant_coursework']}.}}
                    \resumeItemListEnd
                    """
        ).replace("%", "\\%").replace("$", "\\$") if info['education']['relevant_coursework'] != "" else ""
        return td(
            fr"""
            \section{{Education}}
                \resumeSubHeadingListStart
                    \resumeSubheading
                    {{{info['education']['institution']}}}{{{info['education']['institution_location']}}}
                    {{{info['education']['degree_name']}}}{{{self.resolve_date(info['education']['start'], info['education']['end'])}{degree_finished}}}
                    {relevant_coursework}
                \resumeSubHeadingListEnd
            """
        )
    
    def _build_experience_position(self, position):
        experience = td(
            fr"""
                    \resumeSubheading
                        {{{position['organization']} -- {position['location']}}}{{{self.resolve_date(position['start'], position['end'])}}}
                        {{{position['position']}}}{{{', '.join(position['skills'])}}}
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
    
    def _build_minor_position(self, position):
        extracurricular = td(
            fr"""
                    \resumeSubheading
                        {{{position['organization']}}}{{{self.resolve_date(position['start'], position['end'])}}}
                        {{{position['location']}}}{{{', '.join(position['skills'])}}}
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

    def _build_minor_section(self, extracurricular_json):
        extracurricular = td(
            r"""
            \section{Extracurriculars}
                \resumeSubHeadingListStart
            """
        )

        for exp in extracurricular_json:
            extracurricular += self._build_minor_position(exp)
        
        extracurricular += td(
            r"""
                    \resumeSubHeadingListEnd
            """
        )
        
        return extracurricular
    
    @property
    def font_name(self):
        return "Computer Modern"

    @property
    def font_path(self):
        return "fonts/Computer Modern/cmunrm.ttf"
    
    @property
    def font_size(self):
        return 9.5
    
    @property
    def margin(self):
        return 1

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

    def _build_doc(self, resume):
        doc = self.preamble

        doc += self.build_header(resume["info"])
        doc += self.build_skills({
            "core_skills": resume["core_skills"],
            "extra_skills": resume["extra_skills"],
            **resume["info"]
        })
        doc += self.build_experiences(resume["experience"])
        for key in self.get_minor_keys(resume):
            doc += self.build_minor_section(resume[key])
        doc += self.build_education(resume["info"])

        doc += r"\end{document}"

        return doc
