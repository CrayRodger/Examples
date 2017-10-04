

import numpy as np
import pandas as pd
import pandas.io.sql as psql
import pyodbc


#Parameters

server = 'localhost'
db = 'tempdb'
#ConStr = 'DRIVER = {SQL Server}; Server =' + server + ';DATABASE =' + db + ';Trusted_Connection=yes'
ConStr = (
    r'Driver={SQL Server};'
    r'Server=localhost;'
    r'Database=tempdb;'
    r'Trusted_Connection=yes;'
    )
print (ConStr)

conn = pyodbc.connect(ConStr)
sql='SELECT * FROM [dbo].[TableFromExcel]'
df = pd.read_sql(sql,conn)
conn.close()

T = 2
mu = df['Numbers'].mean()
sigma = df['Numbers'].std()
S0 = 20
dt = 0.01
N = round(T/dt)
t = np.linspace(0, T, N)

#Loop
for x in range(0, 20):
    W = np.random.standard_normal(size = N) 
    W = np.cumsum(W)*np.sqrt(dt) ### standard brownian motion ###
    X = (mu-0.5*sigma**2)*t + sigma*W 
    S = S0*np.exp(X) ### geometric brownian motion ###
    conn = pyodbc.connect(ConStr)
    cursor = conn .cursor()
    for row in range(0,t.size-1):
        cursor.execute('insert into [dbo].[PythonData](X, Y) values (?, ?)', t[row], S[row])
        conn.commit()
            
    conn.close()






