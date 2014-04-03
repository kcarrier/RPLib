createversions
================================

:mod:`RPLib` -- createversions
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: createversions

Usage
---------------------------------------------
* **Only works with enterprise geodatabases.**
* **The output version name is prefixed by the geodatabase user name**
    * **for example, SDE.version1**
* **The output version's permissions are set to public by default.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"
        createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

        RPLib.createversions(sdeOwner,createVersions_List,True,"sde.default")

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"
        createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

        RPLib.createversions(sdeOwner,createVersions_List)

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**
    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"
        createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

        if RPLib.createversions(sdeOwner,createVersions_List,True,"sde.default"):
            print("successful, run another tool")
        else:
            print("failed, run another tool")

Example 4
---------------------------------------------
    **Notice you do not need to specify the PublicAccess or ParentVersion parameters because by default:**
      * **PublicAccess = True**
      * **ParentVersion = "sde.default"**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"
        createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

        if RPLib.createversions(sdeOwner,createVersions_List):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
