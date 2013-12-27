reconcilepost
================================

:mod:`RPLib` -- reconcilepost
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: reconcilepost

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **The reconcile process requires that you have full permissions to all the feature classes that have been modified in the version being edited.**
* **The reconcile process detects differences between the edit version and the target version and flags these differences as conflicts. If conflicts exist, they should be resolved.**
* **After running the reconcile process successfully with, all_versions = True, all vesions in the geodatabase will appear the same.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        RPLib.reconcilepost(sdeOwner,"C:/TESTGIS","","sde.DEFAULT",True,True,True,True,True,True,True)

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        RPLib.reconcilepost(sdeOwner,"C:/TESTGIS")

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        if RPLib.reconcilepost(sdeOwner,"C:/TESTGIS","","sde.DEFAULT",True,True,True,True,True,True,True):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

Example 4
---------------------------------------------
    **Notice you do not need to specify these parameters because by default:**
      * **versions           = None - Will gather all versions for the connection file used**
      * **parent_version     = "sde.default"**
      * **delete_version     = True**
      * **all_versions       = True**
      * **acquire_locks      = True**
      * **abort_if_conflicts = True**
      * **by_object          = True**
      * **favor_target       = True**
      * **post               = True**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        if RPLib.reconcilepost(sdeOwner,"C:/TESTGIS"):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
