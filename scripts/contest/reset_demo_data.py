from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from deeptutor.services.evidence.diagnosis import build_student_diagnosis
from deeptutor.services.evidence.diagnosis_feedback import create_diagnosis_feedback
from deeptutor.services.evidence.intervention_assignments import create_intervention_assignment
from deeptutor.services.evidence.recommendation_acks import create_recommendation_ack
from deeptutor.services.evidence.recommendation_feedback import create_recommendation_feedback
from deeptutor.services.evidence.teacher_actions import create_teacher_action
from deeptutor.services.evidence.teacher_insights import build_teacher_insights_payload
from deeptutor.services.evidence.teacher_overrides import create_teacher_override
from deeptutor.services.session.sqlite_store import SQLiteSessionStore


DEMO_KB_ID = "contest-demo-quadratics"
ASSESSMENT_SESSION_ID = "contest-assessment-demo"
TUTOR_SESSION_ID = "contest-tutor-demo"
DEMO_MARKER = "[contest-demo]"
DEMO_COHORT = "Class 9A1"
DEMO_OWNER = "Contest Demo Teacher"
SECONDS_PER_DAY = 24 * 60 * 60

DEMO_STUDENTS = [
    {"id": "Ngoc An", "focus_topic": "quadratic factoring"},
    {"id": "Minh Chau", "focus_topic": "quadratic factoring"},
    {"id": "Bao Han", "focus_topic": "discriminant selection"},
    {"id": "Quoc Dat", "focus_topic": "graph interpretation"},
]

DEMO_SHAREABLE_PACKS = [
    {
        "name": DEMO_KB_ID,
        "description": "Contest-ready pack for Grade 9 quadratic equations and common factoring errors.",
        "subject": "Mathematics",
        "grade": "Grade 9",
        "curriculum": "Vietnam secondary algebra",
        "learning_objectives": [
            "Solve quadratic equations",
            "Explain common factoring mistakes",
            "Check roots against the original equation",
        ],
        "owner": DEMO_OWNER,
        "sharing_status": "public",
        "tags": ["algebra", "quadratics", "contest-demo"],
        "difficulty": "intermediate",
        "language": "Vietnamese",
        "estimated_hours": 6.0,
        "prerequisites": ["Linear equations", "Integer arithmetic"],
        "content_types": ["notes", "worked_examples", "practice_sets"],
        "documents": [
            "lesson-overview.md",
            "factoring-patterns.md",
            "common-mistakes.md",
            "guided-practice.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Lan",
                "rating": 5,
                "comment": "Students used the mistake notes right away during revision week.",
                "created_at": "2026-04-18T08:30:00",
            },
            {
                "reviewer": "Teacher Minh",
                "rating": 4,
                "comment": "Clear sequence for remediation after a short quiz.",
                "created_at": "2026-04-17T14:10:00",
            },
        ],
        "created_at": "2026-04-10T08:00:00",
        "updated_at": "2026-04-29T09:15:00",
    },
    {
        "name": "contest-demo-factoring-foundations",
        "description": "Warm-up pack for factor pairs, sign checks, and binomial pattern fluency.",
        "subject": "Mathematics",
        "grade": "Grade 8",
        "curriculum": "Vietnam secondary algebra",
        "learning_objectives": [
            "Recognize factor pairs",
            "Track positive and negative signs while factoring",
        ],
        "owner": "Teacher Thu",
        "sharing_status": "public",
        "tags": ["factoring", "foundations"],
        "difficulty": "beginner",
        "language": "Vietnamese",
        "estimated_hours": 4.0,
        "prerequisites": ["Multiplication facts"],
        "content_types": ["notes", "exit_tickets"],
        "documents": [
            "factor-pairs.md",
            "sign-check-drill.md",
            "exit-ticket.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Hanh",
                "rating": 5,
                "comment": "Strong prep before moving to quadratics.",
                "created_at": "2026-04-20T09:00:00",
            }
        ],
        "created_at": "2026-04-08T09:30:00",
        "updated_at": "2026-04-27T11:00:00",
    },
    {
        "name": "contest-demo-linear-systems-bridge",
        "description": "Bridge pack linking substitution habits to later quadratic structure work.",
        "subject": "Mathematics",
        "grade": "Grade 9",
        "curriculum": "Vietnam secondary algebra",
        "learning_objectives": [
            "Solve linear systems by substitution",
            "Explain why variable isolation matters",
        ],
        "owner": "Teacher Bao",
        "sharing_status": "team",
        "tags": ["systems", "algebra-bridge"],
        "difficulty": "intermediate",
        "language": "Vietnamese",
        "estimated_hours": 5.0,
        "prerequisites": ["Linear equations"],
        "content_types": ["notes", "practice_sets"],
        "documents": [
            "substitution-review.md",
            "bridge-examples.md",
            "guided-exercises.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Phuc",
                "rating": 4,
                "comment": "Useful bridge unit for mixed-ability groups.",
                "created_at": "2026-04-16T07:45:00",
            }
        ],
        "created_at": "2026-04-07T10:00:00",
        "updated_at": "2026-04-25T15:00:00",
    },
    {
        "name": "contest-demo-geometry-proof-starters",
        "description": "Short proof starters for building justification language in lower-secondary geometry.",
        "subject": "Mathematics",
        "grade": "Grade 8",
        "curriculum": "Vietnam geometry foundations",
        "learning_objectives": [
            "State known and unknown information clearly",
            "Use congruence clues in short written proofs",
        ],
        "owner": "Teacher Nhi",
        "sharing_status": "public",
        "tags": ["geometry", "proof-writing"],
        "difficulty": "intermediate",
        "language": "Vietnamese",
        "estimated_hours": 3.5,
        "prerequisites": ["Basic angle relationships"],
        "content_types": ["worked_examples", "discussion_prompts"],
        "documents": [
            "proof-language.md",
            "triangle-congruence.md",
            "discussion-prompts.md",
        ],
        "marketplace_reviews": [],
        "created_at": "2026-04-05T13:30:00",
        "updated_at": "2026-04-21T08:40:00",
    },
    {
        "name": "contest-demo-statistics-charts",
        "description": "Chart-reading pack with class survey data and common interpretation traps.",
        "subject": "Mathematics",
        "grade": "Grade 7",
        "curriculum": "Vietnam applied statistics",
        "learning_objectives": [
            "Read bar and line charts accurately",
            "Summarize a class dataset in one sentence",
        ],
        "owner": "Teacher Giang",
        "sharing_status": "public",
        "tags": ["statistics", "charts"],
        "difficulty": "beginner",
        "language": "Vietnamese",
        "estimated_hours": 2.5,
        "prerequisites": ["Whole-number comparison"],
        "content_types": ["slides", "practice_sets"],
        "documents": [
            "class-survey.md",
            "bar-charts.md",
            "line-charts.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Vy",
                "rating": 4,
                "comment": "Good for quick dashboard screenshots with varied metadata.",
                "created_at": "2026-04-14T12:00:00",
            }
        ],
        "created_at": "2026-04-04T08:00:00",
        "updated_at": "2026-04-19T09:25:00",
    },
    {
        "name": "contest-demo-microscope-observation-writing",
        "description": "STEM pack for recording microscope observations with precise evidence language.",
        "subject": "Science",
        "grade": "Grade 7",
        "curriculum": "Integrated STEM",
        "learning_objectives": [
            "Describe what is observed before drawing conclusions",
            "Use evidence-based sentence starters",
        ],
        "owner": "Teacher Quynh",
        "sharing_status": "team",
        "tags": ["science", "stem", "observation-writing"],
        "difficulty": "beginner",
        "language": "Vietnamese",
        "estimated_hours": 3.0,
        "prerequisites": ["Basic lab routines"],
        "content_types": ["lab-sheet", "rubrics"],
        "documents": [
            "microscope-routine.md",
            "observation-sentences.md",
            "lab-checklist.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Dung",
                "rating": 5,
                "comment": "Nice cross-subject example for the marketplace page.",
                "created_at": "2026-04-13T16:20:00",
            }
        ],
        "created_at": "2026-04-03T10:20:00",
        "updated_at": "2026-04-18T14:55:00",
    },
    {
        "name": "contest-demo-graph-reading-extensions",
        "description": "Extension pack for connecting graph features to verbal reasoning.",
        "subject": "Mathematics",
        "grade": "Grade 9",
        "curriculum": "Vietnam algebra applications",
        "learning_objectives": [
            "Interpret turning points and intercepts",
            "Explain graph behavior in words",
        ],
        "owner": "Teacher Linh",
        "sharing_status": "public",
        "tags": ["graphs", "reasoning"],
        "difficulty": "advanced",
        "language": "Vietnamese",
        "estimated_hours": 4.5,
        "prerequisites": ["Coordinate plane", "Linear graphs"],
        "content_types": ["worked_examples", "practice_sets"],
        "documents": [
            "graph-features.md",
            "reasoning-prompts.md",
            "challenge-questions.md",
        ],
        "marketplace_reviews": [
            {
                "reviewer": "Teacher Khoa",
                "rating": 4,
                "comment": "Strong extension material for confident students.",
                "created_at": "2026-04-15T17:00:00",
            }
        ],
        "created_at": "2026-04-06T07:50:00",
        "updated_at": "2026-04-26T10:35:00",
    },
]

