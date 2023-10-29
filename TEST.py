import sqlite3 as sq


print('start')

with sq.connect(r"\\SRV2\data_base\patient_data_base.db") as conn:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM patient_data")
    total_i = cur.fetchall()

print('selected')
total = 0
for i in total_i:
    total += 1

print('total count ', total)
