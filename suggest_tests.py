import json
from collections import Counter
def suggest_new_tests():
    try:
        with open('jira_bugs.json') as f:
            bugs=json.load(f)
    except Exception:
        bugs=[]
    module_bugs=Counter(b.get('module','Unknown') for b in bugs)
    high_risk={m for m,c in module_bugs.items() if c>1}
    try:
        with open('postman_collection.json') as f:
            collection=json.load(f)
    except Exception:
        collection={'item':[]}
    existing_tests={item.get('name','').lower() for item in collection.get('item',[]) if 'request' in item}
    suggestions=[]
    for module in sorted(high_risk):
        for item in collection.get('item',[]):
            name=item.get('name','').lower()
            url=''
            try:
                url=item.get('request',{}).get('url','')
                if isinstance(url,dict):
                    url=url.get('raw','') or ''
            except Exception:
                url=''
            if module.lower() in name and name not in existing_tests:
                suggestions.append({'module':module,'test_name':item.get('name',''),'reason':f"{module_bugs[module]} open bugs in {module}"})
            elif module.lower() in url.lower() and name not in existing_tests:
                suggestions.append({'module':module,'test_name':item.get('name',''),'reason':f"{module_bugs[module]} open bugs in {module} (matched by URL)"})
    for module in sorted(high_risk):
        if not any(s['module']==module for s in suggestions):
            suggestions.append({'module':module,'test_name':f'Add API test for {module}','reason':f'{module_bugs[module]} open bugs in {module}'})
    return suggestions[:10]

if __name__=='__main__':
    print(suggest_new_tests())
