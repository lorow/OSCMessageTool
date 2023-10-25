from queue import Queue, Empty
from typing import Optional

from rich.layout import Layout


class SentReceivedWidget:
    def __init__(self, sent_messages_queue: Queue, received_messages_queue: Queue):
        self.layout: Optional[Layout] = None
        self.sent_messages_queue = sent_messages_queue
        self.received_messages_queue = received_messages_queue
        self.buffered_messages_cap = 10

        self.messages_sent = 0
        self.messages_received = 0

        self.received_messages_buffer = []
        self.sent_messages_buffer = []

    def setup(self, layout: Layout):
        self.layout = layout
        self.layout.split_row(
            Layout("messages_sent", size=50),
            Layout("messages_received", size=50),
        )

    def get_messages(self):
        sent_message = None
        received_message = None
        try:
            sent_message = self.sent_messages_queue.get_nowait()
        except Empty:
            pass

        try:
            received_message = self.received_messages_queue.get_nowait()
        except Empty:
            pass

        if sent_message:
            self.messages_sent += 1
            if len(self.sent_messages_buffer) == self.buffered_messages_cap:
                del self.sent_messages_buffer[0]
            self.sent_messages_buffer.append(sent_message)

        if received_message:
            self.messages_received += 1
            if len(self.received_messages_buffer) == self.buffered_messages_cap:
                del self.received_messages_buffer[0]
            self.received_messages_buffer.append(received_message)

    def get_messages_stats(self) -> (int, int):
        return self.messages_sent, self.messages_received

    def render(self):
        pass
