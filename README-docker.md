### Удалить все контейнеры
docker rm -f $(docker ps -aq)

### Удалить все образы
docker rmi -f $(docker images -q)

### Удалить все тома
docker volume rm $(docker volume ls -q)

### Удалить все пользовательские сети
docker network rm $(docker network ls -q | grep -v 'bridge\|host\|none')

### Удалить весь кэш сборки
docker builder prune --all --force

### Также можно финально подчистить:
docker system prune -a --volumes --force
