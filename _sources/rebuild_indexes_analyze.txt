rebuild_indexes_analyze
================================

:mod:`RPLib` -- rebuild_indexes_analyze
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: rebuild_indexes_analyze

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **After data loading, deleting, updating, and compressing operations, it is important to rebuild indexes and update statistics in the database.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"
        # Exlude tables that have the below variations in their name from the process.
        # Views will typically throw errors with this tool.
        excludeList = ['VW_', '_VW', 'V_', '_V',]

        RPLib.rebuild_indexes_analyze(dataOwner, excludeList, False, True, False, True, True, True)

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**
    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        RPLib.rebuild_indexes_analyze(dataOwner)

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**

    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"
        # Exlude tables that have the below variations in their name from the process.
        # Views will typically throw errors with this tool.
        excludeList = ['VW_', '_VW', 'V_', '_V',]

        if RPLib.rebuild_indexes_analyze(dataOwner, excludeList, False, True, False, True, True, True):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

Example 4
---------------------------------------------
    **Notice you do not need to specify these parameters because by default:**
      * **excludeList = Is an empty list by default**
      * **include_system  = False**
          * **You must be the geodatabase administrator for this option to be True.**
      * **delta_only      = True**
      * **analyze_base    = True**
      * **analyze_delta   = True**
      * **analyze_archive = True**
      * **include_system  = True**

    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        if RPLib.rebuild_indexes_analyze(dataOwner):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
