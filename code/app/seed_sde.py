# app/seed_sde.py
"""Seed SDE prep tracker data."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.sde_prep import (
    BehavioralStory,
    DailyTask,
    DifficultyEnum,
    LeetCodeProblem,
    ProblemCategoryEnum,
    ProblemStatusEnum,
    SystemDesignStatusEnum,
    SystemDesignTopic,
    WeekPlan,
)


def _make_url(slug: str) -> str:
    return f"https://leetcode.com/problems/{slug}/"


def seed_default_user(db) -> int:
    """Create default demo user if not exists."""
    existing_user = db.query(User).filter_by(email="demo@example.com").first()
    if existing_user:
        return existing_user.id

    user = User(first_name="Demo", last_name="User", email="demo@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ Created default user: {user.email}")
    return user.id


def seed_leetcode_problems(db, user_id: int) -> int:
    """Seed LeetCode problems."""
    if db.query(LeetCodeProblem).filter_by(user_id=user_id).count() > 0:
        return 0

    problems = [
        # Arrays / Strings (Blind 75)
        (1, "Two Sum", DifficultyEnum.EASY, ProblemCategoryEnum.ARRAYS, "two-sum", True),
        (121, "Best Time to Buy and Sell Stock", DifficultyEnum.EASY, ProblemCategoryEnum.ARRAYS, "best-time-to-buy-and-sell-stock", True),
        (238, "Product of Array Except Self", DifficultyEnum.MEDIUM, ProblemCategoryEnum.ARRAYS, "product-of-array-except-self", True),
        (15, "3Sum", DifficultyEnum.MEDIUM, ProblemCategoryEnum.ARRAYS, "3sum", True),
        (11, "Container With Most Water", DifficultyEnum.MEDIUM, ProblemCategoryEnum.ARRAYS, "container-with-most-water", True),
        (3, "Longest Substring Without Repeating Characters", DifficultyEnum.MEDIUM, ProblemCategoryEnum.ARRAYS, "longest-substring-without-repeating-characters", True),
        (76, "Minimum Window Substring", DifficultyEnum.HARD, ProblemCategoryEnum.ARRAYS, "minimum-window-substring", True),
        # Hash Tables (Blind 75)
        (242, "Valid Anagram", DifficultyEnum.EASY, ProblemCategoryEnum.HASH_TABLES, "valid-anagram", True),
        (49, "Group Anagrams", DifficultyEnum.MEDIUM, ProblemCategoryEnum.HASH_TABLES, "group-anagrams", True),
        # Trees (Blind 75)
        (104, "Maximum Depth of Binary Tree", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "maximum-depth-of-binary-tree", True),
        (100, "Same Tree", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "same-tree", True),
        (226, "Invert Binary Tree", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "invert-binary-tree", True),
        (102, "Binary Tree Level Order Traversal", DifficultyEnum.MEDIUM, ProblemCategoryEnum.TREES, "binary-tree-level-order-traversal", True),
        (124, "Binary Tree Maximum Path Sum", DifficultyEnum.HARD, ProblemCategoryEnum.TREES, "binary-tree-maximum-path-sum", True),
        # Linked List (Blind 75)
        (206, "Reverse Linked List", DifficultyEnum.EASY, ProblemCategoryEnum.LINKED_LISTS, "reverse-linked-list", True),
        (141, "Linked List Cycle", DifficultyEnum.EASY, ProblemCategoryEnum.LINKED_LISTS, "linked-list-cycle", True),
        (21, "Merge Two Sorted Lists", DifficultyEnum.EASY, ProblemCategoryEnum.LINKED_LISTS, "merge-two-sorted-lists", True),
        (23, "Merge k Sorted Lists", DifficultyEnum.HARD, ProblemCategoryEnum.LINKED_LISTS, "merge-k-sorted-lists", True),
        # Graphs (Blind 75)
        (133, "Clone Graph", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "clone-graph", True),
        (207, "Course Schedule", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "course-schedule", True),
        (200, "Number of Islands", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "number-of-islands", True),
        # DP (Blind 75)
        (70, "Climbing Stairs", DifficultyEnum.EASY, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "climbing-stairs", True),
        (198, "House Robber", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "house-robber", True),
        (300, "Longest Increasing Subsequence", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "longest-increasing-subsequence", True),
        (322, "Coin Change", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "coin-change", True),
        (139, "Word Break", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "word-break", True),
        # Extra core problems
        (217, "Contains Duplicate", DifficultyEnum.EASY, ProblemCategoryEnum.HASH_TABLES, "contains-duplicate", False),
        (347, "Top K Frequent Elements", DifficultyEnum.MEDIUM, ProblemCategoryEnum.HEAPS, "top-k-frequent-elements", False),
        (125, "Valid Palindrome", DifficultyEnum.EASY, ProblemCategoryEnum.ARRAYS, "valid-palindrome", False),
        (56, "Merge Intervals", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GREEDY, "merge-intervals", False),
        (57, "Insert Interval", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GREEDY, "insert-interval", False),
        (435, "Non-overlapping Intervals", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GREEDY, "non-overlapping-intervals", False),
        (33, "Search in Rotated Sorted Array", DifficultyEnum.MEDIUM, ProblemCategoryEnum.BINARY_SEARCH, "search-in-rotated-sorted-array", False),
        (74, "Search a 2D Matrix", DifficultyEnum.MEDIUM, ProblemCategoryEnum.MATRIX, "search-a-2d-matrix", False),
        (73, "Set Matrix Zeroes", DifficultyEnum.MEDIUM, ProblemCategoryEnum.MATRIX, "set-matrix-zeroes", False),
        (167, "Two Sum II", DifficultyEnum.MEDIUM, ProblemCategoryEnum.BINARY_SEARCH, "two-sum-ii-input-array-is-sorted", False),
        (153, "Find Minimum in Rotated Sorted Array", DifficultyEnum.MEDIUM, ProblemCategoryEnum.BINARY_SEARCH, "find-minimum-in-rotated-sorted-array", False),
        (704, "Binary Search", DifficultyEnum.EASY, ProblemCategoryEnum.BINARY_SEARCH, "binary-search", False),
        (20, "Valid Parentheses", DifficultyEnum.EASY, ProblemCategoryEnum.STACKS_QUEUES, "valid-parentheses", False),
        (155, "Min Stack", DifficultyEnum.MEDIUM, ProblemCategoryEnum.STACKS_QUEUES, "min-stack", False),
        (739, "Daily Temperatures", DifficultyEnum.MEDIUM, ProblemCategoryEnum.STACKS_QUEUES, "daily-temperatures", False),
        (215, "Kth Largest Element in an Array", DifficultyEnum.MEDIUM, ProblemCategoryEnum.HEAPS, "kth-largest-element-in-an-array", False),
        (208, "Implement Trie", DifficultyEnum.MEDIUM, ProblemCategoryEnum.TREES, "implement-trie-prefix-tree", False),
        (105, "Construct Binary Tree from Preorder and Inorder", DifficultyEnum.MEDIUM, ProblemCategoryEnum.TREES, "construct-binary-tree-from-preorder-and-inorder-traversal", False),
        (98, "Validate Binary Search Tree", DifficultyEnum.MEDIUM, ProblemCategoryEnum.TREES, "validate-binary-search-tree", False),
        (543, "Diameter of Binary Tree", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "diameter-of-binary-tree", False),
        (572, "Subtree of Another Tree", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "subtree-of-another-tree", False),
        (297, "Serialize and Deserialize Binary Tree", DifficultyEnum.HARD, ProblemCategoryEnum.TREES, "serialize-and-deserialize-binary-tree", False),
        (235, "Lowest Common Ancestor of a BST", DifficultyEnum.EASY, ProblemCategoryEnum.TREES, "lowest-common-ancestor-of-a-binary-search-tree", False),
        (19, "Remove Nth Node From End", DifficultyEnum.MEDIUM, ProblemCategoryEnum.LINKED_LISTS, "remove-nth-node-from-end-of-list", False),
        (143, "Reorder List", DifficultyEnum.MEDIUM, ProblemCategoryEnum.LINKED_LISTS, "reorder-list", False),
        (2, "Add Two Numbers", DifficultyEnum.MEDIUM, ProblemCategoryEnum.LINKED_LISTS, "add-two-numbers", False),
        (22, "Generate Parentheses", DifficultyEnum.MEDIUM, ProblemCategoryEnum.STACKS_QUEUES, "generate-parentheses", False),
        (46, "Permutations", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GREEDY, "permutations", False),
        (78, "Subsets", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GREEDY, "subsets", False),
        (994, "Rotting Oranges", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "rotting-oranges", False),
        (417, "Pacific Atlantic Water Flow", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "pacific-atlantic-water-flow", False),
        (684, "Redundant Connection", DifficultyEnum.MEDIUM, ProblemCategoryEnum.GRAPHS, "redundant-connection", False),
        (131, "Palindrome Partitioning", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "palindrome-partitioning", False),
        (91, "Decode Ways", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "decode-ways", False),
        (62, "Unique Paths", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "unique-paths", False),
        (1143, "Longest Common Subsequence", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "longest-common-subsequence", False),
        (647, "Palindromic Substrings", DifficultyEnum.MEDIUM, ProblemCategoryEnum.DYNAMIC_PROGRAMMING, "palindromic-substrings", False),
        (371, "Sum of Two Integers", DifficultyEnum.MEDIUM, ProblemCategoryEnum.BIT_MANIPULATION, "sum-of-two-integers", False),
        (136, "Single Number", DifficultyEnum.EASY, ProblemCategoryEnum.BIT_MANIPULATION, "single-number", False),
        (268, "Missing Number", DifficultyEnum.EASY, ProblemCategoryEnum.BIT_MANIPULATION, "missing-number", False),
    ]

    seen_numbers: set[int] = set()
    rows: list[LeetCodeProblem] = []
    for number, title, difficulty, category, slug, blind in problems:
        if number in seen_numbers:
            continue
        seen_numbers.add(number)
        rows.append(
            LeetCodeProblem(
                number=number,
                title=title,
                difficulty=difficulty,
                category=category,
                url=_make_url(slug),
                is_blind_75=blind,
                status=ProblemStatusEnum.NOT_STARTED,
                attempts=0,
                user_id=user_id,
            )
        )

    db.add_all(rows)
    db.commit()
    return len(rows)


def seed_system_design_topics(db, user_id: int) -> int:
    """Seed system design topics."""
    if db.query(SystemDesignTopic).filter_by(user_id=user_id).count() > 0:
        return 0

    topics = [
        "Twitter",
        "URL Shortener",
        "Instagram",
        "Uber",
        "Netflix",
        "Amazon",
        "WhatsApp",
        "Dropbox",
        "Shopping Cart (Walmart)",
        "Inventory Management (Walmart)",
        "Pricing Engine (Walmart)",
        "Search & Recommendation",
        "Rate Limiter",
        "Notification System",
        "Distributed Cache",
    ]

    rows = [
        SystemDesignTopic(
            title=topic,
            description=f"Design the {topic} system with scale, reliability, and cost in mind.",
            status=SystemDesignStatusEnum.NOT_STARTED,
            practice_count=0,
            resources=json.dumps([]),
            user_id=user_id,
        )
        for topic in topics
    ]
    db.add_all(rows)
    db.commit()
    return len(rows)
def seed_week_plans(db, user_id: int) -> int:
    """Seed 12-week plan."""
    if db.query(WeekPlan).filter_by(user_id=user_id).count() > 0:
        return 0

    weeks = [
        (1, "Resume & Networking", "Foundational prep for outreach and resume polish.", [
            "Update resume",
            "Optimize LinkedIn",
            "Reach out to 5 engineers",
            "Apply to 10 companies",
        ]),
        (2, "Behavioral Prep", "Build and rehearse STAR stories.", [
            "Brainstorm 20 STAR stories",
            "Write 10 full stories",
            "Record 3 stories",
            "Research companies",
        ]),
        (3, "Arrays, Strings, Hash Tables", "Core data structure mastery.", [
            "Solve 20-25 problems",
            "Master two pointers",
            "Master sliding window",
            "Hash table patterns",
        ]),
        (4, "Trees & Linked Lists", "Classic traversal and pointer techniques.", [
            "Solve 17-20 problems",
            "Master DFS/BFS",
            "Binary tree traversals",
            "Linked list manipulation",
        ]),
        (5, "Graphs & Dynamic Programming", "Graph search + DP patterns.", [
            "Solve 14-16 problems",
            "Master graph DFS/BFS",
            "1D DP patterns",
            "2D DP patterns",
        ]),
        (6, "Advanced Topics + Hard Problems", "Stretch into harder topics.", [
            "Solve 15 problems",
            "Master heaps",
            "Backtracking patterns",
            "5 hard problems",
        ]),
        (7, "System Design Fundamentals", "Foundational system design practice.", [
            "Read DDIA Ch 1-3",
            "Study caching",
            "Database scaling",
            "Twitter + URL Shortener",
        ]),
        (8, "Distributed Systems", "Distributed services at scale.", [
            "Message queues",
            "Microservices",
            "API design",
            "Instagram + Uber",
        ]),
        (9, "Advanced System Design", "Scale + consistency topics.", [
            "Consistent hashing",
            "CAP theorem",
            "DDIA Ch 7-9",
            "Netflix + Amazon",
        ]),
        (10, "E-commerce Systems", "Commerce flows and reliability.", [
            "Design shopping cart",
            "Inventory system",
            "Pricing engine",
            "Mock interviews",
        ]),
        (11, "Intensive Mock Interviews", "High intensity practice week.", [
            "2 coding mocks",
            "1 system design mock",
            "1 behavioral mock",
            "Review",
        ]),
        (12, "Final Prep & Polish", "Finalize for loops.", [
            "2 full-loop mocks",
            "Company research",
            "STAR stories",
            "Final LeetCode review",
        ]),
    ]

    rows = [
        WeekPlan(
            week_number=week,
            title=title,
            description=desc,
            goals=json.dumps(goals),
            is_completed=False,
            completion_percentage=0.0,
            user_id=user_id,
        )
        for week, title, desc, goals in weeks
    ]
    db.add_all(rows)
    db.commit()
    return len(rows)
def _problem_id_map(db, user_id: int) -> dict[int, int]:
    return {
        problem.number: problem.id
        for problem in db.query(LeetCodeProblem).filter_by(user_id=user_id).all()
    }


def _week_plan_map(db, user_id: int) -> dict[int, int]:
    return {
        week.week_number: week.id
        for week in db.query(WeekPlan).filter_by(user_id=user_id).all()
    }


def _add_day_tasks(
    tasks: list[DailyTask],
    *,
    week_number: int,
    day_number: int,
    day_name: str,
    items: Iterable[dict],
    week_plan_id: int,
    problem_map: dict[int, int],
    user_id: int,
) -> None:
    for order, item in enumerate(items, start=1):
        tasks.append(
            DailyTask(
                week_number=week_number,
                day_number=day_number,
                day_name=day_name,
                task_order=order,
                task_title=item["title"],
                task_description=item.get("description"),
                task_type=item["type"],
                estimated_minutes=item.get("minutes"),
                related_problem_id=problem_map.get(item.get("problem_number"))
                if item.get("problem_number")
                else None,
                related_topic_id=None,
                week_plan_id=week_plan_id,
                is_completed=False,
                user_id=user_id,
            )
        )


def seed_daily_tasks(db, user_id: int) -> int:
    """Seed daily tasks for weeks 1-3."""
    if db.query(DailyTask).filter_by(user_id=user_id).count() > 0:
        return 0

    problem_map = _problem_id_map(db, user_id)
    week_map = _week_plan_map(db, user_id)
    tasks: list[DailyTask] = []

    week1 = [
        (1, "Monday", [
            {"title": "Update Resume", "type": "PREPARATION", "minutes": 90},
            {"title": "Create Achievement List", "type": "PREPARATION", "minutes": 60},
        ]),
        (2, "Tuesday", [
            {"title": "Optimize LinkedIn", "type": "PREPARATION", "minutes": 60},
            {"title": "Research Target Companies", "type": "PREPARATION", "minutes": 90},
        ]),
        (3, "Wednesday", [
            {"title": "Reach Out to 5 Engineers", "type": "NETWORKING", "minutes": 60},
            {"title": "Join Communities", "type": "NETWORKING", "minutes": 45},
        ]),
        (4, "Thursday", [
            {"title": "Apply to 10 Companies", "type": "PREPARATION", "minutes": 120},
            {"title": "Setup Job Tracker", "type": "PREPARATION", "minutes": 30},
        ]),
        (5, "Friday", [
            {"title": "Solve Easy LeetCode", "type": "LEETCODE", "minutes": 90, "problem_number": 1},
            {"title": "Review Data Structures", "type": "REVIEW", "minutes": 60},
        ]),
        (6, "Saturday", [
            {"title": "STAR Story Practice", "type": "BEHAVIORAL", "minutes": 60},
            {"title": "Networking Follow-ups", "type": "NETWORKING", "minutes": 30},
        ]),
        (7, "Sunday", [
            {"title": "Week Reflection", "type": "REVIEW", "minutes": 30},
            {"title": "Plan Next Week", "type": "PREPARATION", "minutes": 45},
        ]),
    ]

    week2_titles = [
        "Write STAR story: leadership win",
        "Write STAR story: conflict resolution",
        "Write STAR story: technical challenge",
        "Write STAR story: failure and recovery",
        "Write STAR story: mentoring",
        "Write STAR story: customer obsession",
        "Write STAR story: ownership",
        "Write STAR story: bias for action",
        "Write STAR story: scalability",
        "Write STAR story: ambiguity",
        "Write STAR story: stakeholder management",
        "Write STAR story: product pivot",
        "Write STAR story: deadline crunch",
        "Write STAR story: cross-team delivery",
    ]

    week2 = []
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day_index in range(7):
        start = day_index * 2
        day_tasks = week2_titles[start:start + 2]
        week2.append(
            (
                day_index + 1,
                day_names[day_index],
                [
                    {
                        "title": day_tasks[0],
                        "type": "BEHAVIORAL",
                        "minutes": 60,
                        "description": "Draft STAR story and capture key metrics.",
                    },
                    {
                        "title": day_tasks[1],
                        "type": "REVIEW",
                        "minutes": 45,
                        "description": "Rehearse out loud and refine impact metrics.",
                    },
                ],
            )
        )

    week3 = [
        (1, "Monday", [
            {"title": "Two Sum", "type": "LEETCODE", "minutes": 30, "problem_number": 1},
            {"title": "Best Time to Buy/Sell Stock", "type": "LEETCODE", "minutes": 30, "problem_number": 121},
            {"title": "Contains Duplicate", "type": "LEETCODE", "minutes": 25, "problem_number": 217},
            {"title": "Valid Anagram", "type": "LEETCODE", "minutes": 30, "problem_number": 242},
            {"title": "Review Two Pointers", "type": "REVIEW", "minutes": 45},
        ]),
        (2, "Tuesday", [
            {"title": "Group Anagrams", "type": "LEETCODE", "minutes": 40, "problem_number": 49},
            {"title": "Top K Frequent Elements", "type": "LEETCODE", "minutes": 45, "problem_number": 347},
            {"title": "Product Except Self", "type": "LEETCODE", "minutes": 40, "problem_number": 238},
            {"title": "Valid Palindrome", "type": "LEETCODE", "minutes": 25, "problem_number": 125},
            {"title": "Review Hash Map Patterns", "type": "REVIEW", "minutes": 30},
        ]),
        (3, "Wednesday", [
            {"title": "Two Sum II", "type": "LEETCODE", "minutes": 30, "problem_number": 167},
            {"title": "3Sum", "type": "LEETCODE", "minutes": 45, "problem_number": 15},
            {"title": "Container With Most Water", "type": "LEETCODE", "minutes": 35, "problem_number": 11},
            {"title": "Review Sliding Window", "type": "REVIEW", "minutes": 30},
            {"title": "Longest Substring", "type": "LEETCODE", "minutes": 40, "problem_number": 3},
        ]),
        (4, "Thursday", [
            {"title": "Minimum Window Substring", "type": "LEETCODE", "minutes": 50, "problem_number": 76},
            {"title": "Merge Intervals", "type": "LEETCODE", "minutes": 35, "problem_number": 56},
            {"title": "Insert Interval", "type": "LEETCODE", "minutes": 35, "problem_number": 57},
            {"title": "Review Interval Patterns", "type": "REVIEW", "minutes": 30},
            {"title": "Set Matrix Zeroes", "type": "LEETCODE", "minutes": 35, "problem_number": 73},
        ]),
        (5, "Friday", [
            {"title": "Search a 2D Matrix", "type": "LEETCODE", "minutes": 30, "problem_number": 74},
            {"title": "Search in Rotated Sorted Array", "type": "LEETCODE", "minutes": 35, "problem_number": 33},
            {"title": "Binary Search", "type": "LEETCODE", "minutes": 25, "problem_number": 704},
            {"title": "Review Binary Search", "type": "REVIEW", "minutes": 25},
            {"title": "Non-overlapping Intervals", "type": "LEETCODE", "minutes": 35, "problem_number": 435},
        ]),
        (6, "Saturday", [
            {"title": "Valid Parentheses", "type": "LEETCODE", "minutes": 25, "problem_number": 20},
            {"title": "Min Stack", "type": "LEETCODE", "minutes": 30, "problem_number": 155},
            {"title": "Daily Temperatures", "type": "LEETCODE", "minutes": 35, "problem_number": 739},
            {"title": "Review Stack Patterns", "type": "REVIEW", "minutes": 30},
            {"title": "Generate Parentheses", "type": "LEETCODE", "minutes": 35, "problem_number": 22},
        ]),
        (7, "Sunday", [
            {"title": "Kth Largest Element", "type": "LEETCODE", "minutes": 35, "problem_number": 215},
            {"title": "Clone Graph", "type": "LEETCODE", "minutes": 40, "problem_number": 133},
            {"title": "Number of Islands", "type": "LEETCODE", "minutes": 40, "problem_number": 200},
            {"title": "Review Graph BFS/DFS", "type": "REVIEW", "minutes": 30},
            {"title": "Course Schedule", "type": "LEETCODE", "minutes": 40, "problem_number": 207},
        ]),
    ]

    for day_number, day_name, items in week1:
        _add_day_tasks(
            tasks,
            week_number=1,
            day_number=day_number,
            day_name=day_name,
            items=items,
            week_plan_id=week_map[1],
            problem_map=problem_map,
            user_id=user_id,
        )

    for day_number, day_name, items in week2:
        _add_day_tasks(
            tasks,
            week_number=2,
            day_number=day_number,
            day_name=day_name,
            items=items,
            week_plan_id=week_map[2],
            problem_map=problem_map,
            user_id=user_id,
        )

    for day_number, day_name, items in week3:
        _add_day_tasks(
            tasks,
            week_number=3,
            day_number=day_number,
            day_name=day_name,
            items=items,
            week_plan_id=week_map[3],
            problem_map=problem_map,
            user_id=user_id,
        )

    db.add_all(tasks)
    db.commit()
    return len(tasks)


def seed_all() -> None:
    """Seed all SDE prep data."""
    init_db()
    db = SessionLocal()

    try:
        user_id = seed_default_user(db)
        added_problems = seed_leetcode_problems(db, user_id)
        added_topics = seed_system_design_topics(db, user_id)
        added_weeks = seed_week_plans(db, user_id)
        added_tasks = seed_daily_tasks(db, user_id)

        print("Seed complete")
        print(f"LeetCode problems added: {added_problems}")
        print(f"System design topics added: {added_topics}")
        print(f"Week plans added: {added_weeks}")
        print(f"Daily tasks added: {added_tasks}")
    except Exception as exc:
        print(f"Seeding failed: {exc}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()