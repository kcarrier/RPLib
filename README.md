RPLib
=====

RPLib is short for Reconcile and Post Library. This is a useful collection of Esri tools and Python functions for
enterprise geodatabase administration. Esri provides many useful tools for geodatabase administration tasks, but when
building a model and exporting it to a Python script, by default, it will typically lack things like iterators, error
trapping, email notification when something does not work as expected, and the ability to control the level of logging
details. RPLib is an attempt to compliment Esri’s tools by providing enhanced error trapping, more useful error handling
and messages, emailing capabilities, more control of logging, and the ability to build if then logic into your scripts
so if a process does not work as expected you can kick off another set of events. Much of the documentation for each
function/tool was taken directly from Esri’s help pages in an effort to be consistent with terminology. Many in the GIS
community wear multiple hats within their organization and some wear all the hats for their organization. The purpose of
building RPLib was to make it easier for those within the community to automate administrative tasks that might have otherwise
been done manually, until now. Hopefully this collection of functions will be useful to your organization and if there are
other functions or processes that would be useful to the community please share and we will try to add it to a future release, thank you!

Updates
=============
04/03/2014 - Added executesql function

Documentation
=============
<a href="http://kcarrier.github.io/RPLib/index.html" target="_blank">Click here</a> for detailed instructions on Installation, List of Functions and Variables, and Implementation Examples.
