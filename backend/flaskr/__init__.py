import json
from msilib.schema import Environment, Error
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def format_question_list(questions_list):
    formatted_questions = [question.format() for question in questions_list]
    return formatted_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type,authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        if request.method != 'GET':
            abort(405)

        categories = Category.query.order_by(Category.type).all()
        if not categories:
            abort(422)

        return jsonify({
            "success": True,
            "categories": {category.id: category.type for category in categories}
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination(every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page_before_cast = request.args.get('page')
        # If a page is provided and it's not a valid integer
        if page_before_cast and not page_before_cast.isdigit():
            abort(400)

        current_questions = Question.query.paginate(
            request.args.get('page', 1, type=int), QUESTIONS_PER_PAGE, False)

        categories = Category.query.all()
        if (current_questions.total == 0):
            abort(404)

        return jsonify({
            "success": True,
            "questions": format_question_list(current_questions.items),
            "total_questions": current_questions.total,
            "current_category": None,
            "categories": {category.id: category.type for category in categories}
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if not question:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': id})

        except Exception as e:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        if ((new_question is None) or (new_answer is None)
                or (new_difficulty is None) or (new_category is None)):
            abort(400)

        question = Question(question=new_question, answer=new_answer,
                            difficulty=new_difficulty, category=new_category)
        question.insert()

        return jsonify({
            'success': True,
            'created': question.id})

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_question():

        body = request.get_json()
        searchTerm = body.get('searchTerm')
        if searchTerm is None:
            abort(400)
        matched_questions = Question.query.filter(
            Question.question.ilike(f'%{searchTerm}%')).paginate(1, QUESTIONS_PER_PAGE, False)

        return jsonify({
            'success': True,
            'questions': format_question_list(matched_questions.items),
            'total_questions': matched_questions.total,
            'current_categroy': None
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):

        category = Category.query.filter_by(id=id).one_or_none()
        if category is None:
            abort(404)
        else:
            try:
                category = category
                questions = Question.query.filter_by(
                    category=category.id).paginate(1, QUESTIONS_PER_PAGE, False)
                return jsonify({
                    'success': True,
                    'questions': format_question_list(questions.items),
                    'total_questions': questions.total,
                    'current_categroy': category.format()['type']})
            except Exception:
                abort(500)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes_by_category():
        questions = None
        quiz_pool = []
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')
        if ((previous_questions is None) or (category is None)):
            abort(400)
        try:
            question_to_ask = {}
            if (category['id'] == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=category['id']).all()

            for question in questions:
                if question.id not in previous_questions:
                    quiz_pool.append(question)

            if len(quiz_pool) <= 0:
                quiz_pool = questions

            question_to_ask = random.choice(quiz_pool)
            return jsonify({
                'success': True,
                'question': question_to_ask.format()
            })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    if __name__ == '__main__':
        app.run(debug=True)

    return app
