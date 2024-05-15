postgre
docker build -t my-postgres-db ./
docker images -a
docker run -d --name my-postgresdb-container -p 5432:5432 my-postgres-db

docker image rm 'nameOfTheImage'
