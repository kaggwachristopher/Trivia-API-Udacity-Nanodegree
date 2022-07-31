import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.environ.get('DATABASE_NAME_TESTS', 'trivia')
        self.database_user = os.environ.get('DATABASE_USERNAME', 'postgres')
        self.database_password = os.environ.get(
            'DATABASE_PASSWORD', 'postgres')
        self.database_host = os.environ.get('DATABASE_HOST', 'localhost:5432')
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.database_user, self.database_password,
                                                               self.database_host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions_should_return_questions_with_200_status_code(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_should_throw_an_error_when_a_non_integer_page_number_is_provided(self):
        res = self.client().get('/questions?page=non_number')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad request")

    def test_get_questions_should_return_categories_with_200_status_code(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        data.popitem()
        self.assertEqual(data['categories'], data['categories'])

    def test_get_categories_endpoint_should_return_405_response_when_the_request_method_is_not_get(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_get_questions_by_categories_should_return_categories_with_200_status_code(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_categroy'], 'Science')
        self.assertNotEqual(len(data['questions']), 0)

    def test_get_questions_by_category_should_return_404_when_the_supplied_category_id_doesnt_exist_in_the_database(self):
        res = self.client().get('/categories/9876/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource not found")

    def test_add_question_should_create_the_question_successfully_when_all_the_required_data_is_provided(self):
        question_before_adding = Question.query.all()
        res = self.client().post('/questions', json={
            'question': 'Sample question',
            'answer': 'sample anwser',
            'difficulty': 1,
            'category': '1'
        })
        question_after_adding = Question.query.all()
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(question_after_adding) -
                        len(question_before_adding) == 1)

    def test_add_question_should_fail_with_a_400_response_code_when_some_required_data_is_not_provided_in_payload(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_search_question_should_retreive_matching_questions_when_a_search_term_is_provided(self):
        res = self.client().post('/search', json={'searchTerm': 'test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question_should_return_bad_response_when_a_search_term_is_not_provided(self):
        res = self.client().post('/search', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_play_quiz_should_return_a_quiz_when_the_payload_contains_the_required_data(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [2, 3, 4],
            'quiz_category': {'id': '1', 'type': 'Science'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_search_play_quiz_should_return_bad_response_when_a_search_term_is_not_provided(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_delete_question_should_successfuly_delete_question_with_supplied_id(self):
        new_questions = Question(
            question="sample question 2", answer="sample answer 2", category="1", difficulty=1)
        new_questions.insert()
        question_id = new_questions.id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_delete_question_should_throw_not_found_when_provided_question_id_does_not_exist(self):
        res = self.client().delete('/questions/789')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
