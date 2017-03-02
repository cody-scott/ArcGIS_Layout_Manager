class TableOfContentsItem(object):
    layer_name = ""
    long_name = ""
    visible = True
    group_layer = False
    transparency = 0.0

    def __init__(self, layer_object):
        if type(layer_object) is dict:
            self.visible = layer_object.get('visible')
            self.long_name = layer_object.get('long_name')
            self.transparency = layer_object.get('transparency')
            self.layer_name = layer_object.get('layer_name')
            self.group_layer = layer_object.get('group_layer')
        else:
            if self._supports(layer_object, "VISIBLE"):
                self.visible = layer_object.visible
            else:
                self.visible = None

            if self._supports(layer_object, "LONGNAME"):
                self.long_name = layer_object.longName
            else:
                self.long_name = None

            if self._supports(layer_object, "TRANSPARENCY"):
                self.transparency = layer_object.transparency
            else:
                self.transparency = None

            if self._supports(layer_object, "NAME"):
                self.layer_name = layer_object.name
            else:
                self.layer_name = None

            if layer_object.isGroupLayer:
                self.group_layer = True
            else:
                self.group_layer = False

    def _supports(self, layer_object, support_arg):
        return layer_object.supports(support_arg)

    def to_dictionary(self):
        dict_item = {
            'layer_name': self.layer_name,
            'long_name': self.long_name,
            'visible': self.visible,
            'group_layer': self.group_layer,
            'transparency': self.transparency
        }
        return dict_item

    def update_toc_feature(self, arcpy_toc_object):
        # if self.layer_name is not None:
        #     arcpy_toc_object.name = self.layer_name
        # if self.long_name is not None:
        #     arcpy_toc_object.name = self.long_name
        if self.transparency is not None:
            arcpy_toc_object.transparency = self.transparency
        if self.visible is not None:
            arcpy_toc_object.visible = self.visible