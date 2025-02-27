# Frontend - Trivia API
The Frontend section of the TRIVIA API contains the user interation part of the app

A user can create questions in specified categories filling in the question text, answer text and the difficulty rating. Questions can also be deleted at will.

Categories can be created so that questions can then be added under it

On the home page, the app allows the user to read the questions in pages each of maximum 10 questions and view the answer by the toggling the Show/Hide Answer button

In the Play section, a user can either seek challenge in a particular section or all sections whereby questions are asked and the user is expected to supply the answer

A session of the game contains 5 questions after which the user is assessed and the final score is made available

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

## Required Tasks

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

### ENDPOINT Behaviours

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "success": True,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": 4
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
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
---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": 5
 }
```

- Returns: a json with new question object, id of the question object and success status

```json
{
  "success":True,
  "question_id": 32,
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
  
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: success status and the id of the question just created

---
```json
{
"success":True,
"created_id":13
}
```

---
`POST '/questions/search'`
- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "something to search for"
}
```

- Returns: search term, success status, any array of questions, an dictionary of categories, a number of totalQuestions that met the search term and the current category id

```json
{
  "searchTerm":"SOMETHING TO SEARCH",
  "success":True,
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": 5
}
```
