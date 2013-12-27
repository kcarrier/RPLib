resumeconnections
================================

:mod:`RPLib` -- resumeconnections
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: resumeconnections

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **This function is used by an administrative user to unblock or allow connections to an Enterprise geodatabase.**
* **If connections are blocked or paused this function will need to be used so new connections can once again be made to the geodatabase.**
* **If this function is attempted to be run by a nonadministrative user the function will fail.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        RPLib.resumeconnections(sdeOwner)

Example 2
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        if RPLib.resumeconnections(sdeOwner):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
