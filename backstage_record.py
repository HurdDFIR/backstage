from datetime import datetime
import logging
import json

log = logging.getLogger()

class Record():
    def __init__(self, file: str):
        self.name = file
        self.backstage_dict = self.load(file)

    def load(self, file):
        with open(file, mode='r', encoding='utf-16-le') as f:
            return json.load(f)


    def convert_date(self, dt):
        EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
        HUNDREDS_OF_NANOSECONDS = 10000000

        if dt == 0 or dt is None:
            return None
        else:
            t = datetime.utcfromtimestamp((dt - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)
            return t.strftime("%Y-%m-%d %H:%M:%S")


    def parse(self):
        new_data = dict()
        new_data_list = list()
        folders = list()
        files = list()
        new_data["SourceFile"] = self.name
        for key, value in self.backstage_dict.items():
            if key == "LastReadOn" or key == "LastModified":
                new_data[key] = self.convert_date(value)
            
            elif key == "Folders":
                if len(value) > 0:
                    for folder in value:
                        folders.append(value)

            elif key == "Files":
                if len(value) > 0:
                    for file in value:
                        files.append(value)

            elif key == "Metadata":
                for key,value in value.items():
                    new_data[key] = value
            
            else:
                new_data[key] = value
   
        fieldnames = []
        nofiles = False
        nofolders = False

        if len(files) > 0:
            for file in files:
                for entry in file:
                    for k in entry.keys():
                        if k not in fieldnames:
                            fieldnames.append(k)
        else:
            nofiles = True

        if len(folders) > 0:
            for folder in folders:
                for entry in folder:
                    for k in entry.keys():
                        if k not in fieldnames:
                            fieldnames.append(k)
        else: 
            nofolders = True

        if not nofiles:
            for file in files:
                for entry in file:
                    data = dict()
                    data.update(new_data)
                    for field in fieldnames:
                        if field not in entry.keys():
                            data[field] = None
                        else:
                            if field == "LastModified":
                                data[field] = self.convert_date(entry[field])
                            else:
                                data[field] = entry[field]

                    data['folder'] = False
                    new_data_list.append(data)
        
        if not nofolders:
            for folder in folders:
                for entry in folder:
                    data = dict()
                    data.update(new_data)
                    for field in fieldnames:
                        if field not in entry.keys():
                            data[field] = None
                        else:
                            if field == "LastModified":
                                data[field] = self.convert_date(entry[field])
                            else:
                                data[field] = entry[field]

                    data['folder'] = True
                    new_data_list.append(data)

        return [i for n, i in enumerate(new_data_list) if i not in new_data_list[n + 1:]]
    