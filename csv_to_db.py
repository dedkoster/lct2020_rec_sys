import argparse

import psycopg2


def main(filename: str, table: str, delimiter: str, batch_size: int):
    conn = psycopg2.connect(
        "postgresql://user:qwerty1234@rc1a-wcmlx33juikool9u.mdb.yandexcloud.net:6432/db")
    cursor = conn.cursor()

    with open(filename, 'r+') as f:
        first_line = f.readline()
        headers = first_line.split(delimiter)

        query = f'create table {table} ('
        query += ','.join([f'"{h}" text' for h in headers])
        query += ');'
        cursor.execute(query)
        conn.commit()

        lines = []
        line = f.readline()
        lines.append(line)

        columns = ','.join([f'"{h}"' for h in headers])

        error_count = 0
        success_count = 0

        while line:
            while len(lines) < batch_size:
                line = f.readline()
                lines.append(line)

            values = ''
            for l in lines:
                values += '('
                fields = l.split(delimiter)

                formatted_fields = []
                for field in fields:
                    ff = field
                    while len(ff) != 0 and (ff[0] == ' ' or ff[-1] == ' '):
                        ff = ff.strip(' ')
                    while len(ff) != 0 and (ff[0] == '"' or ff[-1] == '"'):
                        ff = ff.strip('"')
                    ff = f'\'{ff}\''
                    formatted_fields.append(ff)
                values += ','.join(formatted_fields)
                values += '),'
            values = values.rstrip(',')
            lines = []

            query = f'insert into {table} ({columns}) values {values};'
            try:
                cursor.execute(query)
                conn.commit()
            except BaseException as e:
                error_count += 1
                print(f'Error {error_count}: {e}')
                cursor.close()
                conn.close()
                conn = psycopg2.connect(
                    "postgresql://user:qwerty1234@rc1a-wcmlx33juikool9u.mdb.yandexcloud.net:6432/db")
                cursor = conn.cursor()
            else:
                success_count += 1
                print(f'Success {success_count}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='filename')
    parser.add_argument('-t', dest='table')
    parser.add_argument('-d', dest='delimiter')
    parser.add_argument('-b', dest='batch_size')

    args = parser.parse_args()

    main(args.filename, args.table, args.delimiter, int(args.batch_size))