import aiohttp
from bs4 import BeautifulSoup

class TransportParser:
    def __init__(self, url, soup):
        self.url = url
        self.soup = soup

    @classmethod
    async def create(cls, url):
        soup = await cls.get_soup(url)
        return cls(url, soup)

    @staticmethod
    async def get_soup(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
        return BeautifulSoup(text, "lxml")

    async def get_titles(self, tag, class_name=None):
        if self.soup:
            return [el.get_text(strip=True) for el in self.soup.find_all(tag, class_=class_name)]
        return []

    async def get_child_titles(self, tag, class_name=None, parent_tag=None, parent_class=None, parent_id=None):
        if self.soup:
            return [
                el.get_text(strip=True)
                for el in self.soup.find_all(tag, class_=class_name)
                if parent_tag is None or el.find_parent(parent_tag, class_=parent_class, id=parent_id)
            ]
        return []

    async def get_link(self, tag, class_name=None):
        if self.soup:
            return [el.get("href") for el in self.soup.find_all(tag, class_=class_name)]
        return []

    async def get_element_info_by_index(self, tag, class_name=None, parent_tag=None, parent_class=None, index=None):
        elements = self.soup.find_all(parent_tag, class_=parent_class)
        if index is not None and index < len(elements):
            current_element = elements[index]
            return [stop.get_text(strip=True) for stop in current_element.find_all(tag, class_=class_name)]
        return []
