import csv
from typing import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s',
)


NEW_CSV_PATH = r"./data/new.csv"
OLD_CSV_PATH = r"./data/old.csv"
SAVE_CSV_PATH = r"./data/save.csv"


class Township:
    def __init__(self, inner_id: str, code: str, name: str):
        self.inner_id = inner_id
        self.code = code
        self.name = name


class District:
    def __init__(self, inner_id: str, code: str, name: str):
        self.inner_id = inner_id
        self.code = code
        self.name = name
        self.township = []

    def add_township(self, township: Township) -> Township:
        for t in self.township:
            if t.name == township.name:
                return t

        self.township.append(township)
        return township

    def get_township(self, township_name: str) -> Township | None:
        for t in self.township:
            if t.name == township_name:
                return t

        return None


class City:
    def __init__(self, inner_id: str, code: str, name: str):
        self.inner_id = inner_id
        self.code = code
        self.name = name
        self.district = []

    def add_district(self, district: District) -> District:
        for d in self.district:
            if d.name == district.name:
                return d

        self.district.append(district)
        return district

    def get_district(self, district_name: str) -> District | None:
        for d in self.district:
            if d.name == district_name:
                return d

        return None


class Prov:
    def __init__(self, inner_id: str, code: str, name: str):
        self.inner_id = inner_id
        self.code = code
        self.name = name
        self.city = []

    def add_city(self, city: City) -> City:
        for c in self.city:
            if c.name == city.name:
                return c

        self.city.append(city)
        return city

    def get_city_by_name(self, city_name: str) -> City | None:
        for c in self.city:
            if c.name == city_name:
                return c

        return None


def read_new_csv() -> List[Dict]:
    new_data = []
    with open(NEW_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_data.append({
                "prov_inner_id": "",
                "prov_code": "",
                "prov": row["prov_name"],

                "city_inner_id": "",
                "city_code": "",
                "city": row["city_name"],

                "district_inner_id": "",
                "district_code": "",
                "district": row["district_name"],

                "township_inner_id": "",
                "township_code": "",
                "township": row["township_name"],
            })

    return new_data


def read_old_csv() -> List[Dict]:
    old_data = []
    with open(OLD_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_data.append({
                "prov_inner_id": row["prov_inner_id"],
                "prov_code": row["prov_code"],
                "prov": row["prov_nm"],

                "city_inner_id": row["city_inner_id"],
                "city_code": row["city_code"],
                "city": row["city_nm"],

                "district_inner_id": row["district_inner_id"],
                "district_code": row["district_code"],
                "district": row["district_nm"],

                "township_inner_id": row["street_town_inner_id"],
                "township_code": row["street_town_code"],
                "township": row["street_town_nm"],
            })

    return old_data


def convert_list_to_class(data: List[Dict]) -> List[Prov]:
    result = []
    for item in data:
        prov = None
        flag = True
        for i in result:
            if i.name == item["prov"]:
                prov = i
                flag = False
                break
        if flag:
            prov = Prov(item["prov_inner_id"], item["prov_code"], item["prov"])
            result.append(prov)

        city = prov.add_city(City(item["city_inner_id"], item["city_code"], item["city"]))
        district = city.add_district(District(item["district_inner_id"], item["district_code"], item["district"]))
        district.add_township(Township(item["township_inner_id"], item["township_code"], item["township"]))

    return result


def delete_old_invalid_prov(old: List[Prov], new: List[Prov]):
    for o in old:
        prov_flag = True
        for n in new:
            if o.name == n.name:
                _delete_old_invalid_city(o, n)
                prov_flag = False
                break
        if prov_flag:
            logging.info("old data delete invalid data, prov_name: %s" % o.name)
            old.remove(o)


def _delete_old_invalid_city(old: Prov, new: Prov):
    for oc in old.city:
        nc = new.get_city_by_name(oc.name)
        if nc is None:
            logging.info("old data delete invalid data, city_name: %s" % oc.name)
            old.city.remove(oc)
            break
        else:
            _delete_old_invalid_district(oc, nc)


def _delete_old_invalid_district(old: City, new: City):
    for od in old.district:
        nd = new.get_district(od.name)
        if nd is None:
            logging.info("old data delete invalid data, district_name: %s" % od.name)
            old.district.remove(od)
            break
        else:
            _delete_old_invalid_township(od, nd)


def _delete_old_invalid_township(old: District, new: District):
    for ot in old.township:
        nt = new.get_township(ot.name)
        if nt is None:
            logging.info("old data delete invalid data, township_name: %s" % ot.name)
            old.township.remove(ot)
            break


def add_old_new_prov(old: List[Prov], new: List[Prov]):
    for n in new:
        prov_flag = True
        for o in old:
            if o.name == n.name:
                _add_old_new_city(o, n)
                prov_flag = False
                break
        if prov_flag:
            logging.info("old data add new data, prov_name: %s" % n.name)
            old.append(n)


def _add_old_new_city(old: Prov, new: Prov):
    for nc in new.city:
        oc = old.get_city_by_name(nc.name)
        if oc is None:
            logging.info("old data add new data, city_name: %s" % nc.name)
            old.city.append(nc)
            break
        else:
            _add_old_new_district(oc, nc)


def _add_old_new_district(old: City, new: City):
    for nd in new.district:
        od = old.get_district(nd.name)
        if od is None:
            logging.info("old data add new data, district_name: %s" % nd.name)
            old.district.append(nd)
            break
        else:
            _add_old_new_township(od, nd)


def _add_old_new_township(old: District, new: District):
    for nt in new.township:
        ot = old.get_township(nt.name)
        if ot is None:
            logging.info("old data add new data, township_name: %s" % nt.name)
            old.township.append(nt)
            break


def save_class_to_csv(data: List[Prov]):
    with open(SAVE_CSV_PATH, encoding='utf-8', mode="w+")as f:
        f.write(
            "prov_inner_id,prov_code,prov_name,city_inner_id,city_code,city_name,district_inner_id,district_code,"
            "district_name,township_inner_id,township_code,township_name\n "
        )

        for prov in data:
            prov_line = prov.inner_id + "," + prov.code + "," + prov.name + ","
            for city in prov.city:
                city_line = city.inner_id + "," + city.code + "," + city.name + ","
                for district in city.district:
                    district_line = district.inner_id + "," + district.code + "," + district.name + ","
                    for township in district.township:
                        township_line = township.inner_id + "," + township.code + "," + township.name + "\n"
                        f.write(prov_line + city_line + district_line + township_line)


def main():
    old_data = read_old_csv()
    old = convert_list_to_class(old_data)

    new_data = read_new_csv()
    new = convert_list_to_class(new_data)

    delete_old_invalid_prov(old, new)
    add_old_new_prov(old, new)

    save_class_to_csv(old)


if __name__ == '__main__':
    main()
