Implementation Examples
=================================================================================================================================================================================================
    **Below are examples of how RPLib can be used to automate geodatabase administration tasks.**

Reconcile and Post with Full Compress (Minimum)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    * **This shows the recommended minimum amount needed to perform a reconcile and post with a full compress.**

    * **If you know no one will be in the database off hours you could remove pauseconnections and resumeconnections from the script below.**

    * **In this example it is assumed ArcGIS Server(AGS) is running on a Windows machine.**

    1.) Stop AGS service through the Windows Services Console.

        a.) "ALL" is used to control the main AGS service through the Windows Services Console. **"ALL" only works with Windows machines.**

        b.) Stop the AGS service, this stops all services on the AGS machine. This should remove all locks from SDE that AGS might create.

        c.) Name of the server where AGS is running.

        d.) Administrative username for AGS.

        e.) Administrative password for AGS.

    2.) Pause all users from connecting to SDE then kill all current connections, pausing the connections before killing the connections will prevent someone from possibly connecting before the kill command is issued.

    3.) Reconcile and Post your versions against the parent version, in this case the parent version is sde.default.

        a.) Specify the connection file.

        b.) The location where the logfile from Esri's reconcile tool will be output.

        c.) Providing an empty list will reconcile all versions.

        d.) Provide the name of the parent version.

        e.) Versions will be deleted after a successful reconcile and post.

        f.) Reconcile edit versions with target version.

        g.) Locks will be aquired because we intend to post the versions.

        h.) Process will be aborted if conflicts are found.

        i.) Changes to the same row or feature in the parent and child versions will conflict during reconcile.

        j.) Changes will be resolved in favor of the target version.

        k.) Version will be posted if a reconcile was successful.

    4.) Compress the database using an administrative user.

    5.) Since reconcile and post was successful the versions need to be recreated. **An email should have been received stating the reconcile and post process was successful.**

        a.) Specify the connection file.

        b.) Specify a list of version names to create.

        c.) Make the permission level access for the version to be PUBLIC.

        d.) Specify the parent version.

    6.) Allow connections to once again be made to the database.

    7.) Start the main AGS service that was stopped in Step 1.

    8.) Since the reconcile and post was not successful, allow new connections to once again be made to the database. **An email should have been received stating the reconcile and post process was not successful.**

    9.) Start the main AGS service that was stopped in Step 1.


    ::

        import RPLib

        if __name__ == '__main__':
            # Email variables
            RPLib.email_To = ('to@yourorganization.org',)
            RPLib.email_From = 'from@organization.org'
            RPLib.email_IP = "10.20.2.8"
            RPLib.email_Port = 587
            RPLib.email_Username = "username"
            RPLib.email_Password = "password"
            RPLib.email_ON = True

            # Logging variables
            LogFileLoc = "C:/GIS/Log"
            RPLib.Logger(LogFileLoc)
            RPLib.verboseLog = False

            # Create versions variable
            createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

            # SDE connection files
            dataOwner = 'C:/GIS/GIS@GISADMIN.sde'
            sdeOwner = 'C:/GIS/GIS@SDE.sde'

            # 1.)                  1a     1b      1c          1d             1e
            RPLib.controlservices("ALL","stop","GISAPP","administrator","password")

            # 2.)
            RPLib.pauseconnections(sdeOwner)
            RPLib.killconnections(sdeOwner)

            # 3.)                     3a       3b      3c       3d       3e   3f   3g   3h   3i   3j   3k
            if RPLib.reconcilepost(sdeOwner,LogFileLoc,[],"sde.DEFAULT",True,True,True,True,True,True,True):
                # 4.)
                RPLib.compressgdb(sdeOwner)
                # 5.)                   5a           5b            5c        5d
                RPLib.createversions(sdeOwner,createVersions_List,True,"sde.default")
                # 6.)
                RPLib.resumeconnections(sdeOwner)
                # 7.)
                RPLib.controlservices("ALL","start","GISAPP","administrator","password")
            else:
                # 8.)
                RPLib.resumeconnections(sdeOwner)
                # 9.)
                RPLib.controlservices("ALL","start","GISAPP","administrator","password")

