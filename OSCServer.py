import rich_click as click
from queue import Queue

from pythonosc import dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer


class OSCServer:
    def __init__(self, ip: str, port: int, output_queue: Queue):
        self.output_queue = output_queue
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.set_default_handler(self.handle_osc_message)

        try:
            self.server = ThreadingOSCUDPServer((ip, port), self.dispatcher)
        except Exception as e:
            click.echo(e)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def handle_osc_message(self, osc_address, value):
        self.output_queue.put((osc_address, value))
