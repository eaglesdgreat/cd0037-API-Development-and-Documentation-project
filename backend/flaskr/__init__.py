from crypt import methods
import os, sys
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    created_questions = questions[start:end]
    
    return created_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={ r"/api/*": { "origins": "*" } })

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            selection = Category.query.order_by(Category.id).all()
            
            categories = {}
            for cat in  [category.format() for category in selection]:
                id = cat['id']
                categories[id] = cat['type']
            
            return jsonify(
                {
                    "success": True,
                    "categories": categories
                }
            )
        except:
            print(sys.exc_info())
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        try: 
            selection = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, selection)
            
            categories = {}
            cat_name = [category.format() for category in Category.query.order_by(Category.id).all()][0]['type']
            for cat in  [category.format() for category in Category.query.order_by(Category.id).all()]:
                id = cat['id']
                categories[id] = cat['type']
            
            if len(questions) == 0:
                abort(404)
            
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "categories": categories,
                    "totalQuestions": len(selection),
                    "currentCategory": cat_name,
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_selected_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
                
            question.delete()
            
            return jsonify(
                {
                    "success": True,
                    "message": "Question deleted successfully.",
                    "deleted": question_id,
                }
            )
        except:
            print(sys.exc_info())
            abort(422)

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
    def create_question():
        try:
            body = request.get_json()
            
            new_question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)
            
            if (new_question or answer or category) is None:
                abort(422)
            
            question = Question(
                question=new_question,
                answer=answer,
                difficulty=difficulty,
                category=category
            )
            
            question.insert()
            
            return jsonify(
                {
                    "success": True,
                    "message": "Question created successfully."
                }
            )
        except:
            print(sys.exc_info())
            abort(400)
        
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
        try:
            body = request.get_json()
            searchTerm = body.get('searchTerm', None)
            selection = Question.query.filter(Question.question.ilike(f"%{searchTerm}%")).order_by(Question.id).all()
            questions = [question.format() for question in selection]       
            
            if len(questions) == 0:
                abort(404)
            
            category_type = ""
            category = Category.query.filter(Category.id == questions[0]['category']).one_or_none()
            
            if category is not None:
                category_type = category.format()['type']
            
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    'totalQuestions': len(selection),
                    'currentCategory': category_type
                }
            )
        except:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
            questions = [question.format() for question in selection]
            
            category = Category.query.filter(Category.id == category_id).one_or_none()
            category_type = ""
            if category is not None:
                category_type = category.format()['type']
            
            if len(questions) == 0:
                abort(400)
                
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    'totalQuestions': len(selection),
                    'currentCategory': category_type
                }
            )
        except:
            abort(400)

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
    def get_quiz_question():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            
            selection = []
            category = Category.query.filter(Category.id == quiz_category['id']).one_or_none()
            id = None
            if category is not None:
                id = category.format()['id']
            
            if id is None:
                selection = Question.query.order_by(Question.id).all()
            else:
                selection = Question.query.filter(Question.category == id).order_by(Question.id).all()
            
            questions = [question.format() for question in selection]
            question = []
            
            for q in questions:
                if not q['id'] in previous_questions:
                    question.append(q)
                    
            if len(question) == 0:
                return jsonify(
                    {
                        "success": True,
                        "question":{},
                        "total_questions": len(questions)
                    }
                )
            else:
                return jsonify(
                    {
                        "success": True,
                        "question": question[0],
                        "total_questions": len(questions)
                    }
                )
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
    
    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "server error"}),
            500,
        )

    return app

