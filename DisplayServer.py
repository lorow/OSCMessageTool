from queue import Queue
from time import sleep

from rich import box
from rich.layout import Layout

from rich.console import Console, Group
from rich.live import Live
from rich.table import Table

from Widgets.StatusHeaderWidget import StatusHeaderWidget, StatusModel


class DisplayServer:
    def __init__(self, sent_messages_queue: Queue, received_messages_queue: Queue) -> None:
        self.sent_messages_queue = sent_messages_queue
        self.received_messages_queue = received_messages_queue
        self.received_messages_buffer = []
        self.sent_messages_buffer = []

        self.poll_tick_rate = 100  # 100ms
        self.message_cap = 100
        self.i = 0

        self.header_widget = StatusHeaderWidget(StatusModel(
            messages_to_send=200,
            is_sending=True,
            is_receiving=False,
            sending_address="127.0.0.1",
            sending_port=2336,
            receiving_port=None,
        ))

        self.main_bar = Table()
        self.header_layout = Layout()
        self.body_layout = Layout()
        self.console = Console()
        self.layout = Layout()

    def start(self):
        self.body_layout.split_row(
            Layout("OSC Messages Sent"),
            Layout("OSC Messages Received"),
        )

    def run(self):
        with Live(console=self.console, screen=False, refresh_per_second=10) as live:
            while True:
                self.i += 1
                live.update(
                    Group(
                        self.header_widget.render(
                            messages_received=self.i,
                            messages_sent=self.i
                        ),
                        self.body_layout
                    )
                )
                sleep(.1)
