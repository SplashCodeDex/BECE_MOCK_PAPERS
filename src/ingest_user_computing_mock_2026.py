#!/usr/bin/env python3
"""Ingest the 2026 user-supplied BECE Computing mock (0201026/27) into the bank.

Source: ten photographed pages supplied by the user (Paper 1 Objective 1-40 + Paper 2 Essay Q1-5).
Writes extracted_questions + canonical questions + question_occurrences, then rebuilds FTS.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"W:\StaralexSchoolStudies\BECE_MOCK_PAPERS\data\metadata\catalog.db")
SOURCE_FILE = "user_mock_0201026-27_Computing_ICT_2026_photos"
SOURCE_NAME = "User-supplied BECE Mock 0201026/27 Computing (2026 photos)"
YEAR = 2026
SUBJECT = "Computing_ICT"
NOW = datetime.now(timezone.utc).isoformat()


def norm(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def dedup_hash(subject: str, text: str, paper_type: str, options: dict) -> str:
    parts = [text]
    if "objective" in (paper_type or "").lower():
        parts += [options.get(c) or "" for c in "abcd"]
    joined = norm(" ".join(parts))
    payload = f"{subject.lower().strip()}|{joined}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# Paper 1 — Objective (40 MCQs). indicator_code pre-tagged per NaCCA mapping.
# ---------------------------------------------------------------------------
PAPER1 = [
    {"question_number": 1, "text": "A group of files is stored in a", "option_a": "graphic", "option_b": "folder", "option_c": "text", "option_d": "word", "correct_answer": "B", "indicator_code": "B7.1.1.2.2"},
    {"question_number": 2, "text": "The act of gaining unauthorized access to computer systems is called", "option_a": "encryption.", "option_b": "hacking.", "option_c": "debugging.", "option_d": "firewalling.", "correct_answer": "B", "indicator_code": "B9.3.3.1.2"},
    {"question_number": 3, "text": "Which layer of the OSI model is responsible for routing and forwarding?", "option_a": "Physical", "option_b": "Data Link", "option_c": "Network", "option_d": "Transport", "correct_answer": "C", "indicator_code": "B8.3.1.1.1"},
    {"question_number": 4, "text": "You can search for an exact phrase when searching the web by", "option_a": "use of an asterisk (*).", "option_b": "searching the web for information by using quotation marks (\"\").", "option_c": "using quotation marks (\"\").", "option_d": "typing a question mark (?).", "correct_answer": "C", "indicator_code": "B8.3.4.1.1"},
    {"question_number": 5, "text": "The robotic club of Zuarungu JHS is to construct a robot with the ability to detect objects around it. The most appropriate sensor to be used is", "option_a": "light sensor.", "option_b": "tactile sensor.", "option_c": "torque sensor.", "option_d": "proximity sensor.", "correct_answer": "D", "indicator_code": "B9.4.3.1.1"},
    {"question_number": 6, "text": "The acronym RFID stands for", "option_a": "Random File Integration Device.", "option_b": "Radio Frequency Identification.", "option_c": "Rapid Frequency Interference Detection.", "option_d": "Remote File Interaction Device.", "correct_answer": "B", "indicator_code": "B8.1.1.1.2"},
    {"question_number": 7, "text": "Which of the following is a disadvantage of portable computing devices?", "option_a": "Portability", "option_b": "Limited battery", "option_c": "Multitasking", "option_d": "Compact size", "correct_answer": "B", "indicator_code": "B8.1.2.1.2"},
    {"question_number": 8, "text": "Which of the following is an example of assistive technology?", "option_a": "Keyboard", "option_b": "Screen reader", "option_c": "Bluetooth speaker", "option_d": "Selfie stick", "correct_answer": "B", "indicator_code": "B8.1.2.1.1"},
    {"question_number": 9, "text": "If you want to count how many cells in a range contain numbers, which function would you use?", "option_a": "COUNTA", "option_b": "COUNT", "option_c": "COUNTIF", "option_d": "SUM", "correct_answer": "B", "indicator_code": "B8.2.4.1.1"},
    {"question_number": 10, "text": "A publishing company wants to produce a storybook that visually impaired children can read using their fingertips. Which type of printer is able to produce tactile output?", "option_a": "Inkjet Printer", "option_b": "Thermal printer", "option_c": "Braille printer", "option_d": "3D printer", "correct_answer": "C", "indicator_code": "B8.1.1.1.3"},
    {"question_number": 11, "text": "The protection method which ensures that only authorized persons can access certain information is", "option_a": "authorization.", "option_b": "authentication.", "option_c": "encryption.", "option_d": "decryption.", "correct_answer": "A", "indicator_code": "B8.3.3.1.2"},
    {"question_number": 12, "text": "What type of attack occurs when an unauthorized person reads or listens to private information?", "option_a": "Interruption", "option_b": "Interception", "option_c": "Modification", "option_d": "Fabrication", "correct_answer": "B", "indicator_code": "B8.3.3.1.1"},
    {"question_number": 13, "text": "Which of the following contributes to the environmental impact of computers?", "option_a": "Minimal power consumption", "option_b": "Short product life cycle", "option_c": "Efficient use of resources", "option_d": "Short manufacturing processes", "correct_answer": "B", "indicator_code": "B7.1.2.1.4"},
    {"question_number": 14, "text": "The default page size in Microsoft Word is", "option_a": "Letter.", "option_b": "A4.", "option_c": "Legal.", "option_d": "Executive.", "correct_answer": "B", "indicator_code": "B8.2.1.1.3"},
    {"question_number": 15, "text": "To find BBC articles about climate change on the BBC website, the search query you would NOT use is", "option_a": "bbc.com climate change", "option_b": "\"bbc.com\"", "option_c": "bbc.com climate change", "option_d": "NOT bbc.com climate change", "correct_answer": "", "indicator_code": "B8.3.4.1.1", "note": "options transcription uncertain (photo blurry); left for review"},
    {"question_number": 16, "text": "Generating fake data to deceive users or systems is termed", "option_a": "duplication.", "option_b": "fabrication.", "option_c": "infringement.", "option_d": "modification.", "correct_answer": "B", "indicator_code": "B8.3.3.1.1"},
    {"question_number": 17, "text": "How many layers are in the OSI model?", "option_a": "5", "option_b": "6", "option_c": "7", "option_d": "8", "correct_answer": "C", "indicator_code": "B8.3.1.1.1"},
    {"question_number": 18, "text": "During a computing lesson, a student presses a shortcut key and a picture of the entire desktop appears on the current slide. In PowerPoint, a captured image of your screen displayed in a slide is a", "option_a": "slideshow.", "option_b": "screenshot.", "option_c": "snapshot.", "option_d": "template.", "correct_answer": "B", "indicator_code": "B9.2.2.1.1"},
    {"question_number": 19, "text": "Which Boolean operator would you use to find webpages containing both \"Ghana\" and \"Accra\"?", "option_a": "OR", "option_b": "NOT", "option_c": "AND", "option_d": "THEN", "correct_answer": "C", "indicator_code": "B8.3.4.1.1"},
    {"question_number": 20, "text": "Which component of a robot serves as its \"brain\"?", "option_a": "Sensors", "option_b": "Controller", "option_c": "Mechanical system", "option_d": "Wheels", "correct_answer": "B", "indicator_code": "B8.4.3.1.1"},
    {"question_number": 21, "text": "A student typing a report wants to arrange his data into neat rows and columns rather than plain paragraphs. Which set of actions will add a table to a Word document?", "option_a": "Click on Insert tab, select Table", "option_b": "Click on Home tab, select Table", "option_c": "Click on Layout tab, select Table", "option_d": "Click on Design tab, select Table", "correct_answer": "A", "indicator_code": "B7.2.1.1.2"},
    {"question_number": 22, "text": "Calculate the result of the expression (18 - 6) - 5 + 4^2 / 8 * 3 using the order of operations.", "option_a": "7", "option_b": "13", "option_c": "18", "option_d": "21", "correct_answer": "B", "indicator_code": "B8.4.2.1.1"},
    {"question_number": 23, "text": "Which layer of the OSI model ensures data is presented in a readable format for the application layer?", "option_a": "Application", "option_b": "Presentation", "option_c": "Session", "option_d": "Transport", "correct_answer": "B", "indicator_code": "B8.3.1.1.1"},
    {"question_number": 24, "text": "Retrieving encrypted information and restoring it to its original state is termed", "option_a": "encoding.", "option_b": "decryption.", "option_c": "transmission.", "option_d": "encryption.", "correct_answer": "B", "indicator_code": "B8.3.3.1.2"},
    {"question_number": 25, "text": "To narrow down results by date, language and region using a search engine, use", "option_a": "Basic Search.", "option_b": "Simple Search.", "option_c": "Quick Search.", "option_d": "Advanced Search.", "correct_answer": "D", "indicator_code": "B8.3.4.1.1"},
    {"question_number": 26, "text": "Which storage device is known for being robust and resistant to physical shocks?", "option_a": "Hard Disk Drive", "option_b": "Solid State Drive", "option_c": "Optical Drive", "option_d": "Magnetic Tape", "correct_answer": "B", "indicator_code": "B8.1.1.1.4"},
    {"question_number": 27, "text": "Maintaining the accuracy and reliability of data over its entire life cycle constitutes data", "option_a": "monopoly.", "option_b": "availability.", "option_c": "integrity.", "option_d": "confidentiality.", "correct_answer": "C", "indicator_code": "B7.3.3.1.1"},
    {"question_number": 28, "text": "Which Boolean operator would you use to find webpages about \"cars\" but exclude \"trucks\"?", "option_a": "AND", "option_b": "OR", "option_c": "NOT", "option_d": "PLUS", "correct_answer": "C", "indicator_code": "B8.3.4.1.1"},
    {"question_number": 29, "text": "One key feature of robot intelligence is the", "option_a": "unlimited memory.", "option_b": "ability to perform tasks autonomously.", "option_c": "access to social media.", "option_d": "absence of power requirements.", "correct_answer": "B", "indicator_code": "B9.4.3.1.1"},
    {"question_number": 30, "text": "Which type of storage device is most likely to be used in a smartphone?", "option_a": "Hard Disk Drive (HDD)", "option_b": "Solid State Drive (SSD)", "option_c": "Embedded Flash Memory", "option_d": "Optical Drive", "correct_answer": "C", "indicator_code": "B8.1.1.1.4"},
    {"question_number": 31, "text": "A teacher wants to count only the students in a list who scored above 50 marks, not just any numeric cell. Which function is used to count cells that meet a specific condition in a list?", "option_a": "COUNT", "option_b": "COUNTA", "option_c": "SUM", "option_d": "COUNTIF", "correct_answer": "D", "indicator_code": "B8.2.4.1.1"},
    {"question_number": 32, "text": "What type of processing is a key feature of Fifth-Generation computers?", "option_a": "Batch processing", "option_b": "Parallel processing", "option_c": "Time-sharing", "option_d": "Sequential processing", "correct_answer": "B", "indicator_code": "B8.1.1.1.1"},
    {"question_number": 33, "text": "The act of sending fraudulent emails to obtain personal information is called", "option_a": "phishing.", "option_b": "debugging.", "option_c": "cracking.", "option_d": "encrypting.", "correct_answer": "A", "indicator_code": "B9.3.3.1.2"},
    {"question_number": 34, "text": "Which of the following is a built-in function in a spreadsheet program?", "option_a": "=D5+3", "option_b": "ADD(A1, B1)", "option_c": "=SUM(C1:C10)", "option_d": "TOTAL", "correct_answer": "C", "indicator_code": "B8.2.4.1.1"},
    {"question_number": 35, "text": "An architecture student wants to produce a physical three-dimensional model of a building she designed on her computer. Which type of printer is most suitable?", "option_a": "Impact printer", "option_b": "Inkjet printer", "option_c": "3D printer", "option_d": "Thermal printer", "correct_answer": "C", "indicator_code": "B8.1.1.1.3"},
    {"question_number": 36, "text": "The default starting number for page numbering in Word is", "option_a": "0.", "option_b": "1.", "option_c": "2.", "option_d": "3.", "correct_answer": "B", "indicator_code": "B8.2.1.1.3"},
    {"question_number": 37, "text": "The two main page orientations available in most documents are", "option_a": "landscape/centre.", "option_b": "portrait/centre.", "option_c": "justify/centre.", "option_d": "landscape/portrait.", "correct_answer": "D", "indicator_code": "B8.2.1.1.3"},
    {"question_number": 38, "text": "Which of the following is a good practice for reducing eye strain while using a computer?", "option_a": "Increasing screen brightness.", "option_b": "Using a screen protector.", "option_c": "Sitting very close to the screen.", "option_d": "Avoiding blinking.", "correct_answer": "B", "indicator_code": "B8.1.3.1.2", "note": "options transcription uncertain (photo blurry); glare-reducing screen protector is the intended answer; session recommends frequent breaks"},
    {"question_number": 39, "text": "Assignment statements are used in programming to", "option_a": "perform calculations.", "option_b": "assign a value to a variable.", "option_c": "check a condition.", "option_d": "print a message.", "correct_answer": "B", "indicator_code": "B8.4.2.1.1"},
    {"question_number": 40, "text": "When a hacker changes the content of a message before it reaches the receiver, it is called", "option_a": "interruption.", "option_b": "interception.", "option_c": "modification.", "option_d": "fabrication.", "correct_answer": "C", "indicator_code": "B8.3.3.1.1"},
]

# ---------------------------------------------------------------------------
# Paper 2 — Essay (structured sub-questions), indicator_code pre-tagged.
# ---------------------------------------------------------------------------
PAPER2 = [
    {"qid": "P2_Q1a_i", "question_number": 1, "text": "(a) A school is considering a digital system to track students' attendance. For this system, unique student ID cards will be scanned to capture and store each student's information. Each card shows the student's name, a card number, expiry date, and a series of black and white lines printed along the bottom edge, which a scanner can read directly into the computer. (i) Name the ID card feature described above that makes direct data entry of student information possible.", "indicator_code": "B8.1.1.1.2"},
    {"qid": "P2_Q1a_ii", "question_number": 1, "text": "(a)(ii) Which device could be used to capture student information from this feature?", "indicator_code": "B7.1.1.1.2"},
    {"qid": "P2_Q1a_iii", "question_number": 1, "text": "(a)(iii) An expert in computer systems has recommended using a Solid-State Drive to store the information captured from the ID cards. Give two reasons for this choice.", "indicator_code": "B8.1.1.1.4"},
    {"qid": "P2_Q1b_intro", "question_number": 2, "text": "(b) 1 SET mysteryNumber TO 6 / 2 SET correct TO False / 3 WHILE correct = False DO / 4 RECEIVE guess FROM (INTEGER) KEYBOARD / 5 IF guess = mysteryNumber THEN / 6 set correct to True / 7 END IF / 8 END WHILE. (i) Identify the three variables in the program.", "indicator_code": "B8.4.1.1.1"},
    {"qid": "P2_Q1b_ii", "question_number": 2, "text": "(b)(ii) State why each of the variables identified in (b)(i) above is used.", "indicator_code": "B8.4.1.1.1"},
    {"qid": "P2_Q1b_iii", "question_number": 2, "text": "(b)(iii) Write the lines of code that demonstrate the following in the algorithm: Sequence; Selection; Iteration.", "indicator_code": "B9.4.2.1.1"},
    {"qid": "P2_Q1c_i", "question_number": 3, "text": "(c) A school procures six pieces of assistive and adaptive technology equipment to support students living with disabilities: I: A small device worn behind the ear that makes sounds louder for someone hard of hearing; II: A tablet loaded with a picture-based app that helps a non-verbal student communicate; III: A strap-on handle that helps someone with a weak grip hold a spoon or fork; IV: An artificial limb that replaces a leg below the knee; V: A chair that helps someone with limited mobility move around; VI: A keyboard with raised dots that a visually impaired person can read by touch. (i) Name each of the devices described above in I to VI.", "indicator_code": "B8.1.2.1.1"},
    {"qid": "P2_Q1c_ii", "question_number": 3, "text": "(c)(ii) Classify each of the devices I to VI as either assistive or adaptive technology.", "indicator_code": "B8.1.2.1.1"},
    {"qid": "P2_Q1c_iii", "question_number": 3, "text": "(c)(iii) State one benefit of each of devices IV and V for the disabilities they support.", "indicator_code": "B8.1.2.1.1"},
    {"qid": "P2_Q2a_i", "question_number": 4, "text": "(a) Frimpong is trying to find the lyrics of a Ghanaian song, but only remembers part of one line: Ghana, the Black Star. How would you assist him to find the complete lyrics online using: (i) an exact phrase search;", "indicator_code": "B8.3.4.1.1"},
    {"qid": "P2_Q2a_ii", "question_number": 4, "text": "(a)(ii) a wildcard operator?", "indicator_code": "B8.3.4.1.1"},
    {"qid": "P2_Q2b", "question_number": 5, "text": "(b) A school wants to keep learning outside class hours, using platforms they already spend time on. In what two ways can social media be beneficial in education?", "indicator_code": "B9.3.2.1.1"},
    {"qid": "P2_Q2c", "question_number": 6, "text": "(c) A group of volunteers working on a community project wants to record their decisions and share updates without needing everyone online at the same time. Outline two benefits of wikis and blogs for this kind of communication.", "indicator_code": "B9.3.4.1.1"},
    {"qid": "P2_Q2d", "question_number": 7, "text": "(d) A small business notices that some of its important customer emails never seem to reach the people they were sent to. Identify two threats that can prevent information from reaching its destination.", "indicator_code": "B9.3.3.1.2"},
    {"qid": "P2_Q3a", "question_number": 8, "text": "(a) While totaling her class's marks, Efuua's spreadsheet shows an unexpected message in a cell instead of a number. How does a formula error occur in a spreadsheet?", "indicator_code": "B8.2.4.1.1"},
    {"qid": "P2_Q3b_i", "question_number": 9, "text": "(b) As Efuua checks her worksheet more closely, she notices three different error messages appearing in different cells. Provide the meaning of the following formula errors: (i) #DIV/0!;", "indicator_code": "B8.2.4.1.1"},
    {"qid": "P2_Q3b_ii", "question_number": 9, "text": "(b)(ii) #REF!;", "indicator_code": "B8.2.4.1.1"},
    {"qid": "P2_Q3b_iii", "question_number": 9, "text": "(b)(iii) ####.", "indicator_code": "B8.2.4.1.1"},
    {"qid": "P2_Q3c", "question_number": 10, "text": "(c) While writing a program to total his shopping bill, Kwame includes the expression 6 * 8 / 2 + (15 - 6) + 3 / 3. Calculate the result of this expression using the correct order of operations.", "indicator_code": "B8.4.2.1.1"},
    {"qid": "P2_Q3d", "question_number": 11, "text": "(d) A programmer names her variables x, y and z, instead of descriptive names like price or student_age. Give two reasons why variables should be given meaningful names when writing a program.", "indicator_code": "B8.4.1.1.1"},
    {"qid": "P2_Q4a", "question_number": 12, "text": "(a) A student writing a project report wants to add a clickable link in her Word document that takes readers directly to a related website. Outline the steps she would follow to create this hyperlink.", "indicator_code": "B9.2.1.1.3"},
    {"qid": "P2_Q4b", "question_number": 13, "text": "(b) A club needs to prepare a slide show for a meeting and also design a printed flyer for the same event. State two differences between the presentation software and the desktop publishing software the club would use for these two tasks.", "indicator_code": "B9.2.3.1.2"},
    {"qid": "P2_Q4c", "question_number": 14, "text": "(c) A student wants to keep his schoolwork and games organized separately, so he divides his hard disk into two visible drives. Explain the purpose of creating multiple partitions on a hard disk.", "indicator_code": "B8.1.1.2.2"},
    {"qid": "P2_Q4d", "question_number": 15, "text": "(d) A club member with no design experience is asked to create a professional-looking newsletter at short notice. Explain two advantages of using predesigned templates in desktop publishing software for this task.", "indicator_code": "B9.2.3.1.1"},
    {"qid": "P2_Q5a", "question_number": 16, "text": "(a) Explain the terms encryption and decryption as applied to data protection.", "indicator_code": "B8.3.3.1.2"},
    {"qid": "P2_Q5b", "question_number": 17, "text": "(b) What is social engineering?", "indicator_code": "B9.3.3.1.2"},
    {"qid": "P2_Q5c", "question_number": 18, "text": "(c) A school office needs to print multi-part carbon receipt forms for its records, while the reception desk prints short till-style slips instantly and quietly. State the main difference between an impact printer and a thermal printer.", "indicator_code": "B8.1.1.1.3"},
    {"qid": "P2_Q5d", "question_number": 19, "text": "(d) An office worker spends most of the day typing at a desk. Give two safety measures that can help ensure risk reduction at her workstation.", "indicator_code": "B8.1.3.1.2"},
]


def main() -> None:
    conn = sqlite3.connect(DB_PATH)

    # Source registry entry for this user-supplied mock.
    conn.execute(
        "INSERT OR IGNORE INTO sources (name, domain, source_type, acquisition, tos_notes, trusted) "
        "VALUES (?, ?, 'mock_compilation', 'user_photos', ?, 1);",
        (
            SOURCE_NAME,
            "local://user-supplied",
            "Private study use only. User-supplied photographed mock paper; not redistributed.",
        ),
    )
    source_id = conn.execute(
        "SELECT id FROM sources WHERE name = ?;", (SOURCE_NAME,)
    ).fetchone()[0]

    # harvested_files row so provenance joins resolve.
    conn.execute(
        "INSERT OR IGNORE INTO harvested_files "
        "(sha256, original_url, file_name, file_type, subject, file_size, local_path, source_domain, is_marking_scheme) "
        "VALUES (?, ?, ?, 'image', ?, 0, ?, ?, 0);",
        (
            hashlib.sha256(SOURCE_FILE.encode()).hexdigest(),
            "local://user-supplied/" + SOURCE_FILE,
            SOURCE_FILE + ".zip",
            SUBJECT,
            "W:/Downloads/20261021_004602.jpg (+9 sibling photos)",
            "local://user-supplied",
        ),
    )
    harvested_id = conn.execute(
        "SELECT id FROM harvested_files WHERE file_name = ?;", (SOURCE_FILE + ".zip",)
    ).fetchone()[0]

    stats = {"extracted": 0, "canonical_new": 0, "canonical_dupes": 0, "occurrences": 0}

    with conn:
        # ---- Paper 2 (essay / structured) ----
        for item in PAPER2:
            raw_id = f"{SOURCE_FILE}_P2_{item['qid']}"
            h = dedup_hash(SUBJECT, item["text"], "Paper 2 - Essay", {})
            qid = f"Q_{h[:12]}"

            conn.execute(
                """
                INSERT OR REPLACE INTO extracted_questions (
                    id, subject, year, paper_type, question_number, question_text,
                    option_a, option_b, option_c, option_d, correct_answer,
                    has_diagram, diagram_path, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, '', '', '', '', '', ?, ?, ?);
                """,
                (
                    raw_id,
                    SUBJECT,
                    YEAR,
                    "Paper 2 - Essay",
                    item["question_number"],
                    item["text"],
                    item.get("has_diagram", 0),
                    item.get("diagram_path"),
                    SOURCE_FILE,
                ),
            )
            stats["extracted"] += 1

            cur = conn.execute(
                "SELECT id FROM questions WHERE id = ?;", (qid,)
            ).fetchone()
            if cur:
                stats["canonical_dupes"] += 1
                conn.execute(
                    "UPDATE questions SET indicator_code = COALESCE(NULLIF(indicator_code,''), ?) WHERE id = ?;",
                    (item["indicator_code"], qid),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, subject, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, has_diagram, diagram_path, year, paper_type,
                        indicator_code, confidence, tag_method, dedup_hash, migrated_from, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        qid,
                        SUBJECT,
                        item["text"],
                        "",
                        "",
                        "",
                        "",
                        "",
                        item.get("has_diagram", 0),
                        item.get("diagram_path"),
                        YEAR,
                        "Paper 2 - Essay",
                        item["indicator_code"],
                        1.0,
                        "manual_mock_ingest_2026",
                        h,
                        raw_id,
                        NOW,
                    ),
                )
                stats["canonical_new"] += 1

            conn.execute(
                """
                INSERT OR IGNORE INTO question_occurrences (
                    question_id, original_id, source_file, harvested_file_id,
                    source_id, original_url, year, paper_type, question_number, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    qid,
                    raw_id,
                    SOURCE_FILE,
                    harvested_id,
                    source_id,
                    "local://user-supplied/" + SOURCE_FILE,
                    YEAR,
                    "Paper 2 - Essay",
                    item["question_number"],
                    NOW,
                ),
            )
            stats["occurrences"] += 1

        # ---- Paper 1 (objective) ----
        for item in PAPER1:
            raw_id = f"{SOURCE_FILE}_P1_q{item['question_number']}_v2"
            options = {
                "a": item["option_a"],
                "b": item["option_b"],
                "c": item["option_c"],
                "d": item["option_d"],
            }
            h = dedup_hash(SUBJECT, item["text"], "Paper 1 - Objective", options)
            qid = f"Q_{h[:12]}"

            conn.execute(
                """
                INSERT OR REPLACE INTO extracted_questions (
                    id, subject, year, paper_type, question_number, question_text,
                    option_a, option_b, option_c, option_d, correct_answer,
                    has_diagram, diagram_path, source_file
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    raw_id,
                    SUBJECT,
                    YEAR,
                    "Paper 1 - Objective",
                    item["question_number"],
                    item["text"],
                    item["option_a"],
                    item["option_b"],
                    item["option_c"],
                    item["option_d"],
                    item["correct_answer"],
                    item.get("has_diagram", 0),
                    item.get("diagram_path"),
                    SOURCE_FILE,
                ),
            )
            stats["extracted"] += 1

            cur = conn.execute(
                "SELECT id FROM questions WHERE id = ?;", (qid,)
            ).fetchone()
            if cur:
                stats["canonical_dupes"] += 1
                conn.execute(
                    "UPDATE questions SET indicator_code = COALESCE(NULLIF(indicator_code,''), ?), "
                    "correct_answer = COALESCE(NULLIF(correct_answer,''), ?) WHERE id = ?;",
                    (item["indicator_code"], item["correct_answer"], qid),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, subject, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, has_diagram, diagram_path, year, paper_type,
                        indicator_code, confidence, tag_method, dedup_hash, migrated_from, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        qid,
                        SUBJECT,
                        item["text"],
                        item["option_a"],
                        item["option_b"],
                        item["option_c"],
                        item["option_d"],
                        item["correct_answer"],
                        item.get("has_diagram", 0),
                        item.get("diagram_path"),
                        YEAR,
                        "Paper 1 - Objective",
                        item["indicator_code"],
                        1.0,
                        "manual_mock_ingest_2026",
                        h,
                        raw_id,
                        NOW,
                    ),
                )
                stats["canonical_new"] += 1

            conn.execute(
                """
                INSERT OR IGNORE INTO question_occurrences (
                    question_id, original_id, source_file, harvested_file_id,
                    source_id, original_url, year, paper_type, question_number, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    qid,
                    raw_id,
                    SOURCE_FILE,
                    harvested_id,
                    source_id,
                    "local://user-supplied/" + SOURCE_FILE,
                    YEAR,
                    "Paper 1 - Objective",
                    item["question_number"],
                    NOW,
                ),
            )
            stats["occurrences"] += 1

        conn.execute("INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');")

    # Export a local category map for the lesson pipeline.
    cat = {}
    for item in PAPER2:
        cat.setdefault(item["indicator_code"], []).append(
            {"ref": item["qid"], "paper": "P2", "text": item["text"][:80]}
        )
    for item in PAPER1:
        cat.setdefault(item["indicator_code"], []).append(
            {
                "ref": f"P1_Q{item['question_number']}",
                "paper": "P1",
                "text": item["text"][:80],
            }
        )

    out = Path(r"W:\StaralexSchoolStudies\BECE_MOCK_PAPERS\data\extracted_questions\mock_0201026_2026_computing_ingest.json")
    out.write_text(
        json.dumps(
            {
                "source_file": SOURCE_FILE,
                "year": YEAR,
                "stats": stats,
                "by_indicator": cat,
                "paper2": PAPER2,
                "paper1": PAPER1,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    conn.close()
    print("INGEST STATS:", stats)
    print("Category map written to", out)


if __name__ == "__main__":
    main()
