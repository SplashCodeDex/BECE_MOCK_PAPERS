"""
GES Common Core Programme (CCP) Curriculum Taxonomy for B7, B8, and B9.
Covers Mathematics, Computing / ICT, and Career Technology / Design (CDT/CAD).
Enriches B9 indicators from local lesson trackers and links lower-grade prerequisites.
"""

import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
GRADE9_MATHS_DIR = WORKSPACE_DIR.parent / "Grade9-Maths"
GRADE9_COMP_DIR = WORKSPACE_DIR.parent / "Grade9-Computing"


# Core Taxonomy Structure: Strands, Substrands, and Indicators
# Covers B7 and B8 foundations + CDT/CAD. B9 items are enriched directly from workspace trackers.

CURRICULUM_DATA: List[Dict[str, Any]] = [
    # =========================================================================
    # MATHEMATICS - B7
    # =========================================================================
    {
        "code": "B7.1.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 1,
        "substrand_title": "Number and Numeration Systems",
        "content_standard": "B7.1.1.1",
        "indicator_text": "Model number quantities more than 1,000,000,000 using graph sheets, isometric papers, and multi-base blocks.",
        "prerequisite_codes": [],
        "keywords": ["place value", "millions", "billions", "large numbers", "numeration"]
    },
    {
        "code": "B7.1.1.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 1,
        "substrand_title": "Number and Numeration Systems",
        "content_standard": "B7.1.1.1",
        "indicator_text": "Compare and order whole numbers more than 1,000,000,000 and represent comparisons using symbols (<, >, =).",
        "prerequisite_codes": [],
        "keywords": ["compare", "order", "inequality", "greater than", "less than"]
    },
    {
        "code": "B7.1.1.1.3",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 1,
        "substrand_title": "Number and Numeration Systems",
        "content_standard": "B7.1.1.1",
        "indicator_text": "Round off, round up, and round down whole numbers and decimals to given place values, decimal places, and significant figures.",
        "prerequisite_codes": [],
        "keywords": ["rounding", "decimal places", "significant figures", "nearest ten", "nearest hundred"]
    },
    {
        "code": "B7.1.2.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B7.1.2.1",
        "indicator_text": "Multiply and divide given numbers by powers and multiples of 10 including decimals and benchmark fractions.",
        "prerequisite_codes": [],
        "keywords": ["powers of 10", "multiplication", "division", "benchmark fractions", "decimals"]
    },
    {
        "code": "B7.1.2.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B7.1.2.1",
        "indicator_text": "Apply mental mathematics strategies and number properties (commutative, associative, distributive) to solve operational problems.",
        "prerequisite_codes": [],
        "keywords": ["mental math", "commutative", "associative", "distributive", "operational laws"]
    },
    {
        "code": "B7.1.2.2.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B7.1.2.2",
        "indicator_text": "Add and subtract directed numbers (integers) and apply them to solve contextual problems.",
        "prerequisite_codes": [],
        "keywords": ["integers", "directed numbers", "negative numbers", "number line", "addition", "subtraction"]
    },
    {
        "code": "B7.1.2.2.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B7.1.2.2",
        "indicator_text": "Multiply and divide directed numbers (integers) using sign rules and apply to word problems.",
        "prerequisite_codes": ["B7.1.2.2.1"],
        "keywords": ["integer multiplication", "integer division", "sign rules", "negative times negative"]
    },
    {
        "code": "B7.1.2.3.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B7.1.2.3",
        "indicator_text": "Perform combined arithmetic operations on numbers using the order of operations (BODMAS / PEMDAS).",
        "prerequisite_codes": ["B7.1.2.1.2", "B7.1.2.2.2"],
        "keywords": ["BODMAS", "PEMDAS", "order of operations", "brackets", "arithmetic hierarchy"]
    },
    {
        "code": "B7.1.3.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 3,
        "substrand_title": "Fractions, Decimals, and Percentages",
        "content_standard": "B7.1.3.1",
        "indicator_text": "Simplify, add, subtract, multiply, and divide proper, improper fractions, and mixed numbers.",
        "prerequisite_codes": [],
        "keywords": ["fractions", "mixed numbers", "common denominator", "reciprocal", "fraction simplification"]
    },
    {
        "code": "B7.1.3.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 3,
        "substrand_title": "Fractions, Decimals, and Percentages",
        "content_standard": "B7.1.3.1",
        "indicator_text": "Convert fluently between fractions, decimals, and percentages and solve percentage of a quantity word problems.",
        "prerequisite_codes": ["B7.1.3.1.1"],
        "keywords": ["percentage", "decimal conversion", "fraction to percent", "percentage of quantity"]
    },
    {
        "code": "B7.1.4.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 4,
        "substrand_title": "Ratios and Proportions",
        "content_standard": "B7.1.4.1",
        "indicator_text": "Express ratios in simplest form and share quantities in a given ratio.",
        "prerequisite_codes": ["B7.1.3.1.1"],
        "keywords": ["ratio", "simplifying ratio", "sharing ratio", "proportional parts"]
    },
    {
        "code": "B7.2.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 1,
        "substrand_title": "Patterns and Relations",
        "content_standard": "B7.2.1.1",
        "indicator_text": "Identify, describe, extend number and geometric patterns, and determine the nth term rule of linear sequences.",
        "prerequisite_codes": [],
        "keywords": ["number sequence", "nth term", "linear pattern", "common difference", "pattern rule"]
    },
    {
        "code": "B7.2.2.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 2,
        "substrand_title": "Algebraic Expressions",
        "content_standard": "B7.2.2.1",
        "indicator_text": "Formulate algebraic expressions from word problems and simplify by collecting like terms.",
        "prerequisite_codes": [],
        "keywords": ["algebraic expression", "like terms", "simplification", "variable", "coefficient"]
    },
    {
        "code": "B7.2.2.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 2,
        "substrand_title": "Algebraic Expressions",
        "content_standard": "B7.2.2.1",
        "indicator_text": "Expand single brackets and evaluate algebraic expressions by substituting numerical values.",
        "prerequisite_codes": ["B7.2.2.1.1"],
        "keywords": ["expanding brackets", "substitution", "evaluating expression", "distributive law"]
    },
    {
        "code": "B7.2.3.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 3,
        "substrand_title": "Variables and Equations",
        "content_standard": "B7.2.3.1",
        "indicator_text": "Solve linear equations in one variable with integer and fractional coefficients.",
        "prerequisite_codes": ["B7.2.2.1.2"],
        "keywords": ["linear equation", "solve for x", "equation balancing", "one variable"]
    },
    {
        "code": "B7.3.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 1,
        "substrand_title": "Shapes and Space",
        "content_standard": "B7.3.1.1",
        "indicator_text": "Identify and calculate unknown angles on a straight line, vertically opposite angles, and angles at a point.",
        "prerequisite_codes": [],
        "keywords": ["angles", "straight line", "vertically opposite", "angles at point", "adjacent angles"]
    },
    {
        "code": "B7.3.1.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 1,
        "substrand_title": "Shapes and Space",
        "content_standard": "B7.3.1.1",
        "indicator_text": "Calculate unknown angles in triangles and parallel lines cut by a transversal (alternate, corresponding, co-interior).",
        "prerequisite_codes": ["B7.3.1.1.1"],
        "keywords": ["parallel lines", "alternate angles", "corresponding angles", "co-interior", "triangle angle sum"]
    },
    {
        "code": "B7.3.2.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 2,
        "substrand_title": "Measurement and Vectors",
        "content_standard": "B7.3.2.1",
        "indicator_text": "Calculate the perimeter and area of composite plane figures (rectangles, triangles, parallelograms, trapezia).",
        "prerequisite_codes": [],
        "keywords": ["perimeter", "area", "rectangle", "triangle", "trapezium", "parallelogram"]
    },
    {
        "code": "B7.4.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 4,
        "strand_title": "Handling Data",
        "substrand_number": 1,
        "substrand_title": "Data and Statistics",
        "content_standard": "B7.4.1.1",
        "indicator_text": "Collect, organize data in frequency tables, and construct/interpret bar charts and pie charts.",
        "prerequisite_codes": [],
        "keywords": ["frequency table", "bar chart", "pie chart", "data presentation", "angles of pie chart"]
    },
    {
        "code": "B7.4.2.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "strand_number": 4,
        "strand_title": "Handling Data",
        "substrand_number": 2,
        "substrand_title": "Chance and Probability",
        "content_standard": "B7.4.2.1",
        "indicator_text": "Calculate the experimental and theoretical probability of single simple events using fractions.",
        "prerequisite_codes": ["B7.1.3.1.1"],
        "keywords": ["probability", "chance", "favourable outcomes", "die roll", "coin toss"]
    },

    # =========================================================================
    # MATHEMATICS - B8
    # =========================================================================
    {
        "code": "B8.1.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 1,
        "substrand_title": "Number and Numeration Systems",
        "content_standard": "B8.1.1.1",
        "indicator_text": "Express large and small numbers in standard index form (A x 10^n where 1 <= A < 10, n in integers).",
        "prerequisite_codes": ["B7.1.1.1.3"],
        "keywords": ["standard form", "scientific notation", "index form", "powers of 10"]
    },
    {
        "code": "B8.1.1.2.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 1,
        "substrand_title": "Number and Numeration Systems",
        "content_standard": "B8.1.1.2",
        "indicator_text": "Demonstrate understanding of sets, subsets, union, intersection, complement, and represent with 2-set Venn diagrams.",
        "prerequisite_codes": [],
        "keywords": ["sets", "subsets", "Venn diagram", "union", "intersection", "complement", "universal set"]
    },
    {
        "code": "B8.1.2.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 2,
        "substrand_title": "Number Operations",
        "content_standard": "B8.1.2.1",
        "indicator_text": "Apply the laws of indices to simplify multiplication, division, and powers of numerical and algebraic terms.",
        "prerequisite_codes": ["B7.1.2.1.1"],
        "keywords": ["indices", "laws of indices", "exponents", "powers", "index rules"]
    },
    {
        "code": "B8.1.3.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 3,
        "substrand_title": "Fractions, Decimals, and Percentages",
        "content_standard": "B8.1.3.1",
        "indicator_text": "Solve real-world commercial problems involving profit, loss, discount, sales tax (VAT), and simple interest (I = PRT / 100).",
        "prerequisite_codes": ["B7.1.3.1.2"],
        "keywords": ["simple interest", "profit", "loss", "discount", "VAT", "cost price", "selling price"]
    },
    {
        "code": "B8.1.4.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 1,
        "strand_title": "Number",
        "substrand_number": 4,
        "substrand_title": "Ratios and Proportions",
        "content_standard": "B8.1.4.1",
        "indicator_text": "Solve problems involving direct and inverse proportions, rates of work, and speed/distance/time.",
        "prerequisite_codes": ["B7.1.4.1.1"],
        "keywords": ["inverse proportion", "rate", "speed", "distance", "time", "work rate"]
    },
    {
        "code": "B8.2.2.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 2,
        "substrand_title": "Algebraic Expressions",
        "content_standard": "B8.2.2.1",
        "indicator_text": "Factorise algebraic expressions by removing common factors and grouping terms in pairs.",
        "prerequisite_codes": ["B7.2.2.1.2"],
        "keywords": ["factorisation", "common factor", "grouping terms", "algebraic factors"]
    },
    {
        "code": "B8.2.3.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 3,
        "substrand_title": "Variables and Equations",
        "content_standard": "B8.2.3.1",
        "indicator_text": "Solve linear inequalities in one variable and represent solution sets on a number line.",
        "prerequisite_codes": ["B7.2.3.1.1"],
        "keywords": ["inequalities", "greater than", "less than or equal", "number line", "truth set"]
    },
    {
        "code": "B8.2.3.1.2",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 2,
        "strand_title": "Algebra",
        "substrand_number": 3,
        "substrand_title": "Variables and Equations",
        "content_standard": "B8.2.3.1",
        "indicator_text": "Solve pairs of simultaneous linear equations in two variables using substitution and elimination methods.",
        "prerequisite_codes": ["B7.2.3.1.1"],
        "keywords": ["simultaneous equations", "elimination", "substitution", "two variables", "linear system"]
    },
    {
        "code": "B8.3.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 1,
        "substrand_title": "Shapes and Space",
        "content_standard": "B8.3.1.1",
        "indicator_text": "Apply Pythagoras' theorem (a^2 + b^2 = c^2) to find missing side lengths in right-angled triangles.",
        "prerequisite_codes": ["B7.3.1.1.2"],
        "keywords": ["Pythagoras", "hypotenuse", "right-angled triangle", "square root", "triple"]
    },
    {
        "code": "B8.3.2.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 2,
        "substrand_title": "Measurement and Vectors",
        "content_standard": "B8.3.2.1",
        "indicator_text": "Calculate the circumference and area of circles, and calculate perimeter/area of sectors.",
        "prerequisite_codes": ["B7.3.2.1.1"],
        "keywords": ["circle", "circumference", "pi", "radius", "diameter", "sector area", "arc length"]
    },
    {
        "code": "B8.3.2.1.2",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 2,
        "substrand_title": "Measurement and Vectors",
        "content_standard": "B8.3.2.1",
        "indicator_text": "Calculate the total surface area and volume of cuboids, cubes, and right circular cylinders.",
        "prerequisite_codes": ["B8.3.2.1.1"],
        "keywords": ["volume", "surface area", "cylinder", "cuboid", "cube", "capacity"]
    },
    {
        "code": "B8.3.3.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 3,
        "strand_title": "Geometry and Measurement",
        "substrand_number": 3,
        "substrand_title": "Position and Transformation",
        "content_standard": "B8.3.3.1",
        "indicator_text": "Perform and describe reflections in coordinate axes (x-axis, y-axis, y = x) and translations by a vector.",
        "prerequisite_codes": [],
        "keywords": ["transformation", "reflection", "translation", "coordinate plane", "vector translation"]
    },
    {
        "code": "B8.4.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "strand_number": 4,
        "strand_title": "Handling Data",
        "substrand_number": 1,
        "substrand_title": "Data and Statistics",
        "content_standard": "B8.4.1.1",
        "indicator_text": "Calculate measures of central tendency (mean, median, mode) and range for ungrouped data sets.",
        "prerequisite_codes": ["B7.4.1.1.1"],
        "keywords": ["mean", "median", "mode", "range", "average", "statistics", "ungrouped data"]
    },

    # =========================================================================
    # COMPUTING - B7 & B8
    # =========================================================================
    {
        "code": "B7.1.1.1.1",
        "grade": "B7",
        "subject": "Computing_ICT",
        "strand_number": 1,
        "strand_title": "Introduction to Computing",
        "substrand_number": 1,
        "substrand_title": "Components of Computers and Computer Systems",
        "content_standard": "B7.1.1.1",
        "indicator_text": "Examine the generational evolution of computing devices from first generation (vacuum tubes) to modern fifth generation.",
        "prerequisite_codes": [],
        "keywords": ["computer generations", "vacuum tubes", "transistors", "integrated circuits", "microprocessors"]
    },
    {
        "code": "B7.1.1.1.2",
        "grade": "B7",
        "subject": "Computing_ICT",
        "strand_number": 1,
        "strand_title": "Introduction to Computing",
        "substrand_number": 1,
        "substrand_title": "Components of Computers and Computer Systems",
        "content_standard": "B7.1.1.1",
        "indicator_text": "Identify and classify hardware components: input, processing (CPU/ALU/CU), output, and storage devices.",
        "prerequisite_codes": [],
        "keywords": ["hardware", "input devices", "output devices", "CPU", "ALU", "storage", "RAM", "ROM"]
    },
    {
        "code": "B7.2.1.1.1",
        "grade": "B7",
        "subject": "Computing_ICT",
        "strand_number": 2,
        "strand_title": "Productivity Software",
        "substrand_number": 1,
        "substrand_title": "Word Processing",
        "content_standard": "B7.2.1.1",
        "indicator_text": "Create, edit, format text (font size, style, color, alignment), and save documents in a word processing application.",
        "prerequisite_codes": [],
        "keywords": ["word processing", "formatting", "editing", "alignment", "saving", "MS Word"]
    },
    {
        "code": "B8.1.1.1.1",
        "grade": "B8",
        "subject": "Computing_ICT",
        "strand_number": 1,
        "strand_title": "Introduction to Computing",
        "substrand_number": 1,
        "substrand_title": "Components of Computers and Computer Systems",
        "content_standard": "B8.1.1.1",
        "indicator_text": "Examine internal system unit components: motherboard, power supply unit, cooling systems, expansion slots, and ports.",
        "prerequisite_codes": ["B7.1.1.1.2"],
        "keywords": ["system unit", "motherboard", "PSU", "expansion slots", "ports", "cooling"]
    },
    {
        "code": "B8.2.4.1.1",
        "grade": "B8",
        "subject": "Computing_ICT",
        "strand_number": 2,
        "strand_title": "Productivity Software",
        "substrand_number": 4,
        "substrand_title": "Electronic Spreadsheet",
        "content_standard": "B8.2.4.1",
        "indicator_text": "Identify spreadsheet interface components (cells, rows, columns, formula bar) and enter data and basic formulas (SUM, AVERAGE).",
        "prerequisite_codes": [],
        "keywords": ["spreadsheet", "excel", "cell reference", "formula", "SUM", "AVERAGE", "rows", "columns"]
    },
    {
        "code": "B8.3.1.1.1",
        "grade": "B8",
        "subject": "Computing_ICT",
        "strand_number": 3,
        "strand_title": "Communication Networks",
        "substrand_number": 1,
        "substrand_title": "Computer Networks",
        "content_standard": "B8.3.1.1",
        "indicator_text": "Examine types of computer networks (LAN, WAN, MAN, PAN, WLAN) and common network topologies (star, bus, ring, mesh).",
        "prerequisite_codes": [],
        "keywords": ["network", "LAN", "WAN", "topology", "star topology", "bus topology", "mesh"]
    },
    {
        "code": "B8.3.3.1.1",
        "grade": "B8",
        "subject": "Computing_ICT",
        "strand_number": 3,
        "strand_title": "Communication Networks",
        "substrand_number": 3,
        "substrand_title": "Information Security",
        "content_standard": "B8.3.3.1",
        "indicator_text": "Identify cybersecurity threats (malware, viruses, worms, phishing, spyware) and practice basic computer safety and antivirus measures.",
        "prerequisite_codes": [],
        "keywords": ["cybersecurity", "virus", "malware", "phishing", "antivirus", "firewall", "passwords"]
    },

    # =========================================================================
    # CDT / CAD (CAREER TECHNOLOGY & CREATIVE ARTS & DESIGN) - B7, B8, B9
    # =========================================================================
    {
        "code": "B7.CDT.1.1.1",
        "grade": "B7",
        "subject": "CDT_CAD",
        "strand_number": 1,
        "strand_title": "Health and Safety & Materials",
        "substrand_number": 1,
        "substrand_title": "Health and Safety in the Workshop",
        "content_standard": "B7.CDT.1.1",
        "indicator_text": "Identify personal protective equipment (PPE), workshop safety rules, hazards, and first aid procedures.",
        "prerequisite_codes": [],
        "keywords": ["PPE", "safety rules", "first aid", "workshop", "hazard", "goggles", "apron"]
    },
    {
        "code": "B7.CDT.1.2.1",
        "grade": "B7",
        "subject": "CDT_CAD",
        "strand_number": 1,
        "strand_title": "Health and Safety & Materials",
        "substrand_number": 2,
        "substrand_title": "Materials for Production (Wood, Metals, Plastics, Food)",
        "content_standard": "B7.CDT.1.2",
        "indicator_text": "Classify common compliant and resistant materials (timber, metals, plastics, fabrics, food commodities) and their properties.",
        "prerequisite_codes": [],
        "keywords": ["materials", "timber", "wood", "metals", "ferrous", "non-ferrous", "plastics", "food"]
    },
    {
        "code": "B8.CDT.2.1.1",
        "grade": "B8",
        "subject": "CDT_CAD",
        "strand_number": 2,
        "strand_title": "Tools, Equipment, and Processes",
        "substrand_number": 1,
        "substrand_title": "Measuring and Marking Out Tools",
        "content_standard": "B8.CDT.2.1",
        "indicator_text": "Identify, use, and care for measuring, marking out, testing, and holding tools (steel rule, try square, calipers, vice).",
        "prerequisite_codes": ["B7.CDT.1.1.1"],
        "keywords": ["measuring tools", "marking out", "try square", "steel rule", "calipers", "bench vice"]
    },
    {
        "code": "B8.CDT.2.2.1",
        "grade": "B8",
        "subject": "CDT_CAD",
        "strand_number": 2,
        "strand_title": "Tools, Equipment, and Processes",
        "substrand_number": 2,
        "substrand_title": "Cutting and Shaping Tools",
        "content_standard": "B8.CDT.2.2",
        "indicator_text": "Select and demonstrate safe use of cutting, shaping, and abrading tools (saws, chisels, planes, files, rasps).",
        "prerequisite_codes": ["B8.CDT.2.1.1"],
        "keywords": ["cutting tools", "saws", "tenon saw", "hack saw", "chisel", "jack plane", "file"]
    },
    {
        "code": "B9.CDT.3.1.1",
        "grade": "B9",
        "subject": "CDT_CAD",
        "strand_number": 3,
        "strand_title": "Drawing and Design",
        "substrand_number": 1,
        "substrand_title": "Technical Drawing and Orthographic Projections",
        "content_standard": "B9.CDT.3.1",
        "indicator_text": "Produce and interpret orthographic projections (first angle and third angle) showing front, plan, and end elevations of solid objects.",
        "prerequisite_codes": [],
        "keywords": ["orthographic projection", "front elevation", "plan view", "end elevation", "first angle", "third angle"]
    },
    {
        "code": "B9.CDT.3.2.1",
        "grade": "B9",
        "subject": "CDT_CAD",
        "strand_number": 3,
        "strand_title": "Drawing and Design",
        "substrand_number": 2,
        "substrand_title": "Isometric and Oblique Pictorial Drawing",
        "content_standard": "B9.CDT.3.2",
        "indicator_text": "Construct isometric and oblique drawings of geometric blocks and furniture joints at 30-degree and 45-degree angles.",
        "prerequisite_codes": ["B9.CDT.3.1.1"],
        "keywords": ["isometric drawing", "oblique drawing", "30 degrees", "pictorial drawing", "isometric axes"]
    },
    {
        "code": "B9.CDT.4.1.1",
        "grade": "B9",
        "subject": "CDT_CAD",
        "strand_number": 4,
        "strand_title": "Design Process and Entrepreneurship",
        "substrand_number": 1,
        "substrand_title": "Design Process Stages",
        "content_standard": "B9.CDT.4.1",
        "indicator_text": "Apply the sequential stages of the design process: situation, brief, specification, generating ideas, development, and evaluation.",
        "prerequisite_codes": [],
        "keywords": ["design process", "design brief", "specification", "evaluation", "situation", "prototype"]
    }
]


