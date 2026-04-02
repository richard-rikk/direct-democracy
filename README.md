# direct-democracy
The latex project that contains code for compiling the direct democracy pdf paper.

## Commands

Start the container:
```shell
docker compose up --build -d
```

Stop the container:
```shell
docker compose down
```

Fix linting and formatting for the python script:
```shell
ruff check --select I --fix
ruff format
```
