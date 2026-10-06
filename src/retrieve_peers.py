import urllib.request,json
from pathlib import Path
urls={
'now_2026q2.html':'https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Second-Quarter-2026-Financial-Results/default.aspx',
'now_2025fy.html':'https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx',
'crm_2027q2.html':'https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Second-Quarter-Fiscal-2027-Results/default.aspx',
'crm_2026fy.html':'https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Fourth-Quarter-Fiscal-2026-Results/default.aspx'}
from bs4 import BeautifulSoup
for name,url in urls.items():
 try:
  content=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();Path('data/raw',name).write_bytes(content)
  soup=BeautifulSoup(content,'html.parser')
  tables=[]
  for table in soup.find_all('table'):
   rows=[]
   for tr in table.find_all('tr'):
    cells=[td.get_text(' ',strip=True) for td in tr.find_all(['td','th'])]
    if cells:rows.append(' | '.join(cells))
   tables.append('\n'.join(rows))
  Path('data/processed',name+'.tables.txt').write_text('\n\n'.join(tables),encoding='utf8');print(name,len(content))
 except Exception as e:print(name,type(e).__name__,str(e))
Path('config/peer_source_urls.json').write_text(json.dumps(urls,indent=2))