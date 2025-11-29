from flask import Flask,render_template,jsonify
import subprocess,os,json
app=Flask(__name__,template_folder='templates',static_folder='static')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/refresh')
def refresh():
    subprocess.run(['python','fetch_jira.py'])
    subprocess.run(['python','clone_reports.py'])
    return jsonify({'status':'refreshed'})
@app.route('/dashboard')
def dashboard():
    bugs=[]
    if os.path.exists('jira_bugs.json'):
        with open('jira_bugs.json') as f:
            bugs=json.load(f)
    modules={}
    for b in bugs:
        module=b.get('module','Unknown')
        modules[module]=modules.get(module,0)+1
    suggestions=[]
    try:
        suggestions=__import__('suggest_tests').suggest_new_tests()
    except Exception:
        suggestions=[]
    total=len(bugs)
    return render_template('dashboard.html',modules=modules,suggestions=suggestions,total_bugs=total)
if __name__=='__main__':
    app.run(debug=True)
