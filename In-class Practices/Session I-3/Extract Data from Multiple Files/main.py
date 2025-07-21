import glob
import pandas as pd

# Download The bbcsport Dataset via http://mlg.ucd.ie/datasets/bbc.html
base_path = "./In-class Practices/Session I-3/Extract Data from Multiple Files/bbcsport/"
topic = ['athletics','cricket','football','rugby','tennis']

def read_and_split_files(filename):
    with open(filename,'r',encoding='latin-1') as f:
        contents = f.readlines()
        contents = list(map(str.strip,contents))
        contents = list(filter(None, contents))
    return contents

def get_data_from_files(_path, _topic):
    files = glob.glob(f"{_path}{_topic}/*.txt")
    titles = []
    subtitles = []
    bodies = []

    for f in files:
        lines = read_and_split_files(f)
        titles.append(lines[0])
        subtitles.append(lines[1])
        bodies.append(' '.join(lines[2:]))

    return pd.DataFrame({
        'topic': _topic,
        'title': titles,
        'subtitle': subtitles,
        'body': bodies
    })

db_bbcsport = pd.concat([get_data_from_files(base_path, t) for t in topic])

print(db_bbcsport.head())
print(db_bbcsport.shape)