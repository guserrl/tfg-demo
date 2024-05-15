FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB world
COPY world.sql init.sql inflation.csv /docker-entrypoint-initdb.d/