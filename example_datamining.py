# Example: Data Mining Online Reserve Records
import os
import csv
import pandas as pd

DATA_FILE = 'course_reserve_dataset.csv'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define path to files in the current directory
def resource_path(relative_path):
    import sys
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,os.path.join(CURRENT_DIR,relative_path))
    return os.path.join(CURRENT_DIR, relative_path)# Load csv file and returns dataframe

# ==============================================================
# FILE LOADING
# ==============================================================
# Load a csv file
def load_csv(fname):
   import pandas as pd
   return pd.read_csv(fname)

# Load excel file and returns dataframe
def load_excel(fname):
  import pandas as pd
  return pd.read_excel(fname)

# Load file and determine if Excel or csv, then return dataframe
def load_datafile(fname):
  start = len(fname)-5
  if start < 0:
    start = 0
  num_periods = fname.count('.',start,len(fname))
  if num_periods == 1:
    name,extension = fname.split('.')
    if extension == 'xlsx' or extension == 'xls':
      print('Excel sheet')
      return load_excel(fname)
    else:
      print('CSV doc')
      return load_csv(fname)
  elif num_periods == 0:
    print('Filename should have a .csv, .txt, or .xlsx extension')
  else:
    print('Filename is improperly formatted. Please rename and ensure it is a CSV or Excel file')
  return None

# ==============================================================
# RECORD - an object wrapper for each record in the dataset
# ==============================================================

class Record:
    # Setup Record from row from a dataframe
    def __init__(self,keys,datalist):
        i = 0
        self.keys = keys

        for val in datalist:
            setattr(self,str(keys[i]),val)
            i+=1

        # Each entry in the course reserves data has a course code and course number stored separately.
        # We combine them to form the course ID and store it in the record as a new field to save time
        try:
          self.course_id = str(getattr(self,'Course code'))+' '+str(self.Coursenumber)
        except:
          print(f'Keys = {keys}')

    # Set/reset the record using the column names and row data from a row
    def read(self,headers,series):
      for hd in headers:
        setattr(self,hd,series[hd])

    # Return the value for a given key/field, or return everything if given "all"
    def get(self,rkey='all'):
        if rkey == 'all' or not rkey in vars(self):
            result =''
            for key in vars(self):
                result = result +'\n' + getattr(self,key)
            return result
        else:
            return getattr(self,rkey)

    # Check to see if the record contains a given value or partial search string
    def has_str(self,searchstr):
        import re
        for key in vars(self):
            strmatch = re.search(searchstr,self.get(key))
            if not strmatch==None:
                return True
        return False

    # Return the contents of the record as a printable string, either in brief format, just the keys, or containing everything 
    def dump(self,rkey='all'):
        if rkey=='brief':
            result = '"'+str(self.Title)+'," '+str(self.Author)+', '+str(getattr(self,'Call number'))+' '+str(self.course_id)
        elif rkey == 'all' or not rkey in vars(self):
            for key in vars(self):
                if not key == 'keys':
                    result = key+': '+str(getattr(self,key))
        elif rkey=='keys':
            result = self.keys
        else:
          result = rkey+': '+str(getattr(self,rkey))
        return result

    # Print the contents of the record to the terminal
    def print(self,rkey='all'):
      print(self.dump(rkey))


