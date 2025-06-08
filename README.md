

## usefull
- работа с hh - https://www.youtube.com/watch?v=E4Nd-_A4me4, https://t.me/goingtoit + related
- работа с resume - https://www.youtube.com/watch?v=9hiYCnydWV4, https://www.youtube.com/watch?v=RUp2HwofyhI + related
- ошибки поиска работы - https://www.youtube.com/watch?v=cSPAiV00_94

## links
- https://solvit.space/
- https://artemshumeiko.zenclass.ru/student/courses/937c3a35-998d-4420-bd3d-9f64db23be23/lessons/18c89b4f-19e3-481f-be49-b9eda822a430
- https://github.com/artemonsh/backend-course/
- https://t.me/+Oc5DtSUQsKwyOWEy
- https://t.me/+3OPzvJ2qmWM2OWRi
- t.me/artemshumeiko
- https://www.youtube.com/@artemshumeiko
- https://s1.sharewood.co/threads/michael-yin-polnoe-rukovodstvo-po-celery-i-fastapi-2022.389982/ - https://cloud.mail.ru/public/hDa4/Rpz7fHKda
- https://s1.sharewood.co/threads/jan-giacomelli-masshtabiruemye-prilozhenija-fastapi-na-aws-2022.389983/ - https://cloud.mail.ru/public/oXco/reQwBzLkf
- https://s1.sharewood.co/threads/michael-herman-razrabotka-cherez-testirovanie-s-pomoschju-fastapi-i-docker-2021.182856/ - https://cloud.mail.ru/public/oeeW/9SecyduZR
- https://hackersandslackers.com/async-requests-aiohttp-aiofiles/
- https://mvp.ed-trees.ru/skill_levels/670/



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
