import sqlite3


def get_con_cur():
    con = sqlite3.connect("auto_ria.db")
    cur = con.cursor()

    return con, cur


def get_site_ids():
    con, cur = get_con_cur()
    res = cur.execute('SELECT site_id FROM cars WHERE status = "on sale" ORDER BY id')
    res = res.fetchall()
    site_ids = [el[0] for el in res]

    return site_ids


def insert_into_cars(list_of_values: list):
    con, cur = get_con_cur()
    cur.executemany("INSERT INTO cars (site_id, price) VALUES (?, ?)", list_of_values)
    con.commit()


def update_data(field: str, new_value, id_num: str):
    con, cur = get_con_cur()
    cur.execute(f'UPDATE cars SET {field} = {new_value} WHERE site_id = "{id_num}";')
    con.commit()


def get_data_of_single_id(id_num: str):
    con, cur = get_con_cur()
    res = cur.execute(f'SELECT price FROM cars WHERE site_id = "{id_num}"')

    return res.fetchone()[0]


def get_all_data():
    con, cur = get_con_cur()
    res = cur.execute('SELECT * FROM cars;')

    return res.fetchall()
