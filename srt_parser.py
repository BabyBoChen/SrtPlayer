import datetime
import re

records = [{'counter':0,'in':0,'out':0,'text':""}]
srt_dur = records[-1]['out']

def main(path_to_file:str):
    global srt_dur
    with open(path_to_file,"r",encoding="utf-8-sig") as srt_file:
        records.clear()
        line = []
        for i in srt_file:
            if i != '\n':
                line.append(i)
            if i == '\n':
                subtitle = {'counter':0,'in':0,'out':0,'text':""}
                try:
                    for j in range(len(line)):
                        if j == 0:
                            subtitle['counter'] = int(line[j])
                        if j == 1:
                            in_datetime_string = re.split(r'\s-->\s|\n',line[j])[0]
                            in_dt = datetime.datetime.strptime(in_datetime_string,r'%H:%M:%S,%f')
                            in_td = datetime.timedelta(hours=in_dt.hour,minutes=in_dt.minute,seconds=in_dt.second,microseconds=in_dt.microsecond)
                            subtitle['in'] = int(in_td/datetime.timedelta(milliseconds=1))
                            out_datetime_string = re.split(r'\s-->\s|\n',line[j])[1]
                            out_dt = datetime.datetime.strptime(out_datetime_string,r'%H:%M:%S,%f')
                            out_td = datetime.timedelta(hours=out_dt.hour,minutes=out_dt.minute,seconds=out_dt.second,microseconds=out_dt.microsecond)
                            subtitle['out'] = int(out_td/datetime.timedelta(milliseconds=1))
                        if j > 1:
                            subtitle['text'] += line[j]
                    records.append(subtitle)
                except Exception as e:
                    print(e)
                line.clear()
    srt_dur = records[-1]['out']

if __name__ == "__main__":
    pass