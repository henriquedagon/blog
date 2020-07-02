#!/bin/bash

# sudo -u postgres psql postgres -c "ALTER USER postgres PASSWORD 'postgres123++';"

psql -U postgres -c "CREATE DATABASE BLOG;"

psql -U postgres -d blog -a -f  create_blog_tables.sql

###########

# psql -v ON_ERROR_STOP=1 --username "POSTGRES_USER" --dbanme "POSTGRES_DB" << -EOSQL

#     --Database Blog
#     --CREATE DATABASE BLOG;

#     -- Posts table
#     CREATE TABLE IF NOT EXISTS POSTS
#     (
#         ID SERIAL PRIMARY KEY, 
#         TITLE VARCHAR(100) NOT NULL, 
#         POST VARCHAR(1000) NOT NULL, 
#         CATEGORIES VARCHAR(1000) NOT NULL, 
#         IMG_FILENAME VARCHAR(1000) NOT NULL, 
#         IMAGE_NAME VARCHAR(1000) NOT NULL,
#         AUTHOR VARCHAR(100) NOT NULL, 
#         DATE VARCHAR(10) NOT NULL
#     );

#     -- Users table
#     CREATE TABLE IF NOT EXISTS USERS
#     (
#         USR VARCHAR(100) PRIMARY KEY, 
#         PASS VARCHAR(100) NOT NULL, 
#         GRP INTEGER NOT NULL
#     );
#     INSERT INTO USERS
#     (USR, PASS, GRP) VALUES
#     ('usuario','1234', 1),
#     ('administrador','12345', 2);

#     -- Groups table
#     CREATE TABLE IF NOT EXISTS GROUPS_DESCRIPTOR
#     (
#         GRP INTEGER PRIMARY KEY, 
#         DESCRIPTION VARCHAR(100) NOT NULL
#     );
#     INSERT INTO GROUPS_DESCRIPTOR
#     (GRP, DESCRIPTION) VALUES
#     (1, 'User'),
#     (2, 'Admin');

# EOSQL
