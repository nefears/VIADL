def read_filenames(filestofind):
    import os
    ##returns list of filenames to with
    for root, dirs, files in os.walk("."):
        files = [filename for filename in files if filename.endswith((filestofind))]
        return files
