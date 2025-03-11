from importlib import import_module
import sys

from resume_builder.backend.templates.template import LatexTemplate


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


if __name__ == "__main__":
    template = sys.argv[1]
    builder_class = getattr(import_module("templates." + template), to_camel_case(template))

    builder: LatexTemplate = builder_class("artifacts/resume_result.json", "artifacts/final_doc.tex")
    builder.build_doc()
