from __future__ import print_function
import arcpy, smtplib, string, sys, time, os, httplib, urllib, json, getpass
import subprocess
from arcpy import env
from datetime import datetime
from email.mime.text import MIMEText
# pylint: disable-msg=C0103
# pylint: disable-msg=C0303
## email method variables
email_ON = False
email_To = ()
email_From = ""
email_Subject = ""
email_Msg = ""
email_IP = ""
email_Port = ""
email_Username = ""
email_Password = ""

## Logging variables
verboseLog = False

## recPost method variables
recpost_Log = ""

## createVersions method variables
createVersions_List = []

def Logger(Log_Loc="",):

    DATE = '%Y_%m_%d'
    TIME = '%H_%M%p'
    Script_Log = Log_Loc

    if not Script_Log == "":
        if arcpy.Exists(Script_Log):
            ScriptLog = ("{0}//ScriptLog"
                        "_{1}_{2}.txt".format(Script_Log,
                                              datetime.now().strftime(DATE),
                                              datetime.now().strftime(TIME)))
            f = open(ScriptLog, 'w')
            sys.stdout = Tee(sys.stdout, f)
        else:
            print("The specified path for storing the log file does not"
                  " exist!\n")
    else:
        print("A path for the log file location must be specified!\n")

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

def clearworkspacecache(Workspace = None,):
    """
    **Clears any ArcSDE workspaces from the ArcSDE workspace cache.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Workspace**        String    Path to SDE connection file.                                                             Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """
    try:
        if verifyworkspace(Workspace,"Clear Workspace Cache","Workspace"):
            if verifysde(Workspace,"Clear Workspace Cache"):
                prnt("Clearing workspace cache "
                     "for : {0} ... ".format(Workspace))
                arcpy.ClearWorkspaceCache_management(Workspace)
                success()
                return True
            else:
                return False
        else:
            return False

    except Exception, e:
        failed()
        Subject = " ERROR: Clear workspace cache"
        Msg = " Error clearing workspace cache for {0}\n".format(Workspace)
        print(Msg+"\n"+str(e))
        if email_ON: email(Subject, Msg)
        return False



def pauseconnections(Workspace = None,):
    """
    **Allows an administrator to disable the ability of nonadministrative users to make connections to an enterprise geodatabase.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Workspace**        String    Path to SDE connection file.                                                             Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """

    # Process: block new connections to the database
    try:
        if verifyworkspace(Workspace,"Pause Connections","Workspace"):
            if verifysde(Workspace,"Pause Connections"):
                prnt( "Blocking new connections "
                      "for : {0} ... ".format(Workspace))
                arcpy.AcceptConnections(Workspace, False)
                success()
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        failed()
        Subject = "ERROR: Pause connections"
        Msg = (
        " An error occurred while trying to pause connections for {0}.\n"
        " Please ensure the connection file provided has the required"
        " permissions to pause database connections.\n Typically the sde"
        " user handles connections to the database.\n If you were not"
        " using a connection file that uses the sde username and password"
        " please try using a connection file which does.".format(Workspace))
        print(Msg+"\n"+" "+ str(e))
        if email_ON: email(Subject, Msg)
        return False

def resumeconnections(Workspace = None,):
    """
    **Allows an administrator to enable the ability of nonadministrative users to make connections to an enterprise geodatabase.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Workspace**        String    Path to SDE connection file.                                                              Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """
    # Process: allow new connections to the database
    try:
        if verifyworkspace(Workspace,"Resume Connections","Workspace"):
            if verifysde(Workspace,"Resume Connections"):
                prnt( "Allowing new connections "
                      "for : {0} ... ".format(Workspace))
                arcpy.AcceptConnections(Workspace, True)
                success()
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        failed()
        Subject = "ERROR: Resume connections"
        Msg = (" An error occurred while trying to resume connections"
              " for {0}.\n Please ensure the connection file provided"
              " has the required permissions to resume database connections.\n"
              " Typically the sde user handles connections to the database.\n"
              " If you were not using a connection file that uses the sde"
              " username and password please try using a connection file"
              " which does.".format(Workspace))
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

def killconnections(Workspace = None,):
    """
    **Allows an administrator to disconnect all users who are currently connected to an Enterprise geodatabase.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Workspace**        String    Path to SDE connection file                                                              Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """
    # Process: disconnect all users from the database.
    try:
        if verifyworkspace(Workspace,"Kill Connections","Workspace"):
            if verifysde(Workspace,"Kill Connections"):
                prnt( "Killing all connections "
                      "for : {0} ... ".format(Workspace))
                arcpy.DisconnectUser(Workspace, "ALL")
                success()
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        failed()
        Subject = " ERROR: Kill connections"
        Msg = (" Error trying to kill connections for {0}.\n"
              " Please ensure the connection file provided has the required"
              " permissions to kill database connections.\n Typically the"
              " sde user handles connections to the database.\n If you were"
              " not using a connection file that uses the sde username and"
              " password please try using a connection file which does."
              "".format(Workspace))
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

def compressgdb(Workspace = None,):
    """
    **Compresses an enterprise geodatabase by removing states not referenced by a version and redundant rows.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Workspace**        String    Path to SDE connection file.                                                             Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """

    try:
        if verifyworkspace(Workspace,"Compress Database","Workspace"):
            if verifysde(Workspace,"Compress Database"):
                prnt("Compressing geodatabase: {0} ... ".format(Workspace))
                arcpy.Compress_management(Workspace)
                success()
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        failed()
        Subject = " ERROR: Compressing geodatabase"
        Msg = " Error compressing geodatabase {0}\n".format(Workspace)
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

def createversions(Workspace = None,
                   Versions_List = [],
                   PublicAccess = True,
                   ParentVerion = None,):

    """
    **Creates a new version(s) in the specified geodatabase.**

    ==================   ========  =======================================================================================  ==========
    Parameter              Type                                      Description                                             Required
    ==================   ========  =======================================================================================  ==========
    **Workspace**        String    Path to SDE connection file .                                                            Yes
    **Versions_List**    List      The name of the version(s) to be created.                                                Yes
    **PublicAccess**     Boolean   The permission access level for the version.                                             No\n
                                   * True = Public **(Default)**\n
                                   * False = Private\n
                                   * "PROTECTED" = Protected
    **ParentVersion**    String    The geodatabase, or version of a geodatabase, on which the new version will be based.    No\n
                                   * None = "sde.default"\n
                                   * "" = "sde.default"\n
    ==================   ========  =======================================================================================  ==========

    **Returns: Boolean**
    """
    if verifyworkspace(Workspace,"Create Versions","Workspace"):
        if verifysde(Workspace,"Create Versions"):
            env.workspace = Workspace
        else:
            return False
    else:
        return False

    if len(Versions_List) == 0:
        Subject = " ERROR: Create versions"
        Msg = (" Invalid expression supplied for parameter"
               " Versions_List !\n The parameter cannot be an empty"
               " list.\n Expected: List.\n Please provide a list"
               " of version name(s) to be created.")
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    else:
        version_name = Versions_List

    if PublicAccess == True:
        access_permission = "PUBLIC"
    elif PublicAccess == False:
        access_permission = "PRIVATE"
    elif PublicAccess == "PROTECTED":
        access_permission = "PROTECTED"
    else:
        Subject = " ERROR: Create versions"
        Msg = ("Invalid expression supplied for parameter PublicAccess !\n"
               ' Expected: True, False, or "PROTECTED" .\n'
               " Received: {0}".format(PublicAccess))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    parent_version = ""
    check_parent = ""
    verList = []

    if ParentVerion is None or len(ParentVerion) ==0:
        parent_version = "sde.default"
    else:
        check_parent = str(ParentVerion)
        check_parent = check_parent.lower()

    for ver in arcpy.da.ListVersions():
        if ver.isOwner == True and ver.name.lower() == check_parent:
            parent_version = ParentVerion

    verList = [ver.name for ver in arcpy.da.ListVersions()
    if ver.isOwner == True and
       ver.name.lower() != parent_version.lower()]

    # convert Lists to strings for comparison
    strverList = ''.join(verList)

    newversions = []
    existingversions = []

    for version in version_name:
        if not str(version) in strverList:
            newversions.append(version)
        else:
            existingversions.append(version)

    if not len(existingversions) == 0:
        Subject = " ERROR: Create versions"
        Msg = (" Unable to create verion(s) {0}, already"
               " exist!".format(existingversions))
        print(Msg)
        if email_ON: email(Subject, Msg)

    if not len(newversions) == 0:
        for version in newversions:
            try:
                prnt( "Creating version : {0} ... ".format(version))
                arcpy.CreateVersion_management(Workspace,
                                               parent_version,
                                               version,
                                               access_permission)
                success()

            except Exception, e:
                failed()
                Subject = " Error: Create versions"
                Msg = (" An error occurred while trying to create"
                       " versions for {0}.\n Please ensure the correct"
                       " connection file is being referenced and that"
                       " the user has permissions to create versions.\n"
                       " Does the parent version being referenced"
                       " exist?\n Is the correct string being passed"
                       " for PublicAccess?\n Please review the log file"
                       " for more detailed"
                       " information.".format(Workspace))

                print(Msg + "\n" + " " + str(e))
                if email_ON: email(Subject, Msg)
                return False

        return True
    else:
        Subject = " ERROR: Create versions"
        Msg = (" No new versions were created.\n All versions"
               " specified: {0} already exist! \n".format(version_name))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

