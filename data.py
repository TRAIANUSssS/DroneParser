import pickle
import traceback

import pandas as pd

digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
digits_size = digits + ["х", ",", '.']


def openFile():
    return pickle.load(open("all_characteristic_RS_STODAT_v2.pkl", "rb"))


def main():
    data_dict = openFile()

    # columns = []
    # for key in data_dict.keys():
    #     drone_dict = data_dict[key][1]
    #     for dron_key in drone_dict:
    #         if dron_key not in columns:
    #             columns.append(dron_key)

    # for column in columns:
    test = [False] * 604
    columns = ['price', "podves", "brand", "category", "cam", "complectation", "country", "color", "engine_type",
               "folding", "fly_in_3d", "follow_me", "headless_mode", "waypoint", "fpv", "point_of_interest", "go_home",
               "altitude_hold", "auto_takeoff_and_landing", 'size_x', 'size_y', 'size_z', 'flight_range', 'weight',
               'barometer', 'accelerometer', "link"
               ]
    df = pd.DataFrame(columns=columns)

    for index, key in enumerate(data_dict.keys()):
        if index == 0:
            # print(df[])
            print(data_dict[key])

        print(index, key)

        _dict = edit_dict(data_dict[key][1])
        for dict_key in _dict.keys():
            df.loc[index, dict_key] = _dict[dict_key]

        desc = data_dict[key][2].split('\n')
        df.loc[index, 'price'] = data_dict[key][0]
        df.loc[index, 'link'] = key

        for line in desc:
            line = line.replace('x', "х").lower()

            value, norm = find_size(line, index)
            if norm:
                df.loc[index, 'size_x'] = value[0]
                df.loc[index, 'size_y'] = value[1]
                df.loc[index, 'size_z'] = value[2]

            value, norm = find_fly_range(line, index)
            if norm:
                df.loc[index, 'flight_range'] = value

            value, norm = find_wight(line, index)
            if norm:
                df.loc[index, 'weight'] = value

            value, norm = find_barometer(line, index)
            if norm:
                df.loc[index, 'barometer'] = 1

            value, norm = find_accelerometer(line, index)
            if norm:
                df.loc[index, 'accelerometer'] = 1

        if df.loc[index, 'accelerometer'] != 1:
            df.loc[index, 'accelerometer'] = 0

        if df.loc[index, 'barometer'] != 1:
            df.loc[index, 'barometer'] = 0
            # if norm:
            #     # print(value)
            #     test[index] = True
            #     break

            # print(line)
        # break
    # print("Найдено:", sum(test))
    print(df["size_x"][603])
    df.to_excel("test_table_v2.xlsx", index=False)


def edit_dict(old_dict):
    new_dict = {}

    cam = old_dict['Наличие камеры:']
    if cam.count("Есть"):
        cam = cam.replace("Есть", '').replace(",", '')
    else:
        cam = None

    new_dict["podves"] = old_dict['Подвес:']
    try:
        new_dict["brand"] = old_dict['Бренд:']
    except:
        new_dict["brand"] = None
    new_dict["category"] = old_dict['Категория:']
    new_dict["cam"] = cam
    new_dict["complectation"] = old_dict['Тип комплекта:']
    new_dict["country"] = old_dict['Страна производитель:']
    new_dict["color"] = old_dict['Цвет:']
    new_dict["engine_type"] = old_dict['Тип двигателя:']
    new_dict["folding"] = 1 if old_dict['Складной:'] == "Да" else 0
    new_dict["fly_in_3d"] = 1 if old_dict['3D пилотирование :'] == "Да" else 0
    new_dict["follow_me"] = 1 if old_dict['Follow Me (Следуй за мной):'] == "Есть" else 0
    new_dict["headless_mode"] = 1 if old_dict['Headless Mode:'] == "Есть" else 0
    new_dict["waypoint"] = 1 if old_dict['Waypoint (Облет заданных точек):'] == "Есть" else 0
    new_dict["fpv"] = 1 if old_dict['FPV (Онлайн трансляция):'] == "Есть" else 0
    new_dict["point_of_interest"] = 1 if old_dict['Point of Interest (Точка интереса):'] == "Есть" else 0
    new_dict["go_home"] = 1 if old_dict['Возврат домой:'] == "Есть" else 0
    new_dict["altitude_hold"] = 1 if old_dict['Удержание высоты:'] == "Есть" else 0
    new_dict["auto_takeoff_and_landing"] = 1 if old_dict['Автоматический взлет и посадка:'] == "Есть" else 0

    return new_dict


