from functools import cmp_to_key

import pandas as pd
import os

output_path = "../../outputs"
error_type = ["True", "Wrong COT", "Wrong syntax", "Wrong calculation", "Wrong understanding", "Information Deviation", "Else"]

def cmp(a, b):
    return int(a[0].split('.')[0]) - int(b[0].split('.')[0])

def convert_to_csv():
    for i in os.listdir(output_path):
        file = os.path.join(output_path, i, "eval.csv")
        try:
            with open(file) as f:
                tmp = []
                for line in f:
                    line = line.split(";")
                    if len(line) < 4:
                        continue
                    for idx in range(len(line)):
                        line[idx] = line[idx].strip()
                    tmp.append(line)
                    tmp = sorted(tmp, key=cmp_to_key(cmp))

                res = pd.DataFrame.from_records(tmp)
                res.columns = ["name", "result", "error_type", "description"]
                res.to_csv(os.path.join(output_path, i, "eval_converted.csv"), index=False)
        except IOError as e:
            continue


def token_used_count(path):
    sum = 0
    for file in os.listdir(path):
        if not file.endswith(".json"):
            continue
        import json
        with open(os.path.join(path, file), "r") as f:
            data = json.load(f)
            if data['token_used'] is None:
                sum += 0
            else:
                sum += data["token_used"]
    return sum


def count_errors():
    result = pd.DataFrame()
    for dir in os.listdir(output_path):
        file_path = os.path.join(output_path, dir, "eval_converted.csv")
        if not os.path.exists(file_path):
            continue
        dict = {}
        for e in error_type:
            dict[e] = 0
        dict["token_used"] = token_used_count(os.path.join(output_path, dir))
        file = pd.read_csv(file_path)
        # print(file.shape)
        for i in range(file.shape[0]):
            if file.iloc[i, 1]:
                dict["True"] += 1
            else:
                wrong_name = file.iloc[i, 2]
                dict[wrong_name] += 1
        result[dir] = dict

    result = result.T
    result["total_questions"] = result.sum(axis=1)
    result["total_questions"] -= result["token_used"]
    result["Execution Accuracy"] = result["True"] / result["total_questions"]
    # print(result)
    result.to_excel("../../outputs/result_count.xlsx")

if __name__ == "__main__":
    # 重跑完eval后需要打开convert_to_csv的注释，手动校验eval_converted.csv后则直接使用count_errors
    # convert_to_csv()
    count_errors()
    print("Done")