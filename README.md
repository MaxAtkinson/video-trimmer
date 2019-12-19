# Trim Videos

## Build

- Run `cp .env.template .env`
- Set up `.env` with AWS credentialss
- Run `make build && make develop` for dev env and `make down` when done
- Or without docker, `python api.py`

## cURL

- POST: `curl -X POST -H 'Content-Type: application/json' -d '{"t_start": 0, "t_end": 5, "src_url": "k3YmNzaTE6XAeocyVuctpmcXe4g_iNWh"}' localhost:5000/videos`

- PUT: `curl -X PUT -H 'Content-Type: application/json' -d '{"t_start": 0, "t_end": 10, "src_url": "k3YmNzaTE6XAeocyVuctpmcXe4g_iNWh"}' localhost:5000/videos`

- DELETE: `curl -X DELETE localhost:5000/videos/{id}`

- GET: `curl localhost:5000/videos/{id}`

- GET list: `curl localhost:5000/videos`
