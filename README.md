# Révision OPSIE · Patrimoine informatique

Bilingual (French/Russian) exam preparation site for the Master II OPSIE course, based on the 13 supplied materials (12 PDFs and one DOCX). The course plan organizes ten learning screens: an introduction plus its nine lessons.

## Run locally

From this directory, run `python server.py` and open `http://127.0.0.1:8000`. The browser saves lesson completion, quiz answers, review flags and language choice in local storage. `server.py` also exposes a small optional SQLite progress API (`/api/health`, `/api/progress/<learner>`); the public static site does not send learner data to a server.

## Content and build

`content/course.json` contains the bilingual lesson notes, sourced quiz questions and French practice exam. PDF citations are PDF page numbers starting at 1; the supplied DOCX has no stable pagination. Run `python tools/extract_course.py "path/to/course/files" output.json` to extract page-labelled source text with pypdf and python-docx. Run `python tools/build_site.py` to prepare `dist/` and a Site archive.

The study notes report what the provided slides say, not a current legal opinion. The slides use conflicting lesson numbering, so navigation follows the course plan. The Belgium territorial question is explicitly marked as unanswered by the supplied materials. Some exam QCM in the teacher files are malformed; the practice questions only use questions that can be reconstructed from the stated course material.
