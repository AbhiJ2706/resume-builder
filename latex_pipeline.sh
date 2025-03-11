company=$1
template=$2
python src/resume_builder/backend/data_builder.py && python src/resume_builder/backend/latex_builder.py $template && python src/resume_builder/backend/doc_api.py --company $company
