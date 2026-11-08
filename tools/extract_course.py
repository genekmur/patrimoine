"""Extract the provided PDF and DOCX course materials to page-labelled JSON."""
from pathlib import Path
import json, sys
from pypdf import PdfReader
from docx import Document

def extract(folder: Path):
    files=[]
    for path in sorted(folder.iterdir()):
        if path.suffix.lower()=='.pdf':
            try:
                reader=PdfReader(str(path))
                pages=[{"page":i+1,"text":page.extract_text() or ""} for i,page in enumerate(reader.pages)]
                files.append({"file":path.name,"kind":"pdf","pages":pages})
            except Exception as e: files.append({"file":path.name,"kind":"pdf","error":str(e)})
        elif path.suffix.lower()=='.docx':
            doc=Document(path)
            text=[p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                text.extend(" | ".join(cell.text for cell in row.cells) for row in table.rows)
            files.append({"file":path.name,"kind":"docx","pages":[],"text":"\n".join(text)})
    return files

if __name__=='__main__':
    if len(sys.argv)<2: raise SystemExit('Usage: python tools/extract_course.py <folder> [output.json]')
    source=Path(sys.argv[1]); output=Path(sys.argv[2]) if len(sys.argv)>2 else Path('course-extracted.json')
    output.write_text(json.dumps(extract(source),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Extracted {len(json.loads(output.read_text(encoding="utf-8")))} files → {output}')
