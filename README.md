Parsing a Register of Judicial Administration
=============================================
Licensing information: READ LICENSE
----
Project source can be downloaded from https://github.com/dents0/Judicial-Administration-Register.git
----
Author
------
Deniss Tsokarev

Description
-----------
This script uses Python modules **Beautiful Soup**, **Pandas** and **Selenium** to parse the registers and lists of the **Ministry of Justice** of Italy *([Ministero della Giustizia](https://amministratorigiudiziari.giustizia.it/pst/RAG/AlboPubblico.aspx))*.

The script grabs data from 2 main tabs of the webpage: **Sezione Ordinaria** and **Sezione Esperti in Gestione Aziendale**, each of which contains a few dozens of pages with data.

Two dataframes are then created using the parsed information and saved into the Excel file **data_table.xlsx**, into 2 separate sheets.

Requirements
------------
Python 3.6+ 

Modules:

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/)
* [Selenium](https://www.seleniumhq.org/docs/)

How it works
------------
1) Running **admin_reg.py** creates a Crome session in which the script goes through the [webpage](https://amministratorigiudiziari.giustizia.it/pst/RAG/AlboPubblico.aspx)'s first tab *(Sezione Ordinaria)* and parses it's data. Then, the session ends.
#
2) After that, another Chrome session starts and the second tab *(Sezione Esperti in Gestione Aziendale)* gets parsed. The session terminates thereafter.

![terminal](https://user-images.githubusercontent.com/28843507/56517914-68ac2280-653e-11e9-8eae-a0c9b9320e8a.PNG)
#
3) Once the Chrome sessions are finished, the script creates two dataframes *(one for each session's data respectively)* and writes them into the specified Excel file.

![sc1](https://user-images.githubusercontent.com/28843507/56607484-eb011900-6608-11e9-819e-cc3303058548.PNG)
#
4) Data from each tab of the parsed webpage will be stored in the Excel file on a separate sheet:

*Sheet 1*
![sheet1](https://user-images.githubusercontent.com/28843507/56517998-9c874800-653e-11e9-8e33-a61128ce92a8.PNG)

*Sheet 2*
![sheet2](https://user-images.githubusercontent.com/28843507/56518076-c93b5f80-653e-11e9-8ebb-6002f280419b.PNG)
