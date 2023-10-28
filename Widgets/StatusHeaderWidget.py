import dataclasses
from typing import Optional

from rich import box
from rich.layout import Layout
from rich.table import Table


@dataclasses.dataclass
class StatusModel:
    messages_to_send: int = 0
    is_sending: bool = False
    is_receiving: bool = False
    sending_address: str = "127.0.0.1"
    sending_port: int = 8888
    receiving_port: Optional[int] = 8889


class StatusHeaderWidget:
    def __init__(self, config: StatusModel):
        self.config = config
        self.layout: Optional[Layout] = None

    def setup(self, layout: Optional[Layout] = None):
        self.layout = layout

    def render(self, **kwargs):
        messages_received = kwargs.get("messages_received", 0)
        messages_sent = kwargs.get("messages_sent", 0)

        main_bar = Table(
            show_header=False,
            box=box.SIMPLE,
            padding=(0, 1),
        )
        main_bar.add_column("", justify="left")
        main_bar.add_column("", justify="left")
        main_bar.add_row(
            "Messages to send: ",
            f"{self.config.messages_to_send}",
        )
        main_bar.add_row(
            f"Sending: {':white_check_mark:' if self.config.is_sending else ':red_square: ' }",
            f"On: {self.config.sending_address}:{self.config.sending_port}",
        )
        main_bar.add_row(
            f"Receiving: {':white_check_mark:' if self.config.is_receiving else ':red_square: ' }",
            f"On: {self.config.receiving_port if self.config.receiving_port else 'N/A'}",
        )
        main_bar.add_row(f"Messages Received: {messages_received}", f"Messages Sent: {messages_sent}")

        self.layout.update(main_bar)
