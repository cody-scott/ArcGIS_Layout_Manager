# Installation
ArcGIS installation is required

Install package via pip

    pip install ArcGIS_Layout_Manager
    
Can either install to the global site packages or if you wish to keep in a virtual environment but use arcpy, toggle global site packages on your virtual environment

    toggleglobalsitepackages -q
    
    
# Usage

Can function from within ArcMap or within a seperate script

Initalize

    from ArcGIS_LayoutManager import LayoutManager
    lm = LayoutManager()
