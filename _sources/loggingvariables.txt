Logging Variables
================================
    **Parameters that can be specified for logging the results of the script.**
    **All parameters are not required by default, although it is recommended that you use all 3 variables to track the status of the scripts so adjustments can be made over time.**

    ==================   ========  ============================================================================================================================================  =========
    Parameter            Type      Description                                                                                                                                   Required
    ==================   ========  ============================================================================================================================================  =========
    **verboseLog**       Boolean   Indicates if Esri geoprocessing messages will be output or if a simple Success or Failed message will appear                                  No

                                   - True = Esri geoprocessing messages will be the output

                                   - False = A simple message indicating whether a function was a Success or Failed **(Default)**

                                        - **Note: When first writing your script it is recommended to use True until everything works as expected then change to False.**

    **LogFileLoc**       String    Indicates a folder where log files will be stored, this can be a local or network location.                                                   No
    **Logger**           Function  Call this function and pass the LogFileLoc variable, this will ensure that all outputs are written to the console and the logfile             No
    ==================   ========  ============================================================================================================================================  =========

Usage
---------------------------------------------

    * **Logging the events within your script is vital especially for long running processes.**
    * **Knowing where, when, and why a function or script failed is essential for troubleshooting.**
    * **Consider setting RPLib.verboseLog = True when you are first getting started to get the Esri geoprocessing output messages. This will help provide a more detailed message.**
    * **Once you are more confident that all errors have been resolved consider changing RPLib.verboseLog = False so your log files become smaller and easier to read and manage.**
    * **All logging will be written to both the console and a log file so you can follow the script while it is running.**

Example 1
---------------------------------------------
    * **Verbose logging is turned on, meaning we will see the Esri geoprocessing output messages.**

    ::

        import RPLib

        LogFileLoc = ("C:/RPLib/Log")
        RPLib.verboseLog = True
        RPLib.Logger(LogFileLoc)

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        RPLib.clearworkspacecache(dataOwner)

    * **Would produce an output like below.**

    ::

        Clearing workspace cache for : C:\GIS\GISADMIN@GIS.sde ...
        Executing: ClearWorkspaceCache C:\GIS\GISADMIN@GIS.sde
        Start Time: Thu Dec 26 08:28:55 2013
        Succeeded at Thu Dec 26 08:28:55 2013 (Elapsed Time: 0.52 seconds)


Example 2
---------------------------------------------
    * **Verbose logging is turned off, meaning we will only see if the function was a Success or Failed.**

    ::

        import RPLib

        LogFileLoc = ("C:/RPLib/Log")
        RPLib.verboseLog = False
        RPLib.Logger(LogFileLoc)

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        RPLib.clearworkspacecache(dataOwner)

    * **Would produce an output like below if no errors were encountered:**

    ::

        Clearing workspace cache for : C:\GIS\GISADMIN@GIS.sde ... Success

    * **Would produce an output like below if errors were encountered:**

    ::

        Clearing workspace cache for : C:\GIS\GISADMIN@GIS.sde ... Failed
