truncateappend
================================

:mod:`RPLib` -- truncateappend
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: truncateappend

Usage
---------------------------------------------
* **Append data from a Source object to a Destination/Target object.**
* **Destination/Target object cannot be versioned.**
* **An exclusive schema lock is not needed to update data in the Destination/Target object, it can be used.**
* **If you do not want to create a replica or do not have the ability to create replicas this could be used in place of replicas.**
* **If you have ArcGIS Server services pointed to a file gdb, you could use this method to update objects in the file gdb without stopping your services.**
* **By adding a Date field to your Destination/Target object you can keep track of when the data was last updated.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**

    ::

        import RPLib

        # SDE SourceObject
        Source = "C:/GIS/GISADMIN@GIS.sde/GISADMIN.Parcels"

        # File gdb DestinationObject
        Destination = "Z:/LandRecords.gdb/Parcels"

        # File gdb, field in Parcels that is of type Date
        DateField = "LASTUPDATED"

        RPLib.truncateappend(Source,Destination,"100000",False,DateField)

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**

    ::

        import RPLib

        # SDE SourceObject
        Source = "C:/GIS/GISADMIN@GIS.sde/GISADMIN.Parcels"

        # File gdb DestinationObject
        Destination = "Z:/LandRecords.gdb/Parcels"

        RPLib.truncateappend(Source,Destination)

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**

    ::

        import RPLib

        # SDE SourceObject
        Source = "C:/GIS/GISADMIN@GIS.sde/GISADMIN.Parcels"

        # File gdb DestinationObject
        Destination = "Z:/LandRecords.gdb/Parcels"

        # File gdb, field in Parcels that is of type Date
        DateField = "LASTUPDATED"

        if RPLib.truncateappend(Source,Destination,"100000",False,DateField):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

Example 4
---------------------------------------------
    **Notice you do not need to specify these parameters because by default:**
      * **SourceObjectCount     = 0**
      * **ObjectsSchemaTest     = False**
      * **DestUpdateField       = None**
      * **FieldMappings         = None**
      * **Subtype               = None**

    ::

        import RPLib

        # SDE SourceObject
        Source = "C:/GIS/GISADMIN@GIS.sde/GISADMIN.Parcels"

        # File gdb DestinationObject
        Destination = "Z:/LandRecords.gdb/Parcels"

        # File gdb, field in Parcels that is of type Date
        DateField = "LASTUPDATED"

        if RPLib.truncateappend(Source,Destination):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
