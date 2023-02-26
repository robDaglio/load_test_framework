import asyncio
import json
import requests
import concurrent.futures

from requests.exceptions import (
    HTTPError,
    ConnectionError,
    Timeout
)

from aiohttp import (
    ClientSession,
    web_exceptions,
    client_exceptions,
    BasicAuth
)

from analytics.decorators import timer, async_timer
from main import log, cfg


class Sender:
    def __init__(
            self,
            payloads: list = None,
            destination_host: str = None,
            destination_port: int = None,
            protocol: str = None,
            destination_endpoint: str = None,
            max_workers: int = None
    ) -> None:
        self.target_url = f'{protocol}://{destination_host}:{destination_port}/{destination_endpoint}' if \
            destination_port else f'{protocol}://{destination_host}/{destination_endpoint}'

        self.payloads = payloads
        self.headers = {'Content-Type': 'application/json'}
        self.results = list()
        self.max_workers = max_workers

    def process_payloads(self):
        for index, payload in enumerate(self.payloads):
            self.results.append(self.send_request(f'Iter: {index}', payload))

    @timer(log)
    def send_request(self, request_id, payload):
        try:
            log.debug(f'Initializing request for thread {request_id}.')
            response = requests.post(
                url=self.target_url,
                headers=self.headers,
                json=payload,
                auth=(cfg.api_user, cfg.api_pass)
            )

            log.debug(f'Status: {response.status_code} | Content: {response.content.decode("utf-8")}')
            return response

        except (HTTPError, ConnectionError, Timeout) as e:
            log.error(e)


class AsyncSender(Sender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def process_payloads(self):
        log.debug('Sending all payloads.')
        await asyncio.gather(*(self.send_request(index, p) for index, p in enumerate(self.payloads)))

    @async_timer(log)
    async def send_request(self, request_id, payload):
        try:
            log.debug(f'Forwarding {payload} to {self.target_url}.')
            log.debug(f'Type: {type(json.dumps(payload))}')

            async with ClientSession() as session:
                async with session.post(
                        url=self.target_url,
                        json=payload,
                        headers=self.headers,
                        auth=BasicAuth(cfg.api_user, cfg.api_pass)
                ) as response:
                    content = await response.text()
                    log.debug(f'Server response: {response.status} | {content}')

            await session.close()
        except web_exceptions.HTTPClientError as e:
            log.error(f'HTTP error: {e}.')

        except client_exceptions.ClientOSError as e:
            log.error(f'ClientOS error: {e}.')


class ThreadedSender(Sender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processing_complete = False

    def process_payloads(self):
        log.debug('Sending all payloads.')
        item_count = 0

        while not self.processing_complete:
            if item_count == len(self.payloads):
                break

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                for index, payload in enumerate(self.payloads):
                    ex.submit(self.send_request, index, payload)

                    item_count += 1