def extract_b9_maths_from_tracker(tracker_path: Path) -> List[Dict[str, Any]]:
    """Extracts all B9 Mathematics indicators, standards, and topics from Grade9-Maths/LESSON_TRACKER.md."""
    if not tracker_path.exists():
        return []

    text = tracker_path.read_text(encoding="utf-8")
    indicators: List[Dict[str, Any]] = []

    # Map Day blocks
    # e.g.:
    # - **Day 1: Strand 1, Sub-strand 1 (Part 1) - Place Value, Large Numbers, and Standard Form**
    #   - Content Standard: B9.1.1.1
    #   - Indicators: B9.1.1.1.1, B9.1.1.1.2
    #   - Core Topics: ...
    day_pattern = re.compile(
        r"-\s+\*\*Day\s+\d+:\s+Strand\s+(\d+),\s+Sub-strand\s+(\d+)[^\-]*-\s+([^\*]+)\*\*\s*"
        r"(?:-\s+Content\s+Standard:\s*([^\n\r]+)\s*)?"
        r"(?:-\s+Indicators?:\s*([^\n\r]+)\s*)?"
        r"(?:-\s+Core\s+Topics:\s*([\s\S]*?)(?=-\s+Status:|-\s+\*\*Day|\n\n##|\Z))",
        re.MULTILINE
    )

    strand_titles = {
        1: "Number",
        2: "Algebra",
        3: "Geometry and Measurement",
        4: "Handling Data"
    }

    substrand_titles = {
        (1, 1): "Numeration Systems",
        (1, 2): "Number Operations",
        (1, 3): "Fractions, Decimals, Percentages",
        (1, 4): "Ratios and Proportions",
        (2, 1): "Patterns and Relations",
        (2, 2): "Algebraic Expressions",
        (2, 3): "Variables and Equations",
        (3, 1): "Shapes and Space",
        (3, 2): "Measurement and Vectors",
        (3, 3): "Position and Transformation",
        (4, 1): "Data and Statistics",
        (4, 2): "Chance and Probability"
    }

    seen_codes = set()

    for match in day_pattern.finditer(text):
        s_num = int(match.group(1))
        sub_num = int(match.group(2))
        day_topic = match.group(3).strip()
        cs_raw = match.group(4) or f"B9.{s_num}.{sub_num}.1"
        cs = cs_raw.strip()
        inds_raw = match.group(5)
        core_topics_raw = match.group(6) or ""

        # Extract topics
        topic_lines = [
            re.sub(r"^[\s\-\*]+", "", line).strip()
            for line in core_topics_raw.splitlines()
            if line.strip() and not line.strip().startswith("-")
        ]
        topic_summary = " ".join(topic_lines) if topic_lines else day_topic

        # Extract keywords
        clean_words = re.findall(r"\b[a-zA-Z]{3,}\b", (day_topic + " " + topic_summary).lower())
        keywords = sorted(list(set([w for w in clean_words if w not in {"the", "and", "for", "with", "from", "part"}])))

        if inds_raw:
            codes = re.findall(r"B9\.\d+\.\d+\.\d+(?:\.\d+)?", inds_raw)
            for code in codes:
                if code in seen_codes:
                    continue
                seen_codes.add(code)

                # Determine prerequisite codes (link to B8/B7 counterparts)
                prereqs = []
                parts = code.split(".")
                if len(parts) >= 4:
                    s_id, sub_id = parts[1], parts[2]
                    b8_counterpart = f"B8.{s_id}.{sub_id}.1.1"
                    b7_counterpart = f"B7.{s_id}.{sub_id}.1.1"
                    prereqs.extend([b8_counterpart, b7_counterpart])

                indicators.append({
                    "code": code,
                    "grade": "B9",
                    "subject": "Mathematics",
                    "strand_number": s_num,
                    "strand_title": strand_titles.get(s_num, f"Strand {s_num}"),
                    "substrand_number": sub_num,
                    "substrand_title": substrand_titles.get((s_num, sub_num), f"Substrand {sub_num}"),
                    "content_standard": cs,
                    "indicator_text": f"{day_topic}: {topic_summary[:250]}",
                    "prerequisite_codes": prereqs,
                    "keywords": keywords[:15]
                })

    return indicators


