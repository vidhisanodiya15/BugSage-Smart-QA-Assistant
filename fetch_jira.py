import requests,json,os
def fetch_jira_bugs():
    if not os.path.exists('config.json'):
        with open('jira_bugs.json','w') as f:
            json.dump([],f)
        return []
    with open('config.json') as f:
        cfg=json.load(f).get('jira',{})
    base=cfg.get('url')
    if not base or 'your-domain' in base:
        with open('jira_bugs.json','w') as f:
            json.dump([],f)
        return []
    url=f"{base}/rest/api/3/search"
    auth=(cfg.get('email'),cfg.get('token'))
    jql=f"project = {cfg.get('project')} AND status != Closed"
    try:
        r=requests.get(url,auth=auth,params={'jql':jql,'fields':'summary,customfield_10020'})
        issues=r.json().get('issues',[])
    except Exception:
        issues=[]
    bugs=[]
    for issue in issues:
        try:
            module=issue.get('fields',{}).get('customfield_10020',[{}])[0].get('value','Unknown')
        except Exception:
            module='Unknown'
        bugs.append({'key':issue.get('key'),'summary':issue.get('fields',{}).get('summary',''),'module':module})
    with open('jira_bugs.json','w') as f:
        json.dump(bugs,f,indent=2)
    return bugs

if __name__=='__main__':
    fetch_jira_bugs()