def find_accelerometer(line, index):
    line = line.replace('-', " ")
    if line.count("акселерометр") > 0:
        # print(index, line)
        return True, True
    return None, None


def find_barometer(line, index):
    line = line.replace('-', " ")
    if line.count("barometer") > 0 or line.count("барометр") > 0:
        # print(index, line)
        return True, True
    return None, None


def find_wight(line, index):
    line = line.replace('-', " ")
    split_line = line.split(" ")
    if ("масса" in split_line or "вес" in split_line) and not "батареи" in split_line and not "батареи:" in split_line:
        value = find_value_split(line, "вес", digits)
        if value == '':
            value = find_value_split(line, "масса", digits)
        # value = value.replace(",", '.')
        if value != '':
            try:
                value = float(value.replace(',', "."))
                if line.count('кг'):
                    value *= 1000
                value = int(value)
                # print(index, value, line)
                return value, True
            except:
                print(traceback.format_exc())
    return None, None


def find_fly_range(line, index):
    line = line.replace('-', " ")
    if line.find("дальность") > -1:
        value = find_value(line, "дальность", digits + [',', "."])
        value = value.replace(",", '.')
        if value != '' and value != '.':
            izmerenie = 1

            for line_index in range(line.find(value), len(line)):
                if line[line_index] == 'м':
                    izmerenie = 1
                    break
                elif line[line_index] == 'к':
                    izmerenie = 1000
                    break
            value = int((float(value) * izmerenie))
            if value > 10:
                # print(index, value, line)
                return value, True
    return None, None


def find_time(line, index):
    if line.find("время") > -1 and line.find("полет") > -1:
        if line.count("2,5 ч"):
            value = 150
        else:
            value = find_value(line, "время", digits)
        if value != '':
            if (int(value) > 5 and int(value) < 100) or int(value) == 150:
                print(index, value, line)
                return True
    return False


def find_size(line, index):
    line = line.replace('x', "х")
    if line.find("размер") > -1:
        if (line.count("мм") > 0 or (line.count("см"))) and line.count("сложенном") == 0 and line.count(
                "х") > 0:
            new_line = ''
            for symb in line:
                if symb in digits_size:
                    new_line += symb
            if new_line.count('х') == 2:
                arr = new_line.split('х')
                new_arr = []
                try:
                    for i, a in enumerate(arr):
                        if a.count(',') > 0:
                            a = a[:a.find(',') + 2]
                        a = float(a.replace(',', '.'))

                        if line.count('см') > 0:
                            a *= 10

                        arr[i] = int(a)

                    new_arr = arr
                    # print(index, new_arr, line)
                    return new_arr, True
                except:
                    pass
                    # print(traceback.format_exc())
                    return None, None
            # print(index, arr, line)
    return None, None


def find_value(line, word, _dict):
    start_index = line.find(word)
    digit_line = ''
    digit = False

    for i in range(start_index, len(line)):
        symbol = line[i]
        if symbol in _dict:
            digit_line += symbol
            digit = True
        else:
            if digit:
                break
    return digit_line


def find_value_split(line, word, _dict):
    words = line.split(" ")
    try:
        start_index = words.index(word)
        digit_line = ''
        digit = False

        for index in range(start_index, len(words)):
            if words[index][0] in _dict:
                word = ''
                for symbol in words[index]:
                    if symbol in _dict + [',', "."]:
                        word += symbol
                return word
    except:
        pass

    return ''

    # df = pd.DataFrame(columns=columns)
    #
    # for index, key in enumerate(data_dict.keys()):
    #     drone_dict = data_dict[key]
    #     for drone_key in drone_dict:
    #         df.loc[index, drone_key] = drone_dict[drone_key]
    #         # print(drone_dict[drone_key])
    #
    # df.to_excel("table.xlsx", index=False)
