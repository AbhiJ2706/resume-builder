from textwrap import dedent as td

from resume_builder.templates.template import LatexTemplate


class Figtree(LatexTemplate):
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
                \textbf{{\Huge \scshape \blue{{{name}}}}} \\ \vspace{{1pt}}
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
    
    def _build_education_entry(self, info):
        degree_finished = " (Expected)" if not info['completed'] else ""
        relevant_coursework = td(fr"""\
                    \resumeItemListStart
                        \resumeItem{{Relevant Coursework: {info['relevant_coursework']}.}}
                    \resumeItemListEnd
                    """
        ).replace("%", "\\%").replace("$", "\\$") if info['relevant_coursework'] != "" else ""

        return td(
            fr"""
                \resumeSubheading
                {{{info['institution']}}}{{{info['institution_location']}}}
                {{{info['degree_name']}}}{{{self.resolve_date(info['start'], info['end'])}{degree_finished}}}
                {relevant_coursework}
                \vspace{{3pt}}
            """
        )

    def _build_education_section(self, info):
        text = td(
            fr"""
            \section{{\blue{{Education}}}}
                \resumeSubHeadingListStart
            """
        )

        for entry in info['education']:
            text += self._build_education_entry(entry)

        text += td(
            fr"""
                \resumeSubHeadingListEnd
            """
        )

        return text
    
    def _build_major_position(self, position):
        text = td(
            fr"""
                    \resumeSubheading
                        {{{position['organization']} -- {position['location']}}}{{{self.resolve_date(position['start'], position['end'])}}}
                        {{{position['position']}}}{{{', '.join(position['skills'])}}}
            """
        )

        text += td(
            r"""
                        \resumeItemListStart
            """
        )

        for point in position["description"]:
            text += td(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        text += td(
            r"""
                        \resumeItemListEnd
            """
        )

        return text

    def _build_major_section(self, name, info):
        text = td(
            fr"""
            \section{{\blue{{{name.title()}}}}}
                \resumeSubHeadingListStart
            """
        )

        for exp in info:
            text += self._build_major_position(exp)
            
        text += td(
            r"""
                    \resumeSubHeadingListEnd
            """
        )
        
        return text
    
    def _build_minor_position(self, position):
        text = td(
            fr"""
                    \resumeSubheading
                        {{{position['organization']}}}{{{self.resolve_date(position['start'], position['end'])}}}
                        {{{position['location']}}}{{{', '.join(position['skills'])}}}
            """
        )

        text += td(
            r"""
                        \resumeItemListStart
            """
        )

        for point in position["description"]:
            text += td(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        text += td(
            r"""
                        \resumeItemListEnd
            """
        )

        return text

    def _build_minor_section(self, name, info):
        text = td(
            fr"""
            \section{{\blue{{{name.title()}}}}}
                \resumeSubHeadingListStart
            """
        )

        for exp in info:
            text += self._build_minor_position(exp)
        
        text += td(
            r"""
                    \resumeSubHeadingListEnd
            """
        )
        
        return text
    
    @property
    def font_name(self):
        return "Figtree"

    @property
    def font_path(self):
        return "fonts/Figtree/static/Figtree-Light.ttf"
    
    @property
    def font_size(self):
        return 10.5
    
    @property
    def margin(self):
        return 0.875

    @property
    def preamble(self):
        with open("latex/xelatex_preamble.tex", "r") as f:
            return f.read()
    
    @property
    def render_script(self):
        return td(
            """\
            #!/bin/sh
            cp -r ../fonts/Figtree . && xelatex final_doc.tex
            """
        )

    def _build_doc(self, resume):
        doc = self.preamble

        doc += r"\begin{document}"

        doc += self.build_header(resume["info"])
        doc += self.build_skills({
            "core_skills": resume["core_skills"],
            "extra_skills": resume["extra_skills"],
            **resume["info"]
        })
        for section in resume["sections"]:
            if section["name"] in self.get_major_sections():
                doc += self.build_major_section(section["name"], section["items"])
            else:
                doc += self.build_minor_section(section["name"], section["items"])
        doc += self.build_education_section(resume["info"])

        doc += r"\end{document}"

        return doc