DEMO_IMPORTED_PACKS = [
    {
        "source_name": DEMO_KB_ID,
        "name": f"{DEMO_KB_ID}__imported",
        "description": "Imported into the contest demo workspace for the active classroom flow.",
        "created_at": "2026-04-29T09:20:00",
        "updated_at": "2026-04-29T09:20:00",
    },
    {
        "source_name": "contest-demo-statistics-charts",
        "name": "contest-demo-statistics-charts__imported",
        "description": "Imported reference pack used to show multiple teacher-owned packs in the workspace.",
        "created_at": "2026-04-28T15:40:00",
        "updated_at": "2026-04-28T15:40:00",
    },
]

DEMO_ASSESSMENTS = [
    {
        "session_id": ASSESSMENT_SESSION_ID,
        "student_id": "Ngoc An",
        "title": "Ngoc An - Quadratic Checkpoint 1",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-17T08:10:00",
        "request": "Generate a short quadratic factoring check for Ngoc An in class 9A1.",
        "quiz_intro": "Generated a short class checkpoint focused on factoring and checking roots.",
        "review": [
            {
                "question_id": "q1",
                "question": "Factor x^2 - 5x + 6",
                "answer": "(x+2)(x+3)",
                "correct_answer": "(x-2)(x-3)",
                "is_correct": False,
                "duration_seconds": 53,
            },
            {
                "question_id": "q2",
                "question": "Solve x^2 - 5x + 6 = 0",
                "answer": "x = -2, -3",
                "correct_answer": "x = 2, 3",
                "is_correct": False,
                "duration_seconds": 61,
            },
            {
                "question_id": "q3",
                "question": "Check whether x = 3 is a root of x^2 - 5x + 6",
                "answer": "Yes",
                "correct_answer": "Yes",
                "is_correct": True,
                "duration_seconds": 22,
            },
            {
                "question_id": "q4",
                "question": "State one sign check to confirm the factors",
                "answer": "Multiply to 6 and add to -5",
                "correct_answer": "Multiply to 6 and add to -5",
                "is_correct": True,
                "duration_seconds": 31,
            },
        ],
    },
    {
        "session_id": "contest-assessment-ngoc-an-followup",
        "student_id": "Ngoc An",
        "title": "Ngoc An - Quadratic Checkpoint 2",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-24T08:05:00",
        "request": "Generate a follow-up factoring check after a reteach mini lesson.",
        "quiz_intro": "Generated a follow-up checkpoint with the same topic and lighter scaffolding.",
        "review": [
            {
                "question_id": "q1",
                "question": "Factor x^2 - 7x + 12",
                "answer": "(x-3)(x-4)",
                "correct_answer": "(x-3)(x-4)",
                "is_correct": True,
                "duration_seconds": 35,
            },
            {
                "question_id": "q2",
                "question": "Solve x^2 - 7x + 12 = 0",
                "answer": "x = 3, 4",
                "correct_answer": "x = 3, 4",
                "is_correct": True,
                "duration_seconds": 29,
            },
            {
                "question_id": "q3",
                "question": "Factor x^2 - x - 12",
                "answer": "(x-4)(x+3)",
                "correct_answer": "(x-4)(x+3)",
                "is_correct": True,
                "duration_seconds": 44,
            },
            {
                "question_id": "q4",
                "question": "Explain how the middle term helps choose the signs",
                "answer": "The factors add to -1 so one sign must be negative.",
                "correct_answer": "The factors add to -1 so one sign must be negative.",
                "is_correct": True,
                "duration_seconds": 41,
            },
        ],
    },
    {
        "session_id": "contest-assessment-minh-chau-1",
        "student_id": "Minh Chau",
        "title": "Minh Chau - Quadratic Checkpoint 1",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-17T08:25:00",
        "request": "Generate a quadratic factoring check for Minh Chau.",
        "quiz_intro": "Generated a class checkpoint focused on factor selection and sign tracking.",
        "review": [
            {
                "question_id": "q1",
                "question": "Factor x^2 - 6x + 8",
                "answer": "(x+2)(x+4)",
                "correct_answer": "(x-2)(x-4)",
                "is_correct": False,
                "duration_seconds": 49,
            },
            {
                "question_id": "q2",
                "question": "Solve x^2 - 6x + 8 = 0",
                "answer": "x = -2, -4",
                "correct_answer": "x = 2, 4",
                "is_correct": False,
                "duration_seconds": 57,
            },
            {
                "question_id": "q3",
                "question": "Check whether x = 4 is a root of x^2 - 6x + 8",
                "answer": "Yes",
                "correct_answer": "Yes",
                "is_correct": True,
                "duration_seconds": 24,
            },
        ],
    },
    {
        "session_id": "contest-assessment-minh-chau-2",
        "student_id": "Minh Chau",
        "title": "Minh Chau - Quadratic Checkpoint 2",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-25T08:15:00",
        "request": "Generate a second factoring check after guided practice.",
        "quiz_intro": "Generated a follow-up checkpoint with one application question included.",
        "review": [
            {
                "question_id": "q1",
                "question": "Factor x^2 - 9x + 20",
                "answer": "(x-4)(x-5)",
                "correct_answer": "(x-4)(x-5)",
                "is_correct": True,
                "duration_seconds": 33,
            },
            {
                "question_id": "q2",
                "question": "Factor x^2 - 2x - 15",
                "answer": "(x-5)(x+3)",
                "correct_answer": "(x-5)(x+3)",
                "is_correct": True,
                "duration_seconds": 39,
            },
            {
                "question_id": "q3",
                "question": "Solve x^2 - 2x - 15 = 0",
                "answer": "x = 5, -3",
                "correct_answer": "x = 5, -3",
                "is_correct": True,
                "duration_seconds": 30,
            },
            {
                "question_id": "q4",
                "question": "Describe one fast way to reject the wrong sign pair",
                "answer": "Check the sum before multiplying out the full expression.",
                "correct_answer": "Check the sum before multiplying out the full expression.",
                "is_correct": True,
                "duration_seconds": 34,
            },
        ],
    },
    {
        "session_id": "contest-assessment-bao-han-1",
        "student_id": "Bao Han",
        "title": "Bao Han - Discriminant Checkpoint 1",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-18T09:05:00",
        "request": "Generate a short discriminant quiz for Bao Han.",
        "quiz_intro": "Generated a checkpoint on choosing the discriminant before solving.",
        "review": [
            {
                "question_id": "q1",
                "question": "What is the discriminant of x^2 - 4x + 7 = 0",
                "answer": "9",
                "correct_answer": "-12",
                "is_correct": False,
                "duration_seconds": 46,
            },
            {
                "question_id": "q2",
                "question": "How many real roots does x^2 - 4x + 7 = 0 have",
                "answer": "2",
                "correct_answer": "0",
                "is_correct": False,
                "duration_seconds": 38,
            },
            {
                "question_id": "q3",
                "question": "What does a negative discriminant tell you",
                "answer": "No real roots",
                "correct_answer": "No real roots",
                "is_correct": True,
                "duration_seconds": 19,
            },
        ],
    },
    {
        "session_id": "contest-assessment-bao-han-2",
        "student_id": "Bao Han",
        "title": "Bao Han - Discriminant Checkpoint 2",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-26T09:10:00",
        "request": "Generate a second discriminant checkpoint with a quick transfer question.",
        "quiz_intro": "Generated a follow-up discriminant check after notebook review.",
        "review": [
            {
                "question_id": "q1",
                "question": "What is the discriminant of x^2 + 2x - 3 = 0",
                "answer": "16",
                "correct_answer": "16",
                "is_correct": True,
                "duration_seconds": 28,
            },
            {
                "question_id": "q2",
                "question": "How many real roots does x^2 + 2x - 3 = 0 have",
                "answer": "2",
                "correct_answer": "2",
                "is_correct": True,
                "duration_seconds": 22,
            },
            {
                "question_id": "q3",
                "question": "What is the discriminant of x^2 + 6x + 10 = 0",
                "answer": "4",
                "correct_answer": "-4",
                "is_correct": False,
                "duration_seconds": 35,
            },
        ],
    },
    {
        "session_id": "contest-assessment-quoc-dat-1",
        "student_id": "Quoc Dat",
        "title": "Quoc Dat - Graph Interpretation 1",
        "knowledge_bases": ["contest-demo-graph-reading-extensions"],
        "created_at": "2026-04-19T10:00:00",
        "request": "Generate a graph interpretation check for Quoc Dat.",
        "quiz_intro": "Generated a graph-reading extension check with one verbal reasoning item.",
        "review": [
            {
                "question_id": "q1",
                "question": "What does the x-intercept represent on a quadratic graph",
                "answer": "A root",
                "correct_answer": "A root",
                "is_correct": True,
                "duration_seconds": 18,
            },
            {
                "question_id": "q2",
                "question": "What does the turning point tell you about the graph",
                "answer": "It shows the maximum or minimum value",
                "correct_answer": "It shows the maximum or minimum value",
                "is_correct": True,
                "duration_seconds": 24,
            },
            {
                "question_id": "q3",
                "question": "Describe how the graph changes after the vertex",
                "answer": "It rises again after the minimum",
                "correct_answer": "It rises again after the minimum",
                "is_correct": True,
                "duration_seconds": 29,
            },
        ],
    },
    {
        "session_id": "contest-assessment-quoc-dat-2",
        "student_id": "Quoc Dat",
        "title": "Quoc Dat - Graph Interpretation 2",
        "knowledge_bases": ["contest-demo-graph-reading-extensions"],
        "created_at": "2026-04-27T10:05:00",
        "request": "Generate a follow-up graph reasoning check for Quoc Dat.",
        "quiz_intro": "Generated a follow-up extension with one transfer item.",
        "review": [
            {
                "question_id": "q1",
                "question": "A graph opens upward and crosses the x-axis twice. What does that imply",
                "answer": "It has two real roots",
                "correct_answer": "It has two real roots",
                "is_correct": True,
                "duration_seconds": 21,
            },
            {
                "question_id": "q2",
                "question": "What does the y-intercept show on y = x^2 - 4x + 3",
                "answer": "The value when x = 0",
                "correct_answer": "The value when x = 0",
                "is_correct": True,
                "duration_seconds": 19,
            },
            {
                "question_id": "q3",
                "question": "Explain one way graph shape supports your answer about roots",
                "answer": "Where it crosses the axis shows the roots",
                "correct_answer": "Where it crosses the axis shows the roots",
                "is_correct": True,
                "duration_seconds": 26,
            },
        ],
    },
]

