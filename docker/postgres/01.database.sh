echo "***** Creating user and database *****"
psql <<- EOSQL
    CREATE DATABASE model_deprecater;
    CREATE USER model_deprecater;
    ALTER USER model_deprecater CREATEDB;
    GRANT ALL PRIVILEGES ON DATABASE model_deprecater TO model_deprecater;
    ALTER USER model_deprecater WITH SUPERUSER;
EOSQL