def extract_b9_computing_from_tracker(tracker_path: Path) -> List[Dict[str, Any]]:
    """Extracts all B9 Computing indicators, strands, and topics from Grade9-Computing/Curriculum_Tracker.md."""
    if not tracker_path.exists():
        return []

    text = tracker_path.read_text(encoding="utf-8")
    indicators: List[Dict[str, Any]] = []

    strand_titles = {
        1: "Introduction to Computing",
        2: "Productivity Software",
        3: "Communication Networks",
        4: "Computational Thinking"
    }

    substrand_titles = {
        (1, 1): "Components of Computers and Computer Systems",
        (1, 2): "Technology in the Community",
        (1, 3): "Health and Safety at Workstations",
        (2, 1): "Word Processing",
        (2, 2): "Presentation",
        (2, 3): "Desktop Publishing",
        (2, 4): "Electronic Spreadsheet",
        (3, 1): "Computer Networks",
        (3, 2): "Internet and Social Media",
        (3, 3): "Information Security",
        (3, 4): "Web Technologies",
        (4, 1): "Introduction to Programming",
        (4, 2): "Algorithms",
        (4, 3): "Robotics",
        (4, 4): "Artificial Intelligence"
    }

    # Matches Day entries:
    # - **Day 1**: Strand 1, Sub-strand 1 (Part 1) - Next-Generation Computing & Supercomputing
    #   - Indicator: B9.1.1.1.1
    #   - Key Topics: Trends in next-generation hardware...
    day_pattern = re.compile(
        r"-\s+\*\*Day\s+\d+\*\*:\s+Strand\s+(\d+),\s+Sub-strand\s+(\d+)[^\-]*-\s+([^\n\r]+)\s*"
        r"(?:-\s+Indicators?:\s*([^\n\r]+)\s*)?"
        r"(?:-\s+Key\s+Topics:\s*([^\n\r]+)\s*)?",
        re.MULTILINE
    )

    seen_codes = set()

    for match in day_pattern.finditer(text):
        s_num = int(match.group(1))
        sub_num = int(match.group(2))
        day_topic = match.group(3).strip()
        inds_raw = match.group(4) or ""
        key_topics = match.group(5) or day_topic

        clean_words = re.findall(r"\b[a-zA-Z]{3,}\b", (day_topic + " " + key_topics).lower())
        keywords = sorted(list(set([w for w in clean_words if w not in {"the", "and", "for", "with", "from", "part"}])))

        codes = re.findall(r"B9\.\d+\.\d+\.\d+(?:\.\d+)?", inds_raw)
        if not codes:
            # Generate default code if missing
            codes = [f"B9.{s_num}.{sub_num}.1.1"]

        for code in codes:
            if code in seen_codes:
                continue
            seen_codes.add(code)

            prereqs = []
            parts = code.split(".")
            if len(parts) >= 4:
                s_id, sub_id = parts[1], parts[2]
                prereqs.append(f"B8.{s_id}.{sub_id}.1.1")

            cs = ".".join(code.split(".")[:4])

            indicators.append({
                "code": code,
                "grade": "B9",
                "subject": "Computing_ICT",
                "strand_number": s_num,
                "strand_title": strand_titles.get(s_num, f"Strand {s_num}"),
                "substrand_number": sub_num,
                "substrand_title": substrand_titles.get((s_num, sub_num), f"Substrand {sub_num}"),
                "content_standard": cs,
                "indicator_text": f"{day_topic}: {key_topics}",
                "prerequisite_codes": prereqs,
                "keywords": keywords[:15]
            })

    return indicators


