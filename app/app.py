from flask import Flask, render_template, url_for, redirect, request, make_response

app = Flask(__name__)

questions = [
    {
        "type" : "multiple_choice",
        "question_text" : "q 1 text",
        "choices" : [
            {
                "id" : "1",
                "text" : "1 choice 1",
            },
            {
                "id" : "2",
                "text" : "1 choice 2",
            },
            {
                "id" : "3",
                "text" : "1 choice 3",
            },
         ],
         "answer_id" : "1",
         "explanation" : "explanation 1",
    },

    {
        "type" : "multiple_choice",
        "question_text" : "q 2 text",
        "choices" : [
            {
                "id" : "1",
                "text" : "2 choice 1",
            },
            {
                "id" : "2",
                "text" : "2 choice 2",
            },
            {
                "id" : "3",
                "text" : "2 choice 3",
            },
         ],
         "answer_id" : "2",
         "explanation" : "explanation 2",
    },

    {
         "type" : "fill_in_the_blanks",
         "question_text" : "q 3 text",
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
    
    if (qno < 2):
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

if __name__ == '__main__':
    app.run(debug=True)






