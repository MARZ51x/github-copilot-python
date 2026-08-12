# Project: Flask Sudoku Game

## Overview

This repository contains a Sudoku web application built with Python, Flask, HTML, CSS, and JavaScript.

The primary goals are:

- Modern, maintainable code architecture
- Responsive and accessible user interface
- Complete Sudoku gameplay functionality
- Reliable validation and puzzle generation
- Local persistence of game results
- Clean user experience in desktop and mobile browsers

When generating code, prioritize maintainability, readability, accessibility, and modular design.

---

# Technology Stack

Backend:
- Python 3
- Flask
- Jinja2 Templates

Frontend:
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)

Storage:
- Local JSON file or browser localStorage for leaderboard persistence

Testing:
- pytest

---

# Coding Standards

## General

Always:

- Follow clean code principles
- Prefer readability over clever implementations
- Keep functions small and focused
- Avoid duplicated logic
- Separate concerns properly
- Use descriptive names

Never:

- Place business logic directly inside template files
- Create giant route files
- Mix Sudoku logic with UI rendering logic

---

# Application Structure

Use a modular structure similar to:

project/
│
├── app.py
├── routes/
├── services/
├── models/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── data/
└── tests/

### Responsibilities

Routes:
- Handle requests and responses only

Services:
- Sudoku generator
- Sudoku solver
- Sudoku validation
- Leaderboard management

Templates:
- Display data only

JavaScript:
- UI interactions
- Timer
- Theme toggle
- Board updates

---

# Error Handling

All user-facing functionality should include graceful error handling.

Requirements:

- Catch expected exceptions
- Return clear error messages
- Never silently fail
- Validate all incoming data

Example scenarios:

- Invalid board state
- Corrupted leaderboard file
- Invalid difficulty selection
- Missing player name

---

# Comments

Write meaningful comments only when necessary.

Use comments for:

- Complex Sudoku algorithms
- Validation logic
- Puzzle generation strategies

Avoid comments that simply restate what code does.

---

# Sudoku Rules

All generated boards must follow official Sudoku rules.

Requirements:

- Exactly one valid solution
- Fully solvable puzzle
- No invalid starting boards

Validation must detect:

- Duplicate values in rows
- Duplicate values in columns
- Duplicate values in 3×3 regions

Return conflict positions whenever possible.

---

# Difficulty Levels

Implement three difficulties:

Easy:
- 40 to 45 prefilled cells

Medium:
- 30 to 39 prefilled cells

Hard:
- 22 to 29 prefilled cells

Difficulty should only affect puzzle clues and not board size.

---

# Prefilled Cells

Requirements:

- Starting clues must be locked
- Users cannot modify locked cells
- Locked cells should be visually distinct

---

# Invalid Move Feedback

Whenever a user enters an invalid value:

- Highlight conflicting cells
- Clearly indicate the error
- Do not shift layout
- Maintain accessibility

Use CSS classes instead of inline styles.

Preferred classes:

- .cell-invalid
- .cell-valid
- .cell-locked

---

# Puzzle Completion

A game is complete only when:

- The board is full
- All values are correct
- No conflicts exist

When completed:

- Stop the timer
- Display a congratulatory message
- Save the result to leaderboard
- Record completion statistics

---

# Hint Function

The Hint button must:

- Find one empty cell
- Insert the correct value
- Lock the revealed value
- Increase hint counter by one

Never:

- Reveal multiple cells
- Solve an entire row, column, or puzzle

---

# Check Function

The Check button must:

- Compare player entries against the solution
- Highlight incorrect cells
- Leave correct cells unchanged

Do not automatically reveal answers.

---

# Timer

The timer must:

- Start when a puzzle loads
- Track minutes and seconds
- Stop on completion
- Continue accurately during gameplay

Format:

MM:SS

Example:

05:27

---

# Leaderboard

Maintain a local Top 10 leaderboard.

Store:

- Player name
- Completion time
- Difficulty
- Hints used

Requirements:

- Keep only the best 10 results
- Sort by fastest completion time
- Persist between sessions

Example:

[
  {
    "name": "Player1",
    "time": 180,
    "difficulty": "Medium",
    "hints": 2
  }
]

---

# User Interface

## Responsive Design

The layout must adapt cleanly to:

- Mobile phones
- Tablets
- Desktop screens

Use:

- CSS Grid
- Flexbox
- Relative sizing
- Media queries

