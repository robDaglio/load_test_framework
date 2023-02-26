import json
import random
from copy import deepcopy
from datetime import datetime
from .payloads import Products, Stages
from main import log


def reset_payload_counter():
    with open('last_event.json', 'r+') as f:
        json.dump({"last": 100000001}, f)


class PayloadGenerator:
    def __init__(self, payload_template: any = None, payload_quantity: int = 1) -> None:
        self.payload_quantity = payload_quantity
        self.payload_template = payload_template

        self.last_event = json.load(open('last_event.json'))['last']
        self.updated_event_id = None
        self.payloads = list()

    def build_json_payload(self):
        log.debug('Building payloads.')
        self.updated_event_id = self.last_event

        for _ in range(self.payload_quantity):
            new_payload = deepcopy(self.payload_template)

            new_payload["EventID"] = str(self.updated_event_id)
            new_payload["DateTime"] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

            new_payload["Stage"] = random.choice(Stages.STAGES.value)
            new_payload["Product"] = random.choice(Products.PRODUCTS.value)

            self.updated_event_id += 1
            self.payloads.append(new_payload)

            log.debug(f'Payload type: {type(new_payload)}\nPayload:\n{new_payload}')

        self.update_last_event_id()

    def update_last_event_id(self):
        log.debug('Updating last event ID.')
        with open('last_event.json', 'r+') as f:
            json.dump({"last": self.updated_event_id}, f)

    def show_payloads(self):
        for payload in self.payloads:
            log.debug(json.dumps(payload, indent=4))