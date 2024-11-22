from flask import Flask, render_template, request, jsonify
from blockchain_voting import is_voter_registered, register_voter, cast_vote, get_candidates_votes, get_admin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('voter.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/voter')
def voter():
    return render_template('voter.html')

@app.route('/register', methods=['POST'])
def register():
    voter_id = request.form['voter_id']
    admin_account = request.form['admin_account']
    result = register_voter(voter_id, admin_account)
    return jsonify({'result': result})

@app.route('/vote', methods=['POST'])
def vote():
    voter_id = request.form['voter_id']
    candidate_id = request.form['candidate_id']
    vote_time = request.form['vote_time']
    result = cast_vote(voter_id, candidate_id, vote_time)
    return jsonify({'result': result})

@app.route('/results', methods=['GET'])
def results():
    results = get_candidates_votes()
    return jsonify(results)

@app.route('/is_admin', methods=['GET'])
def is_admin():
    admin_account = request.args.get('admin_account')
    admin = get_admin()
    if admin_account.lower() == admin.lower():
        return jsonify({'is_admin': True})
    else:
        return jsonify({'is_admin': False})
    
@app.route('/voters', methods=['GET'])
def get_voters():
    try:
        # Get the list of registered voters' addresses
        voters_list = get_registered_voters  # This assumes you are maintaining this list in your contract
        return jsonify(voters_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3000)
