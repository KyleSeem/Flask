Optional Assignment: Semi-Restful Users

Have 7 routes in your server.py. Because we are working with 'users', they might look like:
1. a GET request to /users - calls the index method to display all the users. This will need a template. 
2. GET request to /users/new - calls the new method to display a form allowing users to create a new user. This will need a template. 
3. GET request /users/<id>/edit - calls the edit method to display a form allowing users to edit an existing user with the given id. This will need a template. 
4. GET /users/<id> - calls the show method to display the info for a particular user with given id. This will need a template. 
5. POST to /users/create - calls the create method to insert a new user record into our database. This POST should be sent from the form on the page /users/new. Have this redirect to /users/<id> once created.
6. GET /users/<id>/destroy - calls the destroy method to remove a particular user with the given id. Have this redirect back to /users once deleted. 
7. POST /users/<id> - calls the update method to process the submitted form sent from /users/<id>/edit. Have this redirect to /users/<id> once updated. 
