syncreplicas
================================

:mod:`RPLib` -- syncreplicas
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: syncreplicas

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **The reconcile process requires that you have full permissions to all the feature classes that have been modified in the version being edited.**
* **The reconcile process detects differences between the edit version and the target version and flags these differences as conflicts. If conflicts exist, they should be resolved.**
* **After running the reconcile process successfully with the, all_versions = True, all vesions in the geodatabase will appear the same.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        # Local variables
        ParentGDB = "C:/GIS/GISADMIN@GIS.sde"
        ChildGDB = "Z:/LandRecords.gdb"
        RepName = "GISReplica"

        RPLib.syncreplicas(ParentGDB,ChildGDB,RepName,True,True,True,True)

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**
    ::

        import RPLib

        # Local variables
        ParentGDB = "C:/GIS/GISADMIN@GIS.sde"
        ChildGDB = "Z:/LandRecords.gdb"
        RepName = "GISReplica"

        RPLib.syncreplicas(ParentGDB,ChildGDB,RepName)

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        # Local variables
        ParentGDB = "C:/GIS/GISADMIN@GIS.sde"
        ChildGDB = "Z:/LandRecords.gdb"
        RepName = "GISReplica"

        if RPLib.syncreplicas(ParentGDB,ChildGDB,RepName,True,True,True,True):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

Example 4
---------------------------------------------
    **Notice you do not need to specify these parameters because by default:**
      * **GDB1_TO_2        = True**
      * **FAVOR_GDB1       = True**
      * **BY_OBJECT        = True**
      * **DO_NOT_RECONCILE = True**

    ::

        import RPLib

        # Local variables
        ParentGDB = "C:/GIS/GISADMIN@GIS.sde"
        ChildGDB = "Z:/LandRecords.gdb"
        RepName = "GISReplica"

        if RPLib.syncreplicas(ParentGDB,ChildGDB,RepName):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
