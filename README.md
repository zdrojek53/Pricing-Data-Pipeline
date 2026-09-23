# Pricing Data Pipeline
## Software that takes in pricing data in excel / pdf format and transforms it to be import-ready.
It's a project that is supposed to take some hours off my coworkers and me, I started it from my own initiative.

**How it works**  
    * The pipeline takes in an input excel file (adapters/ConfigAdapter.py) and sends a query to the database (db_extraction/extract_db_data.py)  
    * Data extraction and transformation depend on a config file 
    * Load process is performed in (main.py), it outputs correctly formatted .xlsx file  

**Future plans**  
    * Implementing pdf scraping


