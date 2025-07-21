import pandas as pd

student_score = "./In-class Practices/Session I-3/Read Custom TXT File/db.txt"

res = []

with open(student_score) as f:
    line = f.readline()
    while line:
        res.append(line.strip().split())
        line = f.readline()

f.close()

db_table = pd.DataFrame(res, columns=['Name', 'Score'])

db_table.info()