DEMO_TUTORS = [
    {
        "session_id": TUTOR_SESSION_ID,
        "student_id": "Ngoc An",
        "title": "Ngoc An - Tutor Replay",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-17T14:15:00",
        "messages": [
            ("user", "I still mix up the signs when I factor x^2 - 5x + 6."),
            (
                "assistant",
                "Start with factor pairs of 6: (1, 6) and (2, 3). Now ask which pair adds to -5. Both numbers must be negative.",
            ),
            ("user", "So I should test the sum before I write the brackets?"),
            (
                "assistant",
                "Yes. Quick check first: the product gives 6 and the sum gives -5, so (x-2)(x-3) is the match. Then verify by expanding once.",
            ),
        ],
    },
    {
        "session_id": "contest-tutor-minh-chau-followup",
        "student_id": "Minh Chau",
        "title": "Minh Chau - Tutor Follow-up",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-18T15:05:00",
        "messages": [
            ("user", "I know the factor pair, but I rush and flip the signs."),
            (
                "assistant",
                "Use a two-step routine: choose the factor pair, then say the target sum out loud before writing the brackets.",
            ),
            ("user", "Can you give me one similar example?"),
            (
                "assistant",
                "Try x^2 - 6x + 8. The pair is 2 and 4, and because the sum must be -6, both signs are negative.",
            ),
        ],
    },
    {
        "session_id": "contest-tutor-bao-han-discriminant",
        "student_id": "Bao Han",
        "title": "Bao Han - Tutor Replay",
        "knowledge_bases": [f"{DEMO_KB_ID}__imported"],
        "created_at": "2026-04-20T13:30:00",
        "messages": [
            ("user", "I forget when the discriminant means there are no real roots."),
            (
                "assistant",
                "Compute b squared minus 4ac first. If the result is negative, the graph does not cross the x-axis, so there are no real roots.",
            ),
            ("user", "So I should decide the number of roots before solving?"),
            (
                "assistant",
                "Exactly. That keeps the logic clean and avoids choosing an impossible answer set.",
            ),
        ],
    },
    {
        "session_id": "contest-tutor-quoc-dat-extension",
        "student_id": "Quoc Dat",
        "title": "Quoc Dat - Extension Replay",
        "knowledge_bases": ["contest-demo-graph-reading-extensions"],
        "created_at": "2026-04-28T11:10:00",
        "messages": [
            ("user", "I can name the vertex, but I want to explain what it means better."),
            (
                "assistant",
                "Describe it as the point where the graph changes direction and where the output reaches its maximum or minimum value.",
            ),
            ("user", "How do I connect that to roots?"),
            (
                "assistant",
                "Use both features together: the vertex shows the turning point, and the x-intercepts show where the output becomes zero.",
            ),
        ],
    },
]