def rebuild_indexes_analyze(Workspace = None,
                            excludeList = None,
                            include_system = False,
                            delta_only = True,
                            only_versioned = True,
                            analyze_base = True,
                            analyze_delta = True,
                            analyze_archive = True,):
    """
    **Updates indexes of datasets and system tables stored in an enterprise geodatabase. Rebuilds existing attribute or spatial
    indexes. Updates database statistics of base tables, delta tables, and archive tables, along with the statistics on those tables
    indexes.**

    ===================   ========  =======================================================================================  ==========
    Parameter               Type                                      Description                                             Required
    ===================   ========  =======================================================================================  ==========
    **Workspace**         String    Path to SDE connection file                                                              Yes
    **excludeList**       List      List of object names to exclude from being processed.                                    No
    **include_system**    Boolean   Indicates whether statistics will be gathered on the states and state lineages tables.   No\n
                                    * True = SYSTEM\n
                                    * False = NO_SYSTEM **(Default)**\n
    **delta_only**        Boolean   Indicates how the indexes will be rebuilt on the selected datasets.                      No\n
                                    * True = ONLY_DELTAS **(Default)**\n
                                    * False = ALL\n
    **only_versioned**    Boolean   Indicates if indexes will only be rebuilt for objects that are versioned.                No\n
                                    * True = Include only versioned objects. **(Default)**\n
                                    * False = Include all database objects versioned and non-versioned.\n
    **analyze_base**      Boolean   Indicates whether the selected dataset base tables will be analyzed.                     No\n
                                    * True = ANALYZE_BASE **(Default)**\n
                                    * False = NO_ANALYZE_BASE\n
    **analyze_delta**     Boolean   Indicates whether the selected dataset delta tables will be analyzed.                    No\n
                                    * True = ANALYZE_DELTA **(Default)**\n
                                    * False = NO_ANALYZE_DELTA\n
    **analyze_archive**   Boolean   Indicates whether the selected dataset delta tables will be analyzed.                    No\n
                                    * True = ANALYZE_ARCHIVE **(Default)**\n
                                    * False = NO_ANALYZE_ARCHIVE\n
    ===================   ========  =======================================================================================  ==========

    **Returns: Boolean**
    """
    if verifyworkspace(Workspace,"Rebuild Indexes Analyze","Workspace"):
        if verifysde(Workspace,"Rebuild Indexes Analyze"):
            env.workspace = Workspace
            userName = arcpy.Describe(Workspace).connectionProperties.user
        else:
            return False
    else:
        return False

    if excludeList is None:
        excludeList = []
    elif type(excludeList) is list:
        xList = excludeList
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = (" Invalid parameter found for excludeList !\n"
               " Expected: List.\n"
               " Please provide a list of objects in the geodatabse"
               " that you do not wish to have included in this process.")
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(include_system) is bool:
        if include_system is False:
            include_system = "NO_SYSTEM"
        else:
            include_system = "SYSTEM"
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter include_system !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(include_system))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(delta_only) is bool:
        if delta_only is False:
            delta_only = "ALL"
        else:
            delta_only = "ONLY_DELTAS"
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter delta_only !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delta_only))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(only_versioned) is bool:
        pass
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter only_versioned !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delta_only))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(analyze_base) is bool:
        if analyze_base is False:
            analyze_base = "NO_ANALYZE_BASE"
        else:
            analyze_base = "ANALYZE_BASE"
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter analyze_base !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delta_only))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(analyze_delta) is bool:
        if analyze_delta is False:
            analyze_delta = "NO_ANALYZE_DELTA"
        else:
            analyze_delta = "ANALYZE_DELTA"
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter analyze_delta !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delta_only))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if type(analyze_archive) is bool:
        if analyze_archive is False:
            analyze_archive = "NO_ANALYZE_ARCHIVE"
        else:
            analyze_archive = "ANALYZE_ARCHIVE"
    else:
        Subject = " ERROR: rebuild index analyze"
        Msg = ("Invalid expression supplied for parameter analyze_archive !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delta_only))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    try:
        prnt("Gathering list of database objects...")

        fcs = arcpy.ListFeatureClasses("*.{0}.*".format(userName))

        fds = arcpy.ListDatasets('*.' + userName + '.*','Feature')

        if not len(fds) == 0:
            for fd in fds:
                fcs += arcpy.ListFeatureClasses(
                "*.{0}.*".format(userName),feature_dataset=fd)

                tbls = arcpy.ListTables("*.{0}.*".format(userName))

                gdb_objects = []

                if not len(fcs) == 0:
                    gdb_objects += fcs

                if not len(tbls) == 0:
                    gdb_objects += tbls

                if only_versioned:
                    for obj in gdb_objects:
                        if not arcpy.Describe(obj).isVersioned:
                            gdb_objects.remove(obj)

                if not len(excludeList) == 0:
                    gdb_objects =[objects.upper() for objects
                                  in gdb_objects if not any(exclude.upper()
                                  for exclude in excludeList if exclude.upper()
                                  in objects.upper())]

                for obj in gdb_objects:
                    if not arcpy.TestSchemaLock(obj):
                        print(" {0} will not be processed, cannot"
                              " get exclusive schema"
                              " lock.\n".format(obj))
                        gdb_objects.remove(obj)
        success()

    except Exception, e:
        failed()
        Subject = " Error: rebuild index analyze"
        Msg = (
              " An error occurred while trying to gather objects"
              " for {0}.\n Please ensure the correct connection file"
              " is being referenced and that the user has permissions"
              " to create versions.\n Does the parent version being"
              " referenced exist?\n Is the correct string being passed"
              " for PublicAccess?\n Please review the log file for more"
              " detailed information.".format(Workspace))

        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

    if not len(gdb_objects) == 0:
        prnt("Beginning Rebuilding Indexes for FeatureClasses and"
             " Tables for user: {0} ... ".format(userName))
        try:
            arcpy.RebuildIndexes_management(Workspace,
                                            include_system,
                                            gdb_objects,
                                            delta_only)
            success()

            if not len(fds) == 0:
                prnt( "Begin Analyzing FeatureDataSets for user:"
                      " {0} ... ".format(userName))
                arcpy.AnalyzeDatasets_management(Workspace,
                                                 include_system,
                                                 fds,
                                                 analyze_base,
                                                 analyze_delta,
                                                 analyze_archive)

                success()

        except Exception, e:
            failed()
            if "000684" in str(e):
                print("  User does not have permissions to work with"
                      " system tables\n")
                try:
                    prnt("  TRYING WITHOUT SYSTEM TABLES!!! Beginning"
                         " Rebuilding Indexes for FeatureClasses and"
                         " Tables for user: {0} ... ".format(userName))
                    arcpy.RebuildIndexes_management(Workspace,
                                                    "NO_SYSTEM",
                                                    gdb_objects,
                                                    "ALL")

                    success()

                    if not len(fds) == 0:
                        prnt( "  TRYING WITHOUT SYSTEM TABLES!!! Begin"
                              " Analyzing FeatureDataSets for user:"
                              " {0} ... ".format(userName))
                        arcpy.AnalyzeDatasets_management(Workspace,
                                                         "NO_SYSTEM",
                                                         fds,
                                                         analyze_base,
                                                         analyze_delta,
                                                         analyze_archive)

                        success()
                        return True

                except Exception, e:
                    failed()
                    Subject = " ERROR: rebuild_indexes_analyze"
                    Msg = (" Rebuild Index and Analyze without system"
                           " table failed for: {0}\n".format(Workspace))
                    print(Msg + "\n" + " " + str(e))
                    if email_ON: email(Subject, Msg)
                    return False

    else:
        print(" No FeatueClasses or Tables were found"
              " for user: {0}".format(userName))

def reconcilepost(Workspace = None,
                  log_folder = None,
                  versions = None,
                  parent_version = None,
                  delete_version = True,
                  all_versions = True,
                  acquire_locks = True,
                  abort_if_conflicts = True,
                  by_object = True,
                  favor_target = True,
                  post = True,):
    """
    **Reconciles a version or multiple versions against a target version.**

    ======================  ========  ===============================================================================================================================================================================================================================================  ==========
    Parameter                 Type                                      Description                                                                                                                                                                                                     Required
    ======================  ========  ===============================================================================================================================================================================================================================================  ==========
    **Workspace**           String    Path to SDE connection file.                                                                                                                                                                                                                     Yes
    **log_folder**          String    Path to folder where log file(s) will be stored.                                                                                                                                                                                                 Yes
    **versions**            List      List of version names to be reconciled and posted.                                                                                                                                                                                               No\n
    **parent_version**      String    The geodatabase, or version of a geodatabase, which owns the version(s).                                                                                                                                                                         No\n
                                      * None  = "sde.default" **(Default)**\n
                                      * ""    = "sde.default"\n
    **delete_version**      Boolean   Indicates if versions will be deleted after posting to target version.                                                                                                                                                                           No\n
                                      * True  = Delete version after posting to target version. **(Default)**\n
                                      * False = Keep version after posting to target version.\n
    **all_versions**        Boolean   Determines which versions will be reconciled when the tool is executed.                                                                                                                                                                          No\n
                                      * True  = Reconciles edit versions with the target version. **(Default)**\n
                                      * False = Reconciles versions that are blocking the target version from compressing.\n
    **acquire_locks**       Boolean   Determines whether feature locks will be acquired.                                                                                                                                                                                               No\n
                                      * True  = Should be used when the intention is to post edits. **(Default)**\n
                                      * False = Should be used when the edit version will not be posted to the target version.
    **abort_if_conflicts**  Boolean   Reconcile will be aborted if conflicts are found between versions.                                                                                                                                                                               No\n
                                      * True  = Aborts the reconcile if conflicts are found. **(Default)**\n
                                      * False = Does not abort the reconcile if conflicts are found.
    **by_object**           Boolean   Describes the conditions required for a conflict to occur.                                                                                                                                                                                       No\n
                                      * True  = Any changes to the same row or feature in the parent and child versions will conflict during reconcile. **(Default)**\n
                                      * False = Only changes to the same attribute of the same row or feature in the parent and child versions will be flagged as a conflict during reconcile. Changes to different attributes will not be considered a conflict during reconcile.\n
    **favor_target**        Boolean   Describes the behavior if a conflict is detected.                                                                                                                                                                                                No\n
                                      * True  = Resolve in favor of the target version. **(Default)**\n
                                      * False = Resolve in favor of the edit version.\n
    **post**                Boolean   Posts the current edit session to the reconciled target version.                                                                                                                                                                                 No\n
                                      * True  = Version will be posted to the target version after the reconcile. **(Default)**\n
                                      * False = Version will not be posted to the target version after the reconcile.
    ======================  ========  ===============================================================================================================================================================================================================================================  ==========

    **Returns: Boolean**
    """
    if verifyworkspace(Workspace,"Reconcile and Post","Workspace"):
        if verifysde(Workspace,"Reconcile and Post"):
            env.workspace = Workspace
        else:
            return False
    else:
        return False

# parameter check reconcilepost log_folder
    if (log_folder == None
        or len(log_folder) == 0
        and type(log_folder) is str
        ):
        recPost_Log = ""
        print("None or empty string found")

    if type(log_folder) is str and arcpy.Exists(log_folder):
            recPost_Log = log_folder
            # remove any trailing or leading spaces
            recPost_Log = recPost_Log.strip()
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter log_folder !\n"
               " The folder location {0} cannot be found.\n"
               " Expected: String.\n"
               " Please provide a valid path to a folder.".format(log_folder))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# paramter check reconcilepost target_version
    if parent_version is None or len(parent_version) == 0:
        target_version = "sde.default"
    elif type(parent_version) is str and len(parent_version) != 0:
        target_version = str(parent_version)
        target_version = target_version.lower()
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter parent_version !\n"
               " Expected: String\n"
               " Received: {0}\n"
               " Please provide the name of the"
               " parent/target version as a string.".format(parent_version))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # paramter check reconcilepost target_version
    # check to ensure parent version exist.
    for ver in arcpy.da.ListVersions():
        if ver.isOwner == True and ver.name.lower() == target_version.lower():
            target_version = parent_version
            #print("found target version")

    if len(target_version) == 0:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter parent_version !\n"
               " The parent_version specified does not exist or could not"
               " be found: {0}".format(parent_version))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    # parameter check reconcilepost edit_versions
    if (versions == None or len(versions) == 0 or versions == "" ):
        edit_versions = [ver.name for ver in arcpy.da.ListVersions()
                         if ver.isOwner == True
                         and ver.name.lower() != target_version.lower()]
        #print("Edit versions are: {0}".format(edit_versions))
        if len(edit_versions) == 0:
            Subject = " ERROR: reconcile and post"
            Msg = ("Reconcile process was not performed !\n"
                   " The specified target version ({0}) has no edit versions"
                   " to reconcile with.".format(target_version))

            print(Msg)
            if email_ON: email(Subject, Msg)
            return False
    elif type(versions) is list and len(versions) != 0:
        edit_versions = versions
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter versions !\n"
               " Expected: List\n"
               " Received: {0}\n"
               " Please provide a valid list of"
               " version names.".format(versions))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost delete_version
    if type(delete_version) is bool:
        if delete_version is False:
            with_delete = "KEEP_VERSION"
        else:
            with_delete = "DELETE_VERSION"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter delete_version !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(delete_version))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost all_versions
    if type(all_versions) is bool:
        if all_versions is False:
            reconcile_mode = "BLOCKING_VERSIONS"
        else:
            reconcile_mode = "ALL_VERSIONS"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter all_versions !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(all_versions))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost acquire_locks
    if type(acquire_locks) is bool:
        if acquire_locks is False:
            acquire_locks = "NO_LOCK_ACQUIRED"
        else:
            acquire_locks = "LOCK_ACQUIRED"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter acquire_locks !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(acquire_locks))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost abort_if_conflicts
    if type(abort_if_conflicts) is bool:
        if abort_if_conflicts is False:
            abort_if_conflicts = "NO_ABORT"
        else:
            abort_if_conflicts = "ABORT_CONFLICTS"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter"
               " abort_if_conflicts !\n"
               " Expected: True or False .\n"
               " Received: {0}".format(abort_if_conflicts))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost by_object
    if type(by_object) is bool:
        if by_object is False:
            conflict_definition = "BY_ATTRIBUTE"
        else:
            conflict_definition = "BY_OBJECT"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter by_object !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(by_object))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost favor_target
    if type(favor_target) is bool:
        if favor_target is False:
            conflict_resolution = "FAVOR_EDIT_VERSION"
        else:
            conflict_resolution = "FAVOR_TARGET_VERSION"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter favor_target !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(favor_target))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    # parameter check reconcilepost post
    if type(post) is bool:
        if post is False:
            with_post = "NO_POST"
        else:
            with_post = "POST"
    else:
        Subject = " ERROR: reconcile and post"
        Msg = ("Invalid expression supplied for parameter post !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(post))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    DATE = '%Y_%m_%d'
    TIME = '%H_%M%p'

    out_log = ("{0}/RecPostProcess"
               "_{1}_{2}.txt".format(recPost_Log,
                                     datetime.now().strftime(DATE),
                                     datetime.now().strftime(TIME)))

    #print(out_log)

    #print(edit_versions)

    # Reconcile, Abort if conflicts are found, keep all versions, write
    # output to logfile
    print("Begin reconciling all versions"
          " {0}\n".format(datetime.now().strftime(TIME)))

    try:
        prnt("Attempting to Reconcile and Post Versions...")
        arcpy.ReconcileVersions_management(Workspace,
                                           reconcile_mode,
                                           target_version,
                                           edit_versions,
                                           acquire_locks,
                                           abort_if_conflicts,
                                           conflict_definition,
                                           conflict_resolution,
                                           with_post,
                                           "KEEP_VERSION",
                                           out_log)
        # Process: Check if conflicts exist
        conflicts = arcpy.GetMessages(1)

        # If this error arises, there were conflicts in one or more
        # of the # versions.
        if "000084" in conflicts:
            # Process: Read Contents of out_log so it can be added to
            # email.
            log_file = open(out_log, 'rb')
            TEXT = MIMEText(log_file.read())
            log_file.close()
            detailed_string = ("\n An error occurred while Reconciling,"
                               " Posting all versions, The first"
                               " Reconcile and Post operation found"
                               " conflicts. Please review and fix the"
                               " conflicts and try again.")
            Subject = " ERROR: Reconcile and Post Conflicts"
            # Append contents of out_log to email message
            Msg = (" {0}\n A conflict was found for: {1}\n"
                   " {2}".format(TEXT,Workspace,detailed_string))
            print(Msg)
            failed()
            if email_ON: email(Subject, Msg)
            return False

        else:
            success()
            # This assumes the reconcile and post process was
            # successful.
            # Reconcile, Abort if conflicts are found, delete all
            # versions since no conflicts were found in previous
            # reconcile, do not write to log file
            if delete_version:
                try:
                    prnt("Reconciling, Posting, and Deleting All"
                         " Versions... ")
                    arcpy.ReconcileVersions_management(Workspace,
                                                       reconcile_mode,
                                                       target_version,
                                                       edit_versions,
                                                       acquire_locks,
                                                       abort_if_conflicts,
                                                       conflict_definition,
                                                       conflict_resolution,
                                                       with_post,
                                                       with_delete)
                    success()
                    log_file = open(out_log, 'rb')
                    TEXT = MIMEText(log_file.read())
                    log_file.close()
                    Subject = (" Success: Reconcile, Post, and"
                               " Delete Versions")
                    Msg = ("{0}\n"
                          " Reconciling, Posting, and Deleting all"
                          " versions was successful".format(TEXT))
                    if email_ON: email(Subject, Msg)
                    return True
                except Exception, e:
                    failed()
                    # Process: Read Contents of out_log so it can be
                    # added to email.
                    log_file = open(out_log, 'rb')
                    TEXT = MIMEText(log_file.read())
                    log_file.close()
                    detailed_string = (
                    "\n An error occurred while Reconciling, Posting,"
                    " and Deleting all versions.\n The first Reconcile"
                    " and Post operation was successful.\n Although"
                    " while attempting to reconcile, post, and delete"
                    " all versions an error was encountered.\n Please"
                    " ensure no connections were being made to the"
                    " database during this time and that no versions"
                    " were in use and try again.")

                    Subject = " Error: Reconcile and Post"
                    Msg = ("{0}\n"
                          " An error occurred while Reconciling,"
                          " Posting, and Deleting all versions"
                          "".format(TEXT,detailed_string))
                    print(Msg + "\n" + " " + str(e))
                    if email_ON: email(Subject, Msg)
                    return False
            else:
                print(" The option to delete_versions was disabled.\n")


    except Exception, e:
        print("Failed\n")
        # Process: Read Contents of out_log so it can be added to email.
        log_file = open(out_log, 'rb')
        TEXT = MIMEText(log_file.read())
        log_file.close()
        detailed_string = (
        "\n The first Reconcile and Post was not successful.\n Please"
        " ensure you are using the proper connection file for the owner"
        " of the versions.\n Additionally ensure there were no active"
        " connections or versions in use during the Reconcile and Post"
        " process and try again.")
        Subject = " Error: Reconcile and Post"
        Msg = ("{0}\n"
              "An error occurred while Reconciling and Posting"
              "All Versions.\n {1}".format(TEXT,detailed_string))
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

def truncateappend(SourceObject = None,
                   DestinationObject = None,
                   SourceObjectCount = None,
                   ObjectsSchemaTest = False,
                   DestUpdateField = None,
                   FieldMappings = None,
                   Subtype = None,):
    """
    **Truncates and appends data from one object to another.**

    ======================  =============   ====================================================================================================  ==========
    Parameter                 Type                                      Description                                                                Required
    ======================  =============   ====================================================================================================  ==========
    **SourceObject**        String          Path to the source geodatabase object.                                                                 Yes
    **DestinationObject**   String          Path to the destination/target geodatabase object.                                                     Yes
    **SourceObjectCount**   Integer         Number of records that must be in the SourceObject before beginning the process.                       No\n
                                            * None = 0 **(Default)**
    **ObjectsSchemaTest**   Boolean         The schema/fields of the input data must match the schema/fields of the target data.                   No\n
                                            * True = Input schema must match the schema of the target.\n
                                            * False = Input schema do not have to match that of the target dataset. **(Default)**
    **DestUpdateField**     String          Provide the name of a field in the DestinationObject.                                                  No\n
                                            * The field must be of type Date.\n
                                            * After data is appended this field will be calculated with the current date and time.
    **FieldMappings**       Field Mapping   Can only be used if ObjectsSchemaTest is False.                                                        No
    **Subtype**             String          A subtype description to assign that subtype to all new data that is appended to the target dataset.   No
    ======================  =============   ====================================================================================================  ==========

    **Returns: Boolean**
    """
    print("Begin Truncate Append.\n")

    prnt(" Checking if Source exist...")
    if verifyobject(SourceObject,"Truncate Append","SourceObject"):
        Source = SourceObject
        success()
    else:
        failed()
        return False

    prnt(" Checking if Destination exist...")
    if verifyobject(DestinationObject,"Truncate Append","DestinationObject"):
        Destination = DestinationObject
        success()
    else:
        failed()
        return False

# parameter check truncate and append SourceObjectCount
    if SourceObjectCount is None:
        SourceCount = 0
    elif SourceObjectCount == "":
        SourceCount = 0
    elif type(SourceObjectCount) is str and len(SourceObjectCount) != 0:
        SourceCount = int(SourceObjectCount)
    elif type(SourceObjectCount) is int:
        SourceCount = SourceObjectCount
    else:
        Subject = " ERROR: truncate and append"
        Msg = ("Invalid expression supplied for parameter SourceObjectCount !\n"
               " The parameter can be:\n"
               '  None, "", an integer, or an integer within double quotes.\n'
               " Please provide a user defined value like below.\n"
               '  None or "" or 1 or "1"')
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    prnt(" Checking count for Source...")
    getCount = int(arcpy.GetCount_management(Source).getOutput(0))
    print("{0}\n".format(getCount))
    prnt(" Checking if {0} >= {1}...".format(getCount, SourceCount))

    if getCount >= int(SourceCount):
        success()
        prnt(" Checking if destination workspace is SDE or Local GDB...")
    else:
        failed()
        Subject = " ERROR: truncate and append"
        Msg = ("Source object did not meet the requirement specified.\n"
               " The Source object did not have enough rows to continue."
              )
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if not ".sde" in Destination:
        print("Local\n")
        prnt(" Checking for exclusive schema lock on destination...")

        if arcpy.TestSchemaLock(Destination):
            success()

        else:
            failed()
            Subject = " ERROR: Truncate Append"
            Msg = ("  Could not acquire a schema lock for: {0},"
                   " might be in use.\n".format(Destination))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False

    else:
        print("SDE\n")
        prnt(" Checking that workspace is not versioned...")
        if not arcpy.Describe(Destination).isVersioned:
            success()
        else:
            failed()
            Subject = " ERROR: Truncate Append"
            Msg = " Data cannot be versioned {0}.\n".format(Destination)
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False

# parameter check truncate and append ObjectsSchemaTest
    if type(ObjectsSchemaTest) is bool:
        if ObjectsSchemaTest is False:
            SchemaTest = "NO_TEST"
        else:
            SchemaTest = "TEST"
    else:
        Subject = " ERROR: truncate and append"
        Msg = ("Invalid expression supplied for parameter ObjectsSchemaTest !\n"
               ' Expected: True or False .\n'
               " Received: {0}".format(ObjectsSchemaTest))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# parameter check truncate and append DestUpdateField
    if type(DestUpdateField) is str and len(DestUpdateField) != 0:
        prnt(" Checking if DestUpdateField is of type Date...")
        destfields = arcpy.ListFields(Destination)
        for field in destfields:
            fieldname = str(field.name)
            if fieldname.upper() == str.upper(DestUpdateField):
                DestUpdateField = fieldname
                FieldType = field.type
                if FieldType == "Date":
                    success()
                else:
                    failed()
                    Subject = " ERROR: truncate and append"
                    Msg = ("Invalid parameter supplied for DestUpdateField !\n"
                           " Expected: (string) Field Name, of type (Date) .\n"
                           " Received: {0} type: {1}".format(DestUpdateField,
                                                             FieldType))
                    print(Msg)
                    if email_ON: email(Subject, Msg)
                    return False
    else:
        Subject = " ERROR: truncate and append"
        Msg = ("Invalid expression supplied for parameter DestUpdateField !\n"
               ' Expected: (string) Field Name .\n'
               " Received: {0}".format(DestUpdateField))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    try:
        prnt(" Truncating Destination table...")
        arcpy.TruncateTable_management(Destination)
        success()

    except Exception, e:
        failed()
        Subject = " ERROR: Truncate Append"
        Msg = (" Error occurred while Truncating:"
               " {0}\n".format(Destination))
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

    try:
        prnt(" Appending Source to Destination...")
        arcpy.Append_management(Source,
                                Destination,
                                SchemaTest,
                                FieldMappings,
                                Subtype)
        success()

    except Exception, e:
        failed()
        Subject = " ERROR: Truncate Append"
        Msg = (" Error occurred while Appending data to:"
               " {0}\n".format(Destination))
        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False

    if len(DestUpdateField) !=0:
        prnt(" Calculating {0} with current date...".format(DestUpdateField))
        try:
            arcpy.CalculateField_management(Destination,
                                DestUpdateField,
                                "calcDay(  !IMPDATE! )",
                                "PYTHON_9.3",
                                "def calcDay(dateField):\\n   "
                                "dateValue = datetime.datetime.now()\\n   "
                                "return dateValue")
            success()
            print("End Truncate Append.\n")
            return True

        except Exception, e:
            failed()
            Subject = " ERROR: Truncate Append"
            Msg = (" Error occurred while calculating"
                   " {0}\n".format(UpdateField))
            print(Msg + "\n" + " " + str(e))
            if email_ON: email(Subject, Msg)
            return False
    else:
        print("No\n")

def syncreplicas(ParentGDB = None,
                 ChildGDB = None,
                 ReplicaName = None,
                 GDB1_TO_2 = True,
                 FAVOR_GDB1 = True,
                 BY_OBJECT = True,
                 DO_NOT_RECONCILE = True,):
    """
    **Synchronizes updates between two replica geodatabases in a direction specified by the user.**

    ======================  =============   ==========================================================================================================  ==========
    Parameter                 Type                                      Description                                                                      Required
    ======================  =============   ==========================================================================================================  ==========
    **ParentGDB**           String          The geodatabase hosting the replica to synchronize, may be local or remote.                                 Yes
    **ChildGDB**            String          The geodatabase hosting the relative replica, geodatabase may be local or remote.                           Yes
    **ReplicaName**         String                                                                                                                      Yes\n
                                            A valid replica with a parent contained within one input geodatabase and a child in the other
                                            input geodatabase.
    **GDB1_TO_2**           Boolean                                                                                                                     No\n
                                            The direction in which you want changes to be sent from geodatabase 1 to geodatabase 2, from
                                            geodatabase 2 to geodatabase 1, or to send changes in both directions. For check-out/check-in
                                            replicas or one-way replicas there is only one appropriate direction. If the replica is two-way
                                            then any of the three choices are available.\n
                                            * True     = FROM_GEODATABASE1_TO_2 -Parent to Child. **(Default)**\n
                                            * False    = FROM_GEODATABASE2_TO_1 -Child to Parent.\n
                                            * "BOTH"   = BOTH_DIRECTIONS **(overrides Boolean)**\n
    **FAVOR_GDB1**          Boolean         Specifies how conflicts are resolved when they are encountered.                                             No\n
                                            * True     = IN_FAVOR_OF_GDB1 -Conflicts resolve in favor of the PARENTGDB. **(Default)**\n
                                            * False    = IN_FAVOR_OF_GDB2 -Conflicts resolve in favor of the CHILDGDB.\n
                                            * "MANUAL" = MANUAL, Manually resolve conflicts in the versioning environment. **(overrides Boolean)**\n
    **BY_OBJECT**           Boolean         Specifies how you would like to define conflicts.                                                           No\n
                                            * True     = BY_OBJECT -Detects conflicts by row. **(Default)**\n
                                            * False    = BY_ATTRIBUTE -Detects conflicts by column.\n
    **DO_NOT_RECONCILE**    Boolean                                                                                                                     No\n
                                            Indicates whether to automatically reconcile once data changes are sent to the parent replica if
                                            there are no conflicts present. This option is only available for check-out/check-in.\n
                                            * True     = DO_NOT_RECONCILE -Do not reconcile. **(Default)**\n
                                            * False    = RECONCILE -Reconcile\n
    ======================  =============   ==========================================================================================================  ==========

    **Returns: Boolean**
    """
    if verifyworkspace(ParentGDB,"Sync Replicas","ParentGDB"):
        if verifysde(ParentGDB,"Sync Replicas"):
            Parent = ParentGDB
        else:
            return False
    else:
        return False

    if verifyworkspace(ChildGDB,"Sync Replicas","ChildGDB"):
        Child = ChildGDB
    else:
        return False

# parameter check syncreplica ReplicaName

    if not (ReplicaName == None
            and len(ReplicaName) != 0
            and type(ReplicaName) is str
            ):
        repname = ReplicaName

    else:
        Subject = " ERROR: Sync Replicas"
        Msg = ("Invalid expression supplied for parameter ReplicaName !\n"
               " The parameter cannot be None or empty.\n"
               " Expected: String.\n"
               " Please provide the name for a Replica within the geodatabase.")
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# parameter check syncreplica ReplicaName in ParentGDB
    for replica in arcpy.da.ListReplicas(ParentGDB):
        repname = str(replica.name)

        if string.upper(ReplicaName) in repname.upper():
            #print("Found a match")
            RepName = repname
            #print(RepName)
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for parameter ReplicaName !\n"
                   " The replica name was not found in the ParentGDB.\n")
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False

