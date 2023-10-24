import dataclasses
from typing import Optional

from rich import box
from rich.layout import Layout
from rich.table import Table


@dataclasses.dataclass
class StatusModel:
    messages_to_send: int
    is_sending: bool
    is_receiving: bool
    sending_address: str
    sending_port: int
    receiving_port: Optional[int]


class StatusHeaderWidget:

    def __init__(self, config: StatusModel):
        self.config = config

    def render(self, layout: Optional[Layout] = None, **kwargs):
        messages_received = kwargs.get("messages_received", 0)
        messages_sent = kwargs.get("messages_sent", 0)

        main_bar = Table(
            show_header=False,
            box=box.SIMPLE,
            padding=(0, 1),
        )
        main_bar.add_column("", justify="left")
        main_bar.add_column("", justify="left")
        main_bar.add_row("Messages to send: ", f"{self.config.messages_to_send}", )
        main_bar.add_row(
            f"Sending: {':white_check_mark:' if self.config.is_sending else ':red_square: ' }",
            f"On: {self.config.sending_address}:{self.config.sending_port}"
        )
        main_bar.add_row(
            f"Receiving: {':white_check_mark:' if self.config.is_receiving else ':red_square: ' }",
            f"On: {self.config.receiving_port if self.config.receiving_port else 'N/A'}"
        )
        main_bar.add_row(
            f"Messages Received: {messages_received}",
            f"Messages Sent: {messages_sent}"
        )
        if layout:
            layout.update(main_bar)
        return main_bar
