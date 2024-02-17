import logging
import typing as t
from logging import Logger
from types import TracebackType

import httpx
from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

import config

_T = t.TypeVar("_T")

logger: Logger = logging.getLogger(__name__)


class RequestClient:
    def __init__(
        self,
        cookies: t.Optional[CookieTypes] = None,
        proxies: t.Optional[ProxiesTypes] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        verify: VerifyTypes = True,
        cert: t.Optional[CertTypes] = None,
        trust_env: bool = True,
    ) -> None:
        proxy: httpx.Proxy = (
            httpx.Proxy(config.get("HTTP_PROXY", raise_error=True))
            if bool(config.get("HTTP_PROXY", False))
            else proxies
        )

        logger.debug(f"Proxy: {proxy}")

        self._client = httpx.Client(
            cookies=cookies,
            proxies=proxy,
            cert=cert,
            verify=verify,
            timeout=timeout,
            trust_env=trust_env,
        )

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def __del__(self) -> None:
        if self.is_closed():
            return

        logger.debug("HTTPX client is not closed, closing it now...")
        self.close()

    def request(
        self,
        method: str,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        with self._client as client:
            return client.request(
                method=method,
                url=url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                auth=auth,
                follow_redirects=follow_redirects,
            )

    def get(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def options(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def head(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "HEAD",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def post(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def put(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def patch(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def delete(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )
