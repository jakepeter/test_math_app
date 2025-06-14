from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "好きなランダムな文字列をここに"

# 単元別の1問問題生成
def generate_question(unit):
    if unit == "1":  # 正負の数
        a = random.randint(-10, 10)
        return f"{a} は正の数ですか？", "はい" if a > 0 else "いいえ" if a < 0 else "ゼロ"
    elif unit == "2":  # 加法と減法
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        return f"{a} + ({b}) = ?", str(a + b)
    elif unit == "3":  # 乗法と除法
        a = random.randint(-9, 9)
        b = random.choice([i for i in range(-5, 6) if i != 0])
        if random.choice([True, False]):
            return f"{a} × {b} = ?", str(a * b)
        else:
            return f"{a * b} ÷ {b} = ?", str(a)
    elif unit == "4":  # 正負の数の利用
        temp = random.randint(-10, 35)
        return f"気温が {temp}℃ のとき、0℃より何℃ {('高い' if temp > 0 else '低い' if temp < 0 else '変わらない')}？", str(abs(temp))
    else:
        return "無効な単元です", ""

# 単元別の問題リストをn問分生成
def generate_questions(unit, n=50):
    questions = []
    for _ in range(n):
        q, a = generate_question(unit)
        questions.append((q, a))
    return questions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz", methods=["POST"])
def quiz():
    unit = request.form.get("unit")
    questions = generate_questions(unit, 50)
    session["questions"] = questions
    session["current"] = 0
    session["unit"] = unit

    question, answer = questions[0]
    return render_template("quiz.html", question=question, answer=answer, unit=unit, current=1, total=50)

@app.route("/result", methods=["POST"])
def result():
    user_answer = request.form.get("user_answer").strip()
    correct_answer = request.form.get("correct_answer").strip()

    current = session.get("current", 0)
    unit = session.get("unit", "")

    is_correct = (user_answer == correct_answer)

    # 現在の問題番号をインクリメント
    current += 1
    session["current"] = current

    if current >= len(session["questions"]):
        # 全問終了したら終了ページに遷移（テンプレートfinish.htmlを用意してください）
        return render_template("finish.html", total=len(session["questions"]))

    question, answer = session["questions"][current]
    return render_template("quiz.html",
                           question=question,
                           answer=answer,
                           unit=unit,
                           current=current+1,
                           total=len(session["questions"]),
                           is_correct=is_correct,
                           user_answer=user_answer,
                           correct_answer=correct_answer)

if __name__ == "__main__":
    app.run(debug=True)
