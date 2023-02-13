"""
Icepak: Importing a PCB and its components via IDF and EDB
----------------------------------------------------------
This example shows how to import a PCB and its components using IDF files (*.ldb/*.bdf).
The *.emn/*.emp combination can also be used in a similar way.
"""

###############################################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports including the opertaing system, Ansys PyAEDT packages.
# Generic Python packages

import os

# PyAEDT Packages

from pyaedt import Icepak
from pyaedt import Desktop
from pyaedt import Hfss3dLayout
from pyaedt.modules.Boundary import BoundaryObject

###############################################################################################
# Input variables, launching AEDT
# The following code will create all input variables that are needed to run this example.
# The selected AEDT version is 23.1 and the project name can be anything.
# This part also sets the path name for the AEDT project.
# It will launch AEDT 2023 R1 in graphical mode.


desktop = Desktop("2023.1", non_graphical=False, new_desktop_session=True)   # New AEDT 23.1 session in graphical mode 
project_name = "Icepak_ECAD_Import.aedt"                                     # Prject name
project_name_full = os.path.join(os.getcwd(), project_name)                  # Project path,  os.getcwd() gets the current path of this Jupyter project


# ## Add an Icepak design to the current project

# In[3]:


ipk = Icepak(project_name_full, designname = "IcepakDesign_ECAD_Import")         # Icepak design name in the project
ipk.save_project()                                                         # Saves the project


# ## Import the IDF files
# Sample *.bdf and *.ldf files are presented here.
# ![bdf.PNG](attachment:bdf.PNG)
# ![ldf.PNG](attachment:ldf.PNG)

# In[4]:


# Imports the idf files with several filtering options incluing caps, resistors, inductors, power, size, ...
# There are also options for the PCB creation (number o flayers, copper percentages, layer sizes). 
# In this examples, the default values are used for the PCB.
# The imported PCB here will be deleted later and replaced by a PCB that has the trace information for higher accuracy.

board_path = os.path.join(os.getcwd(), 'A1.bdf')     # the *.bdf board file name in the current path 
library_path = os.path.join(os.getcwd(), 'A1.ldf')   # the *.ldf library file name in the current path 

ipk.import_idf(board_path, library_path=None, control_path=None, 
                  filter_cap=False, filter_ind=False, filter_res=False, 
                  filter_height_under=None, filter_height_exclude_2d=False, 
                  power_under=None, create_filtered_as_non_model=False, 
                  high_surface_thick='0.07mm', low_surface_thick='0.07mm', 
                  internal_thick='0.07mm', internal_layer_number=2, 
                  high_surface_coverage=30, low_surface_coverage=30, 
                  internal_layer_coverage=30, trace_material='Cu-Pure', 
                  substrate_material='FR-4', create_board=True, 
                  model_board_as_rect=False, model_device_as_rect=True, 
                  cutoff_height='5mm', component_lib='')


# ## Fit to scale, save the project

# In[5]:


ipk.modeler.fit_all()    # scales to fit all objects in AEDT
ipk.save_project()       # saves the project


# ## Add an HFSS 3D Layout design with the layout information of the PCB

# In[6]:


Layout_name = 'A1_uprev'          # 3D layout name available for import, the extension of .aedb should not be listed here

hfss3dLO = Hfss3dLayout(project_name.split('.aedt')[0], 'PCB_temp')      # adding a dummy HFSS 3D layout to the current project

edb_full_path = os.path.join(os.getcwd(), Layout_name+'.aedb\edb.def')   # path to the EDB file
hfss3dLO.import_edb(edb_full_path)                                       # importing the EDB file           
hfss3dLO.save_project()                                                  # save the new project so files are stored in the path     

ipk.delete_design(name='PCB_temp', fallback_design=None)                 # deleting the dummy layout from the original project


# In[7]:


# This part creates a 3D component PCB in Icepak from the imported EDB file
# 1 watt is assigned to the PCB as power input

component_name = "PCB_ECAD"

odb_path = os.path.join(os.getcwd(), Layout_name+'.aedt')
ipk.create_pcb_from_3dlayout(
    component_name, odb_path, Layout_name, resolution=2, extenttype="Polygon", outlinepolygon='poly_0', 
    custom_x_resolution=None, custom_y_resolution=None,power_in=1)


# ## Delete PCB objects
# Delete the PCB object from IDF import.

# In[8]:


ipk.modeler.delete_objects_containing("IDF_BoardOutline", False)


# ## Compute power budget

# In[9]:


# creates a setup to be able to calculate the power
ipk.create_setup("setup1")

power_budget, total = ipk.post.power_budget("W")
print(total)


# ## Closing and releasing AEDT

# In[10]:


ipk.close_project()      # close the project
ipk.release_desktop()    # release the AEDT session.  If this step is missing, AEDT cannot be closed.


# In[ ]:




