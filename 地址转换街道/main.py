from typing import Union
import requests


BASE_URL = "https://restapi.amap.com/v3/geocode/geo?parameters"
KEY = "c40679f564f41c971c9a5580f4db96f6"


class StressInfo:
    def __init__(self,
                 country: str, province: str, city: str, district: str,
                 township: str, street: str, number: str, location: str):
        self.country = country
        self.province = province
        self.city = city
        self.district = district
        self.township = township
        self.street = street
        self.number = number
        self.location = location

    def __str__(self) -> str:
        return "country:{} province:{} city:{} district:{} township:{} street:{} number:{} location:{}".format(
            self.country, self.province, self.city, self.district,
            self.township, self.street, self.number, self.location,
        )


def address2stress(address: str, city: str) -> Union[StressInfo, None]:
    param = {
        "key": KEY,
        "address": address,
        "city": city
    }
    resp = requests.get(url=BASE_URL, params=param)
    if resp.status_code != 200:
        print("request status code: ", resp.status_code)
        return None

    geo = resp.json()['geocodes'][0]

    return StressInfo(
        geo['country'], geo['province'], geo['city'], geo['district'],
        geo['township'], geo['street'], geo['number'], geo['location'],
    )


if __name__ == '__main__':
    stress_info = address2stress("北京市朝阳区阜通东大街6号", "")
    if stress_info is None:
        print("address2stress error")
    else:
        # print("stress_info: ", stress_info)
        print(stress_info)
