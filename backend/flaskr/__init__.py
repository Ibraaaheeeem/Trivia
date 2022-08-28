import os
import math
from re import search
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    @TODO: DONE
    """
    CORS(app)


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    @TODO: DONE
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        query_all_categories = Category.query.all()
        if not query_all_categories:
            abort(404, "No category present")
        all_categories = {category.id:category.type for category in query_all_categories}
        return jsonify({
            "success":True,
            "categories":all_categories
        })

    
    """
    @TODO:
    Create an endpoint to handle POST request
    to add a new category
    """
    @app.route('/categories', methods = ['POST'])
    def create_new_category():
        incoming_json = request.get_json()
        new_category_to_create = incoming_json.get('new_category_name')

        query_all_categories = Category.query.all()
        all_category_names = [category.type for category in query_all_categories]
        if new_category_to_create in all_category_names:
            abort (404, "Category already exist")
        new_category = Category(
            type=new_category_to_create
        )
        new_category.insert()
        return jsonify({
            "success":True,
            "category_id":new_category.id
        })
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
        
        page_number = request.args.get("page", 1, type=int)
        all_questions_query = Question.query.all()
        all_categories_query = Category.query.all()
        totalQuestions = len(all_questions_query)
        total_pages = math.ceil(totalQuestions/QUESTIONS_PER_PAGE)

        if page_number > total_pages:
            abort(404, 'Page number out of range')

        elif page_number < 1:
            abort(404, 'Invalid page number')
        
        # Get first and last question of the page
        start = (page_number - 1) * QUESTIONS_PER_PAGE
        end = start + 10

        #paged_questions = all_questions_query

        return jsonify({
            "success":True,
            "questions":[{
                "id":question.id,
                "question":question.question,
                "answer":question.answer,
                "category":question.category,
                "difficulty":question.difficulty,
                
            } 
            for question in all_questions_query[start:end]
            ],
            "categories":{category.id:category.type for category in all_categories_query},
            "currentCategory":None,
            "totalQuestions":len(all_questions_query)
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods = ['DELETE'])
    def delete_question(question_id):

        question_to_delete = Question.query.get(question_id)
        if not question_to_delete:
            abort(404, "Question does not exist")
        question_to_delete.delete()
        question_to_delete = Question.query.get(question_id)
        if question_to_delete:
            abort(500, "Could not delete question")
        return jsonify({
            "success":True,
            "deleted_id":question_id
        })

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
    def add_new_question():
        incoming_question = request.get_json()
        question = incoming_question['question']
        answer = incoming_question['answer']
        category=incoming_question['category']
        difficulty=incoming_question['difficulty']
        
        
        if category is None:
            abort(404, 'No category found')
        
        elif question == '':
            abort(422, "Missing question text")
        
        elif answer == '':
            abort(422, "Missing answer text")

        question_to_create = Question(
        question, answer, category, difficulty  
        )
        question_to_create.insert()
        return jsonify({
            "success":True,
            "created_id":question_to_create.id
        })
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods = ['POST'])
    def search_questions():
        incoming_json_object = request.get_json()
        search_term = incoming_json_object['searchTerm']
        search_query = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        if not search_query:
            abort(404, "No item found")
        
        search_categories = [
            question.category 
            for question in 
            Question.query.filter(
            Question.question.ilike(
            f'%{search_term}%')).
            distinct(Question.category).
            all()
            ]
        
        return jsonify({
            'searchTerm': search_term,
            'success': True,
            'questions': [{
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty
                } for question in search_query
            ],
            'total_questions': len(search_query),
            'categories': search_categories
        })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<category_type>/questions')
    def get_questions_by_category(category_type):
        this_category = category_type
        all_categories = [category.type for category in Category.query.all()] 
        
        if category_type not in all_categories:
            abort(404, "Category does not exist")
        questions_in_category = Question.query.filter(Question.category == category_type).all()

        if not questions_in_category:
            abort(404, "No question in category")
        
        return jsonify({
            'totalQuestions': len(questions_in_category),
            'currentCategory': this_category,
            'success': True,
            'questions': [{
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty,  
            } 
            for question in questions_in_category
            ],
            
        })
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
    def get_quiz_play():
        # THIS ENDPOINT ALLOWS THE USER TO PLAY THE TRIVIA GAME BY
        # SELECTING A PARTICULAR CATEGORY OR ALL TO GET QUESTIONS
        # FROM ANY CATEGORY

        # Get category
        incoming_json = request.get_json()
        current_category = incoming_json.get('quiz_category')
        all_questions_in_categories = None
        print(current_category)
        # If Category is ALL, retrieve question from any category
        if current_category == 'ALL':
            all_questions_in_categories = Question.query.filter().all()
        else:
            all_questions_in_categories = Question.query.filter(
                Question.category == current_category).all()

        # abort if no question in the selected category
        if not all_questions_in_categories:
            abort(400, 'No question or category')

        # This line retrieves all questions already answered in the current
        # game session
        previous_questions = incoming_json.get('previous_questions')

        # These ids are all valid ids related to the current category being
        # played
        all_questions_ids = [
            question.id for question in all_questions_in_categories
        ]

        # When there are no more new question, notify the user and abort
        if len(previous_questions) >= len(all_questions_ids):
            abort(404, 'No new question')
        random_int = -1

        # if there are new questions, select a random question from the pool
        while True:
            random_int = random.randint(
                min(all_questions_ids), max(all_questions_ids))
            if (random_int not in previous_questions and
                    random_int in all_questions_ids):
                break
        if random_int > 0:
            this_question = Question.query.get(random_int)

        random_question = {

            'id': this_question.id,
            'question': this_question.question,
            'answer': this_question.answer,
            'category': this_question.category,
            'difficulty': this_question.difficulty

        }

        # return the question to client
        return jsonify({

            'question': random_question,
            'success': True,
            'question_id': this_question.id
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify({
            'message': error.description,
            'success': False,
        })
        response.status_code = 404
        return response

    @app.errorhandler(400)
    def unknown_request(error):
        response = jsonify({
            'message': error.description,
            'success': False,
        })
        response.status_code = 400
        return response

    @app.errorhandler(422)
    def invalid_data(error):
        response = jsonify({
            'message': error.description,
            'success': False,
        })
        response.status_code = 422
        return response

    @app.errorhandler(500)
    def server_error(error):
        response = jsonify({
            'message': error.description,
            'success': False,
        })
        response.status_code = 500
        return response


    return app

