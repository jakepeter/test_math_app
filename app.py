import os
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "好きなランダムな文字列をここに"

# 理科の問題リスト（単元別）
science_questions = {
    "1": [  # 生物の観察
        ("顕微鏡のレンズを切り替えることで変わるのは？", "倍率"),
        ("プレパラートに使うカバーガラスは何のために使う？", "試料を押さえるため"),
        ("観察するとき、最初に使う対物レンズの倍率は？", "低倍率"),
        ("細胞を見るときに使う顕微鏡の種類は？", "光学顕微鏡"),
        ("顕微鏡で観察するとき、試料の準備に使う液体は？", "水"),
        # ... 25問以上追加
    ],
    "2": [  # 花のつくりなど
        ("種子をつくらない植物は？", "コケ植物"),
        ("維管束がない植物の例は？", "ゼニゴケ"),
        ("双子葉類の植物の葉脈の形は？", "網状脈"),
        ("単子葉類の根の生え方は？", "ひげ根"),
        # ... 25問以上追加
    ],
    # 必要に応じて単元を追加（例："3": [...], "4": [...]）
}

# 数学の問題生成
def generate_math_question(unit):
    if unit == "1":
        a = random.randint(-10, 10)
        return f"{a} は正の数ですか？", "はい" if a > 0 else "いいえ" if a < 0 else "ゼロ"
    elif unit == "2":
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        return f"{a} + ({b}) = ?", str(a + b)
    elif unit == "3":
        a = random.randint(-9, 9)
        b = random.choice([i for i in range(-5, 6) if i != 0])
        if random.choice([True, False]):
            return f"{a} × {b} = ?", str(a * b)
        else:
            return f"{a * b} ÷ {b} = ?", str(a)
    elif unit == "4":
        temp = random.randint(-10, 35)
        return f"気温が {temp}℃ のとき、0℃ より何℃ {('高い' if temp > 0 else '低い' if temp < 0 else '変わらない')}？", str(abs(temp))
    else:
        return "無効な単元です", ""

# 理科の問題生成（ランダム）
def generate_science_question(unit):
    questions = science_questions.get(unit, [("無効な単元です", "")])
    return random.choice(questions)

# 問題をn問生成
def generate_questions(subject, unit, n=30):
    questions = []
    for _ in range(n):
        if subject == "math":
            q, a = generate_math_question(unit)
        elif subject == "science":
            q, a = generate_science_question(unit)
        else:
            q, a = "無効な科目です", ""
        questions.append((q, a))
    return questions

# トップページ：科目選択
@app.route("/")
def index():
    return render_template("index.html")

# 単元選択ページ
@app.route("/select_subject", methods=["POST"])
def select_subject():
    subject = request.form.get("subject")
    session["subject"] = subject
    return render_template("select_unit.html", subject=subject)

# クイズ開始
@app.route("/quiz", methods=["POST"])
def quiz():
    subject = session.get("subject")
    unit = request.form.get("unit")
    questions = generate_questions(subject, unit, 30)
    session["questions"] = questions
    session["current"] = 0
    session["unit"] = unit

    question, answer = questions[0]
    return render_template("quiz.html", question=question, answer=answer, unit=unit, subject=subject, current=1, total=30)

# 回答後
@app.route("/result", methods=["POST"])
def result():
    user_answer = request.form.get("user_answer").strip()
    correct_answer = request.form.get("correct_answer").strip()

    current = session.get("current", 0)
    subject = session.get("subject", "")
    unit = session.get("unit", "")

    is_correct = (user_answer == correct_answer)

    current += 1
    session["current"] = current

    if current >= len(session["questions"]):
        return render_template("finish.html", total=len(session["questions"]))

    question, answer = session["questions"][current]
    return render_template("quiz.html",
                           question=question,
                           answer=answer,
                           unit=unit,
                           subject=subject,
                           current=current + 1,
                           total=len(session["questions"]),
                           is_correct=is_correct,
                           user_answer=user_answer,
                           correct_answer=correct_answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