DEMO_OBSERVATIONS = [
    {
        "observation_id": "contest-demo-obs-ngoc-an-a1",
        "session_id": ASSESSMENT_SESSION_ID,
        "student_id": "Ngoc An",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q1",
        "is_correct": False,
        "latency_seconds": 53,
        "hint_count": 1,
        "retry_count": 2,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-17T08:14:00",
    },
    {
        "observation_id": "contest-demo-obs-ngoc-an-a2",
        "session_id": ASSESSMENT_SESSION_ID,
        "student_id": "Ngoc An",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q2",
        "is_correct": False,
        "latency_seconds": 61,
        "hint_count": 1,
        "retry_count": 2,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-17T08:16:00",
    },
    {
        "observation_id": "contest-demo-obs-ngoc-an-t1",
        "session_id": TUTOR_SESSION_ID,
        "student_id": "Ngoc An",
        "source": "tutoring",
        "topic": "quadratic factoring",
        "question_id": "followup-1",
        "is_correct": True,
        "latency_seconds": 37,
        "hint_count": 1,
        "retry_count": 1,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-17T14:20:00",
    },
    {
        "observation_id": "contest-demo-obs-ngoc-an-a3",
        "session_id": "contest-assessment-ngoc-an-followup",
        "student_id": "Ngoc An",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q3",
        "is_correct": True,
        "latency_seconds": 44,
        "hint_count": 0,
        "retry_count": 1,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-24T08:18:00",
    },
    {
        "observation_id": "contest-demo-obs-minh-chau-a1",
        "session_id": "contest-assessment-minh-chau-1",
        "student_id": "Minh Chau",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q1",
        "is_correct": False,
        "latency_seconds": 49,
        "hint_count": 1,
        "retry_count": 2,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-17T08:28:00",
    },
    {
        "observation_id": "contest-demo-obs-minh-chau-a2",
        "session_id": "contest-assessment-minh-chau-1",
        "student_id": "Minh Chau",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q2",
        "is_correct": False,
        "latency_seconds": 57,
        "hint_count": 1,
        "retry_count": 2,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-17T08:31:00",
    },
    {
        "observation_id": "contest-demo-obs-minh-chau-t1",
        "session_id": "contest-tutor-minh-chau-followup",
        "student_id": "Minh Chau",
        "source": "tutoring",
        "topic": "quadratic factoring",
        "question_id": "followup-1",
        "is_correct": True,
        "latency_seconds": 34,
        "hint_count": 1,
        "retry_count": 1,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-18T15:12:00",
    },
    {
        "observation_id": "contest-demo-obs-minh-chau-a3",
        "session_id": "contest-assessment-minh-chau-2",
        "student_id": "Minh Chau",
        "source": "assessment",
        "topic": "quadratic factoring",
        "question_id": "q4",
        "is_correct": True,
        "latency_seconds": 34,
        "hint_count": 0,
        "retry_count": 0,
        "dominant_error": "procedure_breakdown",
        "created_at": "2026-04-25T08:18:00",
    },
    {
        "observation_id": "contest-demo-obs-bao-han-a1",
        "session_id": "contest-assessment-bao-han-1",
        "student_id": "Bao Han",
        "source": "assessment",
        "topic": "discriminant selection",
        "question_id": "q1",
        "is_correct": False,
        "latency_seconds": 46,
        "hint_count": 1,
        "retry_count": 1,
        "dominant_error": "concept_gap",
        "created_at": "2026-04-18T09:08:00",
    },
    {
        "observation_id": "contest-demo-obs-bao-han-a2",
        "session_id": "contest-assessment-bao-han-1",
        "student_id": "Bao Han",
        "source": "assessment",
        "topic": "discriminant selection",
        "question_id": "q2",
        "is_correct": False,
        "latency_seconds": 38,
        "hint_count": 1,
        "retry_count": 1,
        "dominant_error": "concept_gap",
        "created_at": "2026-04-18T09:10:00",
    },
    {
        "observation_id": "contest-demo-obs-bao-han-t1",
        "session_id": "contest-tutor-bao-han-discriminant",
        "student_id": "Bao Han",
        "source": "tutoring",
        "topic": "discriminant selection",
        "question_id": "followup-1",
        "is_correct": True,
        "latency_seconds": 27,
        "hint_count": 1,
        "retry_count": 0,
        "dominant_error": "concept_gap",
        "created_at": "2026-04-20T13:34:00",
    },
    {
        "observation_id": "contest-demo-obs-bao-han-a3",
        "session_id": "contest-assessment-bao-han-2",
        "student_id": "Bao Han",
        "source": "assessment",
        "topic": "discriminant selection",
        "question_id": "q3",
        "is_correct": False,
        "latency_seconds": 35,
        "hint_count": 0,
        "retry_count": 1,
        "dominant_error": "concept_gap",
        "created_at": "2026-04-26T09:16:00",
    },
    {
        "observation_id": "contest-demo-obs-quoc-dat-a1",
        "session_id": "contest-assessment-quoc-dat-1",
        "student_id": "Quoc Dat",
        "source": "assessment",
        "topic": "graph interpretation",
        "question_id": "q1",
        "is_correct": True,
        "latency_seconds": 18,
        "hint_count": 0,
        "retry_count": 0,
        "dominant_error": "",
        "created_at": "2026-04-19T10:04:00",
    },
    {
        "observation_id": "contest-demo-obs-quoc-dat-a2",
        "session_id": "contest-assessment-quoc-dat-1",
        "student_id": "Quoc Dat",
        "source": "assessment",
        "topic": "graph interpretation",
        "question_id": "q2",
        "is_correct": True,
        "latency_seconds": 24,
        "hint_count": 0,
        "retry_count": 0,
        "dominant_error": "",
        "created_at": "2026-04-19T10:06:00",
    },
    {
        "observation_id": "contest-demo-obs-quoc-dat-t1",
        "session_id": "contest-tutor-quoc-dat-extension",
        "student_id": "Quoc Dat",
        "source": "tutoring",
        "topic": "graph interpretation",
        "question_id": "followup-1",
        "is_correct": True,
        "latency_seconds": 22,
        "hint_count": 0,
        "retry_count": 0,
        "dominant_error": "",
        "created_at": "2026-04-28T11:14:00",
    },
    {
        "observation_id": "contest-demo-obs-quoc-dat-a3",
        "session_id": "contest-assessment-quoc-dat-2",
        "student_id": "Quoc Dat",
        "source": "assessment",
        "topic": "graph interpretation",
        "question_id": "q3",
        "is_correct": True,
        "latency_seconds": 26,
        "hint_count": 0,
        "retry_count": 0,
        "dominant_error": "",
        "created_at": "2026-04-27T10:08:00",
    },
]

