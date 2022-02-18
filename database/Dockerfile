FROM postgres:latest
ENV POSTGRES_PASSWORD=postgres1234
ENV POSTGRES_USER=pguser
ENV POSTGRES_DB=starlink
COPY create_table.sql /docker-entrypoint-initdb.d/create_fixtures.sql
