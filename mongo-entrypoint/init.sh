#!/usr/bin/env bash
echo "Creating mongo users"
mongo admin --host localhost -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --eval "db.createUser({user: '$(echo $DB_USER)', pwd: '$(echo $DB_PASS)', roles: [{role: 'readWrite', db: 'waifu'}]});"
echo "Done"