DEMO_SHAREABLE_PACK_NAMES = [pack["name"] for pack in DEMO_SHAREABLE_PACKS]
DEMO_IMPORTED_PACK_NAMES = [pack["name"] for pack in DEMO_IMPORTED_PACKS]
DEMO_KB_NAMES = DEMO_SHAREABLE_PACK_NAMES + DEMO_IMPORTED_PACK_NAMES
DEMO_SESSION_IDS = [row["session_id"] for row in DEMO_ASSESSMENTS] + [row["session_id"] for row in DEMO_TUTORS]
DEMO_STUDENT_IDS = [row["id"] for row in DEMO_STUDENTS]


def _validate_local_api_base(api_base: str) -> None:
    parsed = urlparse(api_base)
    if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1"}:
        raise ValueError("Use a local API base such as http://localhost:8001")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        return {}


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _iso_to_timestamp(value: str) -> float:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc).timestamp()


def _clear_demo_knowledge_packs(project_root: Path) -> dict:
    kb_root = project_root / "data" / "knowledge_bases"
    config_path = kb_root / "kb_config.json"
    config = _read_json(config_path)
    config.setdefault("knowledge_bases", {})
    for name in DEMO_KB_NAMES:
        config["knowledge_bases"].pop(name, None)
        pack_dir = kb_root / name
        if pack_dir.exists():
            shutil.rmtree(pack_dir)
    _write_json(config_path, config)
    return config


def _pack_metadata(pack: dict, *, sharing_status: str | None = None, imported_from: str | None = None) -> dict:
    metadata = {
        "name": pack["name"],
        "description": pack["description"],
        "rag_provider": "llamaindex",
        "status": "ready",
        "subject": pack["subject"],
        "grade": pack["grade"],
        "curriculum": pack["curriculum"],
        "learning_objectives": list(pack["learning_objectives"]),
        "owner": pack["owner"],
        "sharing_status": sharing_status or pack["sharing_status"],
        "tags": list(pack.get("tags", [])),
        "difficulty": pack.get("difficulty"),
        "language": pack.get("language"),
        "estimated_hours": pack.get("estimated_hours"),
        "prerequisites": list(pack.get("prerequisites", [])),
        "content_types": list(pack.get("content_types", [])),
    }
    if imported_from:
        metadata["imported_from"] = imported_from
    return metadata


def _write_pack_files(kb_root: Path, pack: dict, *, metadata: dict) -> Path:
    pack_dir = kb_root / pack["name"]
    (pack_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)
    (pack_dir / "rag_storage").mkdir(parents=True, exist_ok=True)
    raw_dir = pack_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for doc_name in pack.get("documents", []):
        (raw_dir / doc_name).write_text(
            f"# {pack['name']}\n\n{doc_name}\n\nDemo-safe placeholder content for local preview.\n",
            encoding="utf-8",
        )
    _write_json(pack_dir / "metadata.json", metadata)
    return pack_dir


