import subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from src.model import run

def main():
 start=datetime.now(timezone.utc).isoformat()
 from src.source_check import check
 check()
 from src.course_validation import run as course_run
 course_run()
 test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],text=True,capture_output=True)
 Path('validation/reproduction-tests.txt').write_text(test.stdout+test.stderr)
 if test.returncode:raise RuntimeError('Validation failed; outputs not regenerated')
 run()
 subprocess.run([sys.executable,'-m','src.peers'],check=True)
 from src.report import run as report
 from src.workbench import sensitivities
 sensitivities()
 report()
 print('Completed reproduction at',datetime.now(timezone.utc).isoformat(),'start',start)
if __name__=='__main__':main()