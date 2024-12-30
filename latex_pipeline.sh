company=$1
python builder.py && python latex_builder.py && python doc_api.py --company $company --latex
