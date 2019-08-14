# -*- coding: utf-8 -*-

import json


def split_task(tasks: [], count: int):
    n = int(len(tasks) / count)
    return [tasks[i:i + n] for i in range(0, len(tasks), n)]


if __name__ == "__main__":
    __SPLIT__ = 16

    # Task Split

    # with open("./data/bjd2.geojson", "r", encoding="utf-8") as fp:
    #     data = json.load(fp)["features"]
    #
    #     sets = split_task(data, __SPLIT__)
    #
    #     for i in range(__SPLIT__):
    #         with open("./data/bjd2.{0}.json".format(i), "w", encoding="utf-8") as sfp:
    #             json.dump(sets[i], sfp, ensure_ascii=False, indent=2)

    # Task Merge
    result = []
    for i in range(__SPLIT__):
        with open("./data/bjd2.{0}.out.json".format(i), "r", encoding="utf-8") as sfp:
            result += json.load(sfp)

    with open("./data/bjd.json", "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