def _config_entry(pack: dict, *, metadata: dict, path_name: str, description: str, imported_from: str | None = None) -> dict:
    entry = {
        "path": path_name,
        "description": description,
        "rag_provider": "llamaindex",
        "status": "ready",
        "created_at": pack["created_at"],
        "updated_at": pack["updated_at"],
        "subject": metadata["subject"],
        "grade": metadata["grade"],
        "curriculum": metadata["curriculum"],
        "learning_objectives": metadata["learning_objectives"],
        "owner": metadata["owner"],
        "sharing_status": metadata["sharing_status"],
        "tags": metadata["tags"],
        "difficulty": metadata["difficulty"],
        "language": metadata["language"],
        "estimated_hours": metadata["estimated_hours"],
        "prerequisites": metadata["prerequisites"],
        "content_types": metadata["content_types"],
        "marketplace_reviews": list(pack.get("marketplace_reviews", [])),
    }
    if imported_from:
        entry["imported_from"] = imported_from
        entry["import_date"] = pack["updated_at"]
    return entry


def _seed_knowledge_packs(project_root: Path) -> dict[str, object]:
    kb_root = project_root / "data" / "knowledge_bases"
    kb_root.mkdir(parents=True, exist_ok=True)
    config = _clear_demo_knowledge_packs(project_root)

    for pack in DEMO_SHAREABLE_PACKS:
        metadata = _pack_metadata(pack)
        _write_pack_files(kb_root, pack, metadata=metadata)
        config["knowledge_bases"][pack["name"]] = _config_entry(
            pack,
            metadata=metadata,
            path_name=pack["name"],
            description=pack["description"],
        )

    shareable_by_name = {pack["name"]: pack for pack in DEMO_SHAREABLE_PACKS}
    for imported in DEMO_IMPORTED_PACKS:
        source_pack = shareable_by_name[imported["source_name"]]
        pack_payload = dict(source_pack)
        pack_payload["name"] = imported["name"]
        pack_payload["description"] = imported["description"]
        pack_payload["sharing_status"] = "private"
        pack_payload["created_at"] = imported["created_at"]
        pack_payload["updated_at"] = imported["updated_at"]
        metadata = _pack_metadata(
            pack_payload,
            sharing_status="private",
            imported_from=imported["source_name"],
        )
        _write_pack_files(kb_root, pack_payload, metadata=metadata)
        config["knowledge_bases"][imported["name"]] = _config_entry(
            pack_payload,
            metadata=metadata,
            path_name=imported["name"],
            description=imported["description"],
            imported_from=imported["source_name"],
        )

    _write_json(kb_root / "kb_config.json", config)
    return {
        "anchor_path": kb_root / DEMO_KB_ID,
        "shareable": DEMO_SHAREABLE_PACK_NAMES,
        "imported": DEMO_IMPORTED_PACK_NAMES,
    }


def _clear_demo_db_records(db_path: Path) -> None:
    SQLiteSessionStore(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executemany("DELETE FROM sessions WHERE id = ?", [(session_id,) for session_id in DEMO_SESSION_IDS])
        conn.executemany("DELETE FROM observations WHERE student_id = ?", [(student_id,) for student_id in DEMO_STUDENT_IDS])
        conn.executemany("DELETE FROM student_states WHERE student_id = ?", [(student_id,) for student_id in DEMO_STUDENT_IDS])

        for table_name, column_name in (
            ("teacher_actions", "teacher_instruction"),
            ("recommendation_acks", "teacher_note"),
            ("recommendation_feedback", "teacher_note"),
            ("teacher_overrides", "teacher_note"),
            ("diagnosis_feedback", "teacher_note"),
        ):
            if _table_exists(conn, table_name):
                conn.execute(f"DELETE FROM {table_name} WHERE {column_name} LIKE ?", (f"%{DEMO_MARKER}%",))
        if _table_exists(conn, "intervention_assignments"):
            conn.execute(
                "DELETE FROM intervention_assignments WHERE teacher_note LIKE ? OR practice_note LIKE ?",
                (f"%{DEMO_MARKER}%", f"%{DEMO_MARKER}%"),
            )
        conn.commit()


def _format_quiz_review(review_rows: list[dict]) -> str:
    lines = ["[Quiz Performance]"]
    for index, row in enumerate(review_rows, start=1):
        status = "Correct" if row["is_correct"] else "Incorrect"
        correct_suffix = f", correct: {row['correct_answer']}" if not row["is_correct"] else ""
        duration_suffix = (
            f", time: {int(row['duration_seconds'])}s"
            if row.get("duration_seconds") is not None
            else ""
        )
        lines.append(
            f"{index}. [{row['question_id']}] Q: {row['question']} -> Answered: {row['answer']} "
            f"({status}{correct_suffix}{duration_suffix})"
        )
    total = len(review_rows)
    correct = sum(1 for row in review_rows if row["is_correct"])
    percent = round((correct / total) * 100) if total else 0
    lines.append(f"Score: {correct}/{total} ({percent}%)")
    return "\n".join(lines)


async def _seed_assessment_sessions(store: SQLiteSessionStore) -> None:
    for row in DEMO_ASSESSMENTS:
        await store.create_session(title=row["title"], session_id=row["session_id"])
        await store.update_session_preferences(
            row["session_id"],
            {
                "capability": "deep_question",
                "tools": ["rag"],
                "knowledge_bases": list(row["knowledge_bases"]),
                "language": "en",
                "student_id": row["student_id"],
                "cohort": DEMO_COHORT,
                "demo": True,
            },
        )
        turn = await store.create_turn(row["session_id"], capability="deep_question")
        await store.add_message(row["session_id"], "user", row["request"], capability="deep_question")
        await store.add_message(row["session_id"], "assistant", row["quiz_intro"], capability="deep_question")
        await store.add_message(
            row["session_id"],
            "user",
            _format_quiz_review(row["review"]),
            capability="deep_question",
        )
        await store.update_turn_status(turn["id"], "completed")


async def _seed_tutor_sessions(store: SQLiteSessionStore) -> None:
    for row in DEMO_TUTORS:
        await store.create_session(title=row["title"], session_id=row["session_id"])
        await store.update_session_preferences(
            row["session_id"],
            {
                "capability": "chat",
                "tools": ["rag"],
                "knowledge_bases": list(row["knowledge_bases"]),
                "language": "en",
                "student_id": row["student_id"],
                "cohort": DEMO_COHORT,
                "demo": True,
            },
        )
        turn = await store.create_turn(row["session_id"], capability="chat")
        for role, content in row["messages"]:
            await store.add_message(row["session_id"], role, content, capability="chat")
        await store.update_turn_status(turn["id"], "completed")


def _set_session_timestamp(db_path: Path, session_id: str, timestamp_value: float) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE sessions SET created_at = ?, updated_at = ? WHERE id = ?",
            (timestamp_value, timestamp_value, session_id),
        )
        conn.execute(
            "UPDATE turns SET created_at = ?, updated_at = ?, finished_at = ? WHERE session_id = ?",
            (timestamp_value, timestamp_value, timestamp_value, session_id),
        )
        message_rows = conn.execute(
            "SELECT id FROM messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        ).fetchall()
        for offset, message_row in enumerate(message_rows):
            conn.execute(
                "UPDATE messages SET created_at = ? WHERE id = ?",
                (timestamp_value + offset * 60, message_row[0]),
            )
        conn.commit()


async def _seed_observations_and_states(store: SQLiteSessionStore) -> dict[str, list[dict]]:
    observation_rows = []
    for row in DEMO_OBSERVATIONS:
        payload = dict(row)
        payload["created_at"] = _iso_to_timestamp(row["created_at"])
        observation_rows.append(payload)
    await store.save_observations(observation_rows)

    observations_by_student: dict[str, list[dict]] = {}
    for student_id in DEMO_STUDENT_IDS:
        observations = await store.list_observations(student_id)
        observations_by_student[student_id] = observations
        state = await store.build_student_state_rollup(student_id)
        if state is not None:
            await store.upsert_student_state(student_id, state)
    return observations_by_student


def _set_student_state_timestamp(db_path: Path, student_id: str, timestamp_value: float) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE student_states SET updated_at = ? WHERE student_id = ?",
            (timestamp_value, student_id),
        )
        conn.commit()