# parameter check syncreplica ReplicaName in ChildGDB
    for replica in arcpy.da.ListReplicas(ChildGDB):
        repname = str(replica.name)

        if string.upper(ReplicaName) in repname.upper():
            #print("Found a match")
            #print(RepName)
            continue
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for parameter ReplicaName !\n"
                   " The replica name was not found in the ChildGDB.\n")
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False

# parameter check syncreplica GDB1_TO_2
    if type(GDB1_TO_2) is bool:
        if GDB1_TO_2 == True:
            in_direction = "FROM_GEODATABASE1_TO_2"
        elif GDB1_TO_2 == False:
            in_direction = "FROM_GEODATABASE2_TO_1"
        elif string.upper(GDB1_TO_2) == "BOTH":
            in_direction = "BOTH"
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for parameter GDB1_TO_2 !\n"
                   ' Expected: True, False, or "BOTH" .\n'
                   " Received: {0}".format(GDB1_TO_2))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False
    else:
        Subject = " ERROR: Sync Replica"
        Msg = ("Invalid expression supplied for parameter GDB1_TO_2 !\n"
               ' Expected: True, False, or "BOTH" .\n'
               " Received: {0}".format(GDB1_TO_2))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# parameter check syncreplica FAVOR_GDB1
    if type(FAVOR_GDB1) is bool:
        if FAVOR_GDB1 == True:
            conflict_policy = "IN_FAVOR_OF_GDB1"
        elif FAVOR_GDB1 == False:
            conflict_policy = "IN_FAVOR_OF_GDB2"
        elif string.upper(FAVOR_GDB1) == "MANUAL":
            conflict_policy = "MANUAL"
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for parameter FAVOR_GDB1 !\n"
                   'Expected: True or False or "MANUAL" \n'
                   'Received: {0}'.format(FAVOR_GDB1))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False
    else:
        Subject = " ERROR: Sync Replica"
        Msg = ("Invalid expression supplied for parameter FAVOR_GDB1 !\n"
               'Expected: True or False or "MANUAL" \n'
               'Received: {0}'.format(FAVOR_GDB1))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# parameter check syncreplica BY_OBJECT
    if type(BY_OBJECT) is bool:
        if BY_OBJECT == True:
            conflict_definition = "BY_OBJECT"
        elif BY_OBJECT == False:
            conflict_definition = "BY_ATTRIBUTE"
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for parameter BY_OBJECT !\n"
                   'Expected: True or False \n'
                   'Received: {0}'.format(BY_OBJECT))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False
    else:
        Subject = " ERROR: Sync Replica"
        Msg = ("Invalid expression supplied for parameter BY_OBJECT !\n"
               'Expected: True or False \n'
               'Received: {0}'.format(BY_OBJECT))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

