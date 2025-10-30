from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/resume-analyze', methods=['POST'])
def resume_analyze():
    data = request.json or {}
    text = data.get('text', '').lower()
    keywords = {
        'python': 3, 'machine learning': 5, 'finance': 4,
        'analysis': 2, 'team': 2, 'lead': 3, 'intern': 3
    }
    score = sum(v for k,v in keywords.items() if k in text)
    hits = [k for k in keywords if k in text]
    recs = []
    if 'python' not in text: recs.append("Add Python or data-related projects.")
    if 'team' not in text: recs.append("Show teamwork or leadership examples.")
    return jsonify({
        "score": score,
        "matched_keywords": hits,
        "recommendations": recs
    })

@app.route('/api/finance', methods=['POST'])
def finance():
    p = request.json or {}
    income = float(p.get('income', 1000))
    expenses = float(p.get('monthly_expenses', 600))
    months = int(p.get('months', 6))
    proj = []
    bal = income
    for m in range(1, months+1):
        bal = bal - expenses + income
        proj.append({"month": m, "balance": round(bal,2)})
    return jsonify({"projections": proj})

TEAM_GOALS = []
@app.route('/api/team-goals', methods=['GET','POST'])
def goals():
    if request.method == 'POST':
        g = request.json or {}
        TEAM_GOALS.append({
            "id": len(TEAM_GOALS)+1,
            "title": g.get('title','Goal'),
            "progress": int(g.get('progress',0))
        })
        return jsonify({"ok":True})
    return jsonify({"goals": TEAM_GOALS})

if __name__ == '__main__':
    app.run(debug=True)
