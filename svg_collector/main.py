import urllib.parse
from pathlib import Path

import cairosvg
import requests
import typer

from svg_collector.view_box import get_view_box

app = typer.Typer()

files = Path("downloads")
files.mkdir(parents=True, exist_ok=True)


@app.command()
def run():
    user_input = input("Enter the URL: ")

    desired_sizes = [100, 500, 1000, 2000]

    while user_input != "q":
        url, *arguments = user_input.split(" ")

        parsed_url = urllib.parse.urlparse(url)
        path = Path(parsed_url.path)
        response = requests.get(url)
        with open(files / path.name, "wb") as f:
            f.write(response.content)

        view_box = get_view_box(response.content)

        argument_to_modify = "output_width" if view_box.width > view_box.height else "output_height"
        file_suffix = ""

        if arguments:
            desired_sizes = [int(arguments[0])]

            if len(arguments) > 1:
                specification = arguments[1]

                if specification == "-h":
                    argument_to_modify = "output_height"
                    file_suffix = "h"
                elif specification == "-w":
                    argument_to_modify = "output_width"
                    file_suffix = "w"

        for size in desired_sizes:

            cairosvg.svg2png(
                bytestring=response.content,
                write_to=f"{files / path.name}_{size}{file_suffix}.png",
                **{argument_to_modify: size},
            )

        user_input = input("Enter the URL: ")


if __name__ == "__main__":

    app()
