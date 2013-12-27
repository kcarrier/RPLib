compressgdb
================================

:mod:`RPLib` -- compressgdb
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: compressgdb

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **To improve geodatabase performance, the geodatabase should be compressed periodically.**
* **A compressed geodatabase is more efficient. A geodatabase that is never compressed is more likely to develop errors.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.***
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        RPLib.compressgdb(sdeOwner)

Example 2
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        if RPLib.compressgdb(sdeOwner):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
