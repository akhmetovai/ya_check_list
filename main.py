import os
import datetime
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import clickhouse_connect


app = FastAPI()
ch_client = clickhouse_connect.get_client(host='localhost', port=18123, username='default')


@app.post("/upload_ddl/")
async def create_upload_file(files: UploadFile):
    lines = files.file.readlines()
    filename = files.filename.split('.')[0].replace('DDL_', '')
    header = 'column,check_type,data_type,description,options'
    columns_ddl = []

    for line in lines:
        line = line.decode("utf-8").strip()
        if line != header:
            column, _, data_type, _, _ = line.split(',')
            columns_ddl.append((column, data_type))
    
    ch_ddl_0 = f"""
    DROP TABLE IF EXISTS {filename};"""
    ch_ddl_1 = f"""
    CREATE TABLE {filename}
    (
    {
        ',$$$'.join(['`' + col_name + '`' + ' ' + data_type for col_name, data_type in columns_ddl])
    }
    )
    ENGINE = MergeTree
    PRIMARY KEY {columns_ddl[0][0]}
    """.replace('$$$', '\n')

    ch_client.command(ch_ddl_0)
    ch_client.command(ch_ddl_1)
    return {'filename': files.filename}


@app.post("/upload_data/")
async def create_upload_file(files: UploadFile):
    lines = files.file.readlines()
    tablename = files.filename.split('.')[0].replace('Data_', '')
    data = []

    for line in lines:
        line = line.decode("utf-8").strip().split(',')
        if line[0] == 'response_id':
            column_names = line
        else:
            for idx, col in enumerate(line):
                if col == '':
                    line[idx] = 'NULL'
            year, month, day = map(int, line[2].strip().split('-'))
            line[2] = datetime.date(year, month, day)
            line[21] = datetime.datetime.now()
            line[23] = datetime.datetime.now()
            data.append(line)
    
    ch_client.insert(tablename, data, column_names=column_names)
    return {'filename': files.filename}


@app.get("/")
async def main():
    content = """
        <body>
            <p>upload_ddl</p>
            <form action="/upload_ddl/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
            <p>upload_data</p>
            <form action="/upload_data/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)
