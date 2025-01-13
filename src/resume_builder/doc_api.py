import json
import os.path
import argparse
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents"]


def generate_latex(company):
    proc = subprocess.Popen(['pdflatex', 'final_doc.tex'], cwd="artifacts")
    proc.communicate()
    os.rename('artifacts/final_doc.pdf', f'output/abhinav_jain_resume_{company}.pdf')


def generate_google_doc(fetch=False, document_id=None, company=None):
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("docs", "v1", credentials=creds)

        if fetch:
            document = service.documents().get(documentId=document_id).execute()

            print(f"The title of the document is: {document.get('title')}")

            with open("complete_resume_doc.json", "w+") as f:
                f.write(json.dumps(document, indent=4))
        
        else:
            document = service.documents().create(body={"title" : f"abhinav_jain_resume_{company.lower()}"}).execute()

            print(document["documentId"])
            
            result = service.documents().batchUpdate(documentId=document["documentId"], body={
                'requests': json.loads(open("artifacts/i_commands.json", "r").read())
            }).execute()
            print(result)

            result = service.documents().batchUpdate(documentId=document["documentId"], body={
                'requests': json.loads(open("artifacts/u_commands.json", "r").read())
            }).execute()
            print(result)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Google docs API client',
        description='Builds/fetches documents',
    )

    parser.add_argument(
        "--company", 
        "-c", 
        type=str, 
        required=False, 
        help="Company which owns the posting."
    )

    parser.add_argument(
        "--fetch", 
        "-f", 
        type=bool, 
        required=False, 
        help="Set to fetch a document."
    )

    parser.add_argument(
        "--id", 
        "-i", 
        type=str, 
        required=False,
        help="ID of document to get."
    )

    parser.add_argument(
        "--latex", 
        "-l", 
        action="store_true",
        help="Generate Latex if set."
    )

    args = parser.parse_args()

    if args.latex:
        generate_latex(company=args.company)
    else:
        if args.fetch:
            if not args.id:
                parser.error('id is required when fetching.')
            generate_google_doc(args.fetch, args.id)
        else:
            if not args.company:
                parser.error('company is required when generating.')
            generate_google_doc(company=args.company)
