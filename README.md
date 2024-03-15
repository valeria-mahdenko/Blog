# Flask App with Docker and Docker Compose

This project is a Flask application that uses Docker and Docker Compose for deployment.

## Requirements

Make sure you have the following tools installed:

- Docker
- Docker Compose

## Setup

Clone the repository:
```bash
git clone https://github.com/valeria-mahdenko/Blog.git
cd Blog
```

## Running the Application
Start the application using Docker Compose:
```bash
docker-compose up --build
```
Open your web browser and go to http://localhost:5000 to check the application.


## Running tests
To run tests, use the following command:
```bash
docker-compose run --rm tests
```
This will run all the tests and return the results in the console.

## Stopping the Application
To stop the application, use the following command:
```bash
docker-compose down
```
This will stop all containers associated with the application.
