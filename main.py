# ======================================================================================================================
# Module Name: KB API Load-Testing FrameWork (kb_alf)
# Description: Application designed for load testing APIs
# Author: Rob Daglio
# ======================================================================================================================


import json
import logging
import asyncio
import sys

from payloads.payloads import PayloadTemplate
from config import cfg
from analytics.decorators import results_list, app_timer, app_run_time


class SystemLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'id'):
            record.id = 'N/A'

        return True


logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(id)s - %(levelname)s: %(message)s',
    level=logging.getLevelName(cfg.log_level.upper()),
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(cfg.log_file, 'a+', 'utf-8')
    ]
)

log = logging.getLogger()
for handler in log.handlers:
    handler.addFilter(SystemLogFilter())

@app_timer
def run_load_test(payloads: dict) -> None:
    from payloads.clients import (
        Sender,
        AsyncSender,
        ThreadedSender
    )

    senders = {
        'sync': Sender,
        'async': AsyncSender,
        'threaded': ThreadedSender
    }

    try:
        sender = senders[cfg.mode](
            payloads=payloads,
            destination_host=cfg.target_host,
            destination_port=cfg.target_port,
            protocol=cfg.proto,
            destination_endpoint=cfg.endpoint,
            max_workers=cfg.max_workers
        )

        if cfg.mode == 'async':
            asyncio.run(sender.process_payloads())
        else:
            sender.process_payloads()

        log.debug('All payloads sent successfully.')

    except Exception as e:
        log.error(f'Operation failed: {e}')



if __name__ == '__main__':
    log.debug(f'Configuration: {json.dumps(vars(cfg), indent=4)}')
    if cfg.mode not in ['sync', 'async', 'threaded']:
        log.info('Please provide a correct mode from the following:\n[\'sync\', \'async\', \'threaded\'].')
        sys.exit()

    from analytics.results import calculate_and_display_results, write_results_csv
    from payloads.gen import PayloadGenerator, reset_payload_counter

    if cfg.reset_counter:
        reset_payload_counter()

    payload_generator = PayloadGenerator(
        payload_template=PayloadTemplate.TEMPLATE.value,
        payload_quantity=cfg.payload_quantity,
    )

    payload_generator.build_json_payload()
    run_load_test(payloads=payload_generator.payloads)

    stats = calculate_and_display_results(results_list, cfg.payload_quantity, app_run_time)

    if cfg.csv_file_name:
        write_results_csv(stats, cfg.csv_file_name)
