# vereinsdaten-data-scraper


[GERMAN BELOW / DEUTSCH UNTEN]

## Description
This project allows you to scrape match data from the ÖFB federation homepages. Initially it is build uppon the BFV site but later support for the other sites will be added.

Different methods will be available to scrape the data all following the FAIR use principle. The data can be scraped directly parsing the returned HTML information from GET requests. 

The links to the sites to be scraped will be crawled.

All data and metadata shall be stored in a relational database like Postgres or MariaDB.

## Design
- Database: 
  - Tables for Analysis
    - TEAMS Table (Which Team in which year which league)
    - PLAYER Table (which Player which game which date)
    - GAME Table (which score, which additional game data
  - Tables with additional data
    - Scrape Meta Data Table (stores information about the scraping)
    
- Link Crawler
  - Get links to games
  
- Scraper
  - HTML Parsing with beautiful soap

## Usage

  - Create Database and Load Schema
  - Write Credentials into db.properties file
  - Install requirements.txt
  - Start main.py
---

## Beschreibung
Durch diesen Code kann man Match, Vereins und Spieler Daten von den Homepages des ÖFB und den Verbänden der einzelnen Bundesländer downloaden und in eine Datenbank zur Analyse speichern. Als erstes wird nur das Speichern von Daten vom BFV programmiert, aber später sollen auch die anderen Verbände abgefragt werden.

Dabei sollen unterschiedliche Abfragemethoden unterstützt werden, welche aber alle den FAIR Prinzipien folgen sollen. Als erstes wird das direkte Scrapen und Parsen von HTML Daten unterstützt. 

Die Links zu den Seiten soll ein Crawler finden.

Alle Daten sollen in einer relationalen Datenbank gespeichert werden.

## Design
https://medium.com/@stefan.preusler/selenium-firefox-in-python-auf-einem-ubuntu-server-df4abc818853

>wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz

> tar -xvzf geckodriver-v0.31.0-linux64.tar.gz

> chmod +x geckodriver

> sudo mv geckodriver /usr/local/bin/

> export PATH=$PATH:/usr/local/bin/geckodriver

>pip install selenium webdriver-manager


## Verwendung

setup:

---

### Contact me / Kontaktiere mich



