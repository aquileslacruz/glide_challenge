# Glide Code Challenge
This project implements some GET endpoints for data provided by a third-party API

## Usage
To initialize containers

    docker-compose up -d --build

## API routes to use

### Get employee list
    curl -X GET 'http://127.0.0.1:5000/employees'

### Get employee detail
    curl -X GET 'http://127.0.0.1:5000/employees/1'

### Get office list
    curl -X GET 'http://127.0.0.1:5000/offices'

### Get office detail
    curl -X GET 'http://127.0.0.1:5000/offices/1'

### Get department list
    curl -X GET 'http://127.0.0.1:5000/departments'

### Get department detail
    curl -X GET 'http://127.0.0.1:5000/departments/1'

## Testing URL argument handling
Another part of the project was the handling of URL arguments in the endpoints, this can be tested with:

    curl -X GET 'http://127.0.0.1:5000/employees?limit=10&offset=10&expand=manager.manager&expand=office&expand=department.superdepartment'
