import json


def build_title(experience, index):
    with open("doc/job_header.json", "r") as job_title:
        job_header_json = json.loads(job_title.read())

        job_title_string = "{company} | {position} | {location} | {duration}\n".format(
            company=experience["company"],
            position=experience["position"],
            location=experience["location"],
            duration=experience["duration"],
        )

        job_domain_string = f"{experience['domain']}, "
        job_skills_string = ", ".join(experience['technologies']) + ".\n"

        job_title_json = job_header_json[0]
        job_summary_json = job_header_json[1]

        job_title_json["startIndex"] = index
        job_title_json["paragraph"]["elements"][0]["startIndex"] = index
        index += len(job_title_string)
        job_title_json["endIndex"] = index
        job_title_json["paragraph"]["elements"][0]["endIndex"] = index

        job_summary_json["startIndex"] = index
        job_summary_json["paragraph"]["elements"][0]["startIndex"] = index
        index += 8
        job_summary_json["paragraph"]["elements"][0]["endIndex"] = index

        job_summary_json["paragraph"]["elements"][1]["startIndex"] = index
        index += len(job_domain_string)
        job_summary_json["paragraph"]["elements"][1]["endIndex"] = index

        job_summary_json["paragraph"]["elements"][2]["startIndex"] = index
        index += 19
        job_summary_json["paragraph"]["elements"][2]["endIndex"] = index

        job_summary_json["paragraph"]["elements"][3]["startIndex"] = index
        index += len(job_skills_string)
        job_summary_json["paragraph"]["elements"][3]["endIndex"] = index
        job_summary_json["endIndex"] = index
        
        job_title_json["paragraph"]["elements"][0]["textRun"]["content"] = job_title_string
        job_summary_json["paragraph"]["elements"][1]["textRun"]["content"] = job_domain_string
        job_summary_json["paragraph"]["elements"][3]["textRun"]["content"] = job_skills_string

        return index, job_title_json, job_summary_json


def build_point(point_string, index):
    with open("doc/point.json", "r") as point:
        point_json = json.loads(point.read())

        point_string += "\n"

        point_json["startIndex"] = index
        point_json["paragraph"]["elements"][0]["startIndex"] = index
        index += len(point_string)
        point_json["endIndex"] = index
        point_json["paragraph"]["elements"][0]["endIndex"] = index

        point_json["paragraph"]["elements"][0]["textRun"]["content"] = point_string

        return index, point_json


def build_line(index, fontsize=5.5):
    with open("doc/line.json", "r") as line:
        line_json = json.loads(line.read())

        line_json["startIndex"] = index
        line_json["paragraph"]["elements"][0]["startIndex"] = index
        index += 1
        line_json["endIndex"] = index
        line_json["paragraph"]["elements"][0]["endIndex"] = index

        line_json["paragraph"]["elements"][0]["textRun"]["content"] = "\n"
        line_json["paragraph"]["elements"][0]["textRun"]["textStyle"]["fontSize"]["magnitude"] = fontsize

        return index, line_json
    

def build_extracurricular_banner(index):
    with open("doc/extracurricular_banner.json", "r") as extracurricular_banner:
        extracurricular_banner_json = json.loads(extracurricular_banner.read())

        extracurricular_title_json = extracurricular_banner_json[0]
        extracurricular_newline_json = extracurricular_banner_json[1]

        extracurricular_title_json["startIndex"] = index
        extracurricular_title_json["paragraph"]["elements"][0]["startIndex"] = index
        index += 17
        extracurricular_title_json["endIndex"] = index
        extracurricular_title_json["paragraph"]["elements"][0]["endIndex"] = index

        extracurricular_newline_json["startIndex"] = index
        extracurricular_newline_json["paragraph"]["elements"][0]["startIndex"] = index
        index += 1
        extracurricular_newline_json["endIndex"] = index
        extracurricular_newline_json["paragraph"]["elements"][0]["endIndex"] = index

        return index, extracurricular_title_json, extracurricular_newline_json


def build_extracurricular_title(extracurricular, index):
    with open("doc/club_header.json", "r") as club_header:
        club_header_json = json.loads(club_header.read())

        club_string = "{organization} | {location} | {duration}\n".format(
            organization=extracurricular["organization"],
            location=extracurricular["location"],
            duration=extracurricular["duration"],
        )

        club_header_json["startIndex"] = index
        club_header_json["paragraph"]["elements"][0]["startIndex"] = index
        index += len(club_string)
        club_header_json["endIndex"] = index
        club_header_json["paragraph"]["elements"][0]["endIndex"] = index

        club_header_json["paragraph"]["elements"][0]["textRun"]["content"] = club_string

        return index, club_header_json


