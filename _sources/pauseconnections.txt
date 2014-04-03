pauseconnections
================================

:mod:`RPLib` -- pauseconnections
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: pauseconnections

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **This function is used by an administrative user to temporarily block connections to an Enterprise geodatabase.**
* **If this function is attempted to be run by a non-administrative user the function will fail.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        RPLib.pauseconnections(sdeOwner)

Example 2
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        if RPLib.pauseconnections(sdeOwner):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
