import sqlite3

DATABASE_NAME = "chatbot.db"


knowledge_data = [

    # =========================
    # UNIVERSITY / COLLEGE
    # =========================

    (
        "What is admission?",
        "Admission is the process through which eligible students enroll in a university or college program. Students should follow the current eligibility, application and counselling requirements.",
        "Admission"
    ),

    (
        "How can I get admission?",
        "Students should check the latest official admission notification for eligibility, application procedure, counselling and required documents.",
        "Admission"
    ),

    (
        "What courses are available?",
        "Universities and colleges offer different undergraduate and postgraduate programs. Students should check the current official course list for available programs and eligibility.",
        "Courses"
    ),

    (
        "What is ECE?",
        "ECE stands for Electronics and Communication Engineering. It covers digital electronics, analog electronics, communication systems, embedded systems, microprocessors, VLSI and semiconductor technologies.",
        "ECE"
    ),

    (
        "What is the fee structure?",
        "The fee structure depends on the program, academic year and applicable university or college policies. Students should verify the latest official fee details before making any payment.",
        "Fees"
    ),

    (
        "Is hostel available?",
        "Hostel facilities may be available depending on the institution and current availability. Students should check the latest official hostel information for fees, rules and room availability.",
        "Hostel"
    ),

    (
        "What are library facilities?",
        "The college library generally provides textbooks, reference books, journals, digital resources and study facilities. Students should check the current library notice for timings and services.",
        "Library"
    ),

    (
        "What scholarships are available?",
        "Scholarship availability depends on government schemes, institutional policies and student eligibility. Students should check the latest scholarship notification and eligibility requirements.",
        "Scholarship"
    ),

    (
        "What is the placement process?",
        "The placement process may include registration, eligibility verification, aptitude tests, technical rounds, interviews and HR rounds. Students should follow the latest placement notices from their institution.",
        "Placement"
    ),

    (
        "How can I contact the college?",
        "Students should use the official college website, administration office or department contact information for current contact details.",
        "Contact"
    ),

    (
        "What is attendance?",
        "Attendance is the record of a student's participation in classes, practical sessions and other academic activities. The required attendance percentage depends on the applicable university and college rules.",
        "Academics"
    ),

    (
        "What is a timetable?",
        "A timetable shows the scheduled classes, practical sessions and other academic activities for students. Students should check the latest timetable issued by their department.",
        "Academics"
    ),

    (
        "What is academic calendar?",
        "An academic calendar contains important academic activities such as semester dates, examinations, holidays, registration and other institutional activities.",
        "Academics"
    ),

    # =========================
    # EXAM RELATED
    # =========================

    (
        "When are semester exams?",
        "Semester examination dates are announced through the official academic or university examination schedule. Students should check the latest official notice for exact dates.",
        "Exams"
    ),

    (
        "What is a semester exam?",
        "A semester examination is an assessment conducted at the end of an academic semester to evaluate a student's knowledge of the subjects studied during that semester.",
        "Exams"
    ),

    (
        "What is an internal exam?",
        "An internal examination is an assessment conducted during the semester as part of the internal evaluation process. The exact pattern and marks distribution depend on the applicable academic rules.",
        "Exams"
    ),

    (
        "What is a practical exam?",
        "A practical examination evaluates a student's practical knowledge and ability to perform experiments, use tools and apply concepts related to a subject.",
        "Exams"
    ),

    (
        "What is an admit card?",
        "An admit card is an examination document that generally contains information such as the student's details, examination information and instructions. Students should carry the required admit card during examinations.",
        "Exams"
    ),

    (
        "How can I get my exam form?",
        "Students should complete the examination form through the officially provided university or college process within the announced deadline.",
        "Exams"
    ),

    (
        "What is a back paper?",
        "A back paper generally refers to a subject that a student needs to clear again because the required passing criteria were not achieved in an earlier attempt.",
        "Exams"
    ),

    (
        "How can I check my result?",
        "Students can check examination results through the official university result portal or the process announced by their institution.",
        "Results"
    ),

    (
        "What is revaluation?",
        "Revaluation is a process through which a student can request a review of the evaluation of an examination answer script, subject to the applicable university rules.",
        "Results"
    ),

    (
        "What is the passing criteria?",
        "Passing criteria depend on the applicable university and course regulations. Students should check the official examination rules for the required marks and other conditions.",
        "Exams"
    ),

    (
        "How many marks are required to pass?",
        "The required passing marks depend on the university, course and examination scheme. Students should refer to the latest official examination regulations.",
        "Exams"
    ),

    (
        "What is syllabus?",
        "A syllabus is a structured outline of the topics, units and learning areas that are covered in a particular academic subject.",
        "Academics"
    ),

    (
        "Where can I find previous year papers?",
        "Previous-year question papers may be available through the official university resources, college library, department or learning portal.",
        "Academics"
    ),

    # =========================
    # TECHNICAL / ECE
    # =========================

    (
        "What is VLSI?",
        "VLSI stands for Very Large Scale Integration. It is the process of integrating a large number of electronic components, especially transistors, onto a single semiconductor chip.",
        "VLSI"
    ),

    (
        "What is embedded system?",
        "An embedded system is a computer-based system designed to perform a specific function within a larger electronic or electrical system. It commonly includes a microcontroller or processor, software and hardware.",
        "Embedded"
    ),

    (
        "What is digital electronics?",
        "Digital electronics deals with electronic circuits that process digital signals, commonly represented using binary values such as 0 and 1.",
        "Digital Electronics"
    ),

    (
        "What is communication system?",
        "A communication system transfers information from a source to a destination through a suitable transmission medium using processes such as modulation, transmission and reception.",
        "Communication"
    ),

    (
        "What is semiconductor?",
        "A semiconductor is a material whose electrical conductivity lies between that of a conductor and an insulator. Silicon is one of the most widely used semiconductor materials.",
        "Semiconductor"
    ),

    (
        "What is microprocessor?",
        "A microprocessor is an integrated electronic circuit that performs processing operations and executes instructions. It is used in many computing and electronic systems.",
        "Microprocessor"
    )
]


def create_knowledge_pack():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    added = 0
    skipped = 0

    for question, answer, category in knowledge_data:

        cursor.execute("""
            SELECT id
            FROM knowledge_base
            WHERE LOWER(question) = LOWER(?)
        """, (question,))

        existing = cursor.fetchone()

        if existing:
            skipped += 1
            continue

        cursor.execute("""
            INSERT INTO knowledge_base
            (question, answer, category, status)
            VALUES (?, ?, ?, 'Active')
        """, (question, answer, category))

        added += 1

    connection.commit()
    connection.close()

    print()
    print("========================================")
    print(" AI UNIVERSITY KNOWLEDGE PACK")
    print("========================================")
    print(f"New entries added : {added}")
    print(f"Existing entries : {skipped}")
    print(f"Total entries    : {len(knowledge_data)}")
    print("========================================")
    print("Knowledge pack installed successfully.")
    print()


if __name__ == "__main__":
    create_knowledge_pack()