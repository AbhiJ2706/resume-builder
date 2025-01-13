import json
import textwrap


def build_header():
    return textwrap.dedent(
        r"""
        \begin{center}
            \textbf{\Huge \scshape Abhinav Jain} \\ \vspace{1pt}
            \small +1 343-558-2078 $|$ \href{mailto:a252jain@uwaterloo.ca}{\underline{a252jain@uwaterloo.ca}} $|$ 
            \href{linkedin.com/in/abhij2706}{\underline{linkedin.com/in/abhij2706}} $|$
            \href{https://github.com/AbhiJ2706}{\underline{https://github.com/AbhiJ2706}}
        \end{center}
        """
    )


def build_skills(languages, technologies):
    return textwrap.dedent(
        fr"""
        \begin{{itemize}}[leftmargin=0.15in, label={{}}]
            \small{{\item{{
                \textbf{{Languages}}{{: {', '.join(languages)}}} \\
                \textbf{{Technologies}}{{: {', '.join(technologies)}}} \\
                \textbf{{Domains}}{{: Software Engineering, ML Engineering, Data Engineering, Embedded Software, Test Automation, AI/ML Research}} \\
            }}}}
        \end{{itemize}}
        """
    )


def build_education():
    return textwrap.dedent(
        r"""
        \section{Education}
            \resumeSubHeadingListStart
                \resumeSubheading
                {University of Waterloo}{Waterloo, ON}
                {Bachelor of Computer Science with AI Specialization (Honors, Co-op)}{Sep. 2020-- May 2025 (Expected)}
            \resumeSubHeadingListEnd
        """
    )


def build_experience(experience_json):
    experience = textwrap.dedent(
        r"""
        \section{Experience}
            \resumeSubHeadingListStart
        """
    )

    for exp in experience_json:
        experience += textwrap.dedent(
            fr"""
                    \resumeSubheading
                        {{{exp['company'] + " | " + exp['location']}}}{{{exp['duration']}}}
                        {{{exp['position']}}}{{{', '.join(exp['technologies'])}}}
            """
        )

        experience += textwrap.dedent(
            r"""
                        \resumeItemListStart
            """
        )

        for point in exp["description"]:
            experience += textwrap.dedent(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        experience += textwrap.dedent(
            r"""
                        \resumeItemListEnd
            """
        )
    
    experience += textwrap.dedent(
        r"""
                \resumeSubHeadingListEnd
        """
    )
    
    return experience


def build_extracurriculars(extracurricular_json):
    extracurricular = textwrap.dedent(
        r"""
        \section{Extracurriculars}
            \resumeSubHeadingListStart
        """
    )

    for exp in extracurricular_json:
        extracurricular += textwrap.dedent(
            fr"""
                    \resumeSubheading
                        {{{exp['organization']}}}{{{exp['duration']}}}
                        {{{exp['location']}}}{{{', '.join(exp['technologies'])}}}
            """
        )

        extracurricular += textwrap.dedent(
            r"""
                        \resumeItemListStart
            """
        )

        for point in exp["description"]:
            extracurricular += textwrap.dedent(
                fr"""
                                \resumeItem{{{point}}}
                """.replace("%", "\\%").replace("$", "\\$")
            )
        
        extracurricular += textwrap.dedent(
            r"""
                        \resumeItemListEnd
            """
        )
    
    extracurricular += textwrap.dedent(
        r"""
                \resumeSubHeadingListEnd
        """
    )
    
    return extracurricular


def build_doc():
    with open("latex/preamble.tex", "r") as preamble, \
            open("artifacts/resume_result.json", "r") as resume, \
            open("artifacts/final_doc.tex", "w+") as final_doc:
        doc = preamble.read()
        resume_json = json.loads(resume.read())

        doc += build_header()

        doc += build_skills(resume_json["languages"], resume_json["frameworks"])

        doc += build_experience(resume_json["experience"])

        doc += build_extracurriculars(resume_json["extracurriculars"])

        doc += build_education()

        doc += r"\end{document}"

        final_doc.write(doc)
        

if __name__ == "__main__":
    build_doc()
