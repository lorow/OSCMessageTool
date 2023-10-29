import threading
from queue import Queue
from time import sleep

from rich.layout import Layout

from rich.console import Console
from rich.live import Live
from rich.table import Table

from Widgets.SentReceivedWIdget import SentReceivedWidget
from Widgets.StatusHeaderWidget import StatusHeaderWidget, StatusModel


class DisplayServer:
    def __init__(
        self,
        event: threading.Event,
        sent_messages_queue: Queue,
        received_messages_queue: Queue,
        display_server_status: StatusModel,
    ) -> None:
        self.event = event
        self.header_widget = StatusHeaderWidget(display_server_status)
        self.sent_received_widget = SentReceivedWidget(
            sent_messages_queue,
            received_messages_queue,
        )

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
        self.layout.split_column(header, body)

        self.header_widget.setup(self.layout["main"]["header"])
        self.sent_received_widget.setup(self.layout["main"]["body"])

    def run(self):
        with Live(console=self.console, screen=False, refresh_per_second=10) as live:
            while not self.event.is_set():
                (
                    messages_sent,
                    messages_received,
                ) = self.sent_received_widget.get_messages_stats()
                self.header_widget.render(
                    messages_received=messages_received,
                    messages_sent=messages_sent,
                )
                self.sent_received_widget.render()

                live.update(self.layout)
                sleep(0.1)
