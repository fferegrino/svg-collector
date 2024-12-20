import requests
import urllib.parse
from pathlib import Path
import cairosvg

files =  Path("downloads")
files.mkdir(parents=True, exist_ok=True)


user_input = input("Enter the URL: ")

desired_widths = [500, 1000, 2000]

while user_input != "q":
    
    url, *arguments = user_input.split(" ")

    parsed_url = urllib.parse.urlparse(url)
    path = Path(parsed_url.path)
    response = requests.get(url)
    with open(files / path.name, "wb") as f:
        f.write(response.content)

    if arguments:
        desired_widths = [int(arguments[0])]

    for width in desired_widths:
        cairosvg.svg2png(
            bytestring=response.content,
            write_to=f"{files / path.name}_{width}.png",
            output_width=width
        )

    user_input = input("Enter the URL: ")