def build_education(index):
    with open("doc/education.json", "r") as education:
        education_json = json.loads(education.read())

        education_json[0]["startIndex"] = index
        education_json[0]["paragraph"]["elements"][0]["startIndex"] = index
        index += 10
        education_json[0]["endIndex"] = index
        education_json[0]["paragraph"]["elements"][0]["endIndex"] = index

        education_json[1]["startIndex"] = index
        education_json[1]["paragraph"]["elements"][0]["startIndex"] = index
        index += 1
        education_json[1]["endIndex"] = index
        education_json[1]["paragraph"]["elements"][0]["endIndex"] = index

        education_json[2]["startIndex"] = index
        education_json[2]["paragraph"]["elements"][0]["startIndex"] = index
        index += 66
        education_json[2]["endIndex"] = index
        education_json[2]["paragraph"]["elements"][0]["endIndex"] = index

        education_json[3]["startIndex"] = index
        education_json[3]["paragraph"]["elements"][0]["startIndex"] = index
        index += 60
        education_json[3]["endIndex"] = index
        education_json[3]["paragraph"]["elements"][0]["endIndex"] = index

        return index, education_json


def build_doc():
    with open("doc/header.json", "r") as header, \
            open("doc/skeleton.json", "r") as skeleton, \
            open("resume_result.json", "r") as resume, \
            open("resume_doc.json", "w+") as final_doc:
        header_json = json.loads(header.read())
        doc = json.loads(skeleton.read())
        resume_json = json.loads(resume.read())

        index = header_json[-1]["endIndex"]

        content = header_json

        for experience in resume_json["experience"]:
            index, title, summary = build_title(experience, index)
            content.append(title)
            content.append(summary)

            for point in experience["description"]:
                index, point = build_point(point, index)
                content.append(point)

            index, line = build_line(index)
            content.append(line)
        
        index, extracurricular_title, extracurricular_newline = build_extracurricular_banner(index)
        content.append(extracurricular_title)
        content.append(extracurricular_newline)

        for experience in resume_json["extracurriculars"]:
            index, title = build_extracurricular_title(experience, index)
            content.append(title)

            for point in experience["description"]:
                index, point = build_point(point, index)
                content.append(point)
                content.append({"add point": None})

            index, line = build_line(index)
            content.append(line)

        index, education = build_education(index)

        content += education
        
        doc["body"]["content"] = content

        final_doc.write(json.dumps(doc, indent=4))


def convert_to_instructions():
    with open("resume_doc.json", "r") as doc, \
            open("i_commands.json", "w+") as i_command_file, \
            open("u_commands.json", "w+") as u_command_file:
        doc_json = json.loads(doc.read())

        i_commands = []
        u_commands = []

        for item in doc_json["body"]["content"]:
            if not item.get("paragraph") and not item.get("startIndex"): continue
            for element in item["paragraph"]["elements"]:
                if element.get("textRun"):
                    i_commands.append(
                        {
                            "insertText": {
                                "text": element["textRun"]["content"],
                                "location": {
                                    "index": element["startIndex"]
                                }
                                #"endOfSegmentLocation": {}
                            }
                        }
                    )
                    if element["textRun"].get("textStyle"):
                        u_commands.append(
                            {
                                "updateTextStyle": {
                                    "range": {
                                        "startIndex": element["startIndex"],
                                        "endIndex": element["endIndex"],
                                    },
                                    "textStyle": element["textRun"]["textStyle"],
                                    "fields": "*"
                                }
                            }
                        )
                        
            if item["paragraph"].get("bullet"):
                u_commands.append(
                    {
                        "createParagraphBullets": {
                            "range": {
                                "startIndex": item["startIndex"],
                                "endIndex": item["endIndex"],
                            },
                            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
                        }
                    }
                )
            
            if item["paragraph"].get("paragraphStyle"):
                u_commands.append(
                    {
                        "updateParagraphStyle": {
                            "range": {
                                "startIndex": item["startIndex"],
                                "endIndex": item["endIndex"],
                            },
                            "paragraphStyle": item["paragraph"]["paragraphStyle"],
                            "fields": "*"
                        }
                    }
                )
        
        u_commands.append(
            {
                "updateDocumentStyle": {
                    "documentStyle": {
                        **doc_json["documentStyle"], 
                        "background": {
                            "color": {
                                "color": {
                                    "rgbColor": {
                                        "red": 1.0,
                                        "green": 1.0,
                                        "blue": 1.0
                                    }
                                }
                            }
                        }
                    },
                    "fields": "*"
                }
            }
        )

        # i_commands = sorted(i_commands, key=lambda x: -1 if list(x.keys())[0] == "insertText" else 1)
        u_commands = sorted(u_commands, key=lambda x: list(x.keys())[0])
        
        i_command_file.write(json.dumps(i_commands, indent=4))
        u_command_file.write(json.dumps(u_commands, indent=4))
        

if __name__ == "__main__":
    build_doc()
    convert_to_instructions()
