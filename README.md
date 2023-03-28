Asynchronous consumption of the Questor Zen API
==========

# This Project

This project goal, is create an asynchronous solution for consuming the **Questor Zen** API to make a bulk API post in a short amount of time.

This was not meant to be used frequently, for this use the Questor Connect app. The intent use is make one large send of XML files, mainly for migrating legacy files.  

**Important**: This script causes considerable stress on the Questor's servers. Do not use it without first consulting the supplier, without prior planning, your API key may be blocked.


# What is Questor Connect and Questor Zen 🤓

Questor Connect is a tool use by some accounting offices contact to help with the receipt of tax documents in the extension XML, use by the brazilian government. It is responsibility of they customers to send this files. Those documents are essencial to make a correct tax bookkeeping, tax returns and tax calculation.

The tool allow the automatic capture of the XML files using the public key certificate emitted by the brazilian government or get files for a given folder. After capchered this documents, it sends to the accounting office through the web app **Questor Zen**.   

The software was developed to work 24/7, so it has limitations to send a lot of files at once to Zen, since is better send a few files for a longer time, to avoid stress on their server.  


# Requirements
Install this modules:
```
pip install aiohttp
pip install peewee
pip install asyncio
pip install elementpath
pip install requests
```

# Run ▶️
**Important**: Remember to run the sript prior or after to brazilian business hours.

You must run the ```main.py``` file, and inform the variables below:
1. ```main_url```: Case the site you use to acesses is: https://**escritorio**.app.questorpublico.com.br, inform "**escritorio**".
2. ```root_dir```: "C:\Folder contaning XMLs"
3. ```token```: The same use in the Questor Connect configuration.

During the execution the program will do:

1. Creation of a database to register the process and the responses with the name ```files.db```.
2. All files in the folder ```root_dir``` will be queried, validated and saved in the database.
3. The XML files will be sent in large packages unsynchronized to the Zen questor.

# 🏃 Results 🏃

In my tests, after the 2nd step, was possible to send 2.000 files in 180 seconds. In general the **Connect** sents 15 XMLs in the same amount of time.

In two weekends and one night shift, I was able to send almost 1M XMLs. This would took 5 months using the **Connect** app.    

# 😅 Problems 🤔

Is not all roses. In some moments the API would keeps responding with 500 error in every call. And after wating 24 hours, it was possible to send the files without errors.

To conclude the whole process, I needed to rerun the script 3 or 4 times in different days.
After analysis, I came to the conclusion that my code was correct and probably the Questor server was blocking me, even when they told me that no block was put in my user.

Maybe my code was an error, but since my goal is just run once, it achieved the end result, so I decided to share with the community. 

Use at will! 😄