def _seed_demo_evidence(store: SQLiteSessionStore, *, student_payloads: list[dict], observations_by_student: dict[str, list[dict]]) -> None:
    insights = build_teacher_insights_payload(
        student_payloads=student_payloads,
        observations_by_student=observations_by_student,
    )
    student_rows = {
        row["student_id"]: row
        for row in insights["students"]
    }
    group_row = next(
        (
            row
            for row in insights["small_groups"]
            if sorted(row["student_ids"]) == ["Minh Chau", "Ngoc An"]
        ),
        None,
    )
    if group_row is None:
        raise RuntimeError("Expected a quadratic factoring small-group storyline for demo data")

    ngoc_action = create_teacher_action(
        store,
        target_type="student",
        target_id="Ngoc An",
        source_recommendation_id=student_rows["Ngoc An"]["recommended_actions"][0]["action_id"],
        action_type="scaffolded_practice",
        topic="quadratic factoring",
        teacher_instruction=f"{DEMO_MARKER} Run a 10-minute sign-check routine with two guided examples before independent practice.",
        priority="high",
    )
    create_recommendation_ack(
        store,
        source_recommendation_id=student_rows["Ngoc An"]["recommended_actions"][0]["action_id"],
        target_type="student",
        target_id="Ngoc An",
        status="accepted",
        teacher_note=f"{DEMO_MARKER} Use this in tomorrow's warm-up block.",
    )
    create_recommendation_feedback(
        store,
        source_recommendation_id=student_rows["Ngoc An"]["recommended_actions"][0]["action_id"],
        target_type="student",
        target_id="Ngoc An",
        feedback_label="practical",
        teacher_note=f"{DEMO_MARKER} The recommendation matches the student's actual error pattern.",
    )
    create_diagnosis_feedback(
        store,
        student_id="Ngoc An",
        source_topic=student_rows["Ngoc An"]["inferred"][0]["topic"],
        source_diagnosis_type=student_rows["Ngoc An"]["inferred"][0]["diagnosis_type"],
        feedback_label="helpful",
        teacher_note=f"{DEMO_MARKER} This lines up with the student's written work.",
    )
    create_intervention_assignment(
        store,
        teacher_action_id=ngoc_action["id"],
        assignment_type="practice_set",
        title="Quadratic factoring sign-check set",
        teacher_note=f"{DEMO_MARKER} Assign four short factor-and-check problems after reteach.",
        practice_note=f"{DEMO_MARKER} Start with sum/product checks before expanding.",
    )

    bao_action = create_teacher_action(
        store,
        target_type="student",
        target_id="Bao Han",
        source_recommendation_id=student_rows["Bao Han"]["recommended_actions"][0]["action_id"],
        action_type="review_prerequisite",
        topic="discriminant selection",
        teacher_instruction=f"{DEMO_MARKER} Review b squared minus 4ac with one worked comparison between positive and negative discriminants.",
        priority="medium",
    )
    create_recommendation_ack(
        store,
        source_recommendation_id=student_rows["Bao Han"]["recommended_actions"][0]["action_id"],
        target_type="student",
        target_id="Bao Han",
        status="deferred",
        teacher_note=f"{DEMO_MARKER} Hold until the class finishes the current factoring cycle.",
    )
    create_recommendation_feedback(
        store,
        source_recommendation_id=student_rows["Bao Han"]["recommended_actions"][0]["action_id"],
        target_type="student",
        target_id="Bao Han",
        feedback_label="relevant",
        teacher_note=f"{DEMO_MARKER} Good fit after notebook review.",
    )
    create_teacher_override(
        store,
        source_recommendation_id=student_rows["Bao Han"]["recommended_actions"][0]["action_id"],
        target_type="student",
        target_id="Bao Han",
        override_reason="needs_more_context",
        teacher_selected_move="review_prerequisite",
        teacher_note=f"{DEMO_MARKER} Teacher wants one prerequisite recap before another quiz.",
    )
    create_diagnosis_feedback(
        store,
        student_id="Bao Han",
        source_topic=student_rows["Bao Han"]["inferred"][0]["topic"],
        source_diagnosis_type=student_rows["Bao Han"]["inferred"][0]["diagnosis_type"],
        feedback_label="incomplete",
        teacher_note=f"{DEMO_MARKER} Useful, but still needs one more observation from class discussion.",
    )
    create_intervention_assignment(
        store,
        teacher_action_id=bao_action["id"],
        assignment_type="prerequisite_review",
        title="Discriminant recap notes",
        teacher_note=f"{DEMO_MARKER} Review the discriminant flow before the next independent attempt.",
        practice_note=f"{DEMO_MARKER} Mark each expression as positive, zero, or negative before solving.",
    )

    group_action = create_teacher_action(
        store,
        target_type="small_group",
        target_id=group_row["target_id"],
        source_recommendation_id=f"group:{group_row['topic']}:{group_row['diagnosis_type']}",
        action_type="small_group_remediation",
        topic=group_row["topic"],
        teacher_instruction=f"{DEMO_MARKER} Pull Ngoc An and Minh Chau for one 12-minute mini group on sign checks and root verification.",
        priority="high",
    )
    create_recommendation_ack(
        store,
        source_recommendation_id=f"group:{group_row['topic']}:{group_row['diagnosis_type']}",
        target_type="small_group",
        target_id=group_row["target_id"],
        status="accepted",
        teacher_note=f"{DEMO_MARKER} This pair can be regrouped during the workshop block.",
    )
    create_recommendation_feedback(
        store,
        source_recommendation_id=f"group:{group_row['topic']}:{group_row['diagnosis_type']}",
        target_type="small_group",
        target_id=group_row["target_id"],
        feedback_label="relevant",
        teacher_note=f"{DEMO_MARKER} Shared misconception is obvious in both assessments.",
    )
    create_intervention_assignment(
        store,
        teacher_action_id=group_action["id"],
        assignment_type="small_group_activity",
        title="Quadratic factoring mini-group",
        teacher_note=f"{DEMO_MARKER} Run one worked example together, then release to paired practice.",
        practice_note=f"{DEMO_MARKER} Students say the target sum before writing factor brackets.",
    )


