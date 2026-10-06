import json,re
from pathlib import Path
from bs4 import BeautifulSoup

def numbers(cells):
 values=[]
 for cell in cells:
  value=cell.replace('$','').replace(',','').strip()
  if re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',value):values.append(float(value.replace('(','-').replace(')',''))/1000)
 return values

def rows(path,match):
 soup=BeautifulSoup(Path(path).read_text(encoding='utf8'),'html.parser')
 matches=[t for t in soup.find_all('table') if match in t.get_text(' ',strip=True)]
 if not matches:raise ValueError('Source statement absent '+match)
 t=min(matches,key=lambda t:len(t.get_text()))
 result={}
 for tr in t.find_all('tr'):
  cells=[x.get_text(' ',strip=True) for x in tr.find_all(['th','td'])]
  if cells and numbers(cells[1:]):result[cells[0]]=numbers(cells[1:])
 return result

def check():
 d=json.loads(Path('data/processed/historical.json').read_text());checks=[]
 labels={'cash':'Cash and cash equivalents','investments':'Marketable securities','ar':'Accounts receivable, net','prepaid':'Prepaid expenses and other current assets','ppe':'Property and equipment, net','rou':'Operating lease right-of-use assets','other_assets':'Other assets','assets':'Total assets','liabilities':'Total liabilities','equity':"Total Palantir's stockholders’ equity",'nci':'Noncontrolling interests'}
 for key,path in [('annual_2025',d['source_annual']),('interim_2026h1',d['source_interim'])]:
  actual=rows(path,'Total assets')
  for name,label in labels.items():
   if label not in actual:
    candidates=[x for x in actual if 'Total Palantir' in x]
    if name=='equity' and candidates:label=candidates[0]
    else:raise ValueError('Missing source label '+label)
   observed=actual[label][0]
   if abs(observed-d[key][name])>1e-6:raise ValueError(f'{key} {name} source mismatch')
   checks.append(dict(period=key,field=name,source_label=label,source_value=observed,model_value=d[key][name],status='pass'))
  isrows=rows(path,'Weighted-average shares of common stock outstanding used in computing earnings per share attributable to common stockholders, basic')
  col=0 if key=='annual_2025' else 2
  for name,label in [('revenue','Revenue'),('ebit','Income from operations'),('net_income','Net income')]:
   observed=isrows[label][col]
   if abs(observed-d[key][name])>1e-6:raise ValueError(f'{key} {name} source mismatch')
   checks.append(dict(period=key,field=name,source_label=label,source_value=observed,model_value=d[key][name],status='pass'))
 cfrows=rows(d['source_interim'],'Cash, cash equivalents, and restricted cash - beginning of period')
 for field,label in [('cfo','Net cash provided by operating activities'),('da','Depreciation and amortization'),('sbc','Stock-based compensation'),('cash_total','Cash, cash equivalents, and restricted cash - end of period')]:
  observed=cfrows[label][0]
  if abs(observed-d['interim_2026h1'][field])>1e-6:raise ValueError('Interim cash-flow source mismatch '+field)
  checks.append(dict(period='interim_2026h1',field=field,source_label=label,source_value=observed,model_value=d['interim_2026h1'][field],status='pass'))
 Path('validation/source-row-checks.json').write_text(json.dumps(checks,indent=2));print('Primary source row checks passed:',len(checks))
if __name__=='__main__':check()