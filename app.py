from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "好きなランダムな文字列をここに"

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
        return f"気温が {temp}℃ のとき、0℃より何℃ {('高い' if temp > 0 else '低い' if temp < 0 else '変わらない')}？", str(abs(temp))
    else:
        return "無効な単元です", ""

# 理科の問題生成（単元1と単元2に30問ずつ）
def generate_science_question(unit):
    if unit == "1":
        questions = [
            ("顕微鏡のレンズを切り替えることで変わるのは？", "倍率"),
            ("プレパラートに使うカバーガラスは何のために使う？", "試料を押さえるため"),
            ("観察するとき、最初に使う対物レンズの倍率は？", "低倍率"),
            ("細胞を見るときに使う顕微鏡の種類は？", "光学顕微鏡"),
            ("顕微鏡で観察するとき、試料の準備に使う液体は？", "水"),
            ("顕微鏡の接眼レンズの倍率は一般的に何倍？", "10倍"),
            ("顕微鏡の倍率はどう計算する？", "接眼レンズ×対物レンズ"),
            ("観察で使うプレパラートの材料は？", "ガラス"),
            ("細胞の観察で最も重要なことは？", "焦点を合わせること"),
            ("生物の観察で使うピンセットの役割は？", "試料をつかむため"),
            ("観察の際に調整する部品は？", "ステージ"),
            ("細胞を染色する染料は？", "メチレンブルー"),
            ("顕微鏡の光源の役割は？", "試料を照らすこと"),
            ("観察に使う紙は？", "ろ紙"),
            ("細胞壁があるのはどの生物？", "植物細胞"),
            ("生物の観察で使うメモは？", "スケッチ"),
            ("顕微鏡の倍率を上げると何が起こる？", "拡大される"),
            ("焦点が合わないとどう見える？", "ぼやける"),
            ("観察の際の試料の厚さは？", "薄くする"),
            ("生物の分類の基本単位は？", "種"),
            ("顕微鏡で見える最小の構造は？", "細胞"),
            ("生物の観察に必要な基本器具は？", "顕微鏡"),
            ("植物細胞に特徴的な構造は？", "葉緑体"),
            ("動物細胞にあるが植物細胞にないものは？", "リソソーム"),
            ("細胞の中の液体は？", "細胞質"),
            ("染色するときに使う液体の名前は？", "ヨウ素液"),
            ("プレパラートを作る手順は？", "試料を載せる→カバーガラスを置く"),
            ("観察中に光量が不足するとどうなる？", "見えにくくなる"),
            ("観察の際に注意することは？", "試料を壊さないこと"),
            ("顕微鏡の倍率を調整するネジは？", "粗動ネジ"),
        ]
    elif unit == "2":
        questions = [
            ("種子をつくらない植物は？", "コケ植物"),
            ("維管束がない植物の例は？", "ゼニゴケ"),
            ("双子葉類の植物の葉脈の形は？", "網状脈"),
            ("単子葉類の根の生え方は？", "ひげ根"),
            ("種子を持つ植物は？", "被子植物"),
            ("植物の分類で葉の形に注目する理由は？", "分類に役立つため"),
            ("シダ植物の特徴は？", "胞子で増える"),
            ("花の構造に関係する部分は？", "雄しべと雌しべ"),
            ("維管束の役割は？", "水や養分の運搬"),
            ("被子植物の種子はどこにある？", "果実の中"),
            ("コケ植物の生活環はどの段階が長い？", "配偶体"),
            ("単子葉類の特徴は？", "葉脈が平行"),
            ("双子葉類の特徴は？", "葉脈が網状"),
            ("シダ植物の葉を何という？", "胞子葉"),
            ("維管束の種類は？", "木部と師部"),
            ("種子植物の特徴は？", "種子で繁殖"),
            ("花の色は何のため？", "昆虫を誘引"),
            ("根の役割は？", "水分と養分の吸収"),
            ("葉緑体は何を行う？", "光合成"),
            ("花粉はどこから出る？", "雄しべ"),
            ("果実の役割は？", "種子の保護と散布"),
            ("植物の分類基準に使う特徴は？", "葉、根、茎の形"),
            ("コケ植物はどんな環境に多い？", "湿った場所"),
            ("単子葉類の例は？", "イネ、トウモロコシ"),
            ("双子葉類の例は？", "サクラ、ホウセンカ"),
            ("根の種類でひげ根の特徴は？", "細かく広がる"),
            ("維管束植物の特徴は？", "維管束を持つ"),
            ("シダ植物の繁殖方法は？", "胞子"),
            ("花の受粉方法は？", "風や昆虫による"),
            ("植物の成長に必要な要素は？", "光、水、二酸化炭素"),
        ]
    else:
        questions = [("無効な単元です", "")]
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
    questions = generate_questions(subject, unit, 30)  # ← ここで30問に指定
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

if __name__ == "__main__":
    app.run(debug=True)
