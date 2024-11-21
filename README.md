
# Modme Clone API

[![codecov](https://codecov.io/github/akhroruz/modme_clone/branch/master/graph/badge.svg?token=2E37XZAA63)](https://codecov.io/github/akhroruz/modme_clone)

## TODO - Talab qilinadi

1. [x] maxsus admin panel
2. [x] sentry
3. [x] github
4. [ ] ruxsatlar (permissions):
    - CEO - barcha ruxsatlar
    - Administrator - (CRUD) student, (CRUD) course, (CRUD) teacher, (CRUD) room, (CRUD) lead, (CRUD) holiday, (CRUD)
      archive, o‘z branchi
    - Branch direktori - (CRUD) student, (CRUD) course, (CRUD) teacher, (CRUD) room, (CRUD) lead, (CRUD) holiday, (CRUD)
      archive, o‘z branchi
    - O‘qituvchi - dars kunlari, o‘z guruhlari
    - Cheklangan administrator - (CRUD) teacher, (CRUD) course, (CRUD) group, o‘z branchi
    - Marketolog - (CRUD) leads
    - Kassa xodimi - (CRUD) students, hisob-kitoblar
5. [x] test (pytest coverage 80% ^)
6. [ ] docker/docker compose
7. [x] elasticsearch
8. [ ] xavfsizlik (security)
9. [x] GitHub actions
10. [ ] server

## Talab qilinmaydi

1. [ ] cache
2. [ ] celery
3. [ ] redis
4. [ ] rabbitmq
5. [ ] cron
6. [x] flake8

## Makefile

- ```make test``` - pytest ni coverage html bilan ishga tushirish
- ```make mig``` - migratsiyalar yaratish va migratsiya qilish
- ```make unmig``` - barcha migratsiya fayllarini o‘chirish
- ```make remig``` - hammasini biryo‘la bajarish
- ```make admin``` - superuser (admin) yaratish
- ```make load``` - barcha ma'lumotlarni yig‘ish
- ```make faker``` - ma'lumotlar bazasida tasodifiy soxta ma'lumotlar yaratish
- ```make search_index``` - Elasticsearch index va mapping yaratish va to‘ldirish
- ```make ram``` - ma'lumotlar bazasidagi barcha jadvalni o‘chirish

![](https://codecov.io/github/akhroruz/modme_clone/branch/master/graphs/sunburst.svg?token=2E37XZAA63)
