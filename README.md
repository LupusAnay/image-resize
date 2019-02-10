# Image Resize
Flask async REST service using for image resizing

Usage: `docker-compose up`

Further information can be found in the 
documentation on Docker and Docker Compose

## API Reference:

### Create resize task:
```http request
POST /operation/resize HTTP/1.1

Content-Type: multipart/form-data
```
Accepts a file in `mulipart/form-data` format and json with height and width 
parameters
Returns a json with created task id, or error

### Get task state
```http request
GET /status/<uuid:task_id> HTTP/1.1
```
Accepts a task id in UUID format as a GET parameter, and returns state of that 
task, or returns 404 if there is not task with given id

### Get task result
```http request
GET /operation/result/<uuid:task_id> HTTP/1.1
```

Accepts a task id in UUID format as a GET parameter, and returns result of that 
task, or returns 404 if there is not task with given id or it's not completed
yet
