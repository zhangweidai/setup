import pandas as pd

df = pd.DataFrame({'B': [1, 1, 1], 'C': [1, 1, 1], 'D':[3,3,3]})
avg = list()
for idx,row in df.iterrows():
    print (sum(row[0:2]))
    avg.append((df.at[idx,"B"] + df.at[idx,"C"])/2)
    
print (df)
idx = 3
df.insert(loc=idx, column='Avg', value=avg)
print (df)
