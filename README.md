# About
This package was created to help with the issues of managing multiple map layouts within a single ArcMap document. 
As it stands currently, the arcpy.mapping package provides many great tools to manipulate map documents to create map books, and manage multiple layouts, but it is cumbersome to create each time.

The LayoutManager attempts to help this by tracking the location and details of Layout Objects on your map document, as well as table of contents items including if it is turned on/off, and transparency.

The data associated with the LayoutManager is stored in JSON which can be easily changed outside of ArcMap.

Finally, the package is usable from within ArcMap's python window, or incorporated into exernal scripts.

# Use Cases

Some potential uses for this would include creating multiple maps that toggle layers on and off in the table of contents.
Creating Data Driven pages that require moving items on and off the map layout.

Many More!

# Installation
ArcGIS installation is required

Install package via pip

    pip install ArcGIS_Layout_Manager
    
To use within ArcMap, install to the global site packages or if you wish to keep in a virtual environment but use arcpy, toggle global site packages on your virtual environment

    toggleglobalsitepackages -q
    
    
# Usage

## Initialize
Can function from within ArcMap or within a seperate script

Within ArcMap

    from ArcGIS_LayoutManager import LayoutManager
    lm = LayoutManager()

From script

Using path to mxd file

    from ArcGIS_LayoutManager import LayoutManager
    mxd_path = r'C:\sample.mxd'
    lm = LayoutManager(mxd_path=mxd_path)
    
or using arcpy.mapping.MapDocument class

    from ArcGIS_LayoutManager import LayoutManager
    mxd = already started arcpy.mapping.MapDocument
    lm = LayoutManage(mxd=mxd)

A layout.json file is created within the same folder as the map document taking the map document name as the beginning
Using the above example, the file would be called sample_layout.json in the folder

* C:\sample.mxd
* C:\sample_layout.json

## Create New Layout

Each layout you would like to use requires a layout to be created.

    lm.create_layout("Layout Name")

Each layout name must be unique. To check existing names call

    lm.list_layouts()
    
## Changing Layouts

To change between your created layouts call

    lm.switch_layout("Layout Name")
    
## Updating Layouts

Once you made one or many changes to a layout within ArcMap, you'll need to update the current layout data.
For your currently activate layout:

    lm.update_layout()
    
For a specific layout

    lm.update_layout("Layout Name")

# Properties

The LayoutManager has a number of properties that can be set according to your want and needs

### Auto Save
Auto Save JSON file when changing to a new layout, updating current layout, or creating new layout.
    
    lm.auto_save = True/False
    
### Move Missing Off Screen
If the LayoutManager encounters a new item that you have added to the layout, but have not updated the active layout to include (such as a new text box or scale bar), then you can chose to either keep it in place in the new layout, or move it off screen.
You can also affix it to a new location and call update_layout() to save its place for future.

    move_missing_off_screen = True/False