# parameter check syncreplica DO_NOT_RECONCILE
    if type(DO_NOT_RECONCILE) is bool:
        if DO_NOT_RECONCILE == True:
            reconcile = "DO_NOT_RECONCILE"
        elif DO_NOT_RECONCILE == False:
            reconcile = "RECONCILE"
        else:
            Subject = " ERROR: Sync Replica"
            Msg = ("Invalid expression supplied for "
                   "parameter DO_NOT_RECONCILE !\n"
                   'Expected: True or False \n'
                   'Received: {0}'.format(DO_NOT_RECONCILE))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False
    else:
        Subject = " ERROR: Sync Replica"
        Msg = ("Invalid expression supplied for "
                   "parameter DO_NOT_RECONCILE !\n"
                   'Expected: True or False \n'
                   'Received: {0}'.format(DO_NOT_RECONCILE))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    prnt("Synchronizing replica {0}...".format(RepName))

    try:
        arcpy.SynchronizeChanges_management(ParentGDB,
                                            RepName,
                                            ChildGDB,
                                            in_direction,
                                            conflict_policy,
                                            conflict_definition,
                                            reconcile)

        success()
        return True
    except Exception, e:
        print("Failed\n")
        if "000622" or "000800" in str(e):
            print("  An error was encountered while trying to synchronize.\n")
            print("  Consider setting DO_NOT_RECONCILE parameter to True.\n")
            print("{0}".format(str(e)))
            prnt("  Attempting to synchronize without reconciling...")
            try:
                arcpy.SynchronizeChanges_management(ParentGDB,
                                                    RepName,
                                                    ChildGDB,
                                                    in_direction,
                                                    conflict_policy,
                                                    conflict_definition,
                                                    "DO_NOT_RECONCILE")
                success()
                return True
            except Exception, e:
                failed()
                Subject = " ERROR: Sync Replica"
                Msg = ("Trying to synchronize changes failed.\n"
                       "An attempt was made to synchronize with reconcile and "
                       "failed.\n"
                       "An attempt was also made to synchronize without "
                       " reconciling and also failed.\n"
                       "Please ensure all parameters are valid and try again."
                      )
                print(Msg + "\n" + " " + str(e))
                if email_ON: email(Subject, Msg)
                return False

