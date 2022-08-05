
from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension


from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = ["start_val"]

@app.route("/")
def create_survey():
    survey = satisfaction_survey
    return render_template("start.html", survey=survey)

@app.route("/start", methods=["post"])
def reset():
    responses = []
    return redirect("/questions/0")
    

@app.route("/questions/<int:q_num>")
def get_questions(q_num):
    if (responses is None):
        # prevent directly going to a question page
        return redirect("/")

    if (len(responses)== len(satisfaction_survey.questions)):
        return redirect("/complete.html")

    if (len(responses) != q_num):
        # prevent going to wrong # question
        flash(f"Access Invalid! Redirecting to question: {len(responses)}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q_num]
    return render_template("questions.html", question=question, question_num=q_num)

@app.route("/answer", methods=["post"])
def get_answers():
    #get data from form (which is like a dictionary) using a key to get the value
    #are .form and .args interchangwable?
     answr = request.form['answer'] 
     responses.append(answr)
     if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
        
     return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def survey_complete():
    return render_template("complete.html")
