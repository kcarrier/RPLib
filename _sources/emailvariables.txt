Email Variables
================================
    **Parameters that can be specified for sending emails.**
    **All parameters are not required by default because it will depend on how your email server is configured, please consult your email administrator.**

    ==================   ========  ============================================================================================================================================  =========
    Parameter            Type      Description                                                                                                                                   Required
    ==================   ========  ============================================================================================================================================  =========
    **email_ON**         Boolean   Indicates if emails will be sent when functions fail.                                                                                         No

                                   - True = Emails will be sent.

                                   - False = Emails will not be sent. **(Default)**

                                   - **Note if using reconcilepost function an email will be sent if the function fails or succeeds when email_ON is set to True.**

    **email_To**         List      Who the email will be sent to. e.g., ("jonedoe@server.com","janedoe@server.com") always include the comma even if only 1 name is used.        No
    **email_From**       String    Who the email will be sent from. e.g., "janesmith@server.com"                                                                                 No
    **email_Subject**    String    The subject of the email to be sent.                                                                                                          No
    **email_Msg**        String    The body of the email                                                                                                                         No
    **email_IP**         String    Indicates the ip address or name of your mail server, this can be local or remote depending on your IT policies.                              No
    **email_Port**       String    Specify the port used for sending emails.                                                                                                     No

                                   - Typically the port for an SMTP server is 25.

                                   - Some Exchange or Outlook servers also use 587.

    **email_Username**   String    If authentication is required specify username here.                                                                                          No

                                   - If a domain is required remember one backslash in python is equivalent to an escape so try something like **domain\\\\username**.

    **email_Password**   String    Specify the password associated with the username.                                                                                            No
    ==================   ========  ============================================================================================================================================  =========

Usage
---------------------------------------------

    * **Email notifications can be helpful when automating processes to let you know when things fail or succeed.**
    * **If the email_ON option is set to True and all other necessary paramters are correct, you will only receive emails when functions fail.**

        - **The exception to this rule is the reconcilepost function, which will send an email if the function fails or succeeds.**

    * **Each function has email capabilities built in and will include the error message encountered.**

Example 1
---------------------------------------------
    * **Simple call to send emails with required parameters specified.**
    * **Notice we are only specifying credentials for the email server, we are not actually sending emails.**
    * **If the clearworkspacecache function failed then johndoe and janedoe would get an email from janesmith indicating this function threw an error in the Subject and the Body of the email would contain the error message.**

    ::

        import RPLib

        RPLib.email_ON = True
        RPLib.email_To = ("jonedoe@server.com","janedoe@server.com")
        RPLib.email_From = "janesmith@server.com"
        RPLib.email_IP = "10.1.1.1"
        RPLib.email_Port = "25"
        RPLib.email_Username = "janesmith" # if domain is required try domain\\janesmith
        RPLib.email_Password = "password"

        dataOwner = "C:/GIS/GISADMIN@GIS.sde"

        RPLib.clearworkspacecache(dataOwner)


Example 2
---------------------------------------------
    * **Simple call to send emails with required parameters specified and user specified Subject and Msg.**
    * **Notice we are sending our own messages outside of the RPLib functions error handling.**
    * **In this example we want to know when the process begins and ends.**

    ::

        import RPLib

        RPLib.email_ON = True
        RPLib.email_To = ("jonedoe@server.com","janedoe@server.com")
        RPLib.email_From = "yournamehere@gmail.com"
        RPLib.email_IP = "smtp.gmail.com"
        RPLib.email_Port = "587"
        RPLib.email_Username = "yournamehere"
        RPLib.email_Password = "password"

        Subject = "The process has started"

        # Msg represents the body of the email.
        Msg = "The automated nightly task has started"

        RPLib.email(Subject, Msg)

        # do stuff here
        #
        #

        Subject = "The process has ended"

        # Msg represents the body of the email.
        Msg = "The automated nightly task has ended"

        RPLib.email(Subject, Msg)
