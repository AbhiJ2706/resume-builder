# resume-builder

## Usage

- Install `hatch`
- In either `templates/jakes_default.py` or `templates/figtree.py`:
  - Update the `_build_header` function latex to include your details.
  - Update the `_build_skills` function latex to include the relevant domains (this will not be required in the future).
  - Update the `_build_education` function latex to include your education details.
- Replace the resume JSON with your own. Format must match example. You can do this using a prompt.
- Put your job posting in `input/posting.txt`.
- Run `hatch run run-latex [company name] [theme name]` where theme name is one of `jakes_default` or `figtree`.

## A note on `gdoc-pipeline`

To use it you must set up the google docs API for python. Place the `credentials.json` in the root directory. You may also need to chage details in the `doc/header.json` file. You are responsible for ensuring the indices for the updated header are correct. Support for this is coming soon.
