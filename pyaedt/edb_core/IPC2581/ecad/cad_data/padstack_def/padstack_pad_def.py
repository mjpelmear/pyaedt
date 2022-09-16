import xml.etree.cElementTree as ET


class PadstackPadDef(object):
    def __init__(self):
        self.layer_ref = ""
        self.pad_use = PadUse().Regular
        self.x = 0.0
        self.y = 0.0
        self.primitive_ref = "CIRCLE_DEFAULT"

    def write_xml(self, padstack_def):
        if padstack_def:
            pad_def = ET.SubElement(padstack_def, "PadstackPadDef")
            pad_def.set("layerRef", self.layer_ref)
            pad_def.set("padUse", self.pad_use)
            location = ET.SubElement(pad_def, "Location")
            location.set("x", self.x)
            location.set("y", self.y)
            standard_primitive = ET.SubElement(pad_def, "StandardPrimitiveRef")
            standard_primitive.set("id", self.primitive_ref)


class PadUse(object):
    (Regular, Antipad, Thermal) = range(1, 3)
