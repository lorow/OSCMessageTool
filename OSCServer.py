import rich_click as click
from queue import Queue

from pythonosc import dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer


class OSCServer:
    def __init__(self, ip: str, port: int, output_queue: Queue, addresses: list[str]):
        self.output_queue = output_queue
        self.dispatcher = dispatcher.Dispatcher()
        try:
            self.server = ThreadingOSCUDPServer((ip, port), self.dispatcher)
        except Exception as e:
            click.echo(e)

        for address in addresses:
            self.dispatcher.map(address, self.handle_osc_message)

    def run(self):
        self.server.serve_forever()

    def handle_osc_message(self, osc_address, value):
        self.output_queue.put((osc_address, value))