# ==============================================================
# CATALOG - An object wrapper for managing a set of Records
# ==============================================================
class Catalog:
    # Setup Catalog by reading in a dataframe and all its contents as Records
    def __init__(self,df):
        self.dataframe = df
        self.catalog = []
        self.keys = df.columns
        for ind in range(0,len(df)):
             record = Record(self.keys,list(df.loc[ind]))
             self.catalog.append(record)

    # Print the catalog's records by dumping the contents of each record
    def print(self,key='all'):
        for ind in range(0,len(self.catalog)):
            print(self.catalog[ind].print(key))

    # Return the catalog
    def get(self):
        return self.catalog

    # Search the catalog for all records containing a match or partial match of the value for a given key
    def search(self,key,value):
        import re
        results = []
        if value == '*':
          return self.catalog

        for record in self.catalog:
            if key in vars(record):
                occ = re.search(value.lower(),str(getattr(record,key)).lower())
                if not occ == None:
                    results.append(record)
            else:
              for k in vars(record):
                occ = re.search(value.lower(),str(getattr(record,k)).lower())
                if not occ == None:
                    results.append(record)

        return results

    # Return a list of courses matching/partial matching a given course id (course code + course number)
    def search_by_course_id(self,courses):
      import re
      results = []
      course_list = courses.split('|')

      for record in self.catalog:
        for course in course_list:
          if record.course_id == course:
            results.append(record)

      return results

    def search_by_keyword(self,searchstr):
      import re
      df = self.dataframe
      results = []
      for ind in range(0,len(df)):
        row = list(df.loc[ind])
        bFound = False
        for i in range(0,len(row)):
          test = re.search(searchstr,str(row[i]).lower())
          if not test == None:
            bFound = True
        if bFound:
          entry = Record(df.loc[ind].index,row)
          results.append(entry)
      for ind in range(0,len(results)):
        results[ind].print('brief')

    def search_by_column(self,colname,searchstr):
      import re
      results = []
      df = self.dataframe
      for ind in range(0,len(df)):
        entry = df.loc[ind]
        test = re.search(searchstr,str(entry[colname]))
        if not test == None:
          headers = ['Title','Author','Course code', 'Coursenumber','Call number']
          if not colname in headers:
            headers.append(colname)

          citation = Record(entry.index.values,entry.to_list())
          citation.print('brief')
          results.append(citation)
      return results

    def count_by_column(self,results,colname):
      import numpy as np

      bFound = False
      reports = []

      for entry in results:
        entry_field = getattr(entry,colname)
        if entry_field == np.nan or entry_field=='':
          continue
        if reports == []:
          report = {colname:getattr(entry,colname),'count':1}
          reports.append(report)
        else:
          bFound = False
          for rep in reports:

            if getattr(entry,colname) == rep[colname]:
              rep['count'] = rep['count'] + 1
              bFound = True

          if bFound == False:
            report = {colname:getattr(entry,colname),'count':1}
            reports.append(report)

      reports.sort(key=lambda x: x['count'],reverse=True)
      return reports

    def search_by_course_number(self,courses):
      results = []
      df = self.dataframe
      course_list = courses.split('|')

      for course in course_list:
        course_code,course_num = course.split(' ')

        for ind in range(0,len(df)):
          entry = df.loc[ind]
          if entry['Course code'] == course_code and entry['Coursenumber'] == course_num:
            headers = ['Title','Author','Course code', 'Coursenumber','Call number']
            
            citation = ''
            for hd in headers:
              citation = citation +str(entry[hd])+', '
            results.append(citation)

      for ind in range(0,len(results)):
        print(results[ind])

      return


    def search_by_course_id(self,courses):      
      results = []
      course_list = courses.split('|')

      for record in self.catalog:
        for course in course_list:
          if record.course_id == course or record.get("Course code") == course:
            results.append(record)

      return results


    def get_book_report(self,book_title='*',bShow=True):
      print('\n=========================')
      print('BOOK REPORT')
      print('=========================')
      if book_title == '*':
        results = self.get()
      else:
        results = self.search('Title',book_title)

      reports = []

      if results == []:
        print(f'No texts titled {book_title} found.')
        return reports

      results.sort(key=lambda x: str(x.Title))

      bFound = False

      for entry in results:
        if reports == []:
          report = {'title':entry.Title,'count':1,'courses':[entry.course_id],'sessions':[entry.Session]}
          reports.append(report)
        else:
          bFound = False
          for rep in reports:
            if entry.Title == rep['title']:
              rep['count'] = rep['count'] + 1
              rep['courses'].append(entry.course_id)
              rep['sessions'].append(entry.Session)
              bFound = True

          if bFound == False:
            report = {'title':entry.Title,'count':1,'courses':[entry.course_id],'sessions':[entry.Session]}
            reports.append(report)
      if bShow == True:
        for rep in reports:
          print(f'\nTitle: {rep["title"]}\n Count: {rep["count"]}\n Courses: {rep["courses"]}\n Sessions: {rep["sessions"]}')
      return reports

    def get_department_report(self,department='*',bShow=True):
      catalog = self.catalog
      print('\n=========================')
      print('DEPARTMENT REPORT')
      print('=========================')
      if department == '*':
        catalog.sort('Course code')
        results = catalog.get()
      else:
        results = catalog.search('Course code',department)

      reports = []

      if results == []:
        print(f'No department titled {department} found.')
        return reports

      results.sort(key=lambda x: str(getattr(x,'Course code')))

      bFound = False

      for entry in results:
        if reports == []:
          report = {'dept':getattr(entry,'Course code'),'count':1}
          reports.append(report)
        else:
          bFound = False
          for rep in reports:
            if getattr(entry,'Course code') == rep['dept']:
              rep['count'] = rep['count'] + 1
              bFound = True

          if bFound == False:
            report = {'dept':getattr(entry,'Course code'),'count':1}
            reports.append(report)

      reports.sort(key=lambda x: x['count'],reverse=True)

      df_reports = pd.DataFrame(reports)
      df_reports.plot.barh(x='dept',y='count')


      if bShow == True:
        catsize = len(catalog.catalog)
        print(f'\nDepartments using LOCR: {len(reports)}')
        print(f'Number of records: {catsize}')
        for rep in reports:
          print(f'{rep["dept"]} Count: {rep["count"]} Presence:{(rep["count"]/catsize):.1%}')

      return reports

    def get_publisher_report(self,publisher='*',bShow=True):
      print('\n=========================')
      print('PUBLISHER REPORT')
      print('=========================')
      if publisher == '*':
        self.sort('Publisher')
        results = self.get()
      else:
        results = self.search('Publisher',publisher)
      reports = self.count_by_column(results,'Publisher')
      if bShow == True:
        for rep in reports:
          print(f'{rep["Publisher"]} Count: {rep["count"]}')
      return reports

# ==============================================================
# MAIN CODE - Load data and generate reports
# ==============================================================

# Load datafile and create catalog of records
df = load_datafile(DATA_FILE)
catalog = Catalog(df)

# Search for records for column values that match or partially match a given string
catalog.search_by_column('Call number','PR878|PS374|PS648|PN3433')

# Search for records that are affiliated with a course id (or partial match if incomplete id given)
catalog.search_by_course_id('ENGL 505A|ENGL 535A')

# Search for records where the title (can be changed to another field) contains one of the following phrases or terms
# Note '|' represents a logical OR (if X or Y, then return value)
#keywords = 'monster|science fiction|fantasy|speculative fiction|horror|weird|spec fic|fairy tale|paranormal|robot|automaton|automata|artificial intelligence|future|climate fiction|dystopian|apocalypse|apocalyptic'
keywords = 'history|physics|intro'
results = catalog.search('Title',keywords)

for result in results:
  result.print('brief')

# Generate a report on books with titles that contain the given phrase
# Report identifies all books with the given phrase as part of their title, then counts the number of records in the catalog for each title
reports = catalog.get_book_report("history")    
#for report in reports:
#  report.print('brief')

# Generate a report on publishers whose names match or partially match a given phrase
# Report identifies how many records are associated with each publisher
reports = catalog.get_publisher_report("Taylor")    
#for report in reports:
#  report.print('brief')