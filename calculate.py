# -*- coding: utf-8 -*-

from shapely.geometry import GeometryCollection, shape

from multiprocessing import Pool
import json


def convert(idx: int):
    with open("./data/bjd2.{0}.json".format(idx), "r", encoding="utf-8") as fp:
        data = json.load(fp)

    result = []
    for item in data:
        geom = shape(item["geometry"])
        result.append({
            "properties": item["properties"],
            "location": list(*geom.centroid.coords),
            "bounds": [[*geom.bounds[:2]], [*geom.bounds[:2]]],
            "geometry": geom.simplify(0.0005, False).to_wkt()
        })

    with open("./data/bjd2.{0}.out.json".format(idx), "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)


def convert2():
    with open("./data/hjd.geojson", "r", encoding="utf-8") as fp:
        data = json.load(fp)

    data = data["features"]

    result = []
    for item in data:
        geom = shape(item["geometry"])
        result.append({
            "properties": item["properties"],
            "location": list(*geom.centroid.coords),
            "bounds": [[*geom.bounds[:2]], [*geom.bounds[:2]]],
            "geometry": geom.simplify(0.0005, False).to_wkt()
        })

    with open("./data/hjd.json", "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    convert2()
    # with Pool(8) as p:
    #    print(p.map(convert, range(16)))