Avoid fixed widths whenever possible.

---

# Sudoku Board Layout

The board must:

- Display a 9×9 grid
- Preserve perfect square cells
- Avoid visual layout shifts
- Maintain consistent spacing

---

# 3×3 Region Styling

The Sudoku board must show alternating colors for each 3×3 region.

Pattern:

A B A
B A B
A B A

This alternating pattern should remain visible in both light and dark themes.

---

# Accessibility

Always generate accessible markup.

Requirements:

- Semantic HTML
- Proper labels
- Keyboard navigation support
- Visible focus states
- Sufficient color contrast
- ARIA attributes where beneficial

Accessibility must never be sacrificed for appearance.

---

# Dark Mode

Dark mode is required.

Requirements:

- Theme toggle button
- CSS custom properties (variables)
- Store preference using localStorage
- Text remains readable
- Buttons remain visible
- Sudoku board remains distinguishable

Example variables:

--background-color
--text-color
--surface-color
--accent-color

---

# Styling Preferences

Prefer:

- CSS modules or organized CSS files
- Reusable classes
- Consistent spacing scale
- Mobile-first design

Avoid:

- Inline styles
- Hardcoded colors throughout components
- Excessive use of !important

---

# JavaScript Guidelines

Use modern JavaScript.

Prefer:

- const and let
- Event listeners
- Modular functions
- Reusable utilities

Avoid:

- Global variables
- jQuery
- Inline event handlers

---

# Testing

Use pytest for backend testing.

Generate tests for:

- Sudoku generation
- Unique solution validation
- Difficulty settings
- Check functionality
- Hint functionality
- Leaderboard updates
- Timer utilities when applicable

Prefer small focused tests over large integration tests.

---

# Code Generation Priority

When multiple solutions are possible, prefer the solution that maximizes:

1. Maintainability
2. Reusability
3. Accessibility
4. Testability
5. Performance

Always generate production-quality code that satisfies the project grading requirements.

---

# Responsible and Effective GitHub Copilot Use

This project is part of an academic assessment that requires demonstrating responsible AI-assisted development practices.

When generating code, documentation, comments, or project artifacts, Copilot should support transparency and critical evaluation of AI-generated suggestions.

## Required Evidence

The repository must contain a folder named:

Screenshots/

This folder will contain screenshots demonstrating how GitHub Copilot was used throughout development.

Required screenshot categories:

1. Setting up the testing framework
2. Ensuring Sudoku boards generate with exactly one unique solution
3. Implementing and validating Top 10 leaderboard storage
4. Styling the Sudoku board so alternating 3×3 regions have different colors

Screenshots should capture:

- The prompt provided to Copilot
- Copilot's generated response
- Relevant context showing how the suggestion was used

---

## Screenshot Naming Convention

Use descriptive filenames.

Examples:

- copilot_testing_framework_prompt.png
- copilot_unique_solution_generation.png
- copilot_top10_localstorage.png
- copilot_alternating_grid_colors.png
- copilot_rejected_suggestion.png

Avoid generic filenames such as:

- screenshot1.png
- image.png
- prompt.png

---

## Demonstrating Critical Evaluation

Do not assume Copilot suggestions are always correct.

At least one example in the project should demonstrate:

- Reviewing a Copilot-generated suggestion
- Identifying a limitation, bug, inefficiency, or incorrect implementation
- Rejecting, modifying, or improving the suggestion

Evidence may be shown through:

### Option 1: Screenshot Evidence

A screenshot showing:

- Original Copilot suggestion
- Developer decision to reject or revise it

### Option 2: Code Comments

Code comments describing why a suggestion was changed.

Example:

```python
# Copilot originally suggested validating the board by checking
# only rows and columns. The implementation was revised to also
# validate 3x3 regions to fully comply with Sudoku rules.
```

---

## Responsible AI Development Practices

When generating code or documentation:

- Verify generated logic before using it
- Prefer correctness over convenience
- Review all generated algorithms
- Ensure Sudoku rules are fully implemented
- Validate generated test cases
- Avoid blindly accepting generated code

Copilot suggestions should be treated as recommendations, not authoritative solutions.

---

## Documentation Expectations

When generating README content or developer documentation:

Include brief explanations of:

- How Copilot was used during development
- What prompts were effective
- What generated suggestions were modified or rejected
- How generated code was verified through testing

This documentation should demonstrate thoughtful and responsible use of AI-assisted development.
``