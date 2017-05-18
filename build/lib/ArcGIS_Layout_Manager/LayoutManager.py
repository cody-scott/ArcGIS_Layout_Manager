


import json
import logging

import os

import arcview
import arcpy

from . import layout_elements, exceptions, table_of_contents_elements

"""
Layout Manager to help with managing multiple ArcGIS Layouts in a single map document
Data for the layout is stored within an associated json file based on the map title
Ex: test.mxd -> test_layout.json
Properties
"""

class LayoutManager(object):
    """
    move_missing_off_screen - automatically moves layout item off screen if not in layout manager (default: True)
    auto_save - auto save the layout when changing between active layouts or updating layout (default: True)
    active_layout - Current active layout
    toc_active - Controls if the table of contents are updated when the layout changes (default: True)
    lyr_active - Controls if the map layout objects are updated when the layout changes (default: True)
    """

    # Moves any missing element from the current layout off screen
    move_missing_off_screen = True

    # Auto save the json contents after a change
    auto_save = True

    # Currently Active Layout
    active_layout = None

    # Should it modify Table of Contents
    toc_active = True

    # Should it modify Layers
    lyr_active = True

    _within_arcmap = False

    _is_active = False
    _mxd = None
    _mxd_name = None
    _mxd_source_path = None
    _layout_json_path = None

    _layouts = {}

    _layout_object_mapper = {
        "DATAFRAME_ELEMENT": layout_elements.DataFrameElement,
        "GRAPHIC_ELEMENT": layout_elements.GraphicElement,
        "LEGEND_ELEMENT": layout_elements.LegendElement,
        "MAPSURROUND_ELEMENT": layout_elements.MapSurroundElement,
        "PICTURE_ELEMENT": layout_elements.PictureElement,
        "TEXT_ELEMENT": layout_elements.TextElement
    }

    def __init__(self, **kwargs):
        """
        Activate Layout Manager
        Will look for layout json file within same folder as map document or create one if nothing is found
        :param kwargs:
        mxd_path
        mxd
        :type kwargs:
        mxd_path = string
        mxd =  arcpy.mapping.MapDocument
        Nothing to use "CURRENT" if working within ArcMap
        """
        try:
            mxd = kwargs.get("mxd")
            mxd_path = kwargs.get("mxd_path")

            self.log_or_print("starting layout mapper", logging.info)

            if type(mxd) == arcpy.mapping.MapDocument:
                self.log_or_print("Using supplied MXD", logging.info)
                self._mxd = mxd
            else:
                if mxd_path is None:
                    self.log_or_print("Using \"CURRENT\" map document", logging.info)
                    self._mxd = arcpy.mapping.MapDocument("CURRENT")
                    self._within_arcmap = True
                elif os.path.isfile(mxd_path):
                    self.log_or_print("Using map document from {}".format(mxd_path), logging.info)
                    self._mxd = arcpy.mapping.MapDocument(mxd_path)
                else:
                    raise exceptions.MXD_ERROR()

            self._activate_mapper()
            self._is_active = True

            layout_items = self._get_layouts()
            if len(layout_items) > 0:
                self.auto_save = False
                self.active_layout = layout_items[0]
                self.switch_layout(self.active_layout)
                self.auto_save = True

        except exceptions.MXD_ERROR as mxd_error:
            self.log_or_print("Error activating MXD", logging.error)
            self.log_or_print("Confirm MXD Path and re-init", logging.error)
        except Exception as e:
            logging.error(e.message)

    def __del__(self):
        del(self._mxd)

    def _get_mxd_source_path(self):
        self.log_or_print("Getting MXD Name and Source Path", logging.info)
        mxd_file_path = self._mxd.filePath
        mxd_source = self._mxd.filePath.replace("\\{}".format(mxd_file_path.split("\\")[-1]), "")
        self._mxd_source_path = mxd_source
        self._mxd_name = mxd_file_path.split("\\")[-1].replace(".mxd", "")
        json_path = os.path.join(self._mxd_source_path, "{}_layout.json".format(self._mxd_name))
        self._layout_json_path = json_path
        return mxd_source

    def _activate_mapper(self):
        if self._is_active:
            self.log_or_print("Mapper already active", logging.warning)

        self._get_mxd_source_path()

        if not os.path.isfile(self._layout_json_path):
            with open(self._layout_json_path, 'w') as fl:
                fl.write("[]")
        else:
            self._read_layout()
        return

    def _read_layout(self):
        self.log_or_print("Loading layout JSON", logging.info)
        data = None
        with open(self._layout_json_path, 'r') as fl:
            data = json.loads(fl.read())

        return_data = {}
        for val in data:
            layout_name = val.get('layout_name')
            layout_types = {}
            layout_items = val.get('layout_items')
            self.toc_active = val.get('toc_active', True)
            self.lyr_active = val.get('lyr_active', True)

            for item in layout_items:
                layout_type_dct = {}
                for ty in layout_items[item]:
                    obj = self._layout_object_mapper[item](ty)
                    layout_type_dct[obj.name] = obj
                layout_types[item] = layout_type_dct

            toc_types = {}
            toc_items = val.get('toc_items', {})
            for item in toc_items:
                toc_val = table_of_contents_elements.TableOfContentsItem(toc_items[item])
                toc_types[toc_val.long_name] = toc_val

            return_data[layout_name] = {
                'layout_name': layout_name,
                'layout_items': layout_types,
                'toc_items': toc_types,
            }

        self._layouts = return_data
        return self._layouts

    def save_layout_json(self):
        self._get_mxd_source_path()
        self.log_or_print("Saving layout JSON to {}".format(self._layout_json_path), logging.info)
        out_data = []
        for item_name in self._layouts:
            item = self._layouts[item_name]
            out_name = item.get('layout_name')
            layouts = {}
            layout_items = item.get('layout_items')
            for item1 in layout_items:
                layout_sub = []
                for sub in layout_items[item1]:
                    layout_sub.append(layout_items[item1][sub].to_dictionary())
                layouts[item1] = layout_sub

            toc = {}
            toc_items = item.get('toc_items', {})
            for item in toc_items:
                toc_val = toc_items[item]
                toc[toc_val.long_name] = toc_val.to_dictionary()

            out_data.append({
                "layout_name": out_name,
                "layout_items": layouts,
                'toc_items': toc,
                'toc_active': self.toc_active,
                'lyr_active': self.lyr_active
            })

        with open(self._layout_json_path, 'w') as fl:
            fl.write(json.dumps(out_data, indent=4))

        return

    def create_layout(self, layout_name):
        try:
            if layout_name in self._get_layouts():
                raise exceptions.LayoutExists()

            self.log_or_print("Creating new layout \"{}\"".format(layout_name), logging.info)
            new_layout = self._generate_layout(layout_name)
            self._layouts[new_layout.get('layout_name')] = new_layout
            self.active_layout = layout_name

            if self.auto_save:
                self.save_layout_json()

        except exceptions.LayoutExists as le:
            self.log_or_print("Layout \"{}\" Exists - Choose a new name".format(layout_name), logging.error)

    def _generate_layout(self, layout_name):
        toc_items = self._get_table_of_contents()
        layout_items = self._get_layout_items()
        layout_dct = {
            'layout_name': layout_name,
            'layout_items': layout_items,
            'toc_items': toc_items
        }
        return layout_dct

    def _get_layout_items(self):
        # search mxd
        logging.info("Collecting layout elements info")
        layout_list_items = {
            "DATAFRAME_ELEMENT": {},
            "GRAPHIC_ELEMENT": {},
            "LEGEND_ELEMENT": {},
            "MAPSURROUND_ELEMENT": {},
            "PICTURE_ELEMENT": {},
            "TEXT_ELEMENT": {}
        }

        existing_names = []
        for layout_item in arcpy.mapping.ListLayoutElements(self._mxd):
            item = self._layout_object_mapper[layout_item.type](layout_item)
            if not self._check_unique_name(item.name, existing_names):
                item.name = self._create_unique_name(layout_item.type, existing_names)
                layout_item.name = item.name
            existing_names.append(item.name)
            layout_list_items[layout_item.type][item.name] = item

        return layout_list_items

    def _check_unique_name(self, name, existing_names):
        if name in existing_names or name is None or name == "":
            self.log_or_print("{} not unique".format(name), logging.info)
            return False
        else:
            self.log_or_print("{} unique".format(name), logging.info)
            return True

    def _create_unique_name(self, base_type, existing_names):
        name = None
        layout_iterator = 0
        while not self._check_unique_name(name, existing_names):
            layout_iterator += 1
            name = "{}_LAYOUT_{}".format(base_type, layout_iterator)
        return name

    def _get_table_of_contents(self):
        self.log_or_print("Generating Table of contents", logging.info)
        layers = {}
        for lyr in arcpy.mapping.ListLayers(self._mxd):
            item = table_of_contents_elements.TableOfContentsItem(lyr)
            layers[item.long_name] = item
        return layers

    def switch_layout(self, new_layout):
        try:
            if self.auto_save:
                self.update_layout()
                self.save_layout_json()

            self.log_or_print("Switching Layout to {}".format(new_layout), logging.info)
            layout_data = self._layouts.get(new_layout)
            if layout_data is None:
                raise exceptions.MissingLayout()

            self.active_layout = layout_data.get('layout_name')
            layout_items = layout_data.get('layout_items')
            toc_items = layout_data.get('toc_items')

            if self.lyr_active:
                self.log_or_print("Updating Layout properties", logging.info)
                for item in arcpy.mapping.ListLayoutElements(self._mxd):
                    layout_element = layout_items.get(item.type, {}).get(item.name, None)
                    if layout_element is not None:
                        layout_element.update_map_feature(item)
                    else:
                        if self.move_missing_off_screen:
                            self.log_or_print('"{}" not found. Moving off screen'.format(item.name), logging.warning)
                            max_x = self._mxd.pageSize.width + item.elementPositionX + 20
                            item.elementPositionX = max_x
                        else:
                            self.log_or_print('"{}" not found.'.format(item.name), logging.warning)

            if self.toc_active:
                self.log_or_print("Updating Table of Contents properties", logging.info)
                for item in arcpy.mapping.ListLayers(self._mxd):
                    toc_var = toc_items.get(item.longName, None)
                    if toc_var is not None:
                        toc_var.update_toc_feature(item)
                    else:
                        self.log_or_print("TOC Item {} is not found in layout manager".format(item.longName), logging.warning)


            if self._within_arcmap:
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()

        except exceptions.MissingLayout as ml:
            self.log_or_print("Layout \"{}\" doesnt exists - please create or check".format(new_layout), logging.error)
        except Exception as e:
            self.log_or_print(e.message, logging.error)

    def update_layout(self, layout_name=None):
        try:
            if layout_name is None:
                new_layout = self._generate_layout(self.active_layout)
                self._layouts[self.active_layout] = new_layout
            else:
                new_layout = self._generate_layout(layout_name)
                self._layouts[layout_name] = new_layout

            if self.auto_save:
                self.save_layout_json()

        except Exception as e:
            self.log_or_print(e.message, logging.error)

    def _get_layouts(self):
        layout_list = []
        for item in self._layouts:
            layout_list.append(self._layouts[item].get('layout_name', ""))
        return  layout_list

    def list_layouts(self):
        layout_list = self._get_layouts()
        outstr = "\n".join(layout_list)
        self.log_or_print(outstr, logging.info)
        return layout_list

    def log_or_print(self, message, log_item):
        """
        Fire log message and print within arcmap
        Arcmap doesn't seem to display messages from logging
        :param message: message to log
        :type message:
        :param log_item: logging method
        :type log_item:
        :return:
        :rtype:
        """
        if self._within_arcmap:
            print(message)
        else:
            log_item(message)
