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

Format latex files:
```shell
latexindent -w -s -l=formatting.yaml tex/General/Settings.tex
```

Format line breaks:
```shell
fmt -w 100 tex/Chapters/apathy.tex
```
