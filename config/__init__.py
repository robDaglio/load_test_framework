import configargparse

parser = configargparse.get_argument_parser(name='default')

parser.add_argument('--log-level', type=str, required=False,
                    default='DEBUG', help='Log level to display.')

parser.add_argument('--log-file', type=str, required=False,
                    default='logs/app.log', help='Log file path.')

parser.add_argument('--payload-quantity', type=int, required=False,
                    default=1, help='The number of payloads to send.')

parser.add_argument('--target-host', type=str, required=False,
                    default='localhost', help='The target host which will receive sent payloads.')

parser.add_argument('--target-port', type=int, required=False,
                    default=None, help='The target port to which payloads will be sent.')

parser.add_argument('--proto', type=str, required=False,
                    default='http', help='The protocol with which to send payloads <http/https>')

parser.add_argument('--endpoint', type=str, required=False,
                    default='blob', help='The API endpoint to which payloads will be sent.')

parser.add_argument('--reset-counter', type=bool, required=False,
                    default=False, help='Reset the payload counter value stored in last.json.')

parser.add_argument('--api-user', type=str, required=False,
                    default=None, help='The api username to pass to basic auth.')

parser.add_argument('--api-pass', type=str, required=False,
                    default=None, help='The api password to pass to basic auth.')

parser.add_argument('--mode', type=str, required=False,
                    default='sync', help='Options: ["sync" | "async" | "threaded"]')

parser.add_argument('--max-workers', type=int, required=False,
                    default=5, help='Max workers- only if "threaded" option is enabled.')

parser.add_argument('--csv-file-name', type=str, required=False,
                    default=None, help='Output CSV file name.')

cfg = parser.parse_known_args()[0]