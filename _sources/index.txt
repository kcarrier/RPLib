.. test documentation master file, created by
   sphinx-quickstart on Wed Oct 09 09:08:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RPLib documentation!
================================

**Welcome to RPLib documentation, RPLib is short for Reconcile and Post Library. This is a useful collection of Esri tools and Python functions for enterprise geodatabase administration. Esri provides many useful tools for geodatabase administration
tasks, but when building a model and exporting it to a Python script, by default, it will typically lack things like iterators, error trapping, email notification when something does not work as expected, and the ability to
control the level of logging details. RPLib is an attempt to compliment Esri's tools by providing enhanced error trapping, more useful error handling and messages, emailing capabilities, more control of logging, and the ability to build
if then logic into your scripts so if a process does not work as expected you can kick off another set of events. Much of the documentation for each function/tool was taken directly from Esri's help pages in an effort to be consistent with
terminology. Many in the GIS community wear multiple hats within their organization and some wear all the hats for their organization. The purpose of building RPLib was to make it easier for those within the community to automate administrative
tasks that might have otherwise been done manually, until now. Hopefully this collection of functions will be useful to your organization and if there are other functions or processes that would be useful to the community
please share and we will try to add it to a future release, thank you!**

Installation
================================
1. Install Python(2.7.x), if you have installed ArcGIS Desktop 10.1 or higher this should have already been installed for you.

2. Typical installs of ArcGIS Desktop will place the folder here inside this folder **"C:\\Python27"**, once inside this folder should see a folder representing the version of ArcGIS Desktop you currently have installed.

    a) **ArcGIS10.1**

    b) **ArcGIS10.2**

3. Copy |RPLib.py| into the folder representing the currently installed version of ArcGIS Desktop. For example;

    a) **C:\\Python27\\ArcGIS10.1**


    b) **C:\\Python27\\ArcGIS10.2**




4. Setup a permanent path for Python **(recommended)** **{optional}**.

    a) **Windows**

        - Right-click My Computer


        - Advanced System Settings --> Advanced tab --> Environment variables


        - Under System Variables Add (or Edit if PYTHONPATH already exists)


            - Variable name  = PYTHONPATH


            - Variable value = add your path here, e.g., **C:\\Python27\\ArcGIS10.x**, "x" represents the version of ArcGIS Desktop you currently have installed


    b) **Mac**

        - Open up Terminal.

        - Type open .bash_profile

        - In the text file that pops up, add this line at the end: export PYTHONPATH=$PYTHONPATH:foo/bar

            - export PYTHONPATH=$PYTHONPATH:foo/bar

            - Replace foo/bar with your path, e.g., ~/Documents/Python/Modules

            - Save the file, restart the Terminal.


5. Install a python IDE(Integrated Development Environment);

    a) |PythonEditors| **for a list of editors and the links to download.**
    b) **PyScripter was used to develop this library but PyScripter is only available to Windows users.**

6. Now open your favorite python editor and try to import RPLib, please remember python is case sensitive

    ::

        import RPLib

    a) **If importing RPLib is successful you should get an empty command prompt or the ability to enter more code.**
    b) **On this new line or prompt type RPLib.clear, if you have intellisense enabled in your editor you should see RPLib.clearworkspacecache.**
    c) **Now you are ready to begin using RPLib.**

Variables
================================
.. toctree::
   :titlesonly:
   :maxdepth: 3

   emailvariables
   loggingvariables

Functions
================================
.. |PythonEditors| raw:: html

   <a href="https://wiki.python.org/moin/PythonEditors" target="_blank">Click here</a>

.. |RPLib.py| raw:: html

    <a href="https://github.com/kcarrier/RPLib/archive/master.zip" target="_blank">RPLib.py</a>

.. toctree::
   :titlesonly:
   :maxdepth: 3

   clearworkspacecache
   pauseconnections
   resumeconnections
   killconnections
   compressgdb
   createversions
   rebuild_indexes_analyze
   reconcilepost
   truncateappend
   syncreplicas
   controlservices
   deletefilesolderthan
   executesql

Implementation Examples
================================
.. toctree::
   :maxdepth: 2

   implementationexamples

Credits
================================
    **I believe in giving credit where credit is due. These are people who have helped in developing RPLib whether they knew it or not. Thank you!**

    **Doug Kotnik(PLI) :** My first mentor who taught me GIS when I knew nothing and allowed me the opportunity to grow.

    **Shawn Dunlavy(MCDIA) :** A mentor who taught me how to be more effective and efficient in problem solving techniques and the power of sharing.

    **Matt Hilliard(MCES) :** A mentor who took my geodatabase administration skills to the next level and presented me with the opportunities to learn more.

    **Eric Moody(MCEO) :** A great friend who has helped me grow my GIS skills by teaching me the finer details of GPS and surveying and who is always pushing me to continue learning through his passion for GIS.

    **Anthony Pagan(MCEO) :** Where to begin, a great and loyal friend who has always given me opportunities to further my programming capabilities by always being willing to be a test site for new ideas, thanks brother!

    **Jason Pardy(Esri) :** Shares with me the best practices for python programming and code structure.

    **Jim Gough(Esri) :** Has always been there to help and explain geodatabase questions, an excellent Esri Instructor and one that I highly recommend!

    **Paul Dodd(Esri) :** Taught me to think outside the box when it came to programming especially with his examples of how to utilize Aggregated Live Feeds(ALF).

    **Eric Rodenberg(Esri) :** Has always been willing to discuss and share new interesting technologies and best practices.

    **Southwest Ohio GIS Users Group(SWOGIS) :** To all my friends in SWOGIS, this library was born out of a need to help others in the GIS community, without all of you this would have never happend. Thank you for always being willing to share!

    **Esri Technical Support :** To the best vendor support group I have ever had the pleasure of working with, your support now and over the years continues to be top notch!

    **Amanda Alamo(CCAO) :** Well cannot forget the boss who allowed me the time and opportunity to build this for our office, thanks Amanda hopefully this helps others as much as it has helped us!

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

