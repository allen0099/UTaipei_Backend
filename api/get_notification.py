import logging
import re
import time
import typing as t

from httpx import Response
from lxml import html
from lxml.etree import _Element, _ElementUnicodeResult
from lxml.html import HtmlElement

from http_client import RequestClient
from .exceptions import WrapperAPIException

logger: logging.Logger = logging.getLogger(__name__)

T = t.TypeVar("T")


def remove_spaces(text: str) -> str:
    return re.sub(r"\s+", "", text.strip())


def add_space(text: str) -> str:
    replace_text: str = remove_spaces(text).replace("(", "（").replace(")", "）")
    add_space_text: str = re.sub(r"([^\x00-\x7F]+)", r" \1 ", replace_text)
    result: str = add_space_text.replace("（", "(").replace("）", ")")
    return result.strip()


def url_check(text: str) -> list[dict[str, t.Any]]:
    links: list[str] = re.findall(r"(https?://\S+)", text)
    if not links:
        return [{"text": add_space(text), "href": None, "linebreak": False}]

    data: list[dict[str, t.Any]] = []

    for link in links:
        list_str: list[str] = text.split(link, 1)
        data.append({"text": f"{add_space(list_str[0])} ", "href": None, "linebreak": False})
        data.append({"text": link, "href": link, "linebreak": False})

        text = list_str[1]

    return data


def href_iter(text: str, hrefs: list[HtmlElement]) -> list[dict[str, t.Any]]:
    data: list[dict[str, t.Any]] = []

    for href in hrefs:
        link: str | None = href.attrib.get("href")

        if text == href.text:
            if link and link.startswith("http"):
                data.append({"text": add_space(text), "href": link, "linebreak": False})
                break

            data.append(
                {
                    "text": add_space(text),
                    "href": "https://my.utaipei.edu.tw/utaipei/index_sky.html",
                    "linebreak": False,
                }
            )

    if not data:
        data.extend(url_check(text))

    return data


def deal_data(div: HtmlElement) -> list[dict[str, t.Any]]:
    original_extract: list[HtmlElement | _ElementUnicodeResult] = div.xpath(".//text() | .//br")
    href_extract: list[HtmlElement] = div.xpath(".//a")

    data: list[dict[str, t.Any]] = []

    for _ in original_extract:
        if isinstance(_, HtmlElement):
            data.append({"text": "", "href": None, "linebreak": True})
            continue

        if (text := _.strip()) != "":
            data.extend(href_iter(text, href_extract))

    return data


class GetNotification:
    URL = "https://my.utaipei.edu.tw/utaipei/index_main.html?123="
    _instance: t.Optional[t.Self] = None

    _response: Response = None
    _last_update: float = 0

    def __new__(cls: t.Type[T]) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @property
    def response(self):
        if time.time() - self._last_update > 3600:
            logger.info("Update master data from API.")
            with RequestClient() as client:
                result: Response = client.get(self.URL)

                if not result.is_success:
                    raise WrapperAPIException("Failed to get result", self.URL, result.text)

                self._response = result
                self._last_update = time.time()

        return self._response

    def get_div(self) -> HtmlElement:
        root: _Element = html.fromstring(self.response.text)

        return root.xpath("//div[@id='std_payment']")[0]

    def result(self) -> list[dict[str, t.Any]]:
        return deal_data(self.get_div())
