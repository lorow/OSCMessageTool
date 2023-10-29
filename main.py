import threading
from queue import Queue
from typing import List

import rich_click as click

from DisplayServer import DisplayServer
from Models import SendingConfiguration
from OSCClient import OSCClient
from OSCServer import OSCServer
from Widgets.StatusHeaderWidget import StatusModel


@click.command()
@click.option("--send_port", help="Port to which send the messages", default=8888)
@click.option("--send_ip", help="IP address to send the messages to", default="127.0.0.1")
@click.option("--receive_port", help="Port on which to listen", default=8889)
@click.option("--command", help="OSC command to send", multiple=True)
@click.option("--value", help="Value to send along the command", multiple=True)
@click.option(
    "--repeat",
    help="amount of times to repeat the command 0-N or INF, can be left empty",
    default="1",
)
@click.option("--timeout", help="Timeout between each message sent", default=2)
@click.option("--listen", is_flag=True, help="Should the app listen for incoming messages")
def main(
    command: str | List[str],
    value: str,
    repeat: int | str,
    send_port: int,
    send_ip: str,
    timeout: int,
    receive_port: int,
    listen: bool,
):
    if send_port <= 0 and receive_port <= 0:
        click.echo("Sending and Receiving disabled, nothing to do here, exiting.")
        exit(0)

    event = threading.Event()
    sent_messages_queue = Queue()
    received_messages_queue = Queue()
    osc_server_instance = None
    threads_to_close = []

    try:
        display_server_status = StatusModel(
            messages_to_send=len(command),
            sending_address=send_ip,
            sending_port=send_port,
            receiving_port=receive_port,
            repeat=repeat,
        )

        setup_sender_server(
            event,
            send_port,
            command,
            value,
            repeat,
            timeout,
            send_ip,
            display_server_status,
            sent_messages_queue,
            threads_to_close,
        )
        osc_server_instance = setup_receiver_server(
            listen,
            receive_port,
            display_server_status,
            received_messages_queue,
            threads_to_close,
        )
        setup_display_server(
            event,
            sent_messages_queue,
            received_messages_queue,
            display_server_status,
            threads_to_close,
        )
    except KeyboardInterrupt:
        event.set()

        # dirty hack to get the ThreadingOSCUDPServer to stop running, events don't work
        if osc_server_instance:
            osc_server_instance.stop()

        for thread in threads_to_close:
            thread.join()
        exit(0)


def setup_sender_server(
    event: threading.Event,
    send_port: int,
    command: List[str],
    value: str,
    repeat: int | str,
    timeout: int,
    send_ip: str,
    display_server_status: StatusModel,
    sent_messages_queue: Queue,
    threads_to_close: List[threading.Thread],
):
    if not send_port:
        return

    if len(command) - len(value):
        click.echo("There's a missmatch in commands and their values, exiting.")
        exit(0)

    address_value_map = dict(zip(command, value))
    message_config = SendingConfiguration(
        repeat=repeat,
        message_timeout=timeout,
        address_value_map=address_value_map,
    )

    display_server_status.is_sending = True
    osc_client = OSCClient(event, send_ip, send_port, sent_messages_queue, message_config)
    osc_client_thread = threading.Thread(target=osc_client.run)
    osc_client_thread.start()
    threads_to_close.append(osc_client_thread)


def setup_receiver_server(
    listen: bool,
    receive_port: int,
    display_server_status: StatusModel,
    received_messages_queue: Queue,
    threads_to_close: List[threading.Thread],
):
    if listen and receive_port:
        display_server_status.is_receiving = True
        osc_server = OSCServer(
            "127.0.0.1",
            receive_port,
            received_messages_queue,
        )
        osc_server_thread = threading.Thread(target=osc_server.run)
        osc_server_thread.start()
        threads_to_close.append(osc_server_thread)
        return osc_server


def setup_display_server(
    event: threading.Event,
    sent_messages_queue: Queue,
    received_messages_queue: Queue,
    display_server_status: StatusModel,
    threads_to_close: List[threading.Thread],
):
    display = DisplayServer(event, sent_messages_queue, received_messages_queue, display_server_status)
    display.start()
    display_thread = threading.Thread(target=display.run)
    display_thread.run()

    threads_to_close.append(display_thread)


if __name__ == "__main__":
    main()