def executesql(Workspace = None, SQLStatement = None,):
    """
    **Execute one or multiple SQL statements against an enterprise geodatabase.**

    ======================  ========  ===============================================================================================================================================================================================================================================  ==========
    Parameter                 Type                                      Description                                                                                                                                                                                                     Required
    ======================  ========  ===============================================================================================================================================================================================================================================  ==========
    **Workspace**           String    Path to SDE connection file.                                                                                                                                                                                                                     Yes
    **SQLStatement**        String    String of SQL statements to execute, statements separated by a semi-colon                                                                                                                                                                        Yes
    ======================  ========  ===============================================================================================================================================================================================================================================  ==========

    **Returns: Boolean**
    """
    try:
        # Make data path relative
        if verifysde(Workspace,"executesql"):

            arcpy.env.workspace = Workspace

            sde_conn = arcpy.ArcSDESQLExecute(Workspace)

            # Get the SQL statements, separated by ; from a text string.
            sql_statement = SQLStatement
            sql_statement_list = sql_statement.split(";")

            # Encode statements as UTF-8
            sql_statement_list = utf8ify(sql_statement_list)

            print("+++++++++++++++++++++++++++++++++++++++++++++\n")
            for sql in sql_statement_list:
                    # Check that item in list is not empty
                    if len(sql) != 0:
                        sde_return = True
                        print("Execute SQL Statement: {0}".format(sql))
                        try:
                            sde_return = sde_conn.execute(sql)
                            print(sde_return)
                        except Exception as err:
                            print(str(err))
                            sde_return = False
                        if isinstance(sde_return, list):
                            print("Number of rows returned by query: "
                                  "{0} rows".format(len(sde_return)))
                        else:
                            if sde_return == True:
                                print("SQL statement: {0} SUCCESS.".format(sql))
                            elif sde_return == False:
                                print("SQL statement: {0} FAILED.".format(sql))
                        print("+++++++++++++++++++++++++++++++++++++++++++++\n")
            return True

    except Exception as err:

        errstring = "'ascii' codec can't encode character"
        if errstring in str(err):
            pass
        else:
            print(str(err))
            return False



