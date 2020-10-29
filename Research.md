- **How is the logged in user being kept track of?**

  Before each request, a check is made to determine if a user is in session storage.

- **What is Flask’s g object?**

  It is a global namespace for holding any data you want during a single app context.

- **What is the purpose of add_user_to_g?**

  To keep track of the entire user instance instead of just the id

- **What does @app.before_request mean?**

  It allows to run a function before each request.
