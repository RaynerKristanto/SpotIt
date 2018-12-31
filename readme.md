

## How to Start Flask app
The runnable .py is `web/main.py`

The conda environment requirements are provided in `web/conda.txt`

To set up for Windows, run `set FLASK_APP=main.py`, then run `flask run` to initialize the app

## Endpoints
The endpoints currently set up are `POST: /create`, `POST: /join`, and `GET: /invite`. 

### POST /create
operates on `formdata` with two parameters: `hostID` and `roomID`. The roomID must be unique across all rooms

### POST /join
operates on `formdata` with two parameters: `userID` and `roomID`. The roomID must exist, and the userID must be uinique
within the room.

### GET /show_rooms
No params. quick way to see a list of the rooms currently available
