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
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
set FLASK_DEBUG=1 && python -m flask run
```

This will detect file changes and restart the server automatically.

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


### Api Documentation

`GET '/categories'`

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

#### `GET '/questions'`
- Fetches a dictionary which includes a list of questions, the category of the returned questions, success status and pagination data
- Request Arguments: `page` (the page number) (optional, integer)
- Returns: A multiple key/value pairs object with the following 

Here is an example of the returned object:

```JSON
{
  "categories": {
    "1": "Sports"
  },
  "current_category": [
    1
  ],
  "questions": [
    {
      "answer": "Mikel Arteta",
      "category": 1,
      "difficulty": 2,
      "id": 12,
      "question": "Who is Arsenal's current manager?"
    }
  ],
  "success": true,
  "total_questions": 5
}
```

#### `DELETE '/questions/<int:question_id>'`
- Deletes the question with the specified `question_id`.
- Request Arguments: `question_id` as a path variable (required, integer)
- Returns: A single key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` depending on the successfullness of the endpoint's execution.
    - `deleted`: Will return the id of the deleted question.

Here is an example of the returned object:

```JSON
{
  
  "success": True,
  "deleted": 3
}
```

#### `POST '/questions'`
- Creates a new question and saves it in the database.
- Request Arguments: a key/value pairs object with the following properties:
    - `question`: the question text.
    - `answer`: the answer to the question to be created.
    - `difficulty`: difficulty level(a whole number).
    - `category`: category ID field.

Sample request object:

```JSON
{
      "answer": "Mikel Arteta",
      "category": 1,
      "difficulty": 2,
      "question": "Who is Arsenal's current manager?"
}
```

- Returns: A single key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` depending on the successfullnes of the endpoint's execution.
    - `created`: Returns the value of the newly created question.id,

Here is an example of the returned object:

```JSON
{
  
  "success": True,
  "created": 3
}
```

#### `POST '/questions_search'`
- Returns questions that match a provided search query
- Request Arguments:
    - `searchTerm`: a substring to compare and match with existing questions
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` depending on the successfullnes of the endpoint's execution.
    - `questions`: contains a list of the matched questions. Each question is a single key/value pairs object containing `id`, `answer`,  `question`, `category` and  `dificulty`.
    - `total_questions`: the number of questions returned.

Here is an example of the returned object:

```JSON
{
  "questions": [
    {
      "id": 3,
      "answer": "Mikel Arteta",
      "category": 1,
      "difficulty": 2,
      "question": "Who is Arsenal's current manager?"
    }
  ],
  "success": true,
  "total_questions": 1,
  "current_category": None
}

```

#### `GET '/categories/<int:category_id>/questions'`
- Returns a questions that fall under a specific category.
- Request Arguments:
    - `category_id`: the `id` of the desired category as a path parameter
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` depending on the successfullnes of the endpoint's execution.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `dificulty`.
    - `total_questions`: the number of questions returned.

Here is an example of the returned object:
```json
{
  "questions": [
    {
      "id": 3,
      "answer": "Mikel Arteta",
      "category": 1,
      "difficulty": 2,
      "question": "Who is Arsenal's current manager?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 5
}
```

#### `POST '/quizzes'`
- Asks a question from a specified `quiz_category`
- Request Arguments:
    - `quiz_category`: question's category id field.
    - `previous_questions`: a list of the recent questions, none of these will be asked if there still some unasked questions

Sample request object
```JSON
{
      "quiz_category": 1,
      "previous_questions": [2,1]
}
```

- Returns: A multiple key/value pairs object with the following content:
    - `success`: can take values `True` or `False` depending on the successfullnes of the endpoint's execution.
    - `question`: contains the question. Question is a key/value pairs object containing `id`,  `question`, `answer`, `category` and  `dificulty`.

Here is an example of the returned object:
```JSON
{
  "question": {
      "id": 3,
      "answer": "Mikel Arteta",
      "category": 1,
      "difficulty": 2,
      "question": "Who is Arsenal's current manager?"
  },
  "success": true
}
```

#### Failed Requests
All failed requests have a similar response structure. <br/>
- Returns: A multiple key/value pairs object with the following content:
    - `success`: All failures will have this value as false
    - `error`: HTTP status code for the failure, read more about status codes [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
    - `message`: Explaination of the failure
```JSON
{
  "success": False,
  "error": 400,
  "message": "Bad Request"
}
```

## Testing

To deploy the tests, navigate into your virtual environment and run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Acknowledgments
Extended appreciation and credits to the following for the helpul resources
- [MDN web docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) for http statuses
