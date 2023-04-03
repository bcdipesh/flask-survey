from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "survey app"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """Handle how to display home page"""

    return render_template('index.html', satisfaction_survey=satisfaction_survey)


@app.route('/start-survey', methods=['POST'])
def start_survey():
    """Sets a session and starts the survey"""

    # responses of people answer to the survey questions
    session['responses'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:question_num>')
def display_question(question_num):
    """Handle how to display question"""

    responses = session['responses']

    # protect questions route
    if (question_num == len(responses)):
        return render_template('question.html', question_num=question_num, question=satisfaction_survey.questions[question_num])
    elif (len(responses) == len(satisfaction_survey.questions)):
        flash("Trying to access invalid question", "Error")
        return redirect('/thank-you')
    else:
        print("inside elif")
        flash("Trying to access invalid question", "Error")
        return redirect(f'/questions/{len(responses)}')


@app.route('/answer', methods=['POST'])
def save_user_answer():
    """Handle how user answer is saved"""

    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    # if all questions are answered redirect to thank you page
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thank-you')

    return redirect(f'/questions/{len(responses)}')


@app.route('/thank-you')
def thank_you():
    """Displays thank you page after completion of a survey"""

    return render_template('thank-you.html')
