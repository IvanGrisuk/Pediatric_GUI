import sqlite3 as sq

local_data = dict()

print("\\\\192.168.19.1\\database\\examination_data_base.db")

with sq.connect(database="./srv_data_base/examination_data_base.db") as conn:
    cur = conn.cursor()
    cur.execute(f"SELECT date_time, doctor_name, status, LN_type, patient_info, "
                f"examination_text, examination_key, add_info "
                f"FROM examination")
    examination_loc = cur.fetchall()

for examination in examination_loc:
    (date_time, doctor_name, status, LN_type,
     patient_info, examination_text,
     examination_key, add_info) = examination
    if len(date_time.split(':')) != 3:
        date_time += ":00"

    local_data[f"{date_time}__{doctor_name}__{patient_info}__{examination_text}"] = (
        date_time, doctor_name, status, LN_type,
        patient_info, examination_text,
        examination_key, add_info
    )

edit_data = list()

for examination in local_data:
    # (date_time, doctor_name, status, LN_type,
    #  patient_info, examination_text,
    #  examination_key, add_info) = local_data.get(examination)
    edit_data.append(local_data.get(examination))

print(len(edit_data))
for i in edit_data:
    print(i)

with sq.connect(database="./srv_data_base/examination_data_base.db") as conn:
    cur = conn.cursor()
    cur.execute("DELETE from examination")
    cur.executemany("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)", edit_data)

print('finish')


