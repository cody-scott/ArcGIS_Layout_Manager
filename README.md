# Installation
ArcGIS installation is required

Install package via pip

    pip install ArcGIS_Layout_Manager
    
Can either install to the global site packages or if you wish to keep in a virtual environment but use arcpy, toggle global site packages on your virtual environment

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

Each layout you would like to use requires a layout to be created. Do this by calling 

    lm.create_layout("Layout Name")
