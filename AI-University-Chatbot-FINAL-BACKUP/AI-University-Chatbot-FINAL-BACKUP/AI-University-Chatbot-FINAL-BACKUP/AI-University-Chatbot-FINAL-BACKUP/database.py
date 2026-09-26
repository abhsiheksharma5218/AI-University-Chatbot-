import sqlite3


DATABASE_NAME = "chatbot.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            user_message TEXT NOT NULL,

            bot_response TEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# DATABASE MIGRATION
# =========================================================

def migrate_database():

    connection = get_connection()

    cursor = connection.cursor()


    # -----------------------------
    # Ensure user_id in chat_history
    # -----------------------------

    cursor.execute("""
        PRAGMA table_info(chat_history)
    """)

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]


    if "user_id" not in columns:

        cursor.execute("""
            ALTER TABLE chat_history
            ADD COLUMN user_id INTEGER
        """)


    # -----------------------------
    # Knowledge Base
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            category TEXT
            DEFAULT 'General',

            status TEXT
            DEFAULT 'Active',

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -----------------------------
    # Feedback
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            user_message TEXT,

            bot_response TEXT,

            rating TEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
    """)


    connection.commit()

    connection.close()


# =========================================================
# SAVE CHAT
# =========================================================

def save_chat(
    user_id,
    user_message,
    bot_response
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (
            user_id,
            user_message,
            bot_response
        )

        VALUES (?, ?, ?)
    """, (
        user_id,
        user_message,
        bot_response
    ))

    connection.commit()

    connection.close()


# =========================================================
# GET CHAT HISTORY
# =========================================================

def get_chat_history(
    user_id=None
):

    connection = get_connection()

    cursor = connection.cursor()


    if user_id is not None:

        cursor.execute("""
            SELECT
                user_message,
                bot_response,
                created_at

            FROM chat_history

            WHERE user_id = ?

            ORDER BY id DESC
        """, (
            user_id,
        ))

    else:

        cursor.execute("""
            SELECT
                user_message,
                bot_response,
                created_at

            FROM chat_history

            ORDER BY id DESC
        """)


    chats = cursor.fetchall()

    connection.close()

    return chats


# =========================================================
# TOTAL QUESTIONS
# =========================================================

def get_total_questions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM chat_history
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result


# =========================================================
# TOTAL USERS
# =========================================================

def get_total_users():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result


# =========================================================
# RECENT CHATS
# =========================================================

def get_recent_chats(
    limit=10
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            chat_history.id,
            chat_history.user_message,
            chat_history.bot_response,
            chat_history.created_at,
            users.name,
            users.email

        FROM chat_history

        LEFT JOIN users
        ON chat_history.user_id = users.id

        ORDER BY chat_history.id DESC

        LIMIT ?
    """, (
        limit,
    ))

    chats = cursor.fetchall()

    connection.close()

    return chats


# =========================================================
# GET ALL STUDENTS
# =========================================================

def get_all_students():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role,
            created_at

        FROM users

        WHERE role = 'student'

        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return students


# =========================================================
# SEARCH STUDENTS
# =========================================================

def search_students(
    search_text=""
):

    connection = get_connection()

    cursor = connection.cursor()

    search_pattern = (
        "%" +
        search_text +
        "%"
    )

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role,
            created_at

        FROM users

        WHERE role = 'student'

        AND (
            name LIKE ?
            OR email LIKE ?
        )

        ORDER BY id DESC
    """, (
        search_pattern,
        search_pattern
    ))

    students = cursor.fetchall()

    connection.close()

    return students


# =========================================================
# TOTAL STUDENTS
# =========================================================

def get_total_students():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role = 'student'
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result


# =========================================================
# STUDENT DETAILS
# =========================================================

def get_student_by_id(
    student_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role,
            created_at

        FROM users

        WHERE id = ?
    """, (
        student_id,
    ))

    student = cursor.fetchone()

    connection.close()

    return student


# =========================================================
# STUDENT QUESTION COUNTS
# =========================================================

def get_student_question_counts():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            users.name,
            users.email,
            COUNT(chat_history.id)

        FROM users

        LEFT JOIN chat_history
        ON users.id = chat_history.user_id

        WHERE users.role = 'student'

        GROUP BY
            users.id

        ORDER BY
            COUNT(chat_history.id) DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


# =========================================================
# DAILY QUESTION COUNTS
# =========================================================

def get_daily_question_counts():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE(created_at),
            COUNT(*)

        FROM chat_history

        GROUP BY DATE(created_at)

        ORDER BY DATE(created_at)
    """)

    data = cursor.fetchall()

    connection.close()

    return data


# =========================================================
# ACTIVE STUDENT COUNT
# =========================================================

def get_active_student_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id)

        FROM chat_history

        WHERE user_id IS NOT NULL
    """)

    result = cursor.fetchone()[0]

    connection.close()

    return result


# =========================================================
# KNOWLEDGE BASE
# =========================================================

def get_knowledge_base():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            question,
            answer,
            category,
            status,
            created_at

        FROM knowledge_base

        ORDER BY id DESC
    """)

    knowledge = cursor.fetchall()

    connection.close()

    return knowledge


# =========================================================
# ADD KNOWLEDGE
# =========================================================

def add_knowledge(
    question,
    answer,
    category="General"
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO knowledge_base
        (
            question,
            answer,
            category,
            status
        )

        VALUES (?, ?, ?, 'Active')
    """, (
        question,
        answer,
        category
    ))

    connection.commit()

    connection.close()


# =========================================================
# DELETE KNOWLEDGE
# =========================================================

def delete_knowledge(
    knowledge_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM knowledge_base

        WHERE id = ?
    """, (
        knowledge_id,
    ))

    connection.commit()

    connection.close()


# =========================================================
# ACTIVE KNOWLEDGE
# =========================================================

def get_active_knowledge():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            question,
            answer,
            category

        FROM knowledge_base

        WHERE status = 'Active'
    """)

    knowledge = cursor.fetchall()

    connection.close()

    return knowledge


# =========================================================
# SAVE FEEDBACK
# =========================================================

def save_feedback(
    user_id,
    user_message,
    bot_response,
    rating
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (
            user_id,
            user_message,
            bot_response,
            rating
        )

        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        user_message,
        bot_response,
        rating
    ))

    connection.commit()

    connection.close()


# =========================================================
# FEEDBACK ANALYTICS
# =========================================================

def get_feedback_summary():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(
                CASE
                    WHEN rating = 'helpful'
                    THEN 1
                    ELSE 0
                END
            ) AS helpful,
            SUM(
                CASE
                    WHEN rating = 'not_helpful'
                    THEN 1
                    ELSE 0
                END
            ) AS not_helpful

        FROM feedback
    """)

    result = cursor.fetchone()

    connection.close()

    return {
        "total": result["total"] or 0,
        "helpful": result["helpful"] or 0,
        "not_helpful": result["not_helpful"] or 0
    }


# =========================================================
# RECENT FEEDBACK
# =========================================================

def get_recent_feedback(
    limit=10
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            feedback.id,
            feedback.user_message,
            feedback.bot_response,
            feedback.rating,
            feedback.created_at,
            users.name,
            users.email

        FROM feedback

        LEFT JOIN users
        ON feedback.user_id = users.id

        ORDER BY feedback.id DESC

        LIMIT ?
    """, (
        limit,
    ))

    feedback = cursor.fetchall()

    connection.close()

    return feedback