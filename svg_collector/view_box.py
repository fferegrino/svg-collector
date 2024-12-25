import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class ViewBox:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1


def get_view_box(file: bytes) -> ViewBox:
    tree = ET.fromstring(file)
    view_box = tree.attrib.get("viewBox", None)
    if view_box:
        x1, y1, x2, y2 = map(float, view_box.split())
        return ViewBox(x1, y1, x2, y2)
    raise ValueError("No viewBox found in the SVG file")
