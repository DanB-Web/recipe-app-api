# recipe-app-api

Recipe API Project

## Commands

Build image directly via appropriate Dockerfile (current dir in this case)
`docker build .`

Build image via approprite `docker-compse.yml` file (will look for nearest)
`docker-compose build`

## Executing shell commands inside a service

`--rm` removes the container after the process (to prevent wasted memory)
`sh -c` runs a shell command inside the named service (`app`, in this case)

`docker-compose run --rm app sh -c 'python manage.py xxxxxx'`
