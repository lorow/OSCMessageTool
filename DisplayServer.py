from queue import Queue
from time import sleep

from rich.layout import Layout

from rich.console import Console
from rich.live import Live
from rich.table import Table

from Widgets.SentReceivedWIdget import SentReceivedWidget
from Widgets.StatusHeaderWidget import StatusHeaderWidget, StatusModel


class DisplayServer:
    def __init__(self, sent_messages_queue: Queue, received_messages_queue: Queue) -> None:
        self.header_widget = StatusHeaderWidget(StatusModel(
            messages_to_send=200,
            is_sending=True,
            is_receiving=False,
            sending_address="127.0.0.1",
            sending_port=2336,
            receiving_port=None,
        ))
        self.sent_received_widget = SentReceivedWidget(sent_messages_queue, received_messages_queue)

        self.main_bar = Table()
        self.console = Console()
        self.layout = Layout()

    def start(self):
        header = Layout(name="header")
        header.size = 6

        body = Layout(name="body")
        self.layout = Layout(
            name="main",
        )
        self.layout.split_column(
            header,
            body
        )

        self.header_widget.setup(self.layout["main"]["header"])
        self.sent_received_widget.setup(self.layout["main"]["body"])

    def run(self):
        with Live(console=self.console, screen=False, refresh_per_second=10) as live:
            while True:
                messages_sent, messages_received = self.sent_received_widget.get_messages_stats()
                self.header_widget.render(
                    messages_received=messages_received,
                    messages_sent=messages_sent
                )
                self.sent_received_widget.render()

                live.update(self.layout)
                sleep(.1)
