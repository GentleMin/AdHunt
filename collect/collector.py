"""
Prototype declaration & interface design of collector.

Created on Mon, Jan 10 2021
@author: Jingtao Min @ ETH Zurich
"""

import requests
from bs4 import BeautifulSoup
from typing import Callable, Any


class PositionItem:
    
    def __init__(self, title: str, institute: str, link: str, from_site: str, position: str, \
        field: str=None, description: str=None, app_link: str=None, app_time: str=None) -> None:
        self.title = title
        self.institute = institute
        self.link = link
        self.from_site = from_site
        self.position = position
        self.field = field
        self.description = description
        self.app_link = app_link
        self.app_time = app_time


class Collector:
    
    def __init__(self, institute: str, url: str, encoding: str="utf-8") -> None:
        self.institute = institute
        self.url = url
        self.encoding = encoding
    
    def get_positions(self) -> "list[PositionItem]":
        pos_list = list()
        return pos_list


HTML_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;" 
                    "q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
}


class HTMLCollector(Collector):
    
    def __init__(self, institute: str, url: str, encoding: str="utf-8", \
        html_header: dict=HTML_HEADER, \
        html_parser: Callable[[BeautifulSoup], "list[PositionItem]"]=lambda x: []) -> None:
        super().__init__(institute, url, encoding=encoding)
        self.html_header = html_header
        self.html_parser = html_parser
    
    def get_positions(self) -> "list[PositionItem]":
        webpage = requests.get(self.website, headers=self.html_header)
        webpage.encoding = self.encoding
        webhtml = BeautifulSoup(webpage.text, "html.parser")
        return self.html_parser(webhtml)


JSON_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
}


class JsonCollector(Collector):
    
    def __init__(self, institute: str, url: str, encoding: str = "utf-8", \
        json_header: dict=JSON_HEADER, \
        json_parser: Callable[[Any], "list[PositionItem]"]=lambda x: []) -> None:
        super().__init__(institute, url, encoding=encoding)
        self.json_header = json_header
        self.json_parser = json_parser
    
    def get_positions(self) -> "list[PositionItem]":
        json_resp = requests.get(self.url, headers=self.json_header)
        json_resp.encoding = self.encoding
        json_resp = json_resp.json()
        return self.json_parser(json_resp)


ETHZ_GEOPHYS_CODES = ("02330" , "02506", "02818", "03476", "03698", \
    "03734", "03953", "03971", "09459", "09494", "02334")

ETHZ_JOBTYPE_CODES = ("", "PhD", "Postdoc", "RA/Junior Researcher", "", \
    "Logistics", "IT Staff", "Technitian/Analyst/Engineer", "Technitian/Analyst/Engineer", "", "Student Assistant")

ethz_ifg_name = "Institute of Geophysics, ETH Zurich"
ethz_ifg_site = "https://geophysics.ethz.ch/institute/jobs/"
ethz_ifg_head = JSON_HEADER.copy()
ethz_ifg_head["Host"] = "geophysics.ethz.ch"
ethz_ifg_url = "https://geophysics.ethz.ch/institute/jobs/_jcr_content/par/jobs.softfactors.json"

def ethz_ifg_parser(json_resp: list) -> "list[PositionItem]":
    pos_list = list()
    for pos in json_resp:
        if pos["characterization"]["internalClassification"] in ETHZ_GEOPHYS_CODES:
            pos_list.append(ethz_ifg_parser_single(pos))
    return pos_list

def ethz_ifg_parser_single(pos: dict) -> PositionItem:
    if "en" in pos["description"]["title"]:
        title = pos["description"]["title"]["en"]
        field = pos["description"]["eth_area"]["en"]
        link = pos["publication"]["jobboardDetailUrl_en"]
        app_link = pos["publication"]["applyUrl_en"]
    elif "de" in pos["description"]["title"]:
        title = pos["description"]["title"]["de"]
        field = pos["description"]["eth_area"]["de"]
        link = pos["publication"]["jobboardDetailUrl_de"]
        app_link = pos["publication"]["applyUrl_de"]
            
    pos_item = PositionItem( title, ethz_ifg_name, link, ethz_ifg_site,
        ETHZ_JOBTYPE_CODES[pos["characterization"]["jobtype_id"]],
        field=field, app_link=app_link)
    return pos_item

