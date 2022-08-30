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
    @TODO: Set upCORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
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
    @TODO: DONE
    """
    @app.route('/categories')
    def get_categories():
        """

        THIS ENDPOINT RETRIEVES ALL CATEGORIES AVAILABLE IN THE DATABASE
        WHERE THERE ARE NO CATEGORIES AVAILABLE, IT RETURNS NONE

        """
        # get all existing categories
        query_all_categories = Category.query.all()
        all_categories = None

        if query_all_categories:
            all_categories = {
                category.id: category.type
                for category in query_all_categories}
        # return categories
        return jsonify({
            "success": True,
            "categories": all_categories
        })

    """
    @TODO:
    Create an endpoint to handle POST request
    to add a new category
    """
    @app.route('/categories', methods=['POST'])
    def create_new_category():
        """

        THIS ENDPOINT RECEIVES A NEW CATEGORY NAME FROM THE FRONT-END
        AND CREATES A NEW CATEGORY OBJECT WITHH NEW NAME IF IT DOESN'T
        CURRENTLY EXIST. IT THEN RETURNS THE NEW CATEGORY ID

        """
        # get intended category name
        incoming_json = request.get_json()
        new_category_to_create = incoming_json.get('new_category_name')

        # get all existing categories and their names
        query_all_categories = Category.query.all()
        all_category_names = [
            category.type for category in query_all_categories]

        # confirm that name does not currently exist
        if new_category_to_create in all_category_names:
            abort(404, "Category already exist")

        # create the category
        new_category = Category(
            type=new_category_to_create
        )

        new_category.insert()

        # return id of new category
        return jsonify({
            "success": True,
            "category_id": new_category.id
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        """

        THIS ENDPOINT RETURNS ALL QUESTIONS AVAILABLE
        IN THE DATABASE IN PAGES OF TEN QUESTIONS EACH
        WHEN PAGE NUMBER IS INVALID OR OUT OF RANGE,
        IT NOTIFIES THE USER APPROPRIATELY

        WHEN THERE ARE NO QUESTION OR CATEGORY AVAILABLE,
        IT DOESN'T ABORT BUT RATHER RETURNS NULL
        """
        # get page number with default as 1
        page_number = request.args.get("page", 1, type=int)

        # get all questions
        all_questions_query = Question.query.all()

        # get all categories
        all_categories_query = Category.query.all()

        # get total questions
        totalQuestions = len(all_questions_query)

        # get total pages
        total_pages = math.ceil(totalQuestions / QUESTIONS_PER_PAGE)

        # initialize questions and categories to return
        # to return None even if they don't exist
        all_questions = None
        all_categories = None

        if page_number > total_pages and totalQuestions >= 1:
            abort(404, 'Page number out of range')

        if page_number < 1:
            abort(404, 'Invalid page number')

        # Get first and last question of the page
        start = (page_number - 1) * QUESTIONS_PER_PAGE
        end = start + 10

        if not all_categories_query:
            all_categories = None
        else:
            all_categories = {
                category.id: category.type
                for category in all_categories_query}

        if not all_questions_query:
            all_questions = None
        else:
            all_questions = [{
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "category": question.category,
                "difficulty": question.difficulty,

            }
                for question in all_questions_query[start:end]
            ]
        # return questions and categories
        return jsonify({
            "success": True,
            "questions": all_questions,
            "categories": all_categories,
            "totalQuestions": len(all_questions_query)
        }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database
    and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        THIS ENDPOINT RECEIVES A QUESTION ID FROM THE FRONT END AND DELETES IT
        IF IT'S AVAILABLE. OTHERWISE, IT NOTIFIES THE USER THAT THE QUESTION
        WITHH THE ID DOES NOT EXIST

        """
        # get id of question to delete
        question_to_delete = Question.query.get(question_id)

        # if id does not exist, abort and notify user
        if not question_to_delete:
            abort(404, "Question does not exist")

        # otherwise, delete the question
        question_to_delete.delete()
        question_to_delete = Question.query.get(question_id)
        if question_to_delete:
            abort(500, "Could not delete question")

        # return id of deleted question
        return jsonify({
            "success": True,
            "deleted_id": question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_new_question():
        """
        THIS ENDPOINT RECIEVES THE DATA ABOUT A QUESTION FROM THE FRONT-END
        AND CREATES A NEW QUESTION IN THE DATABASE
        WITH BAD FORMAT SUCH AS EMPTY QUESTION OR ANSWER TEXT
        THE OPERATION ABORTS WITH NOTIFICATION TO THE FRONT-END
        """
        # retrieve question data
        incoming_question = request.get_json()
        question = incoming_question['question']
        answer = incoming_question['answer']
        category = incoming_question['category']
        difficulty = incoming_question['difficulty']

        if category is None:
            abort(404, 'No category found')

        elif question == '':
            abort(422, "Missing question text")

        elif answer == '':
            abort(422, "Missing answer text")

        # form the Question object
        question_to_create = Question(
            question, answer, category, difficulty
        )

        # insert into the database
        question_to_create.insert()
        return jsonify({
            "success": True,
            "created_id": question_to_create.id
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
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        THIS ENDPOINT SEARCHES THE DB FOR A QUESTION TEXT
        AND RETURNS ALL MATCHING QUESTIONS
        """
        # get incoming json object and retrieve the search term
        incoming_json_object = request.get_json()
        search_term = incoming_json_object['searchTerm']
        search_query = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        # if the search query does not exist, return no item found
        if not search_query:
            abort(404, "No item found")

        # return categories of found questions
        search_categories = [
            question.category
            for question in
            Question.query.filter(
                Question.question.ilike(
                    f'%{search_term}%')).
            distinct(Question.category).
            all()
        ]

        # return search result
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
            'categories': search_categories,
            'total_questions': len(search_query)

        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<category_id>/questions')
    def get_questions_by_category(category_id):
        """
        THIS ENDPOINT FETCHES ALL QUESTIONS IN A PARTICULAR CATEGORY
        USING THE CATEGORY_ID RECEIVED FROM THE FRONT-END

        """
        # retrieve ids of all categories in the database
        all_categories_ids = [category.id for category in Category.query.all()]
        this_category_id = int(category_id)
        questions_in_category = None

        # if no category_id is specified, get all questions
        # otherwise, retrieve questions from a particular category
        if this_category_id == 0:
            questions_in_category = Question.query.all()
        elif this_category_id not in all_categories_ids:
            abort(404, "Category does not exist")
        else:
            questions_in_category = Question.query.filter(
                Question.category == category_id).all()
        if not questions_in_category:
            abort(404, "No question in category")

        # return all questions retrieved from the database
        # belonging to the category
        return jsonify({
            'totalQuestions': len(questions_in_category),
            'currentCategory': this_category_id,
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
        """
        THIS ENDPOINT ALLOWS THE USER TO PLAY THE TRIVIA GAME BY
        SELECTING A PARTICULAR CATEGORY OR ALL TO GET VARYING
        QUESTIONS FROM ANY CATEGORY

        """
        # Get category index
        incoming_json = request.get_json()
        current_category_index = int(incoming_json.get('quiz_category'))
        all_questions_in_categories = None

        # Get all category indices
        all_category_indices = [
            category.id for category in Category.query.all()]

        # If No particular category is specified, get questions from all
        # categories is requested
        if current_category_index == 0:
            all_questions_in_categories = Question.query.all()

        # Otherwise verify the category index is valid
        elif current_category_index in all_category_indices:
            # then get all questions in the category
            all_questions_in_categories = Question.query.filter(
                Question.category == current_category_index).all()

        # abort if no question in the selected category
        if not all_questions_in_categories:
            abort(404, 'No question or category')

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

    def cat_index_to_type(id):
        c = Category.query.get(id)
        if c is not None:
            return (c.one()).type

    return app