def _set_evidence_timestamps(db_path: Path) -> None:
    table_updates = {
        "teacher_actions": [
            ("teacher_instruction LIKE '%Ngoc An%'", "2026-04-24T15:10:00"),
            ("teacher_instruction LIKE '%Bao Han%'", "2026-04-26T14:25:00"),
            ("teacher_instruction LIKE '%Minh Chau%'", "2026-04-25T10:30:00"),
        ],
        "recommendation_acks": [
            ("teacher_note LIKE '%warm-up block%'", "2026-04-24T15:00:00"),
            ("teacher_note LIKE '%current factoring cycle%'", "2026-04-26T14:20:00"),
            ("teacher_note LIKE '%workshop block%'", "2026-04-25T10:20:00"),
        ],
        "recommendation_feedback": [
            ("teacher_note LIKE '%actual error pattern%'", "2026-04-24T15:05:00"),
            ("teacher_note LIKE '%notebook review%'", "2026-04-26T14:22:00"),
            ("teacher_note LIKE '%Shared misconception%'", "2026-04-25T10:22:00"),
        ],
        "teacher_overrides": [
            ("teacher_note LIKE '%prerequisite recap%'", "2026-04-26T14:24:00"),
        ],
        "diagnosis_feedback": [
            ("teacher_note LIKE '%written work%'", "2026-04-24T15:08:00"),
            ("teacher_note LIKE '%class discussion%'", "2026-04-26T14:26:00"),
        ],
        "intervention_assignments": [
            ("title = 'Quadratic factoring sign-check set'", "2026-04-24T15:12:00"),
            ("title = 'Discriminant recap notes'", "2026-04-26T14:28:00"),
            ("title = 'Quadratic factoring mini-group'", "2026-04-25T10:32:00"),
        ],
    }
    with sqlite3.connect(db_path) as conn:
        for table_name, rules in table_updates.items():
            if not _table_exists(conn, table_name):
                continue
            for where_clause, iso_value in rules:
                ts_value = _iso_to_timestamp(iso_value)
                conn.execute(
                    f"UPDATE {table_name} SET created_at = ?, updated_at = ? WHERE {where_clause}",
                    (ts_value, ts_value),
                )
        conn.commit()


async def _seed_db(project_root: Path) -> dict[str, object]:
    db_path = project_root / "data" / "user" / "chat_history.db"
    _clear_demo_db_records(db_path)
    store = SQLiteSessionStore(db_path)

    await _seed_assessment_sessions(store)
    await _seed_tutor_sessions(store)

    for row in DEMO_ASSESSMENTS:
        _set_session_timestamp(db_path, row["session_id"], _iso_to_timestamp(row["created_at"]))
    for row in DEMO_TUTORS:
        _set_session_timestamp(db_path, row["session_id"], _iso_to_timestamp(row["created_at"]))

    observations_by_student = await _seed_observations_and_states(store)
    for student_id, observations in observations_by_student.items():
        latest_ts = max(float(item["created_at"]) for item in observations)
        _set_student_state_timestamp(db_path, student_id, latest_ts)

    student_payloads = []
    for student_id in DEMO_STUDENT_IDS:
        observations = observations_by_student[student_id]
        student_state = await store.get_student_state(student_id)
        student_payloads.append(
            build_student_diagnosis(
                student_id=student_id,
                observations=observations,
                student_state=student_state,
            )
        )

    _seed_demo_evidence(
        store,
        student_payloads=student_payloads,
        observations_by_student=observations_by_student,
    )
    _set_evidence_timestamps(db_path)

    return {
        "db_path": db_path,
        "session_ids": DEMO_SESSION_IDS,
        "student_ids": DEMO_STUDENT_IDS,
    }


def reset_demo_data(project_root: str | Path = ".", *, api_base: str = "http://localhost:8001") -> dict:
    _validate_local_api_base(api_base)
    root = Path(project_root).expanduser().resolve()
    kb_state = _seed_knowledge_packs(root)
    db_state = asyncio.run(_seed_db(root))
    return {
        "knowledge_pack": DEMO_KB_ID,
        "knowledge_packs": {
            "shareable": list(kb_state["shareable"]),
            "imported": list(kb_state["imported"]),
        },
        "sessions": list(db_state["session_ids"]),
        "students": list(db_state["student_ids"]),
        "paths": {
            "knowledge_pack": str(kb_state["anchor_path"]),
            "session_db": str(db_state["db_path"]),
        },
        "api_base": api_base,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset local contest demo-safe data.")
    parser.add_argument("--project-root", default=".", help="Repository root to write demo data under.")
    parser.add_argument("--api-base", default="http://localhost:8001", help="Local API base safety check.")
    args = parser.parse_args()
    result = reset_demo_data(args.project_root, api_base=args.api_base)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
