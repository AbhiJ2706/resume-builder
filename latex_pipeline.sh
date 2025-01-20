company=$1
template=$2
python src/resume_builder/builder.py && python src/resume_builder/latex_builder.py $template && python src/resume_builder/doc_api.py --company $company --latex
