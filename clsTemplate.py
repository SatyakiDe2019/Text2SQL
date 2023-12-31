################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  27-Dec-2023               ####
#### Modified On: 31-Dec-2023               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the template for    ####
#### OpenAI prompts to get the correct      ####
#### response.                              ####
####                                        ####
################################################

# Template to use for the system message prompt
templateVal_1 = """### Instructions:
Your task is convert a question into a SQL query, given a SQLLite database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float

### Input:
Generate a SQL query that answers the questioq `{question}`.
This query will run on a database whose schema is represented in this string:
"""

templateVal_2 = """
### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
```sql
"""
