# Installation
ArcGIS installation is required

Install package via pip

    pip install ArcGIS_Layout_Manager
    
Can either install to the global site packages or if you wish to keep in a virtual environment but use arcpy, toggle global site packages on your virtual environment

    toggleglobalsitepackages -q
    
    
# Usage

Can function from within ArcMap or within a seperate script

Initialize within ArcMap

    from ArcGIS_LayoutManager import LayoutManager
    lm = LayoutManager()

Initialize from script

Using path to mxd file

    from ArcGIS_LayoutManager import LayoutManager
    mxd_path = r'C:\sample.mxd'
    lm = LayoutManager(mxd_path=mxd_path)
    
or using arcpy.mapping.MapDocument class

    from ArcGIS_LayoutManager import LayoutManager
    mxd = already started arcpy.mapping.MapDocument
    lm = LayoutManage(mxd=mxd)
