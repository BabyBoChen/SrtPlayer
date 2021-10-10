import datetime
import os
import pathlib
import re
from chardet.universaldetector import UniversalDetector

class SrtLoader():

    def __init__(self):
        self.file_name = ""
        self.file_exist = False
        self.records = []
        self.srt_dur = 0
        self.encoding = "utf-8-sig"
        self.pattern = re.compile(\
            r'(\d+\n)'+\
            r'(\d\d:\d\d:\d\d,\d\d\d)'+\
            r'(?:[ ]*-*>[ ]*)'+\
            r'(\d\d:\d\d:\d\d,\d\d\d)'+\
            r'(?:[ ]*\n)'+\
            r'((?:.+\n)+)'+\
            r'(\n)'\
            ,re.MULTILINE)
        self.srt_ready = False
    
    def get_file_encoding(self, file_path:str):   
        detector = UniversalDetector()
        with open (file_path,'rb') as f:
            for line in f.readlines():
                detector.feed(line)
                if detector.done: break
            detector.close()
        return(detector.result['encoding'])

    def load(self,file_name:str):
        self.file_exist = os.path.exists(file_name)
        if self.file_exist == True:
            try:
                try:
                    srt_file = open(file_name,"r",encoding=self.encoding)
                    srt_file.read()
                    srt_file.seek(0)
                except UnicodeDecodeError:
                    new_encoding = self.get_file_encoding(file_name)
                    srt_file = open(file_name,"r",encoding=new_encoding)
                    srt_file.seek(0)
####################################################################################################
                text = ""
                lines = srt_file.readlines()
                srt_file.close()
                for i in range(len(lines)):
                    line = re.sub(r'\r*\n*\r*','',lines[i])
                    text += line + '\n'
                    if i == len(lines)-1:
                        if line != "":
                            text += '\n'

                temp_rec = []
                matches = re.findall(self.pattern,text)
                for match in matches:

                    subtitle = {'counter':0,'in':0,'out':0,'text':""}
                    subtitle['counter'] = match[0].replace('\n','')
                    in_dt = datetime.datetime.strptime(match[1],r'%H:%M:%S,%f')
                    in_td = datetime.timedelta(hours=in_dt.hour,minutes=in_dt.minute,\
                        seconds=in_dt.second,microseconds=in_dt.microsecond)
                    subtitle['in'] = in_td/datetime.timedelta(milliseconds=1)
                    out_dt = datetime.datetime.strptime(match[2],r'%H:%M:%S,%f')
                    out_td = datetime.timedelta(hours=out_dt.hour,minutes=out_dt.minute,\
                        seconds=out_dt.second,microseconds=out_dt.microsecond)
                    subtitle['out'] = out_td/datetime.timedelta(milliseconds=1)
                    subtitle['text'] = match[3]

                    if len(temp_rec) != 0:
                        if subtitle['out'] > subtitle['in'] and subtitle['in'] >= temp_rec[-1]['out']:
                            temp_rec.append(subtitle)
                    else:
                        if subtitle['out'] > subtitle['in']:
                            temp_rec.append(subtitle)
                    
                if len(temp_rec) == 0:
                    raise Exception

                self.records.clear()
                for record in temp_rec:
                    self.records.append(record)
                self.file_name = pathlib.Path(file_name).name.replace('.srt','')
                self.srt_dur = self.records[-1]['out']
                self.srt_ready = True
                return 1
####################################################################################################
            except Exception as e:
                if __name__ == "__main__":
                    print("can't read the file")
                    print(e)
                return 2
        elif self.file_exist == False:
            if __name__ == "__main__":
                print("file does't exist")
            return 0

if __name__ == "__main__":
    a = SrtLoader()
    a.load("/home/babybo/Videos/Rick and Morty 3x05.srt")
    print(a.records)
