# Bedrock

Scaffolding and example code for a simple app (API only, no UI). Includes:

- A Flask app with user accounts (register/login/check auth)
    - Uses a Postgres database
- A Celery worker for async tasks
    - Uses Redis as a broker
    - Shares code with the Flask app, so it can access DB models etc.
- Celery beat for scheduled tasks

Demo code exercises all of this functionality. The codebase is small enough
that you should be able to read through all of it in about 15 minutes.

## Development tips

- This repo uses [Docker Compose](https://docs.docker.com/compose/). Get the
  site running locally with `docker compose up --build`. Test that it's working
  by navigating to <http://localhost:8080/ping>.
- If you change database models, you probably want to discard all persistent
  state in the database (rather than bother with a database migration). You can
  do this with `docker compose down -v`.
- The Flask web server is set up to auto-reload on changes. Celery/Beat do not:
  if you change jobs/schedules, you should restart the corresponding services.
  You can do this like `docker compose restart worker` (or `beat`).
- To interact with the service, use a REST client like
  [Postman](https://www.postman.com/product/rest-client/), or use cURL on your
  command line.

## Example interaction

```console
$ curl -H 'Content-Type: application/json' \
	-XPOST localhost:8080/register \
	--data '{"username": "alice", "password": "supersecret"}'

$ curl localhost:8080/status/alice
{
  "status": null
}

$ curl -H 'Content-Type: application/json' \
	-XPOST localhost:8080/login \
	--data '{"username": "alice", "password": "supersecret"}'
{
  "token": "60164b1b85f70c820a0f048f6aadf71a4b7324fc0672f81099dad3eb53ff5c84"
}

$ curl -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer 60164b1b85f70c820a0f048f6aadf71a4b7324fc0672f81099dad3eb53ff5c84' \
	-XPOST localhost:8080/status \
	--data '{"status": "On vacation in Tahiti."}'

$ curl localhost:8080/status/alice
{
  "status": "On vacation in Tahiti."
}

$ # wait for a day...
$ curl localhost:8080/status/alice
{
  "status": null
}
```

## Warm-up exercise

If you want an idea for a warm-up exercise to get familiar with modifying the
code (DB models, routes, Celery tasks, ...), here are some ideas:

- Add a `/users` route that lists all users.
- Get a user's email via their GitHub profile.
    - Add a `/email/<username>` endpoint that returns a user's email address by
      looking it up in their GitHub profile.
    - Use the GitHub REST API, or the
      [PyGithub](https://github.com/PyGithub/PyGithub) library (recommended).
    - You might need to get a GitHub personal access token (and create the
      client with `github = Github("<YOUR TOKEN HERE>")`. You can create a
      token [here](https://github.com/settings/tokens). You can create a
      "Personal access token (classic)" and leave all the checkboxes empty: you
      only need read-only access to public information, which needs access to
      none of the specialized scopes.
