import os
import json
import csv

class FileStuff:
    @staticmethod
    def does_path_exist(filename):
        return os.path.exists(filename)

    @staticmethod
    def write_text_file(filename, content):
        mode = 'a' if FileStuff.does_path_exist(filename) else 'w'
        dirpath = os.path.dirname(filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(filename, mode, encoding='utf-8') as f:
            match content:
                case list() | tuple() if all(isinstance(item, str) for item in content):
                    f.writelines(content)
                case list() | tuple() if not all(isinstance(item, str) for item in content):
                    f.writelines([str(item) + '\n' for item in content])
                case str():
                    f.write(content + '\n')
                case dict():
                    for key, value in content.items():
                        f.write(f"{key}: {value}\n")
                case _:
                    f.write(str(content) + '\n')

    @staticmethod
    def read_text_file(filename, to="list_string"):
        if not FileStuff.does_path_exist(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, 'r', encoding='utf-8') as f:
            if to == "list_string":
                return f.read().split()
            elif to == "list_int":
                return [int(x) for x in f.read().split()]
            elif to == "list_float":
                return [float(x) for x in f.read().split()]
            elif to == "raw_dictionary":
                return {i: line.strip() for i, line in enumerate(f.readlines())}
            elif to == "formatted_dictionary":
                return {
                    line.split(':')[0].strip(): line.split(':')[1].strip()
                    for line in f.readlines()
                    if ':' in line
                }
            else:
                raise ValueError(f"Unknown 'to' argument: {to}")

    @staticmethod
    def save_to_csv(filename, data):
        mode = 'a' if FileStuff.does_path_exist(filename) else 'w'
        dirpath = os.path.dirname(filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(filename, mode, newline='', encoding='utf-8') as f:
            if isinstance(data, dict):
                fieldnames = list(data.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if mode == 'w':
                    writer.writeheader()
                writer.writerow(data)
            elif isinstance(data, (list, tuple)):
                writer = csv.writer(f)
                writer.writerow(data)
            else:
                writer = csv.writer(f)
                writer.writerow([data])

    @staticmethod
    def read_csv_file(filename, to="list_string"):
        if not FileStuff.does_path_exist(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, 'r', encoding='utf-8') as f:
            if to == "dictionary":
                reader = csv.DictReader(f)
                return [row for row in reader]
            f.seek(0)
            reader = csv.reader(f)
            if to == "list_string":
                return [row for row in reader]
            elif to == "list_int":
                return [[int(item) for item in row] for row in reader]
            elif to == "list_float":
                return [[float(item) for item in row] for row in reader]
            elif to == "raw_dictionary":
                return [{i: item for i, item in enumerate(row)} for row in reader]
            else:
                raise ValueError(f"Unknown 'to' argument: {to}")

    @staticmethod
    def write_json_file(filename, data):
        dirpath = os.path.dirname(filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        if FileStuff.does_path_exist(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            if isinstance(existing, list):
                existing.append(data)
            else:
                existing = [existing, data]
        else:
            existing = data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=4)

    @staticmethod
    def read_json_file(filename):
        if not FileStuff.does_path_exist(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


class DemoRunner:
    filename = "demo"
    demo_number = 0
    filename = f"{filename}_{demo_number}"

    @classmethod
    def change_filename(cls, name):
        cls.filename = f"{name}_{cls.filename.split('_')[1]}"

    @classmethod
    def update_demo_number(cls):
        cls.filename = f"{cls.filename.split('_')[0]}_{cls.demo_number}"

    def __init__(self, folder="current"):
        self.path = folder
        if self.path != "current":
            self.path = os.path.join(os.getcwd(), self.path)
            if not os.path.exists(self.path):
                os.makedirs(self.path)

    def update_filepath(self):
        if self.path != "current":
            self.filepath = os.path.join(self.path, DemoRunner.filename)
        else:
            self.filepath = DemoRunner.filename

    def new_demo(self):
        DemoRunner.demo_number += 1
        DemoRunner.update_demo_number()
        self.update_filepath()
        self.text_path = self.filepath + ".txt"
        self.csv_file = self.filepath + ".csv"
        self.json_file = self.filepath + ".json"
        print(f"\nRunning demo {DemoRunner.demo_number} with new filename: {DemoRunner.filename}")

    def demo(self, name="demo"):
        if name != "demo":
            DemoRunner.change_filename(name)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, ["List String Line 1\n", "List String Line 2\n", "List String Line 3\n"])
        list_items = FileStuff.read_text_file(self.text_path, "list_string")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        print("Demo List after list of strings:", list_items)
        print("Demo Raw Dictionary after list of strings:", dict_stuff)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, ("Tuple String Line 1\n", "Tuple String Line 2\n", "Tuple String Line 3\n"))
        list_items = FileStuff.read_text_file(self.text_path, "list_string")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        print("Demo List after Tuple:", list_items)
        print("Demo Raw Dictionary after Tuple:", dict_stuff)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, [1, 2, 3])
        list_items = FileStuff.read_text_file(self.text_path, "list_int")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        list_str = FileStuff.read_text_file(self.text_path, "list_string")
        print("Demo List after List Int:", list_items)
        print("Demo Raw Dictionary after List Int:", dict_stuff)
        print("Demo List String after List Int:", list_str)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, (4.4, 5.5, 6.6))
        list_items = FileStuff.read_text_file(self.text_path, "list_float")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        list_str = FileStuff.read_text_file(self.text_path, "list_string")
        print("Demo List after Tuple Float:", list_items)
        print("Demo Raw Dictionary after Tuple Float:", dict_stuff)
        print("Demo List String after Tuple Float:", list_str)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, {"key1": "value1", "key2": "value2"})
        list_items = FileStuff.read_text_file(self.text_path, "formatted_dictionary")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        list_str = FileStuff.read_text_file(self.text_path, "list_string")
        print("Demo List after Dictionary:", list_items)
        print("Demo Raw Dictionary after Dictionary:", dict_stuff)
        print("Demo List String after Dictionary:", list_str)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, "Single String Line as input")
        list_items = FileStuff.read_text_file(self.text_path, "list_string")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        print("Demo List after Single String Line:", list_items)
        print("Demo Raw Dictionary after Single String Line:", dict_stuff)

        self.new_demo()
        FileStuff.write_text_file(self.text_path, 123.45)
        list_str = FileStuff.read_text_file(self.text_path, "list_string")
        list_float = FileStuff.read_text_file(self.text_path, "list_float")
        dict_stuff = FileStuff.read_text_file(self.text_path, "raw_dictionary")
        print("Demo List String after Float:", list_str)
        print("Demo List Float after Float:", list_float)
        print("Demo Raw Dictionary after Float:", dict_stuff)

        self.new_demo()
        FileStuff.save_to_csv(self.csv_file, ["Column1", "Column2", "Column3"])
        list_items = FileStuff.read_csv_file(self.csv_file, "list_string")
        dict_stuff = FileStuff.read_csv_file(self.csv_file, "raw_dictionary")
        print("Demo List after CSV List String:", list_items)
        print("Demo Raw Dictionary after CSV List String:", dict_stuff)

        self.new_demo()
        FileStuff.save_to_csv(self.csv_file, {"Column1": "Value1", "Column2": "Value2"})
        list_items = FileStuff.read_csv_file(self.csv_file, "list_string")
        dict_stuff = FileStuff.read_csv_file(self.csv_file, "dictionary")
        print("Demo List after CSV Dictionary:", list_items)
        print("Demo Dictionary after CSV Dictionary:", dict_stuff)

        self.new_demo()
        FileStuff.write_json_file(self.json_file, {"key1": "value1", "key2": "value2"})
        json_data = FileStuff.read_json_file(self.json_file)
        print("Demo JSON after writing JSON file:", json_data)


if __name__ == "__main__":
    demo1 = DemoRunner("experiments1")
    demo1.demo()
    demo2 = DemoRunner("experiments2")
    demo2.demo("CreatedByDemo2")
    demo1.change_filename("ChangedByDemo1")
    demo2.demo()
