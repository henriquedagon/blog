FROM postgres

# MAINTAINER Henrique Dias "henrique-90@poli.ufrj.br"

ENV POSTGRES_PASSWORD postgres123++
ENV POSTGRES_DB blog

COPY ./create_blog_tables.sql /docker-entrypoint-initdb.d



