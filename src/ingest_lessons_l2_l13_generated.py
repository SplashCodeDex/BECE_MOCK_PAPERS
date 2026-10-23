#!/usr/bin/env python3
"""Add generated exercise questions from Lessons 2-13 into the BECE bank."""
from __future__ import annotations

import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(r"W:\StaralexSchoolStudies\BECE_MOCK_PAPERS\data\metadata\catalog.db")
YEAR = 2026
SUBJECT = "Mathematics"
NOW = datetime.now(timezone.utc).isoformat()
SOURCE_NAME = "Generated Staralex Lesson exercises L2-L13"


def norm(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# (lesson_slug, paper_type, indicator_code, question_text)
ITEMS = [
    # L2 Number Systems & Venn
    ("L2", "P1", "B9.1.1.2.1", "Which of these sets is the smallest? A. {whole numbers} B. {composite numbers} C. {natural numbers} D. {integers}"),
    ("L2", "P2", "B9.1.1.2.1", "Classify 5 under every family that fits (N, W, Z, Q)."),
    ("L2", "P2", "B9.1.1.2.1", "Classify -3 under every family that fits."),
    ("L2", "P2", "B9.1.1.2.1", "Classify 0 under every family that fits."),
    ("L2", "P2", "B9.1.1.2.1", "Is 0.25 rational? Give a reason."),
    ("L2", "P2", "B9.1.1.2.1", "Is the square root of 9 rational? Give a reason."),
    ("L2", "P2", "B9.1.1.2.1", "Is the square root of 7 rational or irrational?"),
    ("L2", "P2", "B9.1.1.2.1", "Write 0.333... as a fraction; hence show it is rational."),
    ("L2", "P2", "B9.1.1.2.2", "U = {1,2,3,4,5,6}, A = {1,2}. Find A complement."),
    ("L2", "P2", "B9.1.1.2.2", "Let X = {2,4,6}, Y = {4,6,8}. Find X intersection Y."),
    ("L2", "P2", "B9.1.1.2.2", "Let X = {2,4,6}, Y = {4,6,8}. Find X union Y."),
    ("L2", "P2", "B9.1.1.2.2", "In a class of 40, 22 play football, 18 play hockey, 9 play both. How many play neither?"),
    ("L2", "P2", "B9.1.1.2.2", "In a survey of 200 people, 120 like tea, 90 like coffee, and 40 like both. How many like neither?"),
    ("L2", "P2", "B9.1.1.2.2", "In a school of 180 pupils, 100 study French, 80 study Twi, and 30 study both. How many study neither?"),
    ("L2", "P2", "B9.1.1.2.2", "Write the set of even numbers between 1 and 11 in curly-bracket notation."),
    ("L2", "P2", "B9.1.1.2.2", "List all elements of {x : x is a factor of 12}."),
    # L3 Indices & Decimals
    ("L3", "P2", "B9.1.2.1.1", "Simplify 2^3 x 2^4."),
    ("L3", "P2", "B9.1.2.1.1", "Simplify 5^6 divided by 5^2."),
    ("L3", "P2", "B9.1.2.1.1", "Simplify (3^2)^3."),
    ("L3", "P2", "B9.1.2.1.1", "Write 2^{-3} as a fraction."),
    ("L3", "P2", "B9.1.2.1.1", "Solve 2^{x+1} = 2^5."),
    ("L3", "P2", "B9.1.2.1.1", "Solve 5^{2x} = 5^6."),
    ("L3", "P2", "B9.1.2.1.1", "Write 3^6 as a power of 9."),
    ("L3", "P2", "B9.1.2.1.1", "Write 4^5 as a power of 2."),
    ("L3", "P2", "B9.1.2.2.1", "Evaluate 15.07 - 3.285."),
    ("L3", "P2", "B9.1.2.2.1", "Evaluate 4.86 divided by 0.3."),
    ("L3", "P2", "B9.1.2.2.2", "Convert 3 hours 20 minutes into minutes."),
    ("L3", "P2", "B9.1.2.2.2", "A bus leaves at 06:45 and arrives at 10:20. How long is the trip?"),
    ("L3", "P2", "B9.1.2.1.4", "List all positive factors of 18."),
    ("L3", "P2", "B9.1.2.1.4", "A class of 36 pupils is split into equal groups. List all possible group sizes greater than 1."),
    ("L3", "P2", "B9.1.2.2.2", "A shirt costs GHS 47.50. Kofi buys 3 shirts and pays with GHS 200. How much change does he receive?"),
    # L4 Fractions
    ("L4", "P2", "B9.1.3.1.1", "Write 2 1/2 as an improper fraction."),
    ("L4", "P2", "B9.1.3.1.1", "Write 11/4 as a mixed number."),
    ("L4", "P2", "B9.1.3.1.1", "Write 0.375 as a percentage."),
    ("L4", "P2", "B9.1.3.1.1", "Write 12.5% as a fraction in its lowest terms."),
    ("L4", "P2", "B9.1.3.1.1", "Which is larger: 5/8 or 3/5?"),
    ("L4", "P2", "B9.1.3.1.1", "Arrange 1/3, 2/5, 1/2 in ascending order."),
    ("L4", "P2", "B9.1.3.1.1", "Find 3/8 of 480."),
    ("L4", "P2", "B9.1.3.1.2", "Evaluate 3/8 + 1/8."),
    ("L4", "P2", "B9.1.3.1.2", "Evaluate 1/3 + 1/4."),
    ("L4", "P2", "B9.1.3.1.2", "Evaluate 5/6 - 1/4."),
    ("L4", "P2", "B9.1.3.1.2", "Evaluate 1/2 + 1/3 x 3/4."),
    ("L4", "P2", "B9.1.3.1.2", "Evaluate (1/2 + 1/3) x 6/5."),
    ("L4", "P2", "B9.1.3.1.1", "Find 35% of GHS 240."),
    ("L4", "P2", "B9.1.3.1.1", "A shirt marked GHS 80 is sold at a 15% discount. Find the sale price."),
    # L5 Ratio & Proportion
    ("L5", "P2", "B9.1.4.1.1", "Simplify the ratio 18 : 24."),
    ("L5", "P2", "B9.1.4.1.2", "Share GHS 720 in the ratio 2 : 3."),
    ("L5", "P2", "B9.1.4.1.1", "y is proportional to x and y = 15 when x = 5. Find y when x = 8."),
    ("L5", "P2", "B9.1.4.1.1", "If 5 pens cost GHS 17.50, find the cost of 8 pens."),
    ("L5", "P2", "B9.1.4.1.1", "A recipe for 4 people uses 300 g rice. How much is needed for 10 people?"),
    ("L5", "P2", "B9.1.4.1.3", "If 12 taps fill a tank in 4 hours, how long will 8 taps take?"),
    ("L5", "P2", "B9.1.4.1.3", "If 6 workers build a wall in 10 days, how many workers are needed to build it in 5 days?"),
    ("L5", "P2", "B9.1.4.1.3", "A car travels 120 km at 40 km/h and returns 120 km at 60 km/h. Find the average speed for the whole journey."),
    ("L5", "P2", "B9.1.4.1.3", "A car uses 8 litres per 100 km. How many litres are needed for 350 km?"),
    ("L5", "P2", "B9.1.4.1.2", "A worker earns GHS 45 per hour for 40 hours a week. What is the weekly wage?"),
    ("L5", "P2", "B9.1.4.1.2", "The same worker gets a 10% rise. What is the new hourly rate?"),
    ("L5", "P2", "B9.1.4.1.3", "Kofi paints a room in 6 hours, Ama in 3 hours. How long working together?"),
    ("L5", "P2", "B9.1.4.1.3", "A printer prints 12 pages per minute. How many pages in 45 minutes?"),
    ("L5", "P2", "B9.1.4.1.2", "A phone costs GHS 400. The price rises by 15%. Find the new price."),
    ("L5", "P2", "B9.1.4.1.2", "A GHS 200 item is sold at a 25% discount. Find the sale price."),
    ("L5", "P2", "B9.1.4.1.1", "Two numbers are in the ratio 3 : 5 and their sum is 96. Find the numbers."),
    ("L5", "P2", "B9.1.4.1.1", "A map has scale 1 : 50 000. What distance does 4 cm represent in km?"),
    # L6 Linear Relations
    ("L6", "P2", "B9.2.1.1.1", "Complete the table for y = 2x - 3, x = -2, -1, 0, 1, 2, 3."),
    ("L6", "P2", "B9.2.1.1.1", "Complete the table for y = -x + 5, x = 0, 1, 2, 3."),
    ("L6", "P2", "B9.2.1.1.1", "For y = 3x - 1, find y when x = 7."),
    ("L6", "P2", "B9.1.4.1.4", "Find the gradient of the line through (1, 2) and (4, -4)."),
    ("L6", "P2", "B9.2.1.1.1", "Find the equation of the line through (0, 1) and (2, 5)."),
    ("L6", "P2", "B9.2.1.1.1", "Write down the gradient and y-intercept of y = -3x + 4."),
    ("L6", "P2", "B9.2.1.1.1", "Find the equation of the line through (0, 9) parallel to y = 4x + 1."),
    ("L6", "P2", "B9.2.1.1.1", "For y = 3x - 1, find x when y = 11."),
    ("L6", "P2", "B9.2.1.1.1", "The line y = 2x + c passes through (3, 10). Find c."),
    ("L6", "P2", "B9.2.1.1.1", "A line has gradient 5 and y-intercept -2. Write its equation."),
    ("L6", "P2", "B9.1.4.1.4", "On a distance-time graph, a car covers 80 km in 2 hours. What is the gradient?"),
    ("L6", "P2", "B9.2.1.1.1", "What is the gradient of a line perpendicular to y = 2x + 3?"),
    ("L6", "P2", "B9.2.1.1.1", "The points (1, 3) and (3, 7) lie on a line. Find its equation."),
    # L7 Algebraic Expressions
    ("L7", "P2", "B9.2.2.1.2", "Evaluate 3x - 5 when x = -2."),
    ("L7", "P2", "B9.2.2.1.2", "Evaluate x^2 + 2x when x = -3."),
    ("L7", "P2", "B9.2.2.1.2", "Evaluate 5(2x - 3) when x = 4."),
    ("L7", "P2", "B9.2.2.1.4", "Simplify 3a + 5b - a + 2b."),
    ("L7", "P2", "B9.2.2.1.4", "Expand 4(x + 2)."),
    ("L7", "P2", "B9.2.2.1.4", "Expand and simplify 3(2x + 1) - 2(x - 4)."),
    ("L7", "P2", "B9.2.2.1.4", "Kofi is x years old. His father is 3 times as old. Find the father's age in 5 years."),
    ("L7", "P2", "B9.2.2.1.4", "A box holds 5x - 3 sweets. How many sweets do 4 boxes hold?"),
    ("L7", "P2", "B9.2.2.1.4", "A rectangle has length (x + 3) and width (x - 1). Find the area."),
    ("L7", "P2", "B9.2.2.1.4", "A rectangle has perimeter 20 cm and length (x + 2), width (x - 1). Find x."),
    ("L7", "P2", "B9.2.2.1.4", "A square of side (x + 4) has a square of side x cut out. Find the shaded area."),
    ("L7", "P2", "B9.2.2.1.4", "Simplify x^3 times x^4."),
    ("L7", "P2", "B9.2.2.1.4", "Simplify a^7 divided by a^2."),
    ("L7", "P2", "B9.2.2.1.4", "Simplify (2x^2)^3."),
    ("L7", "P2", "B9.2.2.1.4", "Write 'three more than twice a number n' as an algebraic expression."),
    ("L7", "P2", "B9.2.2.1.4", "A rectangle has length (2x + 3) and width (x - 1). Expand the area expression."),
    ("L7", "P2", "B9.2.2.1.3", "Factorise 12a + 16b."),
    # L8 Equations & Inequalities
    ("L8", "P2", "B9.2.3.1.1", "Solve x + 7 = 12."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 3x - 4 = 11."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 5x + 2 = 2x + 14."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 7x - 5 = 3x + 15."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 4(x - 3) = 2x."),
    ("L8", "P2", "B9.2.3.1.1", "Solve -2x > 6."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 3x - 1 <= 8."),
    ("L8", "P2", "B9.2.3.1.1", "Solve -x < 5."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 2(x - 3) = 8."),
    ("L8", "P2", "B9.2.3.1.1", "Solve 3(2x + 1) = 21."),
    ("L8", "P2", "B9.2.3.1.1", "Solve x/3 + 2 = 6."),
    ("L8", "P2", "B9.2.3.1.1", "Solve (2x + 1)/2 = 5."),
    ("L8", "P2", "B9.2.3.1.3", "Three consecutive integers sum to 27. Find them."),
    ("L8", "P2", "B9.2.3.1.3", "A rectangle has perimeter 30 cm. The length is 2 cm more than the width. Find the width."),
    ("L8", "P2", "B9.2.3.1.2", "Represent x <= 4 on a number line."),
    ("L8", "P2", "B9.2.3.1.2", "Represent 1 < x <= 5 on a number line."),
    # L9 Angles & Trig
    ("L9", "P2", "B9.3.1.1.1", "An isosceles triangle has a vertex angle of 40 degrees. Find each base angle."),
    ("L9", "P2", "B9.3.1.1.1", "Find the missing angle in a triangle with angles 50 degrees and 60 degrees."),
    ("L9", "P2", "B9.3.1.1.1", "In an equilateral triangle, what is each angle?"),
    ("L9", "P2", "B9.3.1.1.1", "A right triangle has an angle of 35 degrees. Find the third angle."),
    ("L9", "P2", "B9.3.1.1.1", "If a transversal makes a corresponding angle of 120 degrees, what is the matching angle?"),
    ("L9", "P2", "B9.3.1.1.1", "Two co-interior angles sum to what?"),
    ("L9", "P2", "B9.3.1.1.1", "One angle on a straight line is 110 degrees. Find the adjacent angle."),
    ("L9", "P2", "B9.3.1.1.1", "Two lines cross making an angle of 75 degrees. State the vertically opposite angle."),
    ("L9", "P2", "B9.3.1.1.2", "Find the hypotenuse of a right triangle with legs 9 and 12."),
    ("L9", "P2", "B9.3.1.1.2", "Hypotenuse 13, one leg 5. Find the other leg."),
    ("L9", "P2", "B9.3.1.1.2", "In a right triangle, opposite = 4, hypotenuse = 5. Find sin theta."),
    ("L9", "P2", "B9.3.1.1.2", "In a right triangle, adjacent = 3, hypotenuse = 5. Find cos theta."),
    ("L9", "P2", "B9.3.1.1.1", "In triangle ABC, angle A = 2 angle B and angle C = 3 angle B. Find all three angles."),
    ("L9", "P2", "B9.3.1.1.1", "An isosceles triangle has base angles 65 degrees. Find the vertex angle."),
    ("L9", "P2", "B9.3.1.2.1", "What is the locus of points equidistant from two points A and B?"),
    ("L9", "P2", "B9.3.1.2.1", "What is the locus of points equidistant from two intersecting lines?"),
    # L10 Measurement & Circles
    ("L10", "P2", "B9.3.2.1.2", "Find the circumference of a circle with radius 14 cm (pi = 22/7)."),
    ("L10", "P2", "B9.3.2.1.2", "Find the area of a circle with radius 7 cm (pi = 22/7)."),
    ("L10", "P2", "B9.3.2.1.2", "The area of a circle is 154 square cm. Find its radius (pi = 22/7)."),
    ("L10", "P2", "B9.3.2.1.2", "Find the perimeter of a semicircle with radius 7 cm (straight edge = diameter)."),
    ("L10", "P2", "B9.3.2.1.2", "Find the area of a semicircle with radius 14 cm (pi = 22/7)."),
    ("L10", "P2", "B9.3.2.1.1", "A map has scale 1 : 50 000. What distance does 4 cm represent in km?"),
    ("L10", "P2", "B9.3.2.1.1", "A 30 m room is drawn at scale 1 : 500. How long is the drawing?"),
    ("L10", "P2", "B9.3.2.1.1", "Convert 3 metres to centimetres."),
    ("L10", "P2", "B9.3.2.1.1", "Convert 2.5 km to metres."),
    ("L10", "P2", "B9.3.2.1.2", "Find the area of a rectangle 8 cm by 5 cm."),
    ("L10", "P2", "B9.3.2.1.2", "Find the perimeter of a rectangle 8 cm by 5 cm."),
    ("L10", "P2", "B9.3.2.1.2", "Find the area of a triangle with base 10 cm and height 6 cm."),
    ("L10", "P2", "B9.3.2.1.2", "The circumference of a circle is 44 cm. Find its radius (pi = 22/7)."),
    ("L10", "P2", "B9.3.2.1.2", "A circle has area 36 pi. Find its circumference."),
    # L11 Vectors
    ("L11", "P2", "B9.3.2.1.4", "Write the position vector of P(4, -3)."),
    ("L11", "P2", "B9.3.2.1.4", "A(1, 2), B(4, 6). Find vector AB."),
    ("L11", "P2", "B9.3.2.1.4", "B(5, 5), vector AB = (2, 1). Find A."),
    ("L11", "P2", "B9.3.2.2.2", "Evaluate (2, 3) + (1, -1)."),
    ("L11", "P2", "B9.3.2.2.2", "Evaluate (5, 4) - (2, 6)."),
    ("L11", "P2", "B9.3.2.2.2", "Vector AB = (1, 2), vector BC = (3, -2). Find vector AC."),
    ("L11", "P2", "B9.3.2.2.2", "Evaluate 3 times (2, -1)."),
    ("L11", "P2", "B9.3.2.2.2", "Find the magnitude of (3, 4)."),
    ("L11", "P2", "B9.3.2.2.2", "Vector AB = (2, -3). Find vector BA."),
    ("L11", "P2", "B9.3.2.1.4", "A(2, 1), B(x, 5), vector AB = (3, 4). Find x."),
    ("L11", "P2", "B9.3.2.2.2", "Evaluate (2, 3) + (-1, 4) - (1, 1)."),
    ("L11", "P2", "B9.3.2.2.2", "Find k if k(2, 6) = (1, 3)."),
    # L12 Data & Statistics
    ("L12", "P2", "B9.4.1.2.2", "Find the mean of 3, 5, 7, 9."),
    ("L12", "P2", "B9.4.1.2.2", "Find the median of 3, 5, 7, 9, 11."),
    ("L12", "P2", "B9.4.1.2.2", "Find the median of 2, 4, 6, 8."),
    ("L12", "P2", "B9.4.1.2.2", "Find the mode of 2, 3, 3, 5, 5, 5, 7."),
    ("L12", "P2", "B9.4.1.2.2", "Find the range of 12, 18, 20, 25."),
    ("L12", "P2", "B9.4.1.2.2", "Find the mean of 2, 4, 6, 8, 10, 12."),
    ("L12", "P2", "B9.4.1.2.2", "Mean of x, 10, 12 is 11. Find x."),
    ("L12", "P2", "B9.4.1.2.2", "Median of 3, 7, x, 15 is 9. Find x."),
    ("L12", "P2", "B9.4.1.2.2", "A set has mean 20 and 5 values. Four of them are 15, 18, 22, 25. Find the fifth."),
    ("L12", "P2", "B9.4.1.1.2", "If f = 2, 3, 5 and x = 1, 2, 3, find the sum of f times x."),
    ("L12", "P2", "B9.4.1.1.2", "A category has 30 out of 120 items. Find its pie chart angle."),
    ("L12", "P2", "B9.4.1.2.2", "Find the mean, median and range of 50, 60, 70, 80."),
    # L13 Probability
    ("L13", "P2", "B9.4.2.1.1", "What is the probability of picking a green pen from a bag with 5 red, 3 blue, 2 green?"),
    ("L13", "P2", "B9.4.2.1.2", "Express 3/8 as a decimal and a percentage."),
    ("L13", "P2", "B9.4.2.1.2", "If P(win) = 2/7, write the odds in favour as a ratio."),
    ("L13", "P2", "B9.4.2.1.1", "Bag: A, A, B. Pick two without replacement. Find P(both A)."),
    ("L13", "P2", "B9.4.2.1.1", "In a bag of 5 red, 3 blue, 2 green pens, find P(red then blue) without replacement."),
    ("L13", "P2", "B9.4.2.1.1", "Find P(blue then red) without replacement from the same bag."),
    ("L13", "P2", "B9.4.2.1.1", "List the sample space for two coin tosses."),
    ("L13", "P2", "B9.4.2.1.1", "Find P(not green) from the pen bag."),
    ("L13", "P2", "B9.4.2.1.1", "Two coins: find P(both heads)."),
    ("L13", "P2", "B9.4.2.1.1", "A class has 20 pupils, 8 girls. Find P(girl) as a fraction, decimal, and percentage."),
    ("L13", "P2", "B9.4.2.1.1", "A bag has 6 blue and 4 red marbles. Find P(blue)."),
    ("L13", "P2", "B9.4.2.1.1", "A spinner has 4 equal sectors, 1 red. Find P(red)."),
    ("L13", "P2", "B9.4.2.1.1", "Die thrown twice. Find P(at least one six)."),
    ("L13", "P2", "B9.4.2.1.1", "A card is drawn from a standard deck. Find P(ace or king)."),
]


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")

    conn.execute(
        "INSERT OR IGNORE INTO sources (name, domain, source_type, acquisition, tos_notes, trusted) "
        "VALUES (?, ?, 'mock_compilation', 'generated_lesson', ?, 1);",
        (
            SOURCE_NAME,
            "local://generated-l2-l13",
            "Original questions written for Staralex lesson packages. Free for study use.",
        ),
    )
    source_id = conn.execute(
        "SELECT id FROM sources WHERE domain = 'local://generated-l2-l13';"
    ).fetchone()[0]

    stats = {"new": 0, "dupe": 0, "occurrences": 0}
    with conn:
        for idx, (lesson, paper, ind, text) in enumerate(ITEMS, start=1):
            paper_type = "Paper 1 - Objective" if paper == "P1" else "Paper 2 - Essay"
            h = hashlib.sha256(f"mathematics|{norm(text)}".encode("utf-8")).hexdigest()
            qid = f"Q_{h[:12]}"
            raw_id = f"GEN_{lesson}_q{idx}"

            cur = conn.execute("SELECT id FROM questions WHERE id = ?;", (qid,)).fetchone()
            if cur:
                stats["dupe"] += 1
            else:
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, subject, question_text, option_a, option_b, option_c, option_d,
                        correct_answer, has_diagram, diagram_path, year, paper_type,
                        indicator_code, confidence, tag_method, dedup_hash, migrated_from, created_at
                    ) VALUES (?, ?, ?, '', '', '', '', '', 0, NULL, ?, ?, ?, 1.0, 'generated_lesson_exercises', ?, ?, ?);
                    """,
                    (qid, SUBJECT, text, YEAR, paper_type, ind, h, raw_id, NOW),
                )
                stats["new"] += 1

            conn.execute(
                """
                INSERT OR IGNORE INTO question_occurrences (
                    question_id, original_id, source_file, harvested_file_id,
                    source_id, original_url, year, paper_type, question_number, created_at
                ) VALUES (?, ?, ?, NULL, ?, ?, ?, ?, ?, ?);
                """,
                (
                    qid,
                    raw_id,
                    f"{SOURCE_NAME}_{lesson}",
                    source_id,
                    f"local://generated/{lesson}",
                    YEAR,
                    paper_type,
                    idx,
                    NOW,
                ),
            )
            stats["occurrences"] += 1

        conn.execute("INSERT INTO questions_fts (questions_fts) VALUES ('rebuild');")

    conn.close()
    print("L2-L13 generated ingest:", stats)


if __name__ == "__main__":
    main()
