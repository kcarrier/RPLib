clearworkspacecache
================================

:mod:`RPLib` -- clearworkspacecache
--------------------------------------------
.. automodule:: RPLib
   :undoc-members:
   :show-inheritance:
.. autofunction:: clearworkspacecache

Usage
---------------------------------------------

* **Only works with enterprise geodatabases.**
* **Helps disconnect idle connections in long-running applications.**
* **Should be run at the end of a script.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        RPLib.clearworkspacecache(dataOwner)

Example 2
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        if RPLib.clearworkspacecache(dataOwner):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
