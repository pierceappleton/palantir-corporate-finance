from html.parser import HTMLParser
from pathlib import Path
class Text(HTMLParser):
 def __init__(self):super().__init__(); self.parts=[]
 def handle_data(self,data):
  if data.strip():self.parts.append(data.strip())
for p in Path('data/raw').glob('*issuer.html'):
 h=Text();h.feed(p.read_text(encoding='utf8')); out=Path('data/processed')/(p.stem+'.txt');out.write_text('\n'.join(h.parts),encoding='utf8');print(out)