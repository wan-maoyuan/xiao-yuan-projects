import logging
from urllib.parse import quote

from DrissionPage import SessionPage


# https://shanghai.anjuke.com/sale/rd1/?q=%E8%8E%B2%E5%BA%B7%E8%8B%91
class AnJuKe:
    def __init__(self):
        self.base_url = "https://shanghai.anjuke.com/sale"
        self.page = SessionPage()

    def get_road_info(self, name: str) -> (str, bool):
        name_url = quote(name)
        url = self.base_url + "/rd1/?q=" + name_url
        self.page.get(url)
        p_list = self.page.eles(".community-info-detail-des-item-short")
        if len(p_list) != 1:
            logging.error("can not find residential quarters info")
            return "", False

        road_info = ""
        span_list = p_list[0].eles("tag:span")
        for span in span_list:
            road_info += span.text

        return road_info, True


if __name__ == '__main__':
    an = AnJuKe()

    road, has = an.get_road_info("莲康苑")
    if has:
        print("road info: ", road)

    road, has = an.get_road_info("鹏健苑")
    if has:
        print("road info: ", road)
