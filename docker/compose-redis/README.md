# Python Web App with Docker Compose and Redis

The application uses the Flask framework and maintains a hit counter in Redis.

## Run 

```sh
# bring up
docker compose up

# bring down
docker compose kill
```
## Compose `yml` file

- Container port 5000 forwarded to host port 5000
- `redis` service uses a public Redis image pulled from the Docker Hub registry.
- `volumes` key mounts the project directory (current directory) on the host to /code inside the container. This allows modifying the code on the fly, without rebuilding image.
