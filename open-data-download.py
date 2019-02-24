import urllib.request
import shutil
import os.path


folder = "d:/dev/alice/alidata/000139038/"
#index = 1

for index in range(1, 20):
    url = "http://opendata.cern.ch/record/1102/files/assets/alice/2010/LHC10h/000139038/ESD/{:04}/AliESDs.root".format(index)
    filename = os.path.join(folder, "AliESDs.{:04}.root".format(index))
    print("Downloading '{}' to {}".format(url, filename))
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print("Complete")