from flask import Flask, render_template, request, redirect, make_response
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            op = request.form['operator']
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                result = num1 / num2 if num2 != 0 else "Error: Divide by zero"
        except:
            result = "Invalid input."
    return render_template('calculator.html', result=result)

@app.route('/dice')
def dice():
    roll = random.randint(1, 6)
    return render_template('dice.html', roll=roll)

@app.route('/password', methods=['GET', 'POST'])
def password():
    pw = ''
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            chars = string.ascii_letters + string.digits + string.punctuation
            pw = ''.join(random.choice(chars) for _ in range(length))
        except:
            pw = "Invalid length."
    return render_template('password.html', password=pw)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = {
        "What is the capital of France?": "paris",
        "What is 5 + 7?": "12",
        "What color do you get by mixing red and blue?": "purple"
    }
    if request.method == 'POST':
        score = 0
        for q in questions:
            answer = request.form.get(q, '').strip().lower()
            if answer == questions[q]:
                score += 1
        return render_template('quiz.html', questions=questions, score=score, submitted=True)
    return render_template('quiz.html', questions=questions, submitted=False)

@app.route('/rps', methods=['GET', 'POST'])
def rps():
    result = None
    computer = None
    if request.method == 'POST':
        choices = ['rock', 'paper', 'scissors']
        user = request.form['choice'].lower()
        computer = random.choice(choices)
        if user == computer:
            result = "It's a tie!"
        elif (user == "rock" and computer == "scissors") or \
             (user == "paper" and computer == "rock") or \
             (user == "scissors" and computer == "paper"):
            result = "You win!"
        else:
            result = "You lose!"
    return render_template('rps.html', result=result, computer=computer)

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'target' not in request.cookies:
        resp = make_response(render_template('guess.html', result=None))
        resp.set_cookie('target', str(random.randint(1, 100)))
        resp.set_cookie('attempts', '0')
        return resp
    else:
        target = int(request.cookies['target'])
        attempts = int(request.cookies['attempts']) + 1
        user_guess = int(request.form['guess'])
        if user_guess < target:
            result = "Too low!"
        elif user_guess > target:
            result = "Too high!"
        else:
            result = f"Correct! You got it in {attempts} tries."
            resp = make_response(render_template('guess.html', result=result, reset=True))
            resp.set_cookie('target', '', expires=0)
            resp.set_cookie('attempts', '', expires=0)
            return resp

        resp = make_response(render_template('guess.html', result=result))
        resp.set_cookie('target', str(target))
        resp.set_cookie('attempts', str(attempts))
        return resp

if __name__ == '__main__':
    app.run(debug=True)
