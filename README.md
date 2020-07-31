# Notes
Few changing for project structure
1. `src`

    Main codebase for a project
    
2. `.github`

    Integration GitHub Action like CI, running tests
    
3. `.docker`
    
    Folder for Docker services

## Project Setup
### Docker
You need to install `docker-compose`. Run command
```shell script
pip install docker-compose
```

After that you can run commands

```shell script
docker-compose build
docker-compose up -d
```

or 
```shell script
make run
```

After that you can run `docker-compose ps`. You will see

```shell script
     Name                   Command               State           Ports
--------------------------------------------------------------------------------
castlabs_db_1    docker-entrypoint.sh postgres    Up      5432/tcp
castlabs_web_1   uvicorn src.app:app --relo ...   Up      0.0.0.0:8000->8000/tcp
```
You can send request to `0.0.0.0:8000`

Swagger `0.0.0.0:8000/docs`

## Testing

### From Docker
1. Install docker-compose
2. Run
    ```shell script
    make test
    ```
   or
   ```shell script
   docker-compose build
   docker-compose up -d
   docker-compose run web pytest . --cov=src
   docker-compose stop
   ```