def controlservices(Folder=None,
                    Operation=None,
                    ServerName=None,
                    UserName=None,
                    Password=None,):
    """
    **Manage individual ArcGIS Server services at the folder level or through
    the Windows Services Console by stopping or starting the main ArcGIS
    Server service.**

    ======================  =============   ============================================================================================================  ==========
    Parameter                 Type                                      Description                                                                        Required
    ======================  =============   ============================================================================================================  ==========
    **Folder**              String                                                                                                                        Yes\n
                                            The folder containing the services you wish to stop or start on your ArcGIS Server.\n

                                            * "ALL" = Will perform the Operation on the main ArcGIS Server service through the Windows Services Console.

                                            **Note "ALL" should only be used on machines running Windows Server.**\n

    **Operation**           String                                                                                                                        Yes\n
                                            Specify the operation you wish to perform on the service(s).\n

                                            * "START" = Will Start services.\n

                                            * "STOP" = Will Stop services.\n

    **ServerName**          String                                                                                                                        Yes\n
                                            The name or IP address of the server where ArcGIS Server is running.\n
    **UserName**            Boolean                                                                                                                       Yes\n
                                            Specify an administrative user for ArcGIS Server.\n
    **Password**            Boolean                                                                                                                       Yes\n
                                            Specify the administrative user password for ArcGIS Server.\n
    ======================  =============   ============================================================================================================  ==========

    **Returns: Boolean**

    """

    # Ask for admin/publisher user name and password
    username = UserName
    password = Password

    # Ask for server name
    serverName = ServerName
    serverPort = 6080

    folder = Folder
    stopOrStart = Operation

    if string.upper(folder) == "ALL":
        if string.upper(stopOrStart) == "STOP":
            try:
                os.system('sc \\\\{0} stop "ArcGIS Server"'.format(serverName))
                success()
                return True
            except Exception, e:
                failed()
                Subject = " ERROR: control services"
                Msg = (" Error occurred while stopping ArcGIS Server"
                       " for: {0}\n".format(serverName))
                print(Msg + "\n" + " " + str(e))
                if email_ON: email(Subject, Msg)
                return False

        if string.upper(stopOrStart) == "START":
            try:
                os.system('sc \\\\{0} start "ArcGIS Server"'.format(serverName))
                success()
                return True
            except Exception, e:
                failed()
                Subject = " ERROR: control services"
                Msg = (" Error occurred while starting ArcGIS Server"
                      " for: {0}\n".format(serverName))
                print(Msg + "\n" + " " + str(e))
                if email_ON: email(Subject, Msg)
                return False

    if not len(folder) == 0:
        if not username == None:
            if not password == None:
                # Print some info
                print("\nThis tool is a sample script that stops or starts"
                      " all services in a folder.\n")

                # Check to make sure stop/start parameter is a valid value
                if [str.upper(stopOrStart) != "START"
                    and str.upper(stopOrStart) != "STOP"]:
                    print(" Invalid STOP/START parameter entered\n")
                    return False

                # Get a token
                token = getToken(username, password, serverName, serverPort)
                #if token == "":
                if not token:
                    return False
                else:

                    # Construct URL to read folder
                    if str.upper(folder) == "ROOT":
                        folder = ""
                    else:
                        folder += "/"

                    folderURL = "/arcgis/admin/services/" + folder

                    # This request only needs the token and the response formatting parameter
                    params = urllib.urlencode({'token': token, 'f': 'json'})

                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

                    # Connect to URL and post parameters
                    httpConn = httplib.HTTPConnection(serverName, serverPort)
                    httpConn.request("POST", folderURL, params, headers)

                    # Read response
                    response = httpConn.getresponse()
                    if (response.status != 200):
                        httpConn.close()
                        print(" Could not read folder information.\n")
                        return False
                    else:
                        data = response.read()

                        # Check that data returned is not an error object
                        if not assertJsonSuccess(data):
                            print(" Error when reading folder"
                                  " information. {0}\n".format(str(data)))
                            return False
                        else:
                            print(" Processed folder information successfully."
                                  " Now processing services...\n")

                        # Deserialize response into Python object
                        dataObj = json.loads(data)
                        httpConn.close()

                        # Loop through each service in the folder and stop or
                        # start it
                        for item in dataObj['services']:

                            fullSvcName = item['serviceName'] + "." + item['type']

                            # Construct URL to stop or start service, then make the request
                            stopOrStartURL = "/arcgis/admin/services/" + folder + fullSvcName + "/" + stopOrStart
                            httpConn.request("POST", stopOrStartURL, params, headers)

                            # Read stop or start response
                            stopStartResponse = httpConn.getresponse()
                            if (stopStartResponse.status != 200):
                                httpConn.close()
                                print(" Error while executing stop or start."
                                      " Please check the URL and try again.\n")
                                return False
                            else:
                                stopStartData = stopStartResponse.read()

                                # Check that data returned is not an error
                                # object
                                if not assertJsonSuccess(stopStartData):
                                    if str.upper(stopOrStart) == "START":
                                        print(" Error returned when starting"
                                              " service {0}.\n"
                                              "".format(fullSvcName))
                                        return False
                                    else:
                                        print(" Error returned when stopping"
                                              " service {0}.\n"
                                              "".format(fullSvcName))
                                        return False

                                    print(stopStartData)

                                else:
                                    print("  Service {0} processed"
                                          " successfully.\n"
                                          "".format(fullSvcName))
                                    return True

                            httpConn.close()

                        # Clean Up
                        #
                        del username
                        del password
                        del serverName
                        del serverPort
                        del folder
                        del stopOrStart

