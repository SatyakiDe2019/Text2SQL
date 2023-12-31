#############################################################
#### Written By: SATYAKI DE                              ####
#### Written On: 17-Dec-2023                             ####
#### Modified On 31-Dec-2023                             ####
####                                                     ####
#### Objective: This is the main calling                 ####
#### python script that will invoke the                  ####
#### main class, which will contextualize the source     ####
#### files & then read the data into pandas dataframe,   ####
#### and then dynamically create the SQL & execute it.   ####
#### And, then fetch the data from the sources based on  ####
#### the query generated dynamically.                    ####
####                                                     ####
#############################################################

import clsDynamicSQLProcess as cdsqlp

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

cd = cdsqlp.clsDynamicSQLProcess()

fileDBPath = cf.conf['DB_PATH']
DBFileName = cf.conf['DB_FILE_NM']
DBFileNameList = cf.conf['DB_FILE_LIST']
debugInd = cf.conf['DEBUG_IND']
joinCond = cf.conf['JOIN_CONDITION']

########################################################
################  End Of Global Area   #################
########################################################

def main():
    try:
        var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*' * 240)
        print('Start Time: ' + str(var))
        print('*' * 240)

        print('*' * 240)
        print('Invoking Dynamic SQL:: ')
        print('*' * 240)

        # Define the keyword to exit the loop
        exit_keyword = "exit"

        while True:

            srcQueryPrompt = str(input('Please provide your question: '))

            if srcQueryPrompt.lower() == exit_keyword:
                break
            else:
                print('\n')

                resDF = cd.genData(srcQueryPrompt, fileDBPath, DBFileNameList, joinCond, debugInd)

                print('Result SQL::')
                print()
                print(resDF)

                print('*' * 240)

                r1 = resDF.shape[0]

                if r1 > 0:
                    print()
                    print('Successfully invoking dynamic SQL!')
                else:
                    print()
                    print('Failed to invoke dynamic SQL!')

        print('*' * 240)
        var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
