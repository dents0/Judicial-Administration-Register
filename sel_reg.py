from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Launch URL
url = "https://amministratorigiudiziari.giustizia.it/pst/RAG/AlboPubblico.aspx"


def create_driver():
    ''' Creates new Chrome session '''
    global driver
    driver = webdriver.Chrome(
        executable_path="C:/Users/denis/Desktop/PYTHON/PythonProjects/WebScrapping/Giustizia/chromedriver_win32/chromedriver")
    driver.implicitly_wait(30)
    driver.get(url)


def get_data():
    ''' Goes through all pages and grabs data from the table '''

    global surnames, firstnames, dob, positions, numbers, subscribed, emails, statuses, last_updates
    # Empty lists, which will store the scraped data
    surnames, firstnames, dob, positions, numbers, subscribed, emails, statuses, last_updates = \
        [], [], [], [], [], [], [], [], []

    pages_remaining = True
    while pages_remaining:  # Go through all pages and grab the data

        # Hand the page source to Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "lxml")
        t = soup.find("table", {"id": "gvAmministratori"})  # Locate the table
        # Grab data from the table and remove unnecessary elements
        clean_data = [tdata.get_text() for tdata in t.select("tr td")]
        for tdata in clean_data:
            if tdata == "\n\n":
                clean_data.remove(tdata)
            elif tdata == "\xa0":
                i = clean_data.index(tdata)
                del clean_data[i:]
            else:
                pass

        # Add scraped data to the relevant empty lists
        surnames.append(clean_data[0::9])
        firstnames.append(clean_data[1::9])
        dob.append(clean_data[2::9])
        positions.append(clean_data[3::9])
        numbers.append(clean_data[4::9])
        subscribed.append(clean_data[5::9])
        emails.append(clean_data[6::9])
        statuses.append(clean_data[7::9])
        last_updates.append(clean_data[8::9])

        # Click the "next page" button while it's available
        try:
            btn = driver.find_element_by_xpath('//*[@id="gvAmministratori_ctl23_ImageButton3"]')
            btn.click()
        # End the loop when the last page is scraped and there is no "next page" button left
        except NoSuchElementException:
            pages_remaining = False


def create_df():
    ''' Creates a dataframe from the lists with scraped information '''
    df = pd.DataFrame({
        "COGNOME": [item for sublist in surnames for item in sublist],
        "NOME": [item for sublist in firstnames for item in sublist],
        "DATA DI NASCITA": [item for sublist in dob for item in sublist],
        "ORDINE APPARTENENZA": [item for sublist in positions for item in sublist],
        "NR. ISCRIZIONE": [item for sublist in numbers for item in sublist],
        "DATA ISCRIZIONE": [item for sublist in subscribed for item in sublist],
        "PEC": [item for sublist in emails for item in sublist],
        "STATO ISCRIZIONE": [item for sublist in statuses for item in sublist],
        "ULTIMO AGGIORNAMENTO": [item for sublist in last_updates for item in sublist]
    })
    return df


def create_sheet(xpath=""):
    '''
    Creates and returns a dataframe.
    As the webpage has 2 tabs with content, 2 dataframes will be created.

    To access the second tab a button has to be clicked, therefore the function takes
    an optional parameter "xpath".
    '''
    create_driver()
    if xpath == "":
        pass
    else:
        btn = driver.find_element_by_xpath(f'{xpath}')
        btn.click()
    get_data()
    driver.quit()  # End the Chrome session
    return create_df()


ordinary = create_sheet()  # Tab "Sezione Ordinaria"
experts = create_sheet('//*[@id="rdblSezione_1"]')  # Tab "Sezione Esperti in Gestione Aziendale"

# Writing created dataframes into the Excel file
with pd.ExcelWriter('data_table.xlsx') as writer:
    ordinary.to_excel(writer, sheet_name="Sezione Ordinaria", index=False)  # Excel Sheet 1
    experts.to_excel(writer, sheet_name="Sezione Esperti", index=False)  # Excel Sheet 2
