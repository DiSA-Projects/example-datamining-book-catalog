# Using Python for Data Mining 
Python code to extract data from an Excel spreadsheet or csv file to produce reports. 
_Original code by Neil Aitken, Digital Scholarship in the Arts, UBC_

## Summary
Often we will get data in the form of an Excel spreadsheet (.xlsx) or a csv file (.csv). Although some queries and research questions can be answered 
using just pandas (Python library for data parsing and analytics), sometimes we have more complicated questions to ask about the dataset that might require a more sophisticated approach. This toolkit turns each 
line entry in the dataform into a Record and then collects all the Records into a Catalog object. The Catalog provides prebuilt functions that handle common types of questions we might have about the dataset, as well as 
more intuitive ways to access and compare the data to create reports.

The example code is designed for working with a mock course reserve data dump (either csv or xlsx), but the approach should work or be easy to modify to meet the needs of other projects and datasets.

## Features
The provided files include:
1. _example_datamining.py_: a code template that defines the Record and Catalog objects, then provides an example of how to use them for handling a dataset pulled from an Excel or csv file.
2. _course_reserve_dataset.csv_: a dummy dataset mimicking what an online course reserve data dump might look like
3. _example_datamining_course_reserves.ipynb_: an example of the code as embedded in a Google/Jupityr Notebook 

You can create your own mock dataset using the pyDatasetGen toolkit - this might be useful if you need a dataset that meets different requirements (different elements, field names, etc).

## Instructions (Google Colab or Jupityr Notebook)
If you want to test this process out without installing anything new, you can use the Notebook file (for either Google Colab or Jupityr Notebook).
1. Download a copy of _example_datamining_course_reserves.ipynb_
2. Download a copy of _course_reserve_dataset.csv_
3. Import the notebook into Jupityr or Google Collab
4. Follow the instructions in the notebook and upload the csv file

## Instructions (Local Install)
If you prefer to run Python on your local machine, create a new folder for this project and follow these steps
1. Download a copy of _example_datamining.py_
2. Download a copy of _course_reserve_dataset.csv_
3. Open the folder as a workspace in VS Code (or whatever your code editor/IDE is).





