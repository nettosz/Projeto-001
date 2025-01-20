

echo "killing old docker processes"
docker-compose rm -fs dataview

echo "building docker containers"
docker-compose up --build -d dataview