Reconcile and Post with Full Compress (Best Practice)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    * **This shows the recommended best practice for performing a reconcile and post with a full compress.**
    * **In this example it is assumed that there is a folder in AGS called "FeatureServices" which houses services that have connections to SDE.**

        * **It is also assumed all other services in AGS point to a file geodatabase(s).**

    * **excludeList is specified to exclude tables that do not need to be included in the rebuild_indexes_analyze function.**
    * **The cleanup of logfiles is handled by the deletefilesolderthan function.**
    * **Workspace caches are cleared at the end of the script to clean up any hanging connections to the database from the script.**

    ::

        import RPLib

        if __name__ == '__main__':
            # Email variables
            RPLib.email_To = ('to@yourorganization.org',)
            RPLib.email_From = 'from@organization.org'
            RPLib.email_IP = "10.20.2.8"
            RPLib.email_Port = 587
            RPLib.email_Username = "username"
            RPLib.email_Password = "password"
            RPLib.email_ON = True

            # Logging variables
            LogFileLoc = "C:/GIS/Log"
            RPLib.Logger(LogFileLoc)
            RPLib.verboseLog = False

            # Exlude tables that have the below variations in their name from the
            # Rebuild indexes and analyze function
            excludeList = ['VW_', '_VW', 'V_', '_V',]

            # Create version variable
            createVersions_List = ['JOHNDOE','JANEDOE','JOHNSMITH','JANESMITH']

            # SDE connection files
            dataOwner = 'C:/GIS/GIS@GISADMIN.sde'
            sdeOwner = 'C:/GIS/GIS@SDE.sde'

            # Rebuild indexes and update statistics to maintain optimal geodatabase performance.
            RPLib.rebuild_indexes_analyze(dataOwner, excludeList, False, True, False, True, True, True)

            ## Stop all services in the folder FeatureServices on ArcGIS Server
            RPLib.controlservices("FeatureServices","stop","GISAPP","administrator","password")

            RPLib.pauseconnections(sdeOwner)
            RPLib.killconnections(sdeOwner)

            if RPLib.reconcilepost(sdeOwner,"C:/TESTGIS",[],"sde.DEFAULT",True,True,True,True,True,True,True):
                RPLib.createversions(sdeOwner,createVersions_List,True,"sde.default")
                RPLib.compressgdb(sdeOwner)
                RPLib.resumeconnections(sdeOwner)
                RPLib.controlservices("FeatureServices","start","GISAPP","administrator","password")
                RPLib.rebuild_indexes_analyze(dataOwner, excludeList, False, True, False, True, True, True)
                RPLib.deletefilesolderthan(14,LogFileLoc)
                RPLib.clearworkspacecache(sdeOwner)
                RPLib.clearworkspacecache(dataOwner)
            else:
                RPLib.resumeconnections(sdeOwner)
                RPLib.controlservices("FeatureServices","start","GISAPP","administrator","password")
                RPLib.deletefilesolderthan(14,LogFileLoc)
                RPLib.clearworkspacecache(sdeOwner)
                RPLib.clearworkspacecache(dataOwner)

Maintain optimal performance without reconciling and posting or full compress
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    * **Some organizations only perform a reconcile and post with a full compress once a week or once a month.**

    * **While there will continue to be an endless debate on the best practices regarding reconciling and posting or getting a full compress, one thing is certain performance must be optimal.**

    * **This example will focus on compressing and rebuilding indexes and updating database statistics within an enterprise geodatabase.**

    ::

        import RPLib

        if __name__ == '__main__':
            # Email variables
            RPLib.email_To = ('to@yourorganization.org',)
            RPLib.email_From = 'from@organization.org'
            RPLib.email_IP = "10.20.2.8"
            RPLib.email_Port = 587
            RPLib.email_Username = "username"
            RPLib.email_Password = "password"
            RPLib.email_ON = True

            # Logging variables
            LogFileLoc = "C:/GIS/Log"
            RPLib.Logger(LogFileLoc)
            RPLib.verboseLog = False

            # Exlude tables that have the below variations in their name from the
            # Rebuild indexes and analyze function
            excludeList = ['VW_', '_VW', 'V_', '_V',]

            # SDE connection files
            dataOwner = 'C:/GIS/GIS@GISADMIN.sde'
            sdeOwner = 'C:/GIS/GIS@SDE.sde'

            # Remove states not referenced by a version and redundant rows.
            if RPLib.compressgdb(sdeOwner):

                # Rebuild indexes and update statistics to maintain optimal geodatabase performance.
                if RPLib.rebuild_indexes_analyze(dataOwner, excludeList, False, True, False, True, True, True):
                    print("Maintenance completed succesfully!")

                else:
                    print("Rebuilding Indexes Failed!")

            else:
                print("Compressing Database Failed!")