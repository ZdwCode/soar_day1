import pandas

pf=pandas.read_excel('./demo1/demo1/logo.xlsx')
pf['type']=0
s="Logo_123"

if "logo" in s or "Logo" in s:
    print('yes')

pf.to_excel('text.xlsx')