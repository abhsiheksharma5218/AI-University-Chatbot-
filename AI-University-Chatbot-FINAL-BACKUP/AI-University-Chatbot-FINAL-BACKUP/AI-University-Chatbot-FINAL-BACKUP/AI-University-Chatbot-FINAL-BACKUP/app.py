from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify
)

from auth import (
    create_users_table,
    register_user,
    login_user
)

from chatbot import get_response

from database import (
    create_database,
    migrate_database,
    save_chat,
    get_chat_history,
    get_total_questions,
    get_total_users,
    get_recent_chats,
    get_all_students,
    search_students,
    get_total_students,
    get_student_by_id,
    get_student_question_counts,
    get_daily_question_counts,
    get_active_student_count,
    get_knowledge_base,
    add_knowledge,
    delete_knowledge,
    save_feedback,
    get_feedback_summary,
    get_recent_feedback
)


app = Flask(__name__)

app.secret_key = "abes-ai-student-support-secret-key"


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_users_table()
create_database()
migrate_database()


# =========================================================
# HOME / AI ASSISTANT
# =========================================================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        user_name=session.get("user_name"),
        user_email=session.get("user_email"),
        user_role=session.get("user_role")
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        success, message = register_user(
            name,
            email,
            password
        )

        if success:
            return redirect("/login")

        return render_template(
            "register.html",
            error=message
        )

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = login_user(
            email,
            password
        )

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["user_role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# AI CHAT
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first."
        }), 401

    data = request.get_json()

    user_message = data.get(
        "message",
        ""
    ).strip()

    if not user_message:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    # Get AI response
    bot_response = get_response(
        user_message
    )

    # Save conversation
    save_chat(
        session["user_id"],
        user_message,
        bot_response
    )

    # Suggested follow-up questions
    suggested_questions = get_suggested_questions(
        user_message
    )

    return jsonify({

        "response": bot_response,

        "suggested_questions":
            suggested_questions
    })


# =========================================================
# SUGGESTED QUESTIONS ENGINE
# =========================================================

def get_suggested_questions(user_message):

    text = user_message.lower()

    suggestions = []

    if "vlsi" in text:

        suggestions = [
            "What is semiconductor technology?",
            "What is digital electronics?",
            "What is an embedded system?"
        ]

    elif (
        "exam" in text
        or "semester" in text
        or "back paper" in text
        or "revaluation" in text
        or "result" in text
    ):

        suggestions = [
            "What is an admit card?",
            "What is a back paper?",
            "How can I check my result?"
        ]

    elif (
        "admission" in text
        or "course" in text
        or "college" in text
        or "aktu" in text
    ):

        suggestions = [
            "What is the fee structure?",
            "What scholarships are available?",
            "How can I get admission?"
        ]

    elif (
        "fee" in text
        or "fees" in text
    ):

        suggestions = [
            "What scholarships are available?",
            "How can I get admission?",
            "Is hostel available?"
        ]

    elif (
        "placement" in text
        or "job" in text
        or "career" in text
    ):

        suggestions = [
            "What is the placement process?",
            "What is VLSI?",
            "What is an embedded system?"
        ]

    elif (
        "ece" in text
        or "electronics" in text
    ):

        suggestions = [
            "What is VLSI?",
            "What is digital electronics?",
            "What is an embedded system?"
        ]

    elif "hostel" in text:

        suggestions = [
            "What is the fee structure?",
            "What scholarships are available?",
            "How can I contact the college?"
        ]

    elif "library" in text:

        suggestions = [
            "What is the academic calendar?",
            "What is attendance?",
            "Where can I find previous year papers?"
        ]

    else:

        suggestions = [
            "What is VLSI?",
            "When are semester exams?",
            "What is the placement process?"
        ]

    return suggestions[:3]


# =========================================================
# FEEDBACK
# =========================================================

@app.route("/feedback", methods=["POST"])
def feedback():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first."
        }), 401

    data = request.get_json()

    user_message = data.get(
        "user_message",
        ""
    )

    bot_response = data.get(
        "bot_response",
        ""
    )

    rating = data.get(
        "rating",
        ""
    )

    if rating not in [
        "helpful",
        "not_helpful"
    ]:

        return jsonify({
            "error": "Invalid feedback."
        }), 400

    save_feedback(
        session["user_id"],
        user_message,
        bot_response,
        rating
    )

    return jsonify({
        "success": True
    })


# =========================================================
# CHAT HISTORY API
# =========================================================

@app.route("/history")
def history():

    if "user_id" not in session:
        return jsonify([])

    chats = get_chat_history(
        session["user_id"]
    )

    return jsonify([
        {
            "user_message": chat["user_message"],
            "bot_response": chat["bot_response"],
            "created_at": chat["created_at"]
        }

        for chat in chats
    ])


# =========================================================
# CONVERSATIONS PAGE
# =========================================================

@app.route("/conversations")
def conversations():

    if "user_id" not in session:
        return redirect("/login")

    chats = get_chat_history(
        session["user_id"]
    )

    return render_template(
        "conversations.html",
        chats=chats,
        user_name=session.get("user_name")
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":

        return """
        <h2>Access Denied</h2>

        <p>Admin access is required.</p>

        <a href="/dashboard">
            Go to Dashboard
        </a>
        """, 403

    total_students = get_total_students()
    total_users = get_total_users()
    total_questions = get_total_questions()

    recent_chats = get_recent_chats(10)

    return render_template(
        "admin.html",

        total_students=total_students,

        total_users=total_users,

        total_questions=total_questions,

        recent_chats=recent_chats
    )


# =========================================================
# ADMIN STUDENTS
# =========================================================

@app.route("/admin/students")
def admin_students():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":
        return "Access Denied", 403

    search_text = request.args.get(
        "search",
        ""
    )

    if search_text:

        students = search_students(
            search_text
        )

    else:

        students = get_all_students()

    return render_template(
        "students.html",
        students=students,
        search_text=search_text
    )


# =========================================================
# STUDENT DETAILS
# =========================================================

@app.route(
    "/admin/students/<int:student_id>"
)
def student_details(student_id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":
        return "Access Denied", 403

    student = get_student_by_id(
        student_id
    )

    if not student:
        return "Student not found", 404

    return render_template(
        "student_details.html",
        student=student
    )


# =========================================================
# ADMIN ANALYTICS
# =========================================================

@app.route("/admin/analytics")
def admin_analytics():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":

        return """
        <h2>Access Denied</h2>

        <p>
            Admin access is required.
        </p>

        <a href="/dashboard">
            Go to Dashboard
        </a>
        """, 403

    total_students = get_total_students()

    total_questions = get_total_questions()

    active_students = (
        get_active_student_count()
    )

    student_question_counts = (
        get_student_question_counts()
    )

    daily_question_counts = (
        get_daily_question_counts()
    )

    feedback_summary = (
        get_feedback_summary()
    )

    recent_feedback = (
        get_recent_feedback(10)
    )

    return render_template(
        "analytics.html",

        total_students=total_students,

        total_questions=total_questions,

        active_students=active_students,

        student_question_counts=
            student_question_counts,

        daily_question_counts=
            daily_question_counts,

        feedback_summary=
            feedback_summary,

        recent_feedback=
            recent_feedback
    )


# =========================================================
# ADMIN KNOWLEDGE BASE
# =========================================================

@app.route("/admin/knowledge")
def admin_knowledge():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":
        return "Access Denied", 403

    knowledge = get_knowledge_base()

    return render_template(
        "knowledge_base.html",
        knowledge=knowledge
    )


# =========================================================
# ADD KNOWLEDGE
# =========================================================

@app.route(
    "/admin/knowledge/add",
    methods=["POST"]
)
def admin_add_knowledge():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":
        return "Access Denied", 403

    question = request.form.get(
        "question",
        ""
    ).strip()

    answer = request.form.get(
        "answer",
        ""
    ).strip()

    category = request.form.get(
        "category",
        "General"
    )

    if question and answer:

        add_knowledge(
            question,
            answer,
            category
        )

    return redirect(
        "/admin/knowledge"
    )


# =========================================================
# DELETE KNOWLEDGE
# =========================================================

@app.route(
    "/admin/knowledge/delete/<int:knowledge_id>",
    methods=["POST"]
)
def admin_delete_knowledge(
    knowledge_id
):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("user_role") != "admin":
        return "Access Denied", 403

    delete_knowledge(
        knowledge_id
    )

    return redirect(
        "/admin/knowledge"
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        user_email=session.get("user_email")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "profile.html",
        user_name=session.get("user_name"),
        user_email=session.get("user_email")
    )


# =========================================================
# PROFILE API
# =========================================================

@app.route("/api/profile")
def api_profile():

    if "user_id" not in session:

        return jsonify({
            "error": "Not logged in"
        }), 401

    return jsonify({

        "id": session.get("user_id"),

        "name": session.get(
            "user_name"
        ),

        "email": session.get(
            "user_email"
        ),

        "role": session.get(
            "user_role"
        )
    })


# =========================================================
# SYSTEM STATUS
# =========================================================

@app.route("/api/system-status")
def system_status():

    return jsonify({

        "ai_assistant": "Online",

        "database": "Connected",

        "knowledge_base": "Active",

        "feedback_system": "Active",

        "student_portal": "Online"
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )