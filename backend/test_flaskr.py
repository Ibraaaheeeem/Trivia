import math
import os
from random import random
import re
from sre_parse import CATEGORIES
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import QUESTIONS_PER_PAGE
from flaskr import create_app
from flask import jsonify
from models import setup_db, Question, Category

QUESTIONS_TO_INSERT = 12
CATEGORIES_TO_INSERT = 5

USER = os.getenv('DB_USER', 'postgres')
PASS = os.getenv('DB_PASS', '')
HOST = os.getenv('DB_HOST', 'localhost:5432')
DBNAME = os.getenv('DB_NAME', 'trivia_test')


class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()

        self.client = self.app.test_client

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            USER,
            PASS,
            HOST,
            DBNAME

        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # self.insert_questions()
            # self.insert_categories()

    def clear_db(self):
        # clear the database questions and categories
        with self.app.app_context():
            try:
                self.db.session.query(Question).delete()
                self.db.session.query(Category).delete()
                self.db.session.commit()
            except BaseException:
                self.db.session.rollback()

    def tearDown(self):
        """Executed after reach test"""
        # clear the db after every test
        self.clear_db()
        pass

    """
    TODO
    Write at least one test for each test for
    successful operation and for expected errors.
    """
    # Test 1

    def test_get_categories(self):

        # INSERTS CATEGORIES INTO THE DATABASE
        # AND TESTS THAT THE CATGORIES ARE RETRIEVED FROM THE DATABASE

        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
        response = self.client().get('/categories')
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result['success'], True)
        self.assertTrue((json_result['categories']))
        # total test categories is 5
        self.assertEqual(len(json_result['categories']), CATEGORIES_TO_INSERT)

    # Test 2
    def test_404_get_categories(self):

        # SIMULATES A CONDITION WHERE THERE ARE NO CATEGORIES
        # ENTERED INTO THE DATABASE
        # PERHAPS IN A NEW SET-UP AND
        # RETURNS AN ERROR NOTIFYING THE USER THAT
        # NO CATEGORY EXISTS

        response = self.client().get('/categories')
        json_result = json.loads(response.data)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(response.status_code, 404)

    # Test 3
    def test_get_questions_per_page_10(self):

        # INSERTS MORE THAN 10 QUESTIONS INTO THE DATABASE
        # AND TESTS THAT THE FIRST 10 QUESTIONS ARE RETRIEVED FROM THE FIRST
        # PAGE

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        response = self.client().get('/questions')
        json_result = json.loads(response.data)
        self.assertEqual(json_result['success'], True)
        # normally, 10 questions per page
        self.assertEqual(len(json_result['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(response.status_code, 200)

    # Test 4
    def test_404_get_questions_per_page_10(self):

        # SIMULATES A CONDITION WHERE THERE ARE NO QUESTIONS IN THE DATABASE
        # AND RETURNS AN ERROR NOTIFYING THE USER NO QUESTIONS EXIST

        response = self.client().get('/questions')
        json_result = json.loads(response.data)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(response.status_code, 404)

    # Test 5
    def test_get_questions_per_page_excessof10(self):

        # INSERTS MORE THAN 10 QUESTIONS INTO THE DATABASE
        # AND TESTS THAT THE EXCESS OF FIRST 10 QUESTIONS ARE RETRIEVED FROM
        # THE SECOND PAGE

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        response = self.client().get('/questions?page=2')
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result['success'], True)
        self.assertEqual(len(json_result['questions']),
                         QUESTIONS_TO_INSERT % QUESTIONS_PER_PAGE)

    # Test 6
    def test_get_questions_per_page_out_of_range(self):
        # INSERTS MORE THAN 10 QUESTIONS INTO THE DATABASE
        # AND TESTS THAT ENTERING A PAGE RANGE
        # OUTSIDE OF THE AVAILABLE
        # PROPERLY NOTIFIES THE USER

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        trial_page_index = math.ceil(QUESTIONS_TO_INSERT / QUESTIONS_PER_PAGE)
        response = self.client().get('/questions?page='
                                     + str(trial_page_index + 1))
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_result['success'], False)

    # Test 7
    def test_get_questions_per_page_invalid(self):
        # TESTS FOR INVALID QUESTIONS PAGE REQUEST
        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        trial_page_index = -1
        response = self.client().get('/questions?page='
                                     + str(trial_page_index + 1))
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_result['success'], False)

    # Test 8
    def test_delete_questions_with_id(self):

        # INSERTS A NEW QUESTION AND THEN
        # CALCULATES THE TOTAL NUMBER OF QUESTIONS IN THE DATABASE
        # COMPARES THE TOTAL NUMBER OF QUESTIONS IS REDUCED BY 1
        # AFTER DELETION

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        trial_q = Question(
            question='Who is the author of this book',
            answer='I don\'t know',
            category=2,
            difficulty=5
        )
        trial_q.insert()
        total_questions_in_db_b4_delete = len(Question.query.all())
        delete_id = trial_q.id
        response = self.client().delete(f'/questions/{delete_id}')
        deleted_trial_q = Question.query.get(delete_id)
        total_questions_in_db_after_delete = len(Question.query.all())
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result['success'], True)
        self.assertEqual(
            total_questions_in_db_b4_delete,
            total_questions_in_db_after_delete + 1)
        self.assertEqual(deleted_trial_q, None)

    # Test 9
    def test_delete_questions_with_invalid_id(self):

        # TEST FOR AN ATTEMPT TO DELETE A QUESTION WITH INVALID ID
        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)

        delete_id = -1
        all_questions_ids = [question.id for question in Question.query.all()]
        total_questions_in_db_b4_delete = len(all_questions_ids)
        while delete_id in all_questions_ids:
            delete_id = random.randint()
        deleted_trial_q = Question.query.get(delete_id)
        response = self.client().delete(f'/questions/{delete_id}')
        total_questions_in_db_after_delete = len(Question.query.all())

        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(
            total_questions_in_db_b4_delete,
            total_questions_in_db_after_delete)
        self.assertEqual(deleted_trial_q, None)

    # Test 10
    def test_create_new_question(self):

        # CREATE A NEW VALID QUESTION
        # VALIDATED BY INCREASE IN THE TOTAL NUMBER OF
        # QUESTIONS BY 1

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        trial_q = {
            'question': 'Who is the author of this book',
            'answer': 'I don\'t know',
            'category': 'Cat 6',
            'difficulty': 5
        }
        total_questions_before = len(Question.query.all())
        response = self.client().post(f'/questions', json=trial_q)
        total_questions_after = len(Question.query.all())
        json_result = json.loads(response.data)
        new_question_id = json_result['created_id']
        created_trial_q = Question.query.get(new_question_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result['success'], True)
        self.assertTrue(json_result['created_id'])
        self.assertTrue(created_trial_q)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    # Test 11
    def test_bad_format_create_new_question(self):

        # ATTEMPT TO INSERT A QUESTION WITH BAD FORMAT
        # SUCH AS AN EMPTY QUESTION OR ANSWER TEXT

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        trial_q = {
            'question': 'Who is the author of this book',
            'answer': '',
            'category': 'Cat 6',
            'difficulty': 5
        }
        total_questions_before = len(Question.query.all())
        response = self.client().post(f'/questions', json=trial_q)
        total_questions_after = len(Question.query.all())
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(total_questions_after, total_questions_before)

    # Test 12
    def test_search_questions_for_term(self):

        # INSERT KNOWN QUESTIONS WITH TEXT OF
        # KNOWN NUMBER OF OCCURENCE
        # SEARCH FOR THE TEXT AND CONFIRM THE SIZE OF THE QUERY RESULT

        search_term = 'Question 1'
        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        search_message = {
            'searchTerm': search_term
        }
        response = self.client().post(f'/questions/search',
                                      json=search_message)
        json_result = json.loads(response.data)
        expected_search_size = len(Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result['success'], True)
        self.assertTrue(json_result['questions'])
        self.assertTrue(json_result['total_questions'])
        self.assertEqual(json_result['total_questions'], expected_search_size)

    # Test 13
    def test_404_search_questions_for_term(self):

        # SEARCHES FOR NON-EXISTING TEXT IN QUESTIONS

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)
        search_message = {
            'searchTerm': 'NON_EXISTING_TERM'
        }
        response = self.client().post(f'/questions/search',
                                      json=search_message)
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_result['success'], False)

    # Test 14
    def test_get_questions_per_category(self):

        # TEST FOR GETTING QUESTIONS BY CATEGORY
        # COMPARES TOTAL NUMBER OF QUESTIONS IN CATEGORY
        # WITH RESULT FROM ENDPOINT

        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
            self.insert_questions(QUESTIONS_TO_INSERT)
        category_type = 'Cat 1'
        expected_size_of_questions = len(
            Question.query.filter(
                Question.category == category_type).all())
        category_type_url_format = category_type.replace(' ', '%20')
        response = self.client().get(
            f'categories/{category_type_url_format}/questions')
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue((json_result['questions']))
        self.assertEqual(
            json_result['totalQuestions'],
            expected_size_of_questions)
        self.assertEqual(json_result['success'], True)

    # Test 15

    def test_404_no_cat_get_questions_per_category(self):

        # SIMULATES ATTEMPT TO GET QUESTIONS FROM A CATEGORY
        # WHEN THE CATEGORY DOES NOT EXIST

        with self.app.app_context():
            self.insert_questions(QUESTIONS_TO_INSERT)

        category_type = 'Cat 1'
        category_type_url_format = category_type.replace(' ', '%20')
        response = self.client().get(f'categories/{category_type}/questions')
        json_result = json.loads(response.data)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(response.status_code, 404)

    # Test 16
    def test_404_no_question_get_questions_per_category(self):

        # SIMULATES ATTEMPT TO GET QUESTIONS WHEN THERE ARE NO QUESTIONS UNDER
        # A CATEGORY

        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
        category_type = 'Cat 1'
        category_type_url_format = category_type.replace(' ', '%20')

        response = self.client().get(f'categories/{category_type}/questions')
        json_result = json.loads(response.data)
        self.assertEqual(json_result['success'], False)
        self.assertEqual(response.status_code, 404)

    # Test 17
    def test_play_quiz(self):

        # GETS RANDOM QUESTION PER CALL
        # ENSURING THAT PREVIOUSLY ANSWERED QUESTIONS ARE NOT REPEATED

        TEST_CATEGORY = 'Cat 1'
        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
            self.insert_questions(QUESTIONS_TO_INSERT)
        all_questions = Question.query.filter(
            Question.category == TEST_CATEGORY)
        all_questions_ids = [question.id for question in all_questions]
        params = {
            'quiz_category': TEST_CATEGORY,
            'previous_questions': [all_questions_ids[0]]
        }
        response = self.client().post(f'/quizzes', json=params)
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_result['question'])
        self.assertTrue(json_result['question_id'] in all_questions_ids)
        self.assertTrue(json_result['question_id'] != all_questions_ids[0])
        self.assertEqual(json_result['success'], True)

    # Test 18
    def test_play_quiz_completed(self):

        # TEST FOR DETECTION AND PROPER PROMPT WHEN ALL QUESTIONS
        # IN A CATEGORY HAVE BEEN COMPLETELY ANSWERED IN GAME

        TEST_CATEGORY = 'Cat 3'
        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
            self.insert_questions(QUESTIONS_TO_INSERT)
        all_questions = Question.query.filter(
            Question.category == TEST_CATEGORY)
        all_questions_ids = [question.id for question in all_questions]
        params = {
            'quiz_category': TEST_CATEGORY,
            'previous_questions': all_questions_ids
        }
        response = self.client().post(f'/quizzes', json=params)
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_result['success'], False)

    # Test 19
    def test_play_quiz_no_question_or_category(self):

        # TESTS FOR ATTEMPT TO PLAY QUIZ
        # WHEN THERE ARE NO QUESTIONS OR CATEGORIES AVAILABLE

        TEST_CATEGORY = 'Cat'
        with self.app.app_context():
            self.insert_categories(CATEGORIES_TO_INSERT)
            self.insert_questions(QUESTIONS_TO_INSERT)
        params = {
            'quiz_category': TEST_CATEGORY,
            'previous_questions': []
        }
        response = self.client().post(f'/quizzes', json=params)
        json_result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_result['success'], False)

    def insert_questions(self, x):
        # INSERTS TEST QUESTIONS
        for i in range(0, x):

            trial_q = Question(
                question='Question ' + str(i + 1),
                answer='Answer' + str(i + 1),
                category='Cat ' + str((i + 1) % 5),
                difficulty=i % 5
            )
            trial_q.insert()

    def insert_categories(self, x):
        # INSERTS TEST CATEGORIES
        for i in range(0, x):
            trial_category = Category(
                type="Cat " + str(i + 1)
            )
            trial_category.insert()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
