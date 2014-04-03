executesql
================================

:mod:`RPLib` -- executesql
--------------------------------------------
.. automodule:: RPLib
   :show-inheritance:
.. autofunction:: executesql

Usage
---------------------------------------------
* **Execute raw SQL statements/queries using an SDE connection file.**

Example 1
---------------------------------------------
    **Simple call with all parameters specified.**
    **Only one SQL statement.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        sqlStatement = "select count(*) from sde.SDE_states;"

        RPLib.executesql(sdeOwner,sqlStatement)

Example 2
---------------------------------------------
    **Simple call with only required parameters specified.**
    **Multiple SQL statements.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        sqlStatement = "select count(*) from sde.SDE_states;select state_id from sde.SDE_states;"

        RPLib.executesql(sdeOwner,sqlStatement)

Example 3
---------------------------------------------
    **If Else logic with all parameters specified.**
    **Multiple SQL statements.**

    ::

        import RPLib

        sdeOwner = "C:/GIS/SDEADMIN@GIS.sde"

        sqlStatement = "select count(*) from sde.SDE_states;select state_id from sde.SDE_states;"

        if RPLib.executesql(sdeOwner,sqlStatement):
            print("successful, run another tool")
        else:
            print("failed, run another tool")
