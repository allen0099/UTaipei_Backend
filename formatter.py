import logging
from copy import copy

import click
from uvicorn.logging import AccessFormatter


class TimedAccessFormatter(AccessFormatter):
    @staticmethod
    def get_color_time(time: float) -> str:
        s: str = "{:.6f}".format(time)

        if time < 0.5:
            s = click.style(str(s), fg="green")
        elif time < 0.7:
            s = click.style(str(s), fg="yellow")
        elif time < 1.0:
            s = click.style(str(s), fg="red")
        else:
            s = click.style(str(s), fg="bright_red")

        return s

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)

        if len(record.args) != 7:
            return super().formatMessage(recordcopy)

        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
            time,
            response_length,
        ) = recordcopy.args  # type: ignore[misc]

        if self.use_colors:
            time = self.get_color_time(time)
        else:
            time = "{:.6f}".format(time)

        recordcopy.__dict__.update(
            {
                "run_time": time,
                "response_length": response_length,
            }
        )

        recordcopy.args = (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        )

        return super().formatMessage(recordcopy)
