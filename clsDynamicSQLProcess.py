#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 17-Dec-2023                         ####
#### Modified On 31-Dec-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### Open AI libraries to dynamically                ####
#### create the SQL & execute on the source data to  ####
#### rerteive desired results.                       ####
####                                                 ####
#########################################################

import pandas as pd
from clsConfigClient import clsConfigClient as cf
import requests
import json

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
from sqlalchemy.schema import CreateTable

import re
from datetime import datetime, timedelta

import clsTemplate as ct

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################
# Global Variables

# Create a SQLite database in memory
engine = create_engine('sqlite:///:memory:')

templateVal_1 = ct.templateVal_1
templateVal_2 = ct.templateVal_2
###############################################
###    End of Global Section                ###
###############################################

class clsDynamicSQLProcess:
    def __init__(self):
        self.authorName = 'Satyaki De'
        self.website = 'www.satyakide.com'
        self.prevSessionDBFileNameList = []
        self.prev_create_table_statement = ''
        self.flag = 'N'
        self.url = cf.conf['BASE_URL']

    # Sample function to convert text to a vector
    def text2SQLBegin(self, DBFileNameList, fileDBPath, srcQueryPrompt, joinCond, debugInd='N'):

        question = srcQueryPrompt
        create_table_statement = ''
        jStr = ''

        print('DBFileNameList::', DBFileNameList)
        print('prevSessionDBFileNameList::', self.prevSessionDBFileNameList)

        if set(self.prevSessionDBFileNameList) == set(DBFileNameList):
            self.flag = 'Y'
        else:
            self.flag = 'N'

        if self.flag == 'N':

            for i in DBFileNameList:
                DBFileName = i

                FullDBname = fileDBPath + DBFileName
                print('File: ', str(FullDBname))

                tabName, _ = DBFileName.split('.')

                # Reading the source data
                df = pd.read_csv(FullDBname)

                # Convert all string columns to lowercase
                df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

                # Convert DataFrame to SQL table
                df.to_sql(tabName, con=engine, index=False)

                # Create a MetaData object and reflect the existing database
                metadata = MetaData()
                metadata.reflect(bind=engine)

                # Access the 'users' table from the reflected metadata
                table = metadata.tables[tabName]

                # Generate the CREATE TABLE statement
                create_table_statement = create_table_statement + str(CreateTable(table)) + '; \n'

                tabName = ''

            for joinS in joinCond:
                jStr = jStr + joinS + '\n'

            self.prevSessionDBFileNameList = DBFileNameList
            self.prev_create_table_statement = create_table_statement

            masterSessionDBFileNameList = self.prevSessionDBFileNameList
            mast_create_table_statement = self.prev_create_table_statement

        else:
            masterSessionDBFileNameList = self.prevSessionDBFileNameList
            mast_create_table_statement = self.prev_create_table_statement

        inputPrompt = (templateVal_1 + mast_create_table_statement + jStr + templateVal_2).format(question=question)

        if debugInd == 'Y':
            print('INPUT PROMPT::')
            print(inputPrompt)

        print('*' * 240)
        print('Find the Generated SQL:')
        print()

        DBFileNameList = []
        create_table_statement = ''

        return inputPrompt

    def text2SQLEnd(self, srcContext, debugInd='N'):
        url = self.url

        payload = json.dumps({"input_text": srcContext,"session_id": ""})
        headers = {'Content-Type': 'application/json', 'Cookie': cf.conf['HEADER_TOKEN']}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text

    def sql2Data(self, srcSQL):
        # Executing the query on top of your data
        resultSQL = pd.read_sql_query(srcSQL, con=engine)

        return resultSQL



    def genData(self, srcQueryPrompt, fileDBPath, DBFileNameList, joinCond, debugInd='N'):
        try:
            authorName = self.authorName
            website = self.website
            var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            print('*' * 240)
            print('SQL Start Time: ' + str(var))
            print('*' * 240)

            print('*' * 240)
            print()

            if debugInd == 'Y':
                print('Author Name: ', authorName)
                print('For more information, please visit the following Website: ', website)
                print()

                print('*' * 240)
            print('Your Data for Retrieval:')
            print('*' * 240)

            if debugInd == 'Y':

                print()
                print('Converted File to Dataframe Sample:')
                print()

            else:
                print()

            context = self.text2SQLBegin(DBFileNameList, fileDBPath, srcQueryPrompt, joinCond, debugInd)
            srcSQL = self.text2SQLEnd(context, debugInd)

            print(srcSQL)
            print('*' * 240)
            print()
            resDF = self.sql2Data(srcSQL)

            print('*' * 240)
            print('SQL End Time: ' + str(var))
            print('*' * 240)

            return resDF

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            df = pd.DataFrame()

            return df
