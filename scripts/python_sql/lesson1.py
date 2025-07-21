from db_connection import get_connection

conn = get_connection()

sql = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(255), phone VARCHAR(255));"
# Запрос выполняется через создание объекта курсора
cursor = conn.cursor()
cursor.execute(sql)
cursor.close()  # в конце закрывается

sql2 = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789');"
cursor = conn.cursor()
cursor.execute(sql2)
cursor.close()

sql3 = "SELECT * FROM users;"
cursor = conn.cursor()
# Указатель на набор данных в памяти СУБД
cursor.execute(sql3)
for row in cursor:
    print(row)
cursor.close()

conn.commit()  # Коммитим, т.е. сохраняем изменения в БД
conn.close()  # Соединение нужно закрыть