def read_filenames(filestofind):
    import os, re
    ##returns list of filenames to with
    compiledexp = str()
    for substring in filestofind:
        compiledexp += '(?=.*'+substring+')'
    for root, dirs, files in os.walk("."):
        files = [filename for filename in files if bool(re.search(compiledexp, filename))]
        return files
