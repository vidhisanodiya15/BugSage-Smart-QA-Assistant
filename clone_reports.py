import os,shutil,json
try:
    import git
except Exception:
    git=None
def clone_test_reports():
    if not os.path.exists('config.json'):
        return
    with open('config.json') as f:
        git_cfg=json.load(f).get('git',{})
    repo=git_cfg.get('repo')
    folder=git_cfg.get('folder','test_reports')
    branch=git_cfg.get('branch','main')
    if not repo or 'yourorg' in repo:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder,exist_ok=True)
        sample={'report':'sample','tests':[]}
        with open(os.path.join(folder,'sample_report.json'),'w') as f:
            json.dump(sample,f,indent=2)
        return
    if git is None:
        return
    if os.path.exists(folder):
        shutil.rmtree(folder)
    git.Repo.clone_from(repo,folder,branch=branch)

if __name__=='__main__':
    clone_test_reports()
