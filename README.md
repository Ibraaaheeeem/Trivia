# API Development and Documentation Final Project

## Trivia App - Udacity Full Stack Web Development Project III

### The task
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting the Project

I forked the starter code on [Github](https://github.com/udacity/cd0037-API-Development-and-Documentation-project) to my local repository

## About the Stack

The development has commenced with some starter code, designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contained a partially completed Flask and SQLAlchemy server. The job was primarily in `__init__.py` to define the endpoints and reference models.py for DB and SQLAlchemy setup.

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. With some experience in React, more functionalities were included in the frontend to improve the app

## Running the app:
For instructions on how to put up the backend, see backend/README.md
For instrucitons on how to start up the frontend, see frontend/README.md
