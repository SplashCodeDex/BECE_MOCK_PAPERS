#!/usr/bin/env python3
"""Ingest the 2026 user-supplied BECE Mathematics mock (0201026/27) into the bank.

Source: six photographed pages supplied by the user (Paper 2 Essay + Paper 1 Objective).
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
SOURCE_FILE = "user_mock_0201026-27_Mathematics_2026_photos"
SOURCE_NAME = "User-supplied BECE Mock 0201026/27 Mathematics (2026 photos)"
YEAR = 2026
SUBJECT = "Mathematics"
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
# Paper 2 — Essay (structured sub-questions). indicator_code pre-tagged.
# ---------------------------------------------------------------------------
PAPER2 = [
    {
        "qid": "P2_Q1a",
        "question_number": 1,
        "text": "(a) Convert the following and express your answers in standard form: (i) 31 days into minutes; (ii) 6 hours into seconds.",
        "indicator_code": "B9.1.1.1.1",
    },
    {
        "qid": "P2_Q1b",
        "question_number": 2,
        "text": "(b) Fred earns GH₵ 2500 a month after tax and Eben earns three times as much. How much is their total income after five years if there are no increases in their earnings?",
        "indicator_code": "B9.1.4.1.2",
    },
    {
        "qid": "P2_Q1c",
        "question_number": 3,
        "text": "(c) The following set of data were collected from an interview: 2, 3, (4m − 3), (3m + 1), 11, 13. If the median in ascending order is 6, find the value of m.",
        "indicator_code": "B9.4.1.2.2",
    },
    {
        "qid": "P2_Q1d",
        "question_number": 4,
        "text": "(d) The following are the marks obtained by 20 students in a class examination: 68, 42, 63, 57, 66, 54, 72, 58, 57, 73, 61, 54, 63, 45, 38, 40, 57, 58, 56, 48. (i) Arrange the marks above on a stem-and-leaf plot in ascending order. (ii) What is the mode? (iii) Determine the median.",
        "indicator_code": "B9.4.1.1.2",
    },
    {
        "qid": "P2_Q2a",
        "question_number": 5,
        "text": "(a) (i) Amina had 2½ litres of water and drank 1/3 litres of it. How many litres of water is she left with? (ii) Find 0.893 × 14.7, correct to 4 decimal places.",
        "indicator_code": "B9.1.3.1.1",
    },
    {
        "qid": "P2_Q2b",
        "question_number": 6,
        "text": "(b) The mean height of 28 students in a class is 162 cm. A new girl, whose height is 149 cm, joins the class. What is the new mean height of the class now?",
        "indicator_code": "B9.4.1.2.2",
    },
    {
        "qid": "P2_Q2c",
        "question_number": 7,
        "text": "(c) (i) Find x if (−3)^(x−2) = −243. (ii) The water consumption pattern of a community is given by 11^(4x−3). If x is in months, find correct to 4 significant figures, the total consumption after 2 months.",
        "indicator_code": "B9.1.2.1.1",
    },
    {
        "qid": "P2_Q2d",
        "question_number": 8,
        "text": "(d) The table below shows the number of marbles students sent to class for a Mathematics lesson. Number of marbles (x): 1, 2, 3, 4, 5, 6. Number of students (f): 4, 5, —, 9, —, 2. f(x): —, —, 42, —, 30, 12. (i) Copy and complete the table. (ii) How many students were in the class? (iii) How many marbles were brought altogether? (iv) What is the highest number of marbles brought by a student?",
        "indicator_code": "B9.4.1.2.2",
    },
    {
        "qid": "P2_Q3a",
        "question_number": 9,
        "text": "(a) In a day, Mark earns GH₵ 8.25 per hour working for 8 hours. He also earns overtime pay, which is 1½ times his regular rate of GH₵ 8.25 for 4 hours. How much pay does he earn altogether in a day?",
        "indicator_code": "B9.1.4.1.2",
    },
    {
        "qid": "P2_Q3b",
        "question_number": 10,
        "text": "(b) Triangle QPR is a right-angled triangle with the right angle at R. QR = 6 cm and PR = 8 cm. The angle at Q is θ. Find (i) |PQ| (ii) tan θ.",
        "indicator_code": "B9.3.1.1.2",
    },
    {
        "qid": "P2_Q3c",
        "question_number": 11,
        "text": "(c) Find the truth set of 6 ≥ 2 − 3x and represent your result on the number line.",
        "indicator_code": "B9.2.3.1.2",
    },
    {
        "qid": "P2_Q3d",
        "question_number": 12,
        "text": "(d) Find the area of a semi-circle whose radius is 7 cm. [Take π = 22/7]",
        "indicator_code": "B9.3.2.1.2",
    },
    {
        "qid": "P2_Q4a",
        "question_number": 13,
        "text": "(a) The numbers of pupils in a primary school is given in the table below. Class One: 35, Two: 45, Three: 24, Four: 33, Five: 23, Six: 20. (i) Draw a pie chart for the data. (ii) What fraction of the pupils are in primary two? (iii) Calculate the percentage of pupils in primary three, four and five altogether, correct to 2 decimal places.",
        "indicator_code": "B9.4.1.1.2",
    },
    {
        "qid": "P2_Q4b",
        "question_number": 14,
        "text": "(b) A straight line has a gradient of 7 and passes through the point P(−2, −3). Find (i) the equation of the line; (ii) the value of k if the point R(k, 4) lies on the line.",
        "indicator_code": "B9.2.1.1.1",
    },
    {
        "qid": "P2_Q4c",
        "question_number": 15,
        "text": "(c) Evaluate 2/3 × 1/4 + 2/5 ÷ 14/15",
        "indicator_code": "B9.1.3.1.2",
    },
    {
        "qid": "P2_Q4d",
        "question_number": 16,
        "text": "(d) The distance from village A to village B is (x + 2) km and the distance from village C to village D is (2x + 1) km. If these distances represent the length and breadth of a rectangular route around the villages, and the total perimeter of the route is 48 km, calculate the value of x.",
        "indicator_code": "B9.2.2.1.4",
    },
    {
        "qid": "P2_Q5a",
        "question_number": 17,
        "text": "(a) In a pen bag, 5 are red, 3 are blue and 2 are green. (i) What is the probability of picking a red pen? (ii) Express the probability of picking a blue pen as a (α) decimal; (β) percentage; (γ) ratio. (iii) If 2 pens are picked in succession without replacement, what is the probability that both are green?",
        "indicator_code": "B9.4.2.1.1",
    },
    {
        "qid": "P2_Q5b",
        "question_number": 18,
        "text": "(b) Asamoah left Takoradi at 11:13 am and got to Tema at 3:08 pm. How long did the journey take?",
        "indicator_code": "B9.1.2.2.2",
    },
    {
        "qid": "P2_Q5c",
        "question_number": 19,
        "text": "(c) If a water pump delivers 20 gallons of water per minute and Kofi can only afford half an hour cost of pumping water to a polytank, how many gallons of water will be pumped into the tank?",
        "indicator_code": "B9.1.4.1.3",
    },
    {
        "qid": "P2_Q5d",
        "question_number": 20,
        "text": "(d) In a market of 36 fishmongers, 28 sell mackerel, 18 sell tilapia and 13 of them sell both. (i) Represent this information on a Venn diagram. (ii) How many in the market are not selling any of the two fishes?",
        "indicator_code": "B9.1.1.2.2",
    },
    {
        "qid": "P2_Q6a",
        "question_number": 21,
        "text": "(a) Find the area of the shaded region in the figure below. A large rectangle has length (5x + 8) and width (6x + 2). Inside it is a smaller unshaded rectangle with length (x + 6) and width (5x).",
        "indicator_code": "B9.2.2.1.4",
    },
    {
        "qid": "P2_Q6b",
        "question_number": 22,
        "text": "(b) Solve 4/(3x) = 7 − 3/x",
        "indicator_code": "B9.2.3.1.1",
    },
    {
        "qid": "P2_Q6c",
        "question_number": 23,
        "text": "(c) Simplify (25x^(-4)) / (5^(-3) × 10x × t^(-8))",
        "indicator_code": "B9.2.2.1.4",
    },
    {
        "qid": "P2_Q6d",
        "question_number": 24,
        "text": "(d) a = (−4, p) and b = (q, 1). Given a + b = (−1, −8), find the value of p and q.",
        "indicator_code": "B9.3.2.2.2",
    },
]

# ---------------------------------------------------------------------------
# Paper 1 — Objective (40 MCQs)
# ---------------------------------------------------------------------------
PAPER1 = [
    {
        "question_number": 1,
        "text": "Find the value of 124.3 + 0.275 + 74.06, correct to one decimal place.",
        "option_a": "198.6",
        "option_b": "198.7",
        "option_c": "892.0",
        "option_d": "892.4",
        "correct_answer": "A",
        "indicator_code": "B9.1.2.2.1",
    },
    {
        "question_number": 2,
        "text": "Solve the inequality: 2x + 1 > 9.",
        "option_a": "x > 3",
        "option_b": "x > 4",
        "option_c": "x > 2",
        "option_d": "x > 1",
        "correct_answer": "B",
        "indicator_code": "B9.2.3.1.1",
    },
    {
        "question_number": 3,
        "text": "A football match starts at 1:20 pm and lasts for 1 hour 50 minutes. At what time will the match end?",
        "option_a": "4:10 pm",
        "option_b": "5:10 pm",
        "option_c": "3:10 pm",
        "option_d": "6:10 pm",
        "correct_answer": "C",
        "indicator_code": "B9.1.2.2.2",
    },
    {
        "question_number": 4,
        "text": "The sum of three consecutive odd integers is 33. Find the numbers.",
        "option_a": "9, 11 and 13",
        "option_b": "7, 9 and 11",
        "option_c": "11, 13 and 15",
        "option_d": "13, 15 and 17",
        "correct_answer": "A",
        "indicator_code": "B9.2.3.1.3",
    },
    {
        "question_number": 5,
        "text": "If the area of a circle is 64π, what is the circumference of the circle?",
        "option_a": "8π",
        "option_b": "16π",
        "option_c": "32π",
        "option_d": "64π",
        "correct_answer": "B",
        "indicator_code": "B9.3.2.1.2",
    },
    {
        "question_number": 6,
        "text": "9 men can complete a piece of work in 51 days. In how many days will 17 men of the same strength finish the same work?",
        "option_a": "29 days",
        "option_b": "31 days",
        "option_c": "27 days",
        "option_d": "37 days",
        "correct_answer": "C",
        "indicator_code": "B9.1.4.1.3",
    },
    {
        "question_number": 7,
        "text": "The mean of the numbers 5, 8, 4, 7 and 2x is 6. Find x.",
        "option_a": "6",
        "option_b": "4",
        "option_c": "3",
        "option_d": "2",
        "correct_answer": "C",
        "indicator_code": "B9.4.1.2.2",
    },
    {
        "question_number": 8,
        "text": "Kojo's age in the next 10 years will be 4 times his age 5 years ago. How old is Kojo now?",
        "option_a": "5",
        "option_b": "6",
        "option_c": "10",
        "option_d": "15",
        "correct_answer": "D",
        "indicator_code": "B9.2.3.1.3",
    },
    {
        "question_number": 9,
        "text": "Which of the following is not equivalent to 3 × 3 × 3 × 3 × 3 × 3?",
        "option_a": "3^6",
        "option_b": "18",
        "option_c": "9^3",
        "option_d": "729",
        "correct_answer": "B",
        "indicator_code": "B9.1.2.1.1",
    },
    {
        "question_number": 10,
        "text": "Find the value of 12x + 9q when x = 11 and q = 3.",
        "option_a": "148",
        "option_b": "159",
        "option_c": "168",
        "option_d": "172",
        "correct_answer": "C",
        "indicator_code": "B9.2.2.1.2",
    },
    {
        "question_number": 11,
        "text": "What is the locus of points that are a fixed distance from a given point?",
        "option_a": "A straight line",
        "option_b": "A circle",
        "option_c": "An arc",
        "option_d": "A rectangle",
        "correct_answer": "B",
        "indicator_code": "B9.3.1.2.1",
    },
    {
        "question_number": 12,
        "text": "If n/100 = 10.5, find the value of n.",
        "option_a": "0.0105",
        "option_b": "0.105",
        "option_c": "1050",
        "option_d": "105",
        "correct_answer": "C",
        "indicator_code": "B9.1.3.1.1",
    },
    {
        "question_number": 13,
        "text": "A is the point with coordinates (2, 3). If vector AB = (5, −4), find the coordinates of B.",
        "option_a": "(7, −1)",
        "option_b": "(−3, 7)",
        "option_c": "(3, −7)",
        "option_d": "(5, 4)",
        "correct_answer": "A",
        "indicator_code": "B9.3.2.1.4",
    },
    {
        "question_number": 14,
        "text": "Evaluate: (0.07 × 0.02) ÷ 14",
        "option_a": "0.01",
        "option_b": "0.001",
        "option_c": "0.0001",
        "option_d": "0.011",
        "correct_answer": "C",
        "indicator_code": "B9.1.2.2.1",
    },
    {
        "question_number": 15,
        "text": "Which of the following sets is the largest?",
        "option_a": "{whole numbers}",
        "option_b": "{composite numbers}",
        "option_c": "{natural numbers}",
        "option_d": "{integers}",
        "correct_answer": "D",
        "indicator_code": "B9.1.1.2.1",
    },
    {
        "question_number": 16,
        "text": "Sam has 5xy toffees and Joe has 20xy toffees. How many more toffees has Joe?",
        "option_a": "15xy",
        "option_b": "15x",
        "option_c": "15y",
        "option_d": "4xy",
        "correct_answer": "A",
        "indicator_code": "B9.2.2.1.4",
    },
    {
        "question_number": 17,
        "text": "Which of the following could be used to find x in the diagram below? A rectangle has total length 9.7 cm along the top. The bottom edge is made of three parts: 2.1 cm, x cm and 3.4 cm.",
        "option_a": "Add 2.1 and 3.4, then subtract the sum from 9.7",
        "option_b": "Add 9.7 and 3.4, then subtract 2.1 from the sum",
        "option_c": "Subtract 2.1 from 3.4, then subtract the difference from 9.7",
        "option_d": "Subtract 3.4 from 9.7, then add 2.1 to the difference",
        "correct_answer": "A",
        "indicator_code": "B9.2.2.1.4",
        "has_diagram": 1,
    },
    {
        "question_number": 18,
        "text": "Find the solution set of the inequality 5 − 5(3 − y) ≤ 65, if y is one of the first 6 multiples of 5.",
        "option_a": "{y: y = 5, 10, 15}",
        "option_b": "{y: y = 5, 10}",
        "option_c": "{y: y = 5, 10, 15, 20}",
        "option_d": "{y: y = 5, 10, 15, 20, 25, 30}",
        "correct_answer": "C",
        "indicator_code": "B9.2.3.1.1",
    },
    {
        "question_number": 19,
        "text": "Mina is x years old now. How old will she be in 10 + y years?",
        "option_a": "(x − 10 + y) years",
        "option_b": "(x − 10 − y) years",
        "option_c": "(x + 10 + y) years",
        "option_d": "(x + 10 − y) years",
        "correct_answer": "C",
        "indicator_code": "B9.2.2.1.4",
    },
    {
        "question_number": 20,
        "text": "A line passes through (1, 2) and (4, y). What is the value of y if the gradient is −2?",
        "option_a": "4",
        "option_b": "−2",
        "option_c": "0",
        "option_d": "−4",
        "correct_answer": "D",
        "indicator_code": "B9.1.4.1.4",
    },
    {
        "question_number": 21,
        "text": "If vector AB = (3, 5) and vector AC = (−4, 5), find vector BC.",
        "option_a": "(7, 10)",
        "option_b": "(−7, −10)",
        "option_c": "(7, −10)",
        "option_d": "(−7, 0)",
        "correct_answer": "D",
        "indicator_code": "B9.3.2.2.2",
    },
    {
        "question_number": 22,
        "text": "A line passes through points (2, 6) and (4, 12). Find the constant of proportionality.",
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "6",
        "correct_answer": "C",
        "indicator_code": "B9.1.4.1.1",
    },
    {
        "question_number": 23,
        "text": "A van travels 154 km in 1¾ hours. Find its speed in km/h.",
        "option_a": "77 km/h",
        "option_b": "88 km/h",
        "option_c": "100 km/h",
        "option_d": "269 km/h",
        "correct_answer": "B",
        "indicator_code": "B9.1.4.1.3",
    },
    {
        "question_number": 24,
        "text": "A hall which is 20 m long is represented on a diagram as 10 cm long. What is the scale of the diagram?",
        "option_a": "1:200",
        "option_b": "1:250",
        "option_c": "1:400",
        "option_d": "1:500",
        "correct_answer": "A",
        "indicator_code": "B9.3.2.1.1",
    },
    {
        "question_number": 25,
        "text": "If 13x − 12 = 5x + 60, find x.",
        "option_a": "−9",
        "option_b": "−6",
        "option_c": "9",
        "option_d": "6",
        "correct_answer": "C",
        "indicator_code": "B9.2.3.1.1",
    },
    {
        "question_number": 26,
        "text": "Order the fractions 3/8, 1/2, 5/16 from the smallest to the largest.",
        "option_a": "3/8 < 1/2 < 5/16",
        "option_b": "1/2 < 3/8 < 5/16",
        "option_c": "5/16 < 3/8 < 1/2",
        "option_d": "1/2 < 5/16 < 3/8",
        "correct_answer": "C",
        "indicator_code": "B9.1.3.1.1",
    },
    {
        "question_number": 27,
        "text": "In the triangle below, XY = YZ and angle XYZ = 42°. Find angle YXZ.",
        "option_a": "138°",
        "option_b": "59°",
        "option_c": "42°",
        "option_d": "69°",
        "correct_answer": "B",
        "indicator_code": "B9.3.1.1.1",
        "has_diagram": 1,
    },
    {
        "question_number": 28,
        "text": "The mean of ten numbers is 58. One of the numbers is 40. What is the mean of the other nine?",
        "option_a": "54",
        "option_b": "56",
        "option_c": "58",
        "option_d": "60",
        "correct_answer": "D",
        "indicator_code": "B9.4.1.2.2",
    },
    {
        "question_number": 29,
        "text": "The population of pigs in a certain farm is 5(2x − 3), where x is in months. Find the population of the pigs in the farm after 4 months.",
        "option_a": "52",
        "option_b": "25",
        "option_c": "30",
        "option_d": "15",
        "correct_answer": "B",
        "indicator_code": "B9.2.2.1.2",
    },
    {
        "question_number": 30,
        "text": "Angle MON and angle PMO are",
        "option_a": "vertically opposite angles",
        "option_b": "alternate angles",
        "option_c": "corresponding angles",
        "option_d": "adjacent angles",
        "correct_answer": "B",
        "indicator_code": "B9.3.1.1.1",
        "has_diagram": 1,
    },
    {
        "question_number": 31,
        "text": "Find the angle MON.",
        "option_a": "48°",
        "option_b": "52°",
        "option_c": "58°",
        "option_d": "65°",
        "correct_answer": "B",
        "indicator_code": "B9.3.1.1.1",
        "has_diagram": 1,
    },
    {
        "question_number": 32,
        "text": "A fly weighs 0.1 kg. How much would 112 flies weigh combined?",
        "option_a": "1.12 kg",
        "option_b": "112 kg",
        "option_c": "11.2 kg",
        "option_d": "0.112 kg",
        "correct_answer": "C",
        "indicator_code": "B9.1.2.2.1",
    },
    {
        "question_number": 33,
        "text": "The population growth of a given town is given by 2^(2m) where m is in years. Find the time needed for the population to be 4^14.",
        "option_a": "7",
        "option_b": "21",
        "option_c": "14",
        "option_d": "28",
        "correct_answer": "C",
        "indicator_code": "B9.1.2.1.1",
    },
    {
        "question_number": 34,
        "text": "Which of the following is an example of numerical data?",
        "option_a": "Eye color",
        "option_b": "Height in metres",
        "option_c": "Type of car",
        "option_d": "Favourite food",
        "correct_answer": "B",
        "indicator_code": "B9.4.1.1.1",
    },
    {
        "question_number": 35,
        "text": "The graph below represents the heights a walker reached during a long trail. Which section of the graph shows the steepest positive gradient?",
        "option_a": "Section A",
        "option_b": "Section B",
        "option_c": "Section H",
        "option_d": "Section F",
        "correct_answer": "B",
        "indicator_code": "B9.1.4.1.4",
        "has_diagram": 1,
    },
    {
        "question_number": 36,
        "text": "The graph below represents the heights a walker reached during a long trail. Which section of the graph shows the shallowest positive gradient?",
        "option_a": "Section A",
        "option_b": "Section B",
        "option_c": "Section F",
        "option_d": "Section G",
        "correct_answer": "C",
        "indicator_code": "B9.1.4.1.4",
        "has_diagram": 1,
    },
    {
        "question_number": 37,
        "text": "The graph below represents the heights a walker reached during a long trail. In which section of the graph is the gradient zero?",
        "option_a": "Section A",
        "option_b": "Section B",
        "option_c": "Section D",
        "option_d": "Section E",
        "correct_answer": "C",
        "indicator_code": "B9.1.4.1.4",
        "has_diagram": 1,
    },
    {
        "question_number": 38,
        "text": "Given that P = (3x − 6, 2y + 5), R = (9, 7) and P = R, find the values of x and y.",
        "option_a": "x = 1 and y = 5",
        "option_b": "x = −5 and y = −1",
        "option_c": "x = 5 and y = 1",
        "option_d": "x = −1 and y = 5",
        "correct_answer": "C",
        "indicator_code": "B9.3.2.1.4",
    },
    {
        "question_number": 39,
        "text": "Solve for x in the equation 15 − 2x = 6.",
        "option_a": "−10.5",
        "option_b": "−4.5",
        "option_c": "4.5",
        "option_d": "10.5",
        "correct_answer": "C",
        "indicator_code": "B9.2.3.1.1",
    },
    {
        "question_number": 40,
        "text": "A baker has 12 identical cakes. In how many different ways can he divide them up into equal packets?",
        "option_a": "4",
        "option_b": "5",
        "option_c": "6",
        "option_d": "7",
        "correct_answer": "C",
        "indicator_code": "B9.1.2.1.4",
    },
]


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")

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
            "W:/Downloads/20261019_055637.jpg (+5 sibling photos)",
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
            raw_id = f"{SOURCE_FILE}_P2_q{item['question_number']}"
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
                # keep best: ensure indicator is filled
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
                    ) VALUES (?, ?, ?, '', '', '', '', '', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        qid,
                        SUBJECT,
                        item["text"],
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
            raw_id = f"{SOURCE_FILE}_P1_q{item['question_number']}"
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

    out = Path(r"W:\StaralexSchoolStudies\BECE_MOCK_PAPERS\data\extracted_questions\mock_0201026_2026_ingest.json")
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
