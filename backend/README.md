# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method Not Found

### Endpoints 
#### GET /categories
- General:
    - Returns: A list of category objects which contains `id` and `type`, and success value
    - Request Arguments: None
    - All questions are returned as result.
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ],
  "success": true,
}
```

#### GET /questions
- General:
    - Returns: A list of questions objects which are paginated, and success value, categories, total number of questions, and current category
    - Request Arguments: `page`
    - Fetch a list of dictionary questions where the key is the id.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

``` {
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ],
  "questions":[
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "totalQuestions": 2,
  "currentCategory": "Science"
  "success": true,
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists.
    - Request Arguments: `question_id`
    - Returns: the id of the deleted book, success value, and success message to update the frontend.
- `curl -X DELETE http://127.0.0.1:5000/question/{question_id}`
```
{
  "deleted": question_id,
  "success": true,
  "message": "Question deleted successfully.",
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted parameters question, answer, difficulty, category.
    - Request Arguments: `question`, `answer`, `difficulty`, `category`
    - Returns: the success value, total books, success message to the frontend.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Is javascript a programming language", "answer":"yes, javascript is a programming language", "difficulty": 2, "category": 1}'`
```
{
  "success": true,
  "message": "Question created successfully."
}
```

#### POST /search
- General:
    - Search for existing questions that matches the search parameters.
    - Request Arguments: `searchTerm`
    - Returns: the questions, success value, total questions, current category to update the frontend.
- `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
  "success": true,
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "totalQuestions": 2,
  "currentCategory": 'History'
}
```

#### GET /categories/{category_id}/questions
- General:
    - Returns: A list of questions objects that the category matches the requested category id, which are paginated, and success value, categories, total number of questions, and current category
    - Request Arguments: `page`
    - Fetch a list of dictionary questions where the key is the id, and the category is same as the requested category sent by the frontend.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` {
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ],
  "questions":[
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "yes, javascript is a programming language", 
      "category": 1, 
      "difficulty": 2, 
      "id": 26, 
      "question": "Is javascript a programming language"
    }, 
    {
      "answer": "yes, python is a programming language", 
      "category": 1, 
      "difficulty": 2, 
      "id": 27, 
      "question": "Is python a programming language"
    }
  ],
  "totalQuestions": 5,
  "currentCategory": "Science"
  "success": true,
}
```

#### POST /quizzes
- General:
    - Get questions to play the quiz. This endpoint should take category and previous question parameters
      and return a random questions within the given category, if provided, and that is not one of the previous questions
    - Request Arguments: `previous_questions`, `quiz_category`
    - Returns: a single random question, success value, to update the frontend.
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5], "quiz_category": "History"}'`
```
{
  "question": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
```