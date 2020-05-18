import zipfile

file = zipfile.ZipFile("./data/NSF_US_data/2000.zip", "r")
for name in file.namelist():
    data = file.read(name)
    # print(name, len(data), repr(data[:10]))
    print(data)
    break
