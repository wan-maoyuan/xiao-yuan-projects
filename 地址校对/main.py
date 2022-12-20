import csv
import logging
from typing import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s',
)

NEW_CSV_PATH = r"./data/new.csv"
OLD_CSV_PATH = r"./data/old.csv"


class Township:
    def __init__(self, value: str):
        self.value = value


class District:
    def __init__(self, value: str):
        self.value = value
        self.township = []

    def add_township(self, township: Township) -> Township:
        for t in self.township:
            if t.value == township.value:
                return t

        self.township.append(township)
        return township

    def get_township(self, township_name: str) -> Township | None:
        for t in self.township:
            if t.value == township_name:
                return t

        return None


class City:
    def __init__(self, value: str):
        self.value = value
        self.district = []

    def add_district(self, district: District) -> District:
        for d in self.district:
            if d.value == district.value:
                return d

        self.district.append(district)
        return district

    def get_district(self, district_name: str) -> District | None:
        for d in self.district:
            if d.value == district_name:
                return d

        return None


class Prov:
    def __init__(self, value: str):
        self.value = value
        self.city = []

    def add_city(self, city: City) -> City:
        for c in self.city:
            if c.value == city.value:
                return c

        self.city.append(city)
        return city

    def get_city_by_name(self, city_name: str) -> City | None:
        for c in self.city:
            if c.value == city_name:
                return c

        return None


def read_new_csv() -> List[Dict]:
    new_data = []
    with open(NEW_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_data.append({
                "prov_code": row["prov_code"],
                "prov": row["prov_name"],

                "city_code": row["city_code"],
                "city": row["city_name"],

                "district_code": row["district_code"],
                "district": row["district_name"],

                "township_code": row["township_code"],
                "township": row["township_name"],
            })

    return new_data


def read_old_csv() -> List[Dict]:
    old_data = []
    with open(OLD_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_data.append({
                "prov_code": row["prov_code"],
                "prov": row["prov_nm"],

                "city_code": row["city_code"],
                "city": row["city_nm"],

                "district_code": row["district_code"],
                "district": row["district_nm"],

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
            if i.value == item["prov"]:
                prov = i
                flag = False
                break
        if flag:
            prov = Prov(item["prov"])
            result.append(prov)

        city = prov.add_city(City(item["city"]))
        district = city.add_district(District(item["district"]))
        district.add_township(Township(item["township"]))

    return result


def compare_old2new(old: List[Prov], new: List[Prov]):
    for o in old:
        prov_flag = True
        for n in new:
            if o.value == n.value:
                compare_prov_old2new(o, n)
                prov_flag = False
                break
        if prov_flag:
            logging.info("old data not in new data, prov name: %s" % o.value)


def compare_prov_old2new(old: Prov, new: Prov):
    for oc in old.city:
        nc = new.get_city_by_name(oc.value)
        if nc is None:
            logging.info("old data not in new data, prov_name: %s city name: %s" % (old.value, oc.value))
            break
        else:
            compare_city_old2new(oc, nc, old.value)


def compare_city_old2new(old: City, new: City, prov: str):
    for od in old.district:
        nd = new.get_district(od.value)
        if nd is None:
            logging.info(
                "old data not in new data, prov_name: %s city name: %s district: %s" %
                (prov, old.value, od.value)
            )
            break
        else:
            compare_district_old2new(od, nd, prov, od.value)


def compare_district_old2new(old: District, new: District, prov: str, city: str):
    for ot in old.township:
        nt = new.get_township(ot.value)
        if nt is None:
            logging.info(
                "old data not in new data, prov_name: %s city name: %s district: %s township: %s" %
                (prov, city, old.value, ot.value)
            )
            break


def main():
    old_data = read_old_csv()
    old = convert_list_to_class(old_data)

    new_data = read_new_csv()
    new = convert_list_to_class(new_data)

    compare_old2new(old, new)
    # compare_old2new(new, old)


if __name__ == '__main__':
    main()
