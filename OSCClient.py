import threading
from time import sleep

from pythonosc import udp_client

from Models import SendingConfiguration


class OSCClient:
    def __init__(
        self,
        event: threading.Event,
        ip: str,
        port: int,
        output_queue,
        sending_configuration: SendingConfiguration,
    ):
        self.event = event
        self.output_queue = output_queue
        self.client = udp_client.SimpleUDPClient(ip, port)
        self.sending_configuration = sending_configuration

    def run(self):
        if self.sending_configuration.repeat.lower() == "inf":
            while not self.event.is_set():
                self.handle_messages()
        else:
            for _ in range(int(self.sending_configuration.repeat)):
                if self.event.is_set():
                    break
                self.handle_messages()

    def handle_messages(self):
        for address, message in self.sending_configuration.address_value_map:
            try:
                message = float(message)
            except ValueError:
                pass

            self.client.send_message(address, float(message))
            self.output_queue.put((address, message))
            # we send each message once every 2 seconds
            sleep(self.sending_configuration.message_timeout or 2)
