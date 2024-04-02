
# Online Library System

SETTEL Task 


## Features

- This Application is compatible with Python 3.8 or any subsequent versions.
- I've used the FastAPI framework in conjunction with SQLAlchemy. 
- For testing purposes, I've employed pytest.
- This application utilizes Swagger and Redoc for API documentation.
- This application can be executed using Docker


## Run Locally

Clone the project

```bash
  git clone https://github.com/abdoconan/SETTEL-Task.git
```

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`ALGORITHM`


Go to the project directory

```bash
  cd SETTEL-Task
```

Create virtual environment

```bash
  python -m venv venv
```
Activate the virtural environment on windows

```bash
  venv\Scripts\activate
```

Install Dependencies 

```bash
  pip install -r requirements.txt
```
Start the application 

```bash
  uvicorn app.main:app --reload
```

## Documentation

Once the application is running, navigate to the API documentation.

[Swagger](http://localhost:8000/docs)

[Redoc](http://localhost:8000/redoc)

## Running Tests

To run tests, make sure that the virtual environment then run the following command

```bash
  pytest
```


## Deployment

To deploy this project into docker image

```bash
  docker build . -t settel:1 
```

To run the application, use the following command


```bash
  docker compose up 
```

## FAQ

#### Which endpoints necessitate authentication?

- /books/new
- /books/edit

#### What steps should be taken to add a new book to the application?

* Make sure to add book categories through API /book_categories/create
* Make sure to logged in before creating any post

#### How should be able to edit a book details?

The user how created it only, otherwise you will get 403 Forbidden

## Appendix

For the api 
```http
  GET /books/list
```
It allows you to filter with multiple owners_ids. You can call the api like this 
```http
  GET /books/list?limit=10&skip=0&owners_ids=1&owners_ids=2
```
The API will function smoothly, filtering with both owner IDs. However, although [Swagger](http://localhost:8000/docs) lacks visibility of this feature, navigating to [Redoc](http://localhost:8000/redoc) will display the appropriate implementation.


## Appendix 2

- You can log in with either email and password or username and password seamlessly.
- Additional fields may appear in the login form, but you can simply send the username and password fields. Other fields are intended for extension purposes.
- If you prefer to log in with an email, simply input the email into the username field in the login form, and it will function correctly.