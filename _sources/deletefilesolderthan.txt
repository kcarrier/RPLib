deletefilesolderthan
================================

:mod:`RPLib` -- deletefilesolderthan
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: deletefilesolderthan

Usage
---------------------------------------------
* **Used to manage logfiles created over a period of time.**
* **Delete log files old than a certain number of days than the current date**

Example 1
---------------------------------------------
    | **Simple call with all parameters specified.**
    | **Delete files older than 14 days or 2 weeks.**

    ::

        import RPLib

        NumberOfDays = 14
        LogFileLoc = "C:/GIS/Logs"

        RPLib.deletefilesolderthan(NumberOfDays,LogFileLoc)

    * **Note All files within this directory will be deleted if they are older than the specified date.**

Example 2
---------------------------------------------
    | **Simple call with all parameters specified.**
    | **Delete files older than 7 days or 1 weeks.**
    | **All files within this directory will be deleted if they are older than the specified date.**
    | **Notice that here we are using a UNC path**

    ::

        import RPLib

        NumberOfDays = 7
        LogFileLoc = "//GIS-SERVER/Scripts/Logs"

        RPLib.deletefilesolderthan(NumberOfDays,LogFileLoc)

Example 3
---------------------------------------------
    | **If Else logic with all parameters specified.**
    | **Delete files older than 21 days or 3 weeks.**
    | **All files within this directory will be deleted if they are older than the specified date.**
    | **Notice that here we are using a UNC path**

    ::

        import RPLib

        NumberOfDays = 21
        LogFileLoc = "//GIS-SERVER/Scripts/Logs"

        if RPLib.deletefilesolderthan(NumberOfDays,LogFileLoc):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

    * **Note - This will start the main ArcGIS Server service through the Windows Services Console.**
