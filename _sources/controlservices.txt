controlservices
================================

:mod:`RPLib` -- controlservices
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: controlservices

Usage
---------------------------------------------
* **If using feature services with ArcGIS Server your data needs to reside in an SDE database.**
* **During database maintenance a database administrator might need to remove locks created by these services by stopping them.**
* **Map services created using data from an SDE database will also produce locks on your data by default.**
* **Typically for a full compress on SDE to be achieved all connections need to be severed, this includes connections from ArcGIS Server.**


Example 1
---------------------------------------------
    | **Simple call with all parameters specified.**
    | **Notice that here we are using the IP address instead of the server name.**

    ::

        import RPLib

        folder = "LandRecords"

        RPLib.controlservices(folder,"stop","192.1.1.1","administrator","password")

    * **Note This will stop all services in the folder LandRecords on ArcGIS Server.**

Example 2
---------------------------------------------
    | **Simple call with all parameters specified.**
    | **Notice that here we are using the server name instead of the IP address.**

    ::

        import RPLib

        RPLib.controlservices("ALL","stop","GISAPP","administrator","password")

    * **Note - This will stop the main ArcGIS Server service through the Windows Services Console.**

Example 3
---------------------------------------------
    | **If Else logic with all parameters specified.**
    | **Notice that here we are using the server name instead of the IP address.**

    ::

        import RPLib

        if RPLib.controlservices("ALL","start","GISAPP","administrator","password"):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

    * **Note - This will start the main ArcGIS Server service through the Windows Services Console.**

Example 4
---------------------------------------------
    | **If Else logic with all parameters specified.**
    | **Notice that here we are using the IP address instead of the servername.**

    ::

        import RPLib

        folder = "LandRecords"

        if RPLib.controlservices(folder,"start","192.1.1.1","administrator","password"):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

    * **Note This will start all services in the folder LandRecords on ArcGIS Server.**
