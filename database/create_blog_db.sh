sudo -u postgres psql postgres -c "ALTER USER postgres PASSWORD 'postgres123++';"

sudo -u postgres psql postgres -c "CREATE DATABASE BLOG;"

sudo -u postgres psql -d blog -a -f  create_blog_tables.sql
