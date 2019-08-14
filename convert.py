# -*- coding: utf-8 -*-

import shapefile
from pyproj import Proj, transform
import json


def convert_shp(path: str):
    sf = shapefile.Reader(path, encoding="euc-kr")

    fields = sf.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []
    for sr in sf.shapeRecords():
        atr = dict(zip(field_names, sr.record))

        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    with open(path+".geojson", "w", encoding="utf-8") as fp:
        data = {
            "type": "FeatureCollection",
            "features": buffer
        }
        json.dump(data, fp, ensure_ascii=False)


if __name__ == "__main__":
    file_idx = [11, 26, 27, 28, 29, 30, 31, 36, 41, 42, 43, 44, 45, 46, 47, 48, 50]

    # for idx in file_idx:
    #     convert_shp("./data/bjd/LSMD_ADM_SECT_UMD_%d"%idx)

    # merging

    # with open("./data/bjd.geojson", "w", encoding="utf-8") as fp:
    #     buffer = []
    #
    #     for idx in file_idx:
    #         with open("./data/bjd/LSMD_ADM_SECT_UMD_%d.geojson"%idx, "r", encoding="utf-8") as fp2:
    #             data = json.load(fp2)
    #             buffer += data["features"]
    #
    #     data = {
    #         "type": "FeatureCollection",
    #         "features": buffer
    #     }
    #
    #     json.dump(data, fp, ensure_ascii=False)

    # reprojection

    original = Proj(init="epsg:5179")
    destination = Proj(init="epsg:4326")

    with open("./data/bjd.geojson", "r", encoding="utf-8") as fp:
        data = json.load(fp)
        features = data["features"]
        total = len(features)
        print(total)

        cnt = 0
        for feature in features:
            cnt += 1
            if cnt%100 == 0:
                print("{0} / {1}".format(cnt, total))

            geom = feature["geometry"]

            if geom["type"] == "Polygon":
                polygons = geom["coordinates"]

                geom["coordinates"] = [
                    [
                        list(transform(original, destination, points[0], points[1]))
                        for points in poly
                    ]
                    for poly in polygons
                ]

            elif geom["type"] == "MultiPolygon":
                multipolygons = geom["coordinates"]

                geom["coordinates"] = [
                    [
                        [
                            list(transform(original, destination, points[0], points[1]))
                            for points in poly
                        ]
                        for poly in polygons
                    ]
                    for polygons in multipolygons
                ]
            else:
                raise Exception("Unexpected type: "+geom["type"])
            print(feature)

        with open("./data/bjd2.geojson", "w", encoding="utf-8") as fp2:
            json.dump(data, fp2, ensure_ascii=False)