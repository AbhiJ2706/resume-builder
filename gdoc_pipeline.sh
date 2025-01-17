company=$1
python src/resume_builder/builder.py && python src/resume_builder/doc_builder.py && python src/resume_builder/doc_api.py --company $company
