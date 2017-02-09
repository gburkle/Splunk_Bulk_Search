
Splunk Bulk Search

This is an interactive script that will make use of a provided file listing IP addresses and/or URL's and search your instance of Splunk for them "one by one".

This script relies 100% on splunk-sdk and REST API. (http://dev.splunk.com/sdks) 

There might be a better way to go about this, but I decided to code the script to get back into Python Scripting.

Install:
Download Folder/Script and place it inside your Splunk-sdk folder. 

[2] Bulk Search: Search list of IPs/Urls one by one. It looks just for the first hit ( | head 1) 
    The intention is to search a big list as fast as possible and get only results that you can then use to dig deeper. 
    Creates a "hits.txt" file with IPs/Urls that returned results.
    Created a "already_checked.txt" with IP's/Urls that have already been checked. (In case you need to cut the search short, or something     goes wrong you can pick up where you left)