def build_full_curriculum_taxonomy() -> List[Dict[str, Any]]:
    """Builds unified curriculum list combining static B7/B8/CDT items and parsed B9 indicators."""
    all_indicators = list(CURRICULUM_DATA)

    # Enrich from Grade 9 Maths tracker
    math_tracker = GRADE9_MATHS_DIR / "LESSON_TRACKER.md"
    b9_math = extract_b9_maths_from_tracker(math_tracker)
    all_indicators.extend(b9_math)

    # Enrich from Grade 9 Computing tracker
    comp_tracker = GRADE9_COMP_DIR / "Curriculum_Tracker.md"
    b9_comp = extract_b9_computing_from_tracker(comp_tracker)
    all_indicators.extend(b9_comp)

    # Deduplicate by code
    deduped: Dict[str, Dict[str, Any]] = {}
    for item in all_indicators:
        deduped[item["code"]] = item

    return list(deduped.values())


def seed_curriculum_database(conn: sqlite3.Connection) -> int:
    """Inserts or updates all curriculum indicators in the database."""
    items = build_full_curriculum_taxonomy()
    
    with conn:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(curriculum_indicators)").fetchall()]
        if "keywords" not in cols:
            conn.execute("ALTER TABLE curriculum_indicators ADD COLUMN keywords TEXT;")
        
        for item in items:
            conn.execute(
                """
                INSERT INTO curriculum_indicators (
                    code, grade, subject, strand_number, strand_title,
                    substrand_number, substrand_title, content_standard,
                    indicator_text, prerequisite_codes, keywords
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(code) DO UPDATE SET
                    grade=excluded.grade,
                    subject=excluded.subject,
                    strand_number=excluded.strand_number,
                    strand_title=excluded.strand_title,
                    substrand_number=excluded.substrand_number,
                    substrand_title=excluded.substrand_title,
                    content_standard=excluded.content_standard,
                    indicator_text=excluded.indicator_text,
                    prerequisite_codes=excluded.prerequisite_codes,
                    keywords=excluded.keywords;
                """,
                (
                    item["code"],
                    item["grade"],
                    item["subject"],
                    item["strand_number"],
                    item["strand_title"],
                    item["substrand_number"],
                    item["substrand_title"],
                    item["content_standard"],
                    item["indicator_text"],
                    json.dumps(item.get("prerequisite_codes", [])),
                    json.dumps(item.get("keywords", []))
                )
            )
    return len(items)


