# Backend - Trivia API
The Backend section of the Trivia API contains endpoints that allow the front end to communicate with it to play the Trivia Game. 

## Setting up the Backend
While in the frontend folder, typing the following commands will start the backend
`export FLASK_APP=flaskr/__init__.py`
`npm run start-backend`

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

# GET ALL CATEGORIES
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys,

  1. `success`: which returns True when the request is successfull
  2. `categories`, that contains an object of `id: category_string` key: value pairs.

```json
"success":True
"categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

# CREATE NEW CATEGORY
`POST '/categories'`

- Fetches a JSON object containing id of the new category that has been created and the success status
- Request Arguments: A JSON object containing the `new_category_name`

```json
"new_category_name":"Biology"
```

- Returns: An object with two keys,

  1. `success`: which returns True when the request is successfull
  2. `category_id`, that contains an object of `id: category_string` key: value pairs.

```json
{
"success":True
"category_id":9
}
```

# GET ALL QUESTIONS
`GET '/questions'`

- Fetches a JSON object containing questions and category dictionaries:
- Request Arguments: optional `page_number` the default of which is 1
  Example: `page_number = 2` 
- Returns: An object with the following keys,

  1. `success`: which is true if operation is successful
  2. `questions`: an array of question dictionaries
  3. `categories`: an array of dictionaries containing categories
  4. `totalQuestions`:the total number of questions available

```json
{
"success":True,
"questions":[{
  "id":32,
  "question":"Who is the author of \"Things fall apart\"",
  "answer":"Chinua Achebe",
  "category":"Literature",
  "difficulty":2,
  }],
"categories":{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
},
"totalQuestions":30
}
```

# DELETE A QUESTION WITH ID
`DELETE '/questions/<int: delete_id>'`
  - Deletes a question from the database using its id
  - Request Arguments: id of the question to be deleted
  Example:
  `id = 9`

  - Returns: 
  `success`: flag which is True if operation is successfully 
  `id`: id of the deleted question
  Example:

  ```json
  {
  "success":True,
  "delete_id":9
  }
  ```

# CREATE A NEW QUESTION
`POST '/questions'`
  - Creates a new question in the database
  - Requests: question parameters such as the 
    `question` The text of the question, 
    `answer` The text of the answer to the question,
    `category` id of the category to which the question belong
    `difficulty`the difficulty level
    
    Example:

    ```json
    {
    "question":"What is python?",
    "answer":"Not a snake",
    "category":5,
    "difficulty":2
    }
    ```

    Returns:
    `success`: evaluates to true if operation is successful, otherwise false
    `created_id`: id of created question

    Example
    ```json
    {
    "success":True,
    "created_id":13
    }
    ```
# SEARCH FOR QUESTIONS WITH A TERM
  `POST '/questions/search'`
   - Searches the database of questions and return questions that match the search term
   - Requests: a JSON object containing
   `searchTerm` the string to search the database for

   Example:
   ```json
   {"searchTerm":"SOMETHING TO SEARCH"}
   ```
   
   -Returns:
   `search_Term` the search term
   `success` returns True if operation is successful
   `questions` an array of dictionaries of questions matching the search phrase
   `categories`: an array of dictionaries containing categories
   `totalQuestions`:the total number of questions available
   
   
   Example:

   ```json
   {
  "searchTerm":"SOMETHING TO SEARCH"
  "success":True,
  "questions":[{
    "id":32,
    "question":"Who is the author of \"Things fall apart\"",
    "answer":"Chinua Achebe",
    "category":"Literature",
    "difficulty":2,
  }],
  "categories":{
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "totalQuestions":30 
  }
  ```
# GET QUESTIONS BY CATEGORY
  - Fetches an array of all questions that occur under the specified category
  - Requests: 
  `category_id`id of the category for which the question is being requested
  e.g `category_id=5`
  
  - Returns:
  ```json
  "totalQuestions":30,
  "currentCategory":5
  "success":True,
  "questions":[{
    "id":32,
    "question":"Who is the author of \"Things fall apart\"",
    "answer":"Chinua Achebe",
    "category":"Literature",
    "difficulty":2,
  }]
  ```

# PLAY THE TRIVIA GAME
`POST '/quizzes'`
  - Fetches a random question in either any or a specified category
  - Requests: 
  `quiz_category` id of the category in which the quiz is being played
  - Returns:
  `question` a dictionary of the question object
  `success` true if operation is successful
  `question_id` id of the returned quesion
  
  Example:
  ```json
  "question":{
    "id":32,
    "question":"Who is the author of \"Things fall apart\"",
    "answer":"Chinua Achebe",
    "category":"Literature",
    "difficulty":2,
  }
  "success":True,
  "question_id": 32
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
