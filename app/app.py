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
         "explanation" : "Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in a markup language.",
    },

    {
        "type" : "multiple_choice",
        "question_text" : "Which CSS property controls the text size?",
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
         "explanation" : "The font-size property sets the size of the text.",
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
            "text" : "margin: 0 auto; ",
        },
     ],
     "answer_id" : "3",
     "explanation" : "margin 0 auto helps to horizontally center that element within its container.",
},
{
    "type" : "multiple_choice",
    "question_text" : "In the following code snippet, what value is given for the left margin in margin: 5px 10px 3px 8px; ?",
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
     "explanation" : "The margin and padding are defined in this order: Top Right Bottom Left.",
},
{
    "type" : "multiple_choice",
    "question_text" : "Which of the following property specifies which sides of an element other floating elements are not allowed?",
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
     "explanation" : "The clear property is used to control the behavior of floating elements. Elements after a floating element will flow around it. To avoid this, use the clear property.",
},
    {
         "type" : "fill_in_the_blanks",
         "question_text" : "If one CSS selector is defined more than once, the most recent rule takes precedence. What command can be added to a rule so that it cannot be overwritten by a later rule? p { color: red _______; } p { color: green; }",
         "answer_id" : "!important",
         "explanation" : "The !important command can make sure that a rule is not overwritten by a later rule.",
    },

    {
         "type" : "fill_in_the_blanks",
         "question_text" : "What argument do you use to set a background image? body { background-image: _______(/img/background.png); }",
         "answer_id" : "url",
         "explanation" : "If you want to set a background image, you can set the location of the image with url(location of image).",
    },

    {
         "type" : "fill_in_the_blanks",
         "question_text" : "What rule do you use to set the font of a <p> tag to Impact? p { _______: Impact; }",
         "answer_id" : "font-family",
         "explanation" : "The font-family rule can be used to set the font of a piece of text.",
    },

    {
         "type" : "fill_in_the_blanks",
         "question_text" : "What argument do you use to make a dotted border around a <div> tag? div { border: _______ 1px black; }",
         "answer_id" : "dotted",
         "explanation" : "You can set arguments in the border rule to change the style of the border (solid, dashed, dotted, etc.).",
    },

    {
         "type" : "fill_in_the_blanks",
         "question_text" : "How do you set the border width to the following values in one line? (Do not include the semicolon.) 5px at the top, 2px at the bottom, 10px at the right, 20px at the left<br />h1 { border: solid 1px black; border-width: _______; }",
         "answer_id" : "5px 10px 2px 20px",
         "explanation" : "In order to set border widths on one line, the order goes top-right-bottom-left.",
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