# =========================================================================
# CANONICAL DIAGRAM REGISTRY (Basic 7–9 NaCCA Mathematics Alignment)
# 46 Canonical Diagrams & 46 Companion Skills
# Strict Policy: Source .tex and 300 DPI .png only (Zero .pdf / .svg)
# =========================================================================

CANONICAL_DIAGRAMS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "diagram_01_number_line_inequality",
        "indicator_code": "B7.1.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Number Line Inequality",
        "tex_file": "data/diagrams/math_redrawn/diagram_01_number_line_inequality.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_01_number_line_inequality.png",
        "skill": "diagram-01-number-line-inequality",
        "skill_file": ".agents/skills/diagram-01-number-line-inequality/SKILL.md",
    },
    {
        "id": 2,
        "name": "diagram_02_parallel_lines_transversal",
        "indicator_code": "B7.3.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Parallel Lines & Transversal",
        "tex_file": "data/diagrams/math_redrawn/diagram_02_parallel_lines_transversal.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_02_parallel_lines_transversal.png",
        "skill": "diagram-02-parallel-lines-transversal",
        "skill_file": ".agents/skills/diagram-02-parallel-lines-transversal/SKILL.md",
    },
    {
        "id": 3,
        "name": "diagram_03_right_triangle_elevation",
        "indicator_code": "B9.3.1.2.1",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Angle of Elevation / Right Triangle",
        "tex_file": "data/diagrams/math_redrawn/diagram_03_right_triangle_elevation.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_03_right_triangle_elevation.png",
        "skill": "diagram-03-right-triangle-elevation",
        "skill_file": ".agents/skills/diagram-03-right-triangle-elevation/SKILL.md",
    },
    {
        "id": 4,
        "name": "diagram_04_venn_two_sets",
        "indicator_code": "B7.1.1.2.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "2-Set Venn Diagram",
        "tex_file": "data/diagrams/math_redrawn/diagram_04_venn_two_sets.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_04_venn_two_sets.png",
        "skill": "diagram-04-venn-two-sets",
        "skill_file": ".agents/skills/diagram-04-venn-two-sets/SKILL.md",
    },
    {
        "id": 5,
        "name": "diagram_05_angle_bisector_construction",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Angle Bisector Construction",
        "tex_file": "data/diagrams/math_redrawn/diagram_05_angle_bisector_construction.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_05_angle_bisector_construction.png",
        "skill": "diagram-05-angle-bisector-construction",
        "skill_file": ".agents/skills/diagram-05-angle-bisector-construction/SKILL.md",
    },
    {
        "id": 6,
        "name": "diagram_06_bearing_three_figure",
        "indicator_code": "B8.3.1.2.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "3-Figure Bearing Ray",
        "tex_file": "data/diagrams/math_redrawn/diagram_06_bearing_three_figure.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_06_bearing_three_figure.png",
        "skill": "diagram-06-bearing-three-figure",
        "skill_file": ".agents/skills/diagram-06-bearing-three-figure/SKILL.md",
    },
    {
        "id": 7,
        "name": "diagram_07_similar_triangles_enlargement",
        "indicator_code": "B9.3.3.1.2",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Similar Triangles & Scale Factor",
        "tex_file": "data/diagrams/math_redrawn/diagram_07_similar_triangles_enlargement.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_07_similar_triangles_enlargement.png",
        "skill": "diagram-07-similar-triangles-enlargement",
        "skill_file": ".agents/skills/diagram-07-similar-triangles-enlargement/SKILL.md",
    },
    {
        "id": 8,
        "name": "diagram_08_3d_cuboid_dimensions",
        "indicator_code": "B7.3.1.2.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "3D Cuboid Mensuration",
        "tex_file": "data/diagrams/math_redrawn/diagram_08_3d_cuboid_dimensions.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_08_3d_cuboid_dimensions.png",
        "skill": "diagram-08-3d-cuboid-dimensions",
        "skill_file": ".agents/skills/diagram-08-3d-cuboid-dimensions/SKILL.md",
    },
    {
        "id": 9,
        "name": "diagram_09_net_square_pyramid",
        "indicator_code": "B7.3.1.2.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "2D Net of Square Pyramid",
        "tex_file": "data/diagrams/math_redrawn/diagram_09_net_square_pyramid.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_09_net_square_pyramid.png",
        "skill": "diagram-09-net-square-pyramid",
        "skill_file": ".agents/skills/diagram-09-net-square-pyramid/SKILL.md",
    },
    {
        "id": 10,
        "name": "diagram_10_running_track_mensuration",
        "indicator_code": "B8.3.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Composite Running Track Perimeter",
        "tex_file": "data/diagrams/math_redrawn/diagram_10_running_track_mensuration.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_10_running_track_mensuration.png",
        "skill": "diagram-10-running-track-mensuration",
        "skill_file": ".agents/skills/diagram-10-running-track-mensuration/SKILL.md",
    },
    {
        "id": 11,
        "name": "diagram_11_polygon_interior_angles",
        "indicator_code": "B8.3.1.2.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Convex Pentagon Interior Angles",
        "tex_file": "data/diagrams/math_redrawn/diagram_11_polygon_interior_angles.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_11_polygon_interior_angles.png",
        "skill": "diagram-11-polygon-interior-angles",
        "skill_file": ".agents/skills/diagram-11-polygon-interior-angles/SKILL.md",
    },
    {
        "id": 12,
        "name": "diagram_12_trapezium_area_composite",
        "indicator_code": "B8.3.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Right Trapezium Altitude",
        "tex_file": "data/diagrams/math_redrawn/diagram_12_trapezium_area_composite.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_12_trapezium_area_composite.png",
        "skill": "diagram-12-trapezium-area-composite",
        "skill_file": ".agents/skills/diagram-12-trapezium-area-composite/SKILL.md",
    },
    {
        "id": 13,
        "name": "diagram_13_pie_chart_angles",
        "indicator_code": "B7.4.1.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Categorical Pie Chart Sectors",
        "tex_file": "data/diagrams/math_redrawn/diagram_13_pie_chart_angles.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_13_pie_chart_angles.png",
        "skill": "diagram-13-pie-chart-angles",
        "skill_file": ".agents/skills/diagram-13-pie-chart-angles/SKILL.md",
    },
    {
        "id": 14,
        "name": "diagram_14_straight_line_angles",
        "indicator_code": "B7.3.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Supplementary Straight Line Angles",
        "tex_file": "data/diagrams/math_redrawn/diagram_14_straight_line_angles.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_14_straight_line_angles.png",
        "skill": "diagram-14-straight-line-angles",
        "skill_file": ".agents/skills/diagram-14-straight-line-angles/SKILL.md",
    },
    {
        "id": 15,
        "name": "diagram_15_circle_sector_chord",
        "indicator_code": "B8.3.1.2.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Chord & Center Subtended Sector",
        "tex_file": "data/diagrams/math_redrawn/diagram_15_circle_sector_chord.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_15_circle_sector_chord.png",
        "skill": "diagram-15-circle-sector-chord",
        "skill_file": ".agents/skills/diagram-15-circle-sector-chord/SKILL.md",
    },
    {
        "id": 16,
        "name": "diagram_16_isosceles_exterior_angle",
        "indicator_code": "B8.3.1.2.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Isosceles Triangle Exterior Angle",
        "tex_file": "data/diagrams/math_redrawn/diagram_16_isosceles_exterior_angle.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_16_isosceles_exterior_angle.png",
        "skill": "diagram-16-isosceles-exterior-angle",
        "skill_file": ".agents/skills/diagram-16-isosceles-exterior-angle/SKILL.md",
    },
    {
        "id": 17,
        "name": "diagram_17_linear_mapping_arrows",
        "indicator_code": "B7.2.2.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Linear Mapping Relation Arrows",
        "tex_file": "data/diagrams/math_redrawn/diagram_17_linear_mapping_arrows.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_17_linear_mapping_arrows.png",
        "skill": "diagram-17-linear-mapping-arrows",
        "skill_file": ".agents/skills/diagram-17-linear-mapping-arrows/SKILL.md",
    },
    {
        "id": 18,
        "name": "diagram_18_kite_perimeter",
        "indicator_code": "B7.3.1.2.2",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Geometric Kite Perimeter",
        "tex_file": "data/diagrams/math_redrawn/diagram_18_kite_perimeter.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_18_kite_perimeter.png",
        "skill": "diagram-18-kite-perimeter",
        "skill_file": ".agents/skills/diagram-18-kite-perimeter/SKILL.md",
    },
    {
        "id": 19,
        "name": "diagram_19_bar_chart_frequency",
        "indicator_code": "B7.4.1.1.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Frequency Bar Chart on Grid",
        "tex_file": "data/diagrams/math_redrawn/diagram_19_bar_chart_frequency.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_19_bar_chart_frequency.png",
        "skill": "diagram-19-bar-chart-frequency",
        "skill_file": ".agents/skills/diagram-19-bar-chart-frequency/SKILL.md",
    },
    {
        "id": 20,
        "name": "diagram_20_construction_30_degrees",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Compass Construction 30 Degrees",
        "tex_file": "data/diagrams/math_redrawn/diagram_20_construction_30_degrees.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_20_construction_30_degrees.png",
        "skill": "diagram-20-construction-30-degrees",
        "skill_file": ".agents/skills/diagram-20-construction-30-degrees/SKILL.md",
    },
    {
        "id": 21,
        "name": "diagram_21_circle_sector_hatching",
        "indicator_code": "B8.3.1.2.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Mensuration 60-Degree Sector",
        "tex_file": "data/diagrams/math_redrawn/diagram_21_circle_sector_hatching.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_21_circle_sector_hatching.png",
        "skill": "diagram-21-circle-sector-hatching",
        "skill_file": ".agents/skills/diagram-21-circle-sector-hatching/SKILL.md",
    },
    {
        "id": 22,
        "name": "diagram_22_triangle_congruent_segments",
        "indicator_code": "B8.3.1.2.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Composite Equilateral & Isosceles",
        "tex_file": "data/diagrams/math_redrawn/diagram_22_triangle_congruent_segments.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_22_triangle_congruent_segments.png",
        "skill": "diagram-22-triangle-congruent-segments",
        "skill_file": ".agents/skills/diagram-22-triangle-congruent-segments/SKILL.md",
    },
    {
        "id": 23,
        "name": "diagram_23_parallel_reflex_angle",
        "indicator_code": "B8.3.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Zigzag Transversal Reflex Angle",
        "tex_file": "data/diagrams/math_redrawn/diagram_23_parallel_reflex_angle.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_23_parallel_reflex_angle.png",
        "skill": "diagram-23-parallel-reflex-angle",
        "skill_file": ".agents/skills/diagram-23-parallel-reflex-angle/SKILL.md",
    },
    {
        "id": 24,
        "name": "diagram_24_pythagoras_triangle",
        "indicator_code": "B9.3.1.2.1",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Right Triangle 5-12-13 Pythagoras",
        "tex_file": "data/diagrams/math_redrawn/diagram_24_pythagoras_triangle.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_24_pythagoras_triangle.png",
        "skill": "diagram-24-pythagoras-triangle",
        "skill_file": ".agents/skills/diagram-24-pythagoras-triangle/SKILL.md",
    },
    {
        "id": 25,
        "name": "diagram_25_venn_circle_triangle",
        "indicator_code": "B8.1.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Non-Standard Circle-Triangle Venn",
        "tex_file": "data/diagrams/math_redrawn/diagram_25_venn_circle_triangle.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_25_venn_circle_triangle.png",
        "skill": "diagram-25-venn-circle-triangle",
        "skill_file": ".agents/skills/diagram-25-venn-circle-triangle/SKILL.md",
    },
    {
        "id": 26,
        "name": "diagram_26_perpendicular_bisector",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Perpendicular Bisector Construction",
        "tex_file": "data/diagrams/math_redrawn/diagram_26_perpendicular_bisector.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_26_perpendicular_bisector.png",
        "skill": "diagram-26-perpendicular-bisector",
        "skill_file": ".agents/skills/diagram-26-perpendicular-bisector/SKILL.md",
    },
    {
        "id": 27,
        "name": "diagram_27_construction_90_degrees",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Compass Construction 90 Degrees",
        "tex_file": "data/diagrams/math_redrawn/diagram_27_construction_90_degrees.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_27_construction_90_degrees.png",
        "skill": "diagram-27-construction-90-degrees",
        "skill_file": ".agents/skills/diagram-27-construction-90-degrees/SKILL.md",
    },
    {
        "id": 28,
        "name": "diagram_28_construction_60_degrees",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Compass Construction 60 Degrees",
        "tex_file": "data/diagrams/math_redrawn/diagram_28_construction_60_degrees.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_28_construction_60_degrees.png",
        "skill": "diagram-28-construction-60-degrees",
        "skill_file": ".agents/skills/diagram-28-construction-60-degrees/SKILL.md",
    },
    {
        "id": 29,
        "name": "diagram_29_construction_45_degrees",
        "indicator_code": "B7.3.1.2.3",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Compass Construction 45 Degrees",
        "tex_file": "data/diagrams/math_redrawn/diagram_29_construction_45_degrees.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_29_construction_45_degrees.png",
        "skill": "diagram-29-construction-45-degrees",
        "skill_file": ".agents/skills/diagram-29-construction-45-degrees/SKILL.md",
    },
    {
        "id": 30,
        "name": "diagram_30_triangle_construction_sss",
        "indicator_code": "B8.3.1.2.3",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Compass SSS Triangle Construction",
        "tex_file": "data/diagrams/math_redrawn/diagram_30_triangle_construction_sss.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_30_triangle_construction_sss.png",
        "skill": "diagram-30-triangle-construction-sss",
        "skill_file": ".agents/skills/diagram-30-triangle-construction-sss/SKILL.md",
    },
    {
        "id": 31,
        "name": "diagram_31_inscribed_circle_triangle",
        "indicator_code": "B9.3.1.2.3",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Inscribed Circle via Angle Bisectors",
        "tex_file": "data/diagrams/math_redrawn/diagram_31_inscribed_circle_triangle.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_31_inscribed_circle_triangle.png",
        "skill": "diagram-31-inscribed-circle-triangle",
        "skill_file": ".agents/skills/diagram-31-inscribed-circle-triangle/SKILL.md",
    },
    {
        "id": 32,
        "name": "diagram_32_reflection_cartesian_grid",
        "indicator_code": "B7.3.3.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Reflection Across x-axis on Grid",
        "tex_file": "data/diagrams/math_redrawn/diagram_32_reflection_cartesian_grid.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_32_reflection_cartesian_grid.png",
        "skill": "diagram-32-reflection-cartesian-grid",
        "skill_file": ".agents/skills/diagram-32-reflection-cartesian-grid/SKILL.md",
    },
    {
        "id": 33,
        "name": "diagram_33_translation_vector_grid",
        "indicator_code": "B8.3.3.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Translation by Vector on Grid",
        "tex_file": "data/diagrams/math_redrawn/diagram_33_translation_vector_grid.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_33_translation_vector_grid.png",
        "skill": "diagram-33-translation-vector-grid",
        "skill_file": ".agents/skills/diagram-33-translation-vector-grid/SKILL.md",
    },
    {
        "id": 34,
        "name": "diagram_34_rotation_cartesian_grid",
        "indicator_code": "B9.3.3.1.1",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Rotation 90 Degrees Anticlockwise",
        "tex_file": "data/diagrams/math_redrawn/diagram_34_rotation_cartesian_grid.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_34_rotation_cartesian_grid.png",
        "skill": "diagram-34-rotation-cartesian-grid",
        "skill_file": ".agents/skills/diagram-34-rotation-cartesian-grid/SKILL.md",
    },
    {
        "id": 35,
        "name": "diagram_35_enlargement_scale_factor",
        "indicator_code": "B9.3.3.1.2",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Enlargement Scale Factor k=2",
        "tex_file": "data/diagrams/math_redrawn/diagram_35_enlargement_scale_factor.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_35_enlargement_scale_factor.png",
        "skill": "diagram-35-enlargement-scale-factor",
        "skill_file": ".agents/skills/diagram-35-enlargement-scale-factor/SKILL.md",
    },
    {
        "id": 36,
        "name": "diagram_36_vector_addition_laws",
        "indicator_code": "B8.3.2.1.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Triangle & Parallelogram Laws",
        "tex_file": "data/diagrams/math_redrawn/diagram_36_vector_addition_laws.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_36_vector_addition_laws.png",
        "skill": "diagram-36-vector-addition-laws",
        "skill_file": ".agents/skills/diagram-36-vector-addition-laws/SKILL.md",
    },
    {
        "id": 37,
        "name": "diagram_37_bearing_back_bearing",
        "indicator_code": "B9.3.1.2.2",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Forward & Back Bearing Stations",
        "tex_file": "data/diagrams/math_redrawn/diagram_37_bearing_back_bearing.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_37_bearing_back_bearing.png",
        "skill": "diagram-37-bearing-back-bearing",
        "skill_file": ".agents/skills/diagram-37-bearing-back-bearing/SKILL.md",
    },
    {
        "id": 38,
        "name": "diagram_38_cylinder_mensuration",
        "indicator_code": "B8.3.1.1.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "3D Cylinder Radius & Height",
        "tex_file": "data/diagrams/math_redrawn/diagram_38_cylinder_mensuration.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_38_cylinder_mensuration.png",
        "skill": "diagram-38-cylinder-mensuration",
        "skill_file": ".agents/skills/diagram-38-cylinder-mensuration/SKILL.md",
    },
    {
        "id": 39,
        "name": "diagram_39_triangular_prism_net",
        "indicator_code": "B7.3.1.2.1",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "2D Net of Right Triangular Prism",
        "tex_file": "data/diagrams/math_redrawn/diagram_39_triangular_prism_net.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_39_triangular_prism_net.png",
        "skill": "diagram-39-triangular-prism-net",
        "skill_file": ".agents/skills/diagram-39-triangular-prism-net/SKILL.md",
    },
    {
        "id": 40,
        "name": "diagram_40_cone_mensuration",
        "indicator_code": "B9.3.1.1.2",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "3D Cone Slant Height & Altitude",
        "tex_file": "data/diagrams/math_redrawn/diagram_40_cone_mensuration.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_40_cone_mensuration.png",
        "skill": "diagram-40-cone-mensuration",
        "skill_file": ".agents/skills/diagram-40-cone-mensuration/SKILL.md",
    },
    {
        "id": 41,
        "name": "diagram_41_cumulative_frequency_ogive",
        "indicator_code": "B9.4.1.2.1",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Cumulative Frequency Ogive & Quartiles",
        "tex_file": "data/diagrams/math_redrawn/diagram_41_cumulative_frequency_ogive.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_41_cumulative_frequency_ogive.png",
        "skill": "diagram-41-cumulative-frequency-ogive",
        "skill_file": ".agents/skills/diagram-41-cumulative-frequency-ogive/SKILL.md",
    },
    {
        "id": 42,
        "name": "diagram_42_stem_and_leaf_plot",
        "indicator_code": "B8.4.1.1.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Ordered Stem-and-Leaf Plot & Key",
        "tex_file": "data/diagrams/math_redrawn/diagram_42_stem_and_leaf_plot.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_42_stem_and_leaf_plot.png",
        "skill": "diagram-42-stem-and-leaf-plot",
        "skill_file": ".agents/skills/diagram-42-stem-and-leaf-plot/SKILL.md",
    },
    {
        "id": 43,
        "name": "diagram_43_circle_tangent_theorems",
        "indicator_code": "B8.3.1.2.2",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Circle Tangents from External Point",
        "tex_file": "data/diagrams/math_redrawn/diagram_43_circle_tangent_theorems.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_43_circle_tangent_theorems.png",
        "skill": "diagram-43-circle-tangent-theorems",
        "skill_file": ".agents/skills/diagram-43-circle-tangent-theorems/SKILL.md",
    },
    {
        "id": 44,
        "name": "diagram_44_regular_polygon_angles",
        "indicator_code": "B8.3.1.2.1",
        "grade": "B8",
        "subject": "Mathematics",
        "topic": "Regular Hexagon Interior/Exterior Angles",
        "tex_file": "data/diagrams/math_redrawn/diagram_44_regular_polygon_angles.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_44_regular_polygon_angles.png",
        "skill": "diagram-44-regular-polygon-angles",
        "skill_file": ".agents/skills/diagram-44-regular-polygon-angles/SKILL.md",
    },
    {
        "id": 45,
        "name": "diagram_45_linear_function_graph",
        "indicator_code": "B7.2.2.1.2",
        "grade": "B7",
        "subject": "Mathematics",
        "topic": "Linear Function y = mx + c on Grid",
        "tex_file": "data/diagrams/math_redrawn/diagram_45_linear_function_graph.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_45_linear_function_graph.png",
        "skill": "diagram-45-linear-function-graph",
        "skill_file": ".agents/skills/diagram-45-linear-function-graph/SKILL.md",
    },
    {
        "id": 46,
        "name": "diagram_46_probability_tree_diagram",
        "indicator_code": "B9.4.2.1.1",
        "grade": "B9",
        "subject": "Mathematics",
        "topic": "Probability Tree (No Replacement)",
        "tex_file": "data/diagrams/math_redrawn/diagram_46_probability_tree_diagram.tex",
        "png_file": "data/diagrams/math_redrawn/diagram_46_probability_tree_diagram.png",
        "skill": "diagram-46-probability-tree-diagram",
        "skill_file": ".agents/skills/diagram-46-probability-tree-diagram/SKILL.md",
    },
]


