from main import log
import statistics
import csv


def calculate_and_display_results(results_list: list, total_payloads: int, run_time: list) -> dict:
    average_execution_time = round(sum(results_list) / float(len(results_list)), 4)
    average_execution_time_ms = int(average_execution_time * 1000)
    max_execution_time = int(max(results_list) * 1000.0)
    min_execution_time = int(min(results_list) * 1000.0)
    median_execution_time = int(round(statistics.median(results_list), 4) * 1000.0)
    app_execution_time = round(run_time[0], 4)
    requests_per_second = round(float(total_payloads) / app_execution_time, 4)

    log.info(f'Average execution time: {average_execution_time_ms} ms')
    log.info(f'Maximum execution time: {max_execution_time} ms')
    log.info(f'Minimum execution time: {min_execution_time} ms')
    log.info(f'Median execution time: {median_execution_time} ms')
    log.info(f'Total execution time: {app_execution_time} s')
    log.info(f'Requests per second: {requests_per_second}')

    return {
        'TotalPayloadsSent': total_payloads,
        'AverageExecutionTime': average_execution_time,
        'MaxExecutiontime': max_execution_time,
        'MinimumExecutionTime': min_execution_time,
        'MedianExecutionTime': median_execution_time,
        'AppExecutionTime': app_execution_time,
        'RequestsPerSecond': requests_per_second
    }

def write_results_csv(results_dict: dict, file_name: str) -> None:
    try:
        log.info(f'Writing results to {file_name}.')

        with open(file_name, 'w') as f:
            csv_writer = csv.writer(f)

            for row in [results_dict.keys(), results_dict.values()]:
                csv_writer.writerow(row)

    except Exception as e:
        log.error(f'Error writing output file: {e}')

