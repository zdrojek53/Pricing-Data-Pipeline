# Pricing Data Pipeline  
Automatically transforms supplier pricelists into import-ready form, reducing each pricelist import from 2 hours to a couple of minutes and import minimizing errors.  
Python version: *Python 3.14.6*

## The problem  
Manual repricing took about 2 hours per supplier, with more than 20 suppliers it becomes a bit of problem. Doing it manually also meant human errors.

## What it does  
* Pipeline takes multiple supplier pricelist and yaml configs.  
* Cleans up and transforms these pricelists.  
* Merges them with SQL Server data and compares.  
* Generates an import-ready file.  

## Business rules  
new_price = supplier_price x multiplier x (1 + margin) x exchange_rate  
Duplicates are removed, unmatched products have their prices zeroed out, invalid prices need to be manually verified (per suspicious price difference).

## Tech stack
Python, pandas, SQLAlchemy/pyobdc, Pydantic