def list_canonical_diagrams(
    subject: Optional[str] = None, grade: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Returns canonical diagrams matching the specified subject and/or grade."""
    res = list(CANONICAL_DIAGRAMS)
    if subject:
        res = [d for d in res if d["subject"].lower() == subject.lower()]
    if grade:
        res = [d for d in res if d["grade"].upper() == grade.upper()]
    return res


def get_canonical_diagram(key: Any) -> Optional[Dict[str, Any]]:
    """Looks up a canonical diagram by integer ID, diagram name, or skill name."""
    if isinstance(key, int):
        for d in CANONICAL_DIAGRAMS:
            if d["id"] == key:
                return d
    elif isinstance(key, str):
        key_clean = key.strip().lower()
        for d in CANONICAL_DIAGRAMS:
            if (
                str(d["id"]) == key_clean
                or d["name"].lower() == key_clean
                or d["skill"].lower() == key_clean
            ):
                return d
    return None


def get_diagrams_for_indicator(
    indicator_code: str, subject: str = "Mathematics"
) -> List[Dict[str, Any]]:
    """Returns all canonical diagrams associated with a specific curriculum indicator."""
    code_clean = indicator_code.strip().upper()
    return [
        d
        for d in CANONICAL_DIAGRAMS
        if d["indicator_code"].upper() == code_clean
        and d["subject"].lower() == subject.lower()
    ]



if __name__ == "__main__":
    items = build_full_curriculum_taxonomy()
    print(f"Total compiled curriculum indicators: {len(items)}")
    by_subject = {}
    by_grade = {}
    for it in items:
        by_subject[it["subject"]] = by_subject.get(it["subject"], 0) + 1
        by_grade[it["grade"]] = by_grade.get(it["grade"], 0) + 1
    print(f"By Subject: {by_subject}")
    print(f"By Grade: {by_grade}")
