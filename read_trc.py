def read_trc(filename, folder, home):
    import pandas, os
    os.chdir(folder)
    MarkerHeaders = pandas.read_table(filename, sep='\t', skiprows=3, nrows=1) #read in header/column name data
    for i in range(2, MarkerHeaders.size-2, 3):
        # rename each column name to have an X, Y, or Z
        # print(i)
        MarkerHeaders.rename(columns={MarkerHeaders.columns[i+1]: MarkerHeaders.columns[i] + 'Y'}, inplace=True)
        MarkerHeaders.rename(columns={MarkerHeaders.columns[i+2]: MarkerHeaders.columns[i] + 'Z'}, inplace=True)
        MarkerHeaders.rename(columns={MarkerHeaders.columns[i]: MarkerHeaders.columns[i] + 'X'}, inplace=True)
    MarkerXYZ = pandas.read_table(filename, sep='\t', skiprows=3, usecols=list(range(0, MarkerHeaders.columns.size)))
    for i in range(0, MarkerHeaders.columns.size-1):
        # Replace original column names with new column names
        # print(i)
        MarkerXYZ.rename(columns={MarkerXYZ.columns[i]: MarkerHeaders.columns[i]}, inplace=True)
    MarkerXYZ = MarkerXYZ.drop(index=0) # drop X Y Z row
    MarkerXYZ = MarkerXYZ.loc[:, ~MarkerXYZ.columns.str.contains('^Unnamed')] # remove unnamed columns
    os.chdir(home)
    return MarkerXYZ