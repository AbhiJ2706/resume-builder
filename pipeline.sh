company=$1
python builder.py && python doc_builder.py && python doc_api.py --company $company