# A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    """
    Helper function for controlservices function. A token is needed to verify
    authentication to manage ArcGIS Server services. All parameters are either
    passed by the controlservices function and or are otherwise hardcoded. Note
    if you named your instance anything other than arcgis please see the
    tokenURL and change to the name of your instance.

    Returns: Boolean
    """
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"

    params = urllib.urlencode({'username': username,
                               'password': password,
                               'client': 'requestip',
                               'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    # Connect to URL and post parameters
    try:
        httpConn = httplib.HTTPConnection(serverName, serverPort)
        httpConn.request("POST", tokenURL, params, headers)
    except Exception, e:
        failed()
        Subject = " ERROR: control services"
        ErrMsg = (" Could not generate a token with the username and password"
                  " provided. \n Also check that the server name/ip address"
                  " provided is valid.")
        Msg = (" Error connecting to {0} on port 6080.\n"
               " {1}\n".format(serverName,ErrMsg))

        print(Msg + "\n" + " " + str(e))
        if email_ON: email(Subject, Msg)
        return False
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print(" Error while fetching tokens from admin URL.\n"
              " Please check the URL and try again.")
        return False
    else:
        data = response.read()
        httpConn.close()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            return

        # Extract the token from it
        token = json.loads(data)
        return token['token']

def assertJsonSuccess(data):
    """
    A function that checks that the input JSON object is not an error object.

    Returns: Boolean
    """
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print("Error: JSON object returns an error. " + str(obj))
        return False
    else:
        return True

def deletefilesolderthan(Number_Of_Days = 0,
                         FolderLocation = "",):
    """
    **Manages the cleanup of logfiles generated by RPLib.**

    ==================   ========  =======================================================================================  =========
    Parameter            Type      Description                                                                              Required
    ==================   ========  =======================================================================================  =========
    **Number_Of_Days**   Integer   Files that are so many days older than the current day will be deleted.                  Yes
    **FolderLocation**   String    The folder where the logfiles are being stored.                                          Yes
    ==================   ========  =======================================================================================  =========

    **Returns: Boolean**
    """
    path = FolderLocation
    days = Number_Of_Days
    if not isinstance(days, int):
        days = int(days)
    if arcpy.Exists(path):
        try:

            prnt("Deleting files older than {0} days...".format(days))
            now = time.time()
            for f in os.listdir(path):
                nf= os.path.join(path, f)
                if os.stat(nf).st_mtime < now - days * 86400:
                    if os.path.isfile(nf):
                        os.remove(nf)
            success()
            return True
        except Exception, e:
            failed()
            Subject = " ERROR: delete files older than"
            Msg = (" An error occurred while trying to delete files in"
                   " {0}\n".format(path))
            print(Msg + "\n" + " " + str(e))
            if email_ON: email(Subject, Msg)
            return False

    else:
        print("The path specified does not exist!")
        return False

def verifysde(Workspace,functionName,):
    """
    Helper function to verify that the workspace specified exist and that it is
    an SDE database. All parameters are passed from other functions.

    Returns: Boolean
    """
    desc = arcpy.Describe(Workspace)

    # Describe function property workspaceFactoryProgID for SDE databases.
    sdewrkspc = "esriDataSourcesGDB.SdeWorkspaceFactory.1"

    # Check if workspace is an SDE database.
    if desc.workspaceFactoryProgID != sdewrkspc:
        Subject = " ERROR: {0}".format(functionName)
        Msg = (" ERROR: {0}\n"
               " This tool only works with SDE databases.\n"
               " Please supply a valid path to an SDE database.\n"
               " Received: {1}\n"
               " Type: {2}\n".format(functionName,
                                     Workspace,
                                     desc.workspaceFactoryProgID))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    else:
        return True

def verifyworkspace(Workspace,functionName,ParameterName):
    """
    Helper function to verify that the workspace specified exist. All parameters
    are passed from other functions.

    Returns: Boolean
    """
    if (Workspace == None
        or len(Workspace) == 0
        or type(Workspace) is not str):

        Subject = " ERROR: {0}".format(functionName)
        Msg = (" ERROR: {0}\n"
               " Invalid expression supplied for parameter {1} !\n"
               " The parameter cannot be None or empty.\n"
               " Expected: String.\n"
               " Please provide a valid path to an enterprise"
               " geodatabase".format(functionName,ParameterName))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

    if not arcpy.Exists(Workspace):
        Subject = " ERROR: {0}".format(functionName)
        Msg = (" Workspace {0} does not exist".format(Workspace))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False
    else:
        return True

def verifyobject(Object,functionName,ParameterName):
    """
    Helper function to verify that an object specified exists. All parameters
    are passed from other functions.

    Returns: Boolean
    """
    if not (Object == None
            and len(Object) != 0
            and type(Object) is str
            ):
        if arcpy.Exists(Object):
                return True
        else:
            Subject = " ERROR: {0}".format(functionName)
            Msg = (" {0} {1} does not exist".format(ParameterName,Object))
            print(Msg)
            if email_ON: email(Subject, Msg)
            return False

    else:
        Subject = " ERROR: {0}".format(functionName)
        Msg = ("Invalid expression supplied for parameter: {0} !\n"
               " The parameter cannot be None or empty.\n"
               " Expected: String.\n"
               " Please provide a valid path to a geodatabase"
               " object like a featureclass or table.".format(Object))
        print(Msg)
        if email_ON: email(Subject, Msg)
        return False

def success():
    """
    Helper function to show that an operation ran successfully. Also handles
    the type of message returned, if verbose logging is enabled the full arcpy
    messages are returned. If verbose logging is disabled a simple message of
    Success is returned.
    """
    msg = "\n" + arcpy.GetMessages() + "\n" if verboseLog else "Success\n"
    print(msg)

def failed():
    """
    Helper function to show that an operation failed. Also handles
    the type of message returned, if verbose logging is enabled the full arcpy
    messages are returned. If verbose logging is disabled a simple message of
    Failed is returned.
    """
    msg = "\n" + arcpy.GetMessages() + "\n" if verboseLog else "Failed\n"
    print(msg)

def prnt(statement):
    """
    Helper function to show messages returned at the end of a line.
    """
    print(statement,end="")

def utf8ify(list):
   '''Encode a list of strings in utf8'''
   return [item.encode('utf8') for item in list]

def email(Subject,Msg):
    """
    Helper function to send detailed information about when a function succeeds
    or fails.
    """
    email_Subject = Subject
    email_Msg = Msg

    # take the email list and use it to send an email to connected users.
    COMMASPACE = ', '
    # Prepare actual message
    BODY = string.join((
            "From: %s" % email_From,
            "To: %s" %  COMMASPACE.join(email_To),
            "Subject: %s" % email_Subject ,
            "",
            email_Msg
            ), "\n")

    # Send the mail
    server = smtplib.SMTP(email_IP,int(email_Port))
    # If Authentication is required specify in the 2 lines below
    username = email_Username
    password = email_Password
    # Ping the server to do a handshake and authenticate
    server.ehlo()
    server.starttls()
    server.ehlo()
    if not username:
        if not password:
            try:
                # Send the email and exit connection to smtp server
                server.sendmail(email_From, email_To, BODY)
                server.quit()
            except:
                print(" Authentication may be required to send emails from this"
                      " SMTP server.\n Please try supplying username and"
                      " password.\n If supplying username and password does"
                      " not work contact your system administrator and verify"
                      " the IP address and PORT numbers are correct.")

    else:
        try:
            server.login(username,password)
            # Send the email and exit connection to smtp server
            server.sendmail(email_From, email_To, BODY)
            server.quit()
        except:
            print(" Authentication may have failed for this SMTP server.\n"
                  " Please verify the username and password.\n If username"
                  " and password are correct consider contacting your system"
                  " administrator to verify the IP address and PORT numbers"
                  " are correct.\n Also ensure that authentication is required,"
                  " try leaving username and password blank and try again.")

def catch_errors(func):
    """Decorator function to support error handling."""
    def decorator(*args, **kwargs):
        """Decorator function"""
        try:
            f = func(*args, **kwargs)
            return f
        except Exception:
            tb = sys.exc_info()[2]
            tbInfo = traceback.format_tb(tb)[-1]
            print('PYTHON ERRORS:\n%s\n%s: %s\n' %
                             (tbInfo, sys.exc_type, sys.exc_value))
            gp_errors = arcpy.GetMessages(2)
            if gp_errors:
                print('GP ERRORS:\n%s\n' % gp_errors)
    # End decorator function
    return decorator
# End catch_errors function