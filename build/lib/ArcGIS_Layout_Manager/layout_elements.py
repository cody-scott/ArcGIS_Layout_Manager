class BaseElement(object):
    elementHeight = 0.0
    elementPositionX = 0.0
    elementPositionY = 0.0
    elementWidth = 0.0
    name = ""

    def __init__(self, layout_object):
        if type(layout_object) is dict:
            self.name = layout_object.get("name")
            self.elementHeight = layout_object.get("elementHeight")
            self.elementWidth = layout_object.get("elementWidth")
            self.elementPositionX = layout_object.get("elementPositionX")
            self.elementPositionY = layout_object.get("elementPositionY")
        else:
            self.name = layout_object.name
            self.elementHeight = layout_object.elementHeight
            self.elementWidth = layout_object.elementWidth
            self.elementPositionX = layout_object.elementPositionX
            self.elementPositionY = layout_object.elementPositionY

    def to_dictionary(self):
        dict_item = {
            "name": self.name,
            "elementHeight": self.elementHeight,
            "elementWidth": self.elementWidth,
            "elementPositionX": self.elementPositionX,
            "elementPositionY": self.elementPositionY
        }
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        arcpy_layout_object.name = self.name
        arcpy_layout_object.elementHeight = self.elementHeight
        arcpy_layout_object.elementWidth = self.elementWidth
        arcpy_layout_object.elementPositionX = self.elementPositionX
        arcpy_layout_object.elementPositionY = self.elementPositionY


class DataFrameElement(BaseElement):
    XMin = 0.0
    XMax = 0.0
    YMin = 0.0
    YMax = 0.0

    def __init__(self, layout_object):
        super(DataFrameElement, self).__init__(layout_object)
        if type(layout_object) is dict:
            self.XMin = layout_object.get('XMin')
            self.XMax = layout_object.get('XMax')
            self.YMin = layout_object.get('YMin')
            self.YMax = layout_object.get('YMax')
        else:
            extent_item = layout_object.extent
            self.XMin = extent_item.XMin
            self.XMax = extent_item.XMax
            self.YMin = extent_item.YMin
            self.YMax = extent_item.YMax


    def to_dictionary(self):
        dict_item = super(DataFrameElement, self).to_dictionary()
        dict_item['XMin'] = self.XMin
        dict_item['XMax'] = self.XMax
        dict_item['YMin'] = self.YMin
        dict_item['YMax'] = self.YMax
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(DataFrameElement, self).update_map_feature(arcpy_layout_object)
        df_extent = arcpy_layout_object.extent
        df_extent.XMin = self.XMin
        df_extent.XMax = self.XMax
        df_extent.YMin = self.YMin
        df_extent.YMax = self.YMax
        arcpy_layout_object.extent = df_extent


class GraphicElement(BaseElement):
    def __init__(self, layout_object):
        super(GraphicElement, self).__init__(layout_object)

    def to_dictionary(self):
        dict_item = super(GraphicElement, self).to_dictionary()
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(GraphicElement, self).update_map_feature(arcpy_layout_object)


class LegendElement(BaseElement):
    title = ""

    def __init__(self, layout_object):
        super(LegendElement, self).__init__(layout_object)
        if type(layout_object) is dict:
            self.title = layout_object.get('title')
        else:
            self.title = layout_object.title

    def to_dictionary(self):
        dict_item = super(LegendElement, self).to_dictionary()
        dict_item["title"] = self.title
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(LegendElement, self).update_map_feature(arcpy_layout_object)
        arcpy_layout_object.title = self.title


class MapSurroundElement(BaseElement):
    def __init__(self, layout_object):
        super(MapSurroundElement, self).__init__(layout_object)

    def to_dictionary(self):
        dict_item = super(MapSurroundElement, self).to_dictionary()
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(MapSurroundElement, self).update_map_feature(arcpy_layout_object)


class PictureElement(BaseElement):
    sourceImage = ""

    def __init__(self, layout_object):
        super(PictureElement, self).__init__(layout_object)
        if type(layout_object) is dict:
            self.sourceImage = layout_object.get('sourceImage')
        else:
            self.sourceImage = layout_object.sourceImage

    def to_dictionary(self):
        dict_item = super(PictureElement, self).to_dictionary()
        dict_item['sourceImage'] = self.sourceImage
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(PictureElement, self).update_map_feature(arcpy_layout_object)
        arcpy_layout_object.sourceImage = self.sourceImage


class TextElement(BaseElement):
    angle = 0.0
    fontSize = 0.0
    text = ""

    def __init__(self, layout_object):
        super(TextElement, self).__init__(layout_object)
        if type(layout_object) is dict:
            self.angle = layout_object.get('angle')
            self.fontSize = layout_object.get('fontSize')
            self.text = layout_object.get('text')
        else:
            self.angle = layout_object.angle
            self.fontSize = layout_object.fontSize
            self.text = layout_object.text

    def to_dictionary(self):
        dict_item = super(TextElement, self).to_dictionary()
        dict_item['angle'] = self.angle
        dict_item['fontSize'] = self.fontSize
        dict_item['text'] = self.text
        return dict_item

    def update_map_feature(self, arcpy_layout_object):
        super(TextElement, self).update_map_feature(arcpy_layout_object)
        arcpy_layout_object.angle = self.angle
        arcpy_layout_object.fontSize = self.fontSize
        arcpy_layout_object.text = self.text
