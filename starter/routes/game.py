from flask import Blueprint, render_template, jsonify, request
from services.generator import generate_by_difficulty
from services.validator import find_conflicts

game_bp = Blueprint('game', __name__)

# Simple in-memory store for current puzzle per-process
CURRENT = {
    'puzzle': None,
    'solution': None,
    'difficulty': None
}


@game_bp.route('/')
def index():
    return render_template('index.html')


@game_bp.route('/api/new')
def new_game():
    difficulty = request.args.get('difficulty', 'Medium')
    puzzle, solution = generate_by_difficulty(difficulty)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['difficulty'] = difficulty
    return jsonify({'puzzle': puzzle, 'difficulty': difficulty})


@game_bp.route('/api/check', methods=['POST'])
def check_board():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@game_bp.route('/api/hint', methods=['POST'])
def hint():
    # Return one correct value for an empty cell
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    import random
    empties = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
    if not empties:
        return jsonify({'error': 'No empty cells'}), 400
    r, c = random.choice(empties)
    return jsonify({'row': r, 'col': c, 'value': solution[r][c]})


@game_bp.route('/api/validate', methods=['POST'])
def validate_board():
    data = request.json
    board = data.get('board')
    conflicts = find_conflicts(board)
    return jsonify({'conflicts': conflicts})
