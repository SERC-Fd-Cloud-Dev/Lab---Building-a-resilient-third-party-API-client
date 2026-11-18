"""Copy a reference checkpoint to a NEW working directory, preserving student work."""
from pathlib import Path
import argparse, shutil
p=argparse.ArgumentParser()
p.add_argument('name',choices=[f'exercise-{i}' for i in range(1,8)]+['homework'])
p.add_argument('destination',type=Path)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
source=root/'solutions'/a.name
if not source.is_dir():
    p.error('This starter export does not include solutions. Ask your tutor for the checkpoint.')
if a.destination.exists():
    p.error('Choose a NEW destination to preserve existing work.')
shutil.copytree(source,a.destination)
if a.name=='homework':
    shutil.copytree(root/'homework/tests',a.destination/'tests',dirs_exist_ok=True)
    shutil.copytree(root/'homework/verification',a.destination/'verification',dirs_exist_ok=True)
    shutil.copy2(root/'homework/pytest.ini',a.destination/'pytest.ini')
else:
    shutil.copytree(root/'tests',a.destination/'tests',dirs_exist_ok=True)
    shutil.copy2(root/'pytest.ini',a.destination/'pytest.ini')
print(a.destination.resolve())
