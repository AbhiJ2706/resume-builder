import os.path
import argparse
import subprocess


def generate_latex(company):
    proc = subprocess.Popen(['./render.sh'], cwd="artifacts")
    proc.communicate()
    os.rename('artifacts/final_doc.pdf', f'output/abhinav_jain_resume_{company}.pdf')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='API client',
        description='Builds documents',
    )

    parser.add_argument(
        "--company", 
        "-c", 
        type=str, 
        required=False, 
        help="Company which owns the posting."
    )

    args = parser.parse_args()

    generate_latex(company=args.company)
    
