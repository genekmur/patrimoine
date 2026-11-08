"""Prepare the static Site build directory and deployable archive."""
from pathlib import Path
import shutil, tarfile
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
shutil.copy(ROOT/'index.html',DIST/'index.html')
shutil.copytree(ROOT/'assets',DIST/'assets')
shutil.copytree(ROOT/'content',DIST/'content')
archive=ROOT.parent/'opsie-site.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    tar.add(ROOT/'.openai'/'hosting.json',arcname='.openai/hosting.json')
    for f in DIST.rglob('*'):
        if f.is_file(): tar.add(f,arcname=f.relative_to(ROOT).as_posix())
print(f'Prepared {DIST} and {archive}')
