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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('eagles', '', '', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            "question": "What programming language does apple use fro their mobile gargets",
            "answer": "Swift programming language",
            "difficulty": 2,
            "category": 1
        }
        
        self.quiz = {
            'previous_questions': [5],
            'quiz_category': {"type": 'History', "id": 4},
        }

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
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        # self.assertTrue(data["currentCategory"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_questions_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_405_sent_category_request_with_invalid_method(self):
        res = self.client().post("/categories", json={'category_id': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
        
    def test_delete_question(self):
        res = self.client().delete("/questions/7")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)
        self.assertEqual(question, None)

    def test_404_delete_question_does_not_exist(self):
        res = self.client().delete("/books/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_bad_method_question_posted(self):
        res = self.client().put('/questions', json={'question': 'noun', 'answer': 'yes', 'category': 4, 'difficulty': 2})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
        
    def test_search_questions(self):
        res = self.client().post('/search', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        # self.assertTrue(data["currentCategory"])
        self.assertTrue(data['totalQuestions'])
        
    def test_422_if_search_not_process(self):
        res = self.client().post('/search', json={'searchTerm': None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def tets_get_questions_for_category(self):
        res = self.client().get('/categories/11/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        
    def test_400_bad_request_getting_questions_for_category(self):
        res = self.client().get('/categories/11000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
    
    def test_get_current_quiz_question(self):
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['total_questions'])
        
    def test_405_method_not_found_current_quiz_question(self):
        res = self.client().get('/quizzes', json=self.quiz)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()