# resume-builder

## Usage

- Install `hatch`
- In `latex_builder.py`, update the `build_header` function latex to include your details.
- In `latex_builder.py`, update the `build_skills` function latex to include the relevant domains (this will not be required in the future).
- In `latex_builder.py`, update the `build_education` function latex to include your education details.
- Replace the resume JSON with your own.
- Put your job posting in `input/posting.txt`.
- Run `hatch run run-latex [company name]`.

## A note on `gdoc-pipeline`

To use it you must set up the google docs API for python. Place the `credentials.json` in the root directory. You may also need to chage details in the `doc/header.json` file. You are responsible for ensuring the indices for the updated header are correct. Support for this is coming soon.
