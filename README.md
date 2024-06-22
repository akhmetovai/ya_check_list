# Check-list prototype

## Brief instruction:

0. pyenv + poetry, poetry install
1. clickhouse:
    * docker volume create clickhouse_vol
    * docker network create app_check_list
    * docker run --rm -d \
    -p 18123:8123 \
    -p 19000:9000 \
    --name my_clickhouse \
    --net=app_check_list \
    -v clickhouse_vol:/var/lib/clickhouse \
    clickhouse/clickhouse-server
    * http://127.0.0.1:18123/play
2. checklist_service:
    * fastapi dev main.py
    * http://127.0.0.1:8000/ - сервис для загрузки DDL и данных.
        * /upload_ddl/
        * /upload_data/
3. datalens:
    * git clone https://github.com/datalens-tech/datalens && cd datalens
    * add app_check_list network to docker-compose
    * HC=1 UI_PORT=8081 docker compose up
    * add connection to clickhouse (host for clickhouse from docker nestat ls)

[Гугл-табличка](https://docs.google.com/spreadsheets/d/1tQhqOeMMH9dXLzMcqUyfH2nVD4ZEN54oRDjIspBAmCo/edit?hl=ru&pli=1&gid=369581489#gid=369581489) с описанием типов данных, карт отображения и примером заполнения.

* DDL_dict: Описание возможных типов данных для чек-листа
* DDL_CheckList_1: Описание DDL для таблицы CheckList_1
* Data_CheckList_1: Данные для таблицы CheckList_1

Данные положить в папку data/

Что касается сервиса для загрузки данных максимально костыльно, но показывает примерно будущую логику 