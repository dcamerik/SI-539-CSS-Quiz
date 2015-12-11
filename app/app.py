from flask import Flask, render_template, url_for, redirect, request, make_response
from forms import ContactForm
from flask.ext.mail import Message, Mail

app = Flask(__name__)
app.secret_key = 'CSSisFun'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'umsiwebdesign@gmail.com',
    MAIL_PASSWORD = '105sstate',))

mail = Mail(app)
questions = [
    {
        "type" : "multiple_choice",
        "question_text" : "What does CSS stand for?",
        "choices" : [
            {
                "id" : "1",
                "text" : "Cascading Style Sheets",
            },
            {
                "id" : "2",
                "text" : "Computer Style Sheets",
            },
            {
                "id" : "3",
                "text" : "Colorful Style Sheets",
            },
         ],
         "answer_id" : "1",
         "explanation" : "Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in a markup language",
    },

    {
        "type" : "multiple_choice",
        "question_text" : "Which CSS property controls the text size",
        "choices" : [
            {
                "id" : "1",
                "text" : "text-style",
            },
            {
                "id" : "2",
                "text" : "font-size",
            },
            {
                "id" : "3",
                "text" : "font-height",
            },
         ],
         "answer_id" : "2",
         "explanation" : "The font-size property sets the size of the text",
    },
{
    "type" : "multiple_choice",
    "question_text" : "Which snippet of CSS is commonly used to center a website horizontally?",
    "choices" : [
        {
            "id" : "1",
            "text" : "site-align: center; ",
        },
        {
            "id" : "2",
            "text" : "margin: center; ",
        },
        {
            "id" : "3",
            "text" : "margin: 0 auto ; ",
        },
     ],
     "answer_id" : "3",
     "explanation" : "Margin 0 auto helps to horizontally center that element within its container",
},
{
    "type" : "multiple_choice",
    "question_text" : "In the following code snippet, what value is given for the left margin margin: 5px 10px 3px 8px;",
    "choices" : [
        {
            "id" : "1",
            "text" : "8px",
        },
        {
            "id" : "2",
            "text" : "5px",
        },
        {
            "id" : "3",
            "text" : "10px",
        },
     ],
     "answer_id" : "1",
     "explanation" : "The margin and padding are defined in this order: Top Right Bottom Left",
},
{
    "type" : "multiple_choice",
    "question_text" : "Which of the following property specifies which sides of an element other floating elements are not allowed.",
    "choices" : [
        {
            "id" : "1",
            "text" : "cleared",
        },
        {
            "id" : "2",
            "text" : "clear",
        },
        {
            "id" : "3",
            "text" : "float",
        },
     ],
     "answer_id" : "2",
     "explanation" : "The clear property is used to control the behavior of floating elements.Elements after a floating element will flow around it. To avoid this, use the clear property.",
},
    {
         "type" : "fill_in_the_blanks",
         "question_text" : "q 4 text",
         "answer_id" : "answer",
         "explanation" : "explanation 3",
    },
]

@app.route('/')
def index():
    return redirect('/next/0')

@app.route('/next/<int:qno>', methods=["GET"])
def next(qno):
    if (qno < 0 or qno >= len(questions)):
        raise ValueError("invalid question number on request: " + qno);

    if (questions [qno] ["type"] == "multiple_choice"):
        resp = make_response(render_template("index.html",
            mode = "mc_question",
            question_number = qno,
            question = questions[qno],
            check_answer_url = url_for("check_answer")
            ))
    else:
        resp = make_response(render_template("index.html",
            mode = "fb_question",
            question_number = qno,
            question = questions[qno],
            check_answer_url = url_for("check_answer")
            ))

    resp.set_cookie('qno', str(qno))

    return resp

@app.route('/check_answer', methods = ['GET','POST'])
def check_answer():
    qno = int(request.cookies.get('qno'))

    question_type = questions[qno]["type"]

    if question_type == "multiple_choice":
        is_all_done = "no"
        if (qno + 1 >= len(questions)):
            is_all_done = "yes"

        expected_answer_id = int(questions[qno]["answer_id"])

        actual_answer_id = int(request.form["choiceRadios"])

        status_value = "incorrect"
        if expected_answer_id == actual_answer_id:
            status_value = "correct"

        return render_template("index.html",
            mode = "answer",
            status = status_value,
            question_number = qno,
            explanation = questions[qno]["explanation"],
            next_question_url = url_for("next", qno=(qno+1)),
            all_done = is_all_done
        )
    elif question_type == "fill_in_the_blanks":
        is_all_done = "no"
        if (qno + 1 >= len(questions)):
            is_all_done = "yes"
        expected_answer_id = questions[qno]["answer_id"]
        actual_answer_id = request.form["answerText"]
        status_value = "incorrect"
        if expected_answer_id == actual_answer_id:
            status_value = "correct"
        return render_template("index.html",
            mode = "answer",
            status = status_value,
            question_number = qno,
            explanation = questions[qno]["explanation"],
            next_question_url = url_for("next", qno = (qno+1)),
            all_done = is_all_done
            )


@app.route('/videos')
def videos():
    return render_template("videos.html", name="videos")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = ContactForm()
    if request.method == 'POST':
        msg = Message(form.subject.data, sender = ("Dana & Radhika", "dcamerik@umich.edu"), recipients = ["dcamerik@umich.edu", "radhikamani88@gmail.com"])
        msg.body = """
        FROM: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        msg_confirm = Message("Confirmation: " + form.subject.data, sender = ("Dana & Radhika", "dcamerik@umich.edu"), recipients = [form.email.data])
        msg_confirm.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
        mail.send(msg_confirm)
        form.reset()
        return render_template('feedback.html', form=form, name="feedback", mode="sent")
    elif request.method == 'GET':
        return render_template('feedback.html', form=form, name="feedback")


if __name__ == '__main__':
    app.run(debug=True)
