import json
from os import path

SPIDER_DATA_FOLDER = "spider_data"
INPUT_JSON_FILENAME = "dev.json"
OUTPUT_JSON_FILENAME = "dev.stats.json"

if __name__ == "__main__":
    """
    Compute some simple stats for the given json training data file
    """
    with open(path.join(SPIDER_DATA_FOLDER, INPUT_JSON_FILENAME), "r") as input_json:
        train_data = json.load(input_json)

    dbs = {}
    query_count = 0

    for entry in train_data:
        db = entry["db_id"]
        if db in dbs:
            db_stat = dbs[db]
        else:
            db_stat = {"name": db, "query_count": 0}
            dbs[db] = db_stat
        db_stat["query_count"] += 1
        query_count += 1

    dbs_list = list(dbs.values())
    dbs_list.sort(key=lambda x: x["query_count"], reverse=True)

    with open(path.join(SPIDER_DATA_FOLDER, OUTPUT_JSON_FILENAME), "w") as output_json:
        json.dump(
            {
                "query_count": query_count,
                "db_count": len(dbs_list),
                "DBs": dbs_list
            }, output_json, indent=4)
