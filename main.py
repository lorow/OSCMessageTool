import threading

import rich_click as click

from DisplayServer import DisplayServer


@click.command()
@click.option("--send_port", help="Port to which send the messages", default=8888)
@click.option("--receive_port", help="Port on which to listen", default=8889)
@click.option("--command", help="OSC command to send")
@click.option("--value", help="Value to send along the command")
@click.option("--repeat", help="amount of times to repeat the command 0-N or INF, can be left empty", default="1")
@click.option("--listen", is_flag=True, help="Should the app listen for incoming messages")
def main(command: str, value: str, repeat: int | str, send_port: int, receive_port: int, listen: bool):
    event = threading.Event()
    try:
        display = DisplayServer(None, None)
        display.start()
        display_thread = threading.Thread(target=display.run())
        display_thread.run()
    except KeyboardInterrupt:
        event.set()
        exit(0)


if __name__ == "__main__":
    main()
