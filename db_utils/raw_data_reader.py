import zipfile
import json
import xml.dom.minidom as xd


def processYearInfo(year):
    file = zipfile.ZipFile("./data/NSF_US_data/%d.zip" % year, "r")
    awards_list = []
    for name in file.namelist():
        try:
            AwardJson = processXML(file, name)
            AwardJson['year'] = year
            awards_list.append(AwardJson)
        except:
            pass
    return awards_list


def processXML(zip_loader, xml_name):
    AwardJson = {}
    data = zip_loader.read(xml_name).decode('utf-8').replace('\n', '')
    doc = xd.parseString(data)
    root: xd.Element = doc.documentElement
    assert len(root.childNodes) == 1 and root.childNodes[0].tagName == 'Award'
    award_node = root.childNodes[0]
    try:
        AwardTitle = award_node.getElementsByTagName('AwardTitle')[0].firstChild.data
    except:
        AwardTitle = 'EmptyTitle'
    try:
        Amount = int(root.getElementsByTagName('AwardAmount')[0].firstChild.data)
    except:
        Amount = -1
    AwardJson['awardID'] = xml_name[:-4]
    AwardJson['amound'] = Amount
    AwardJson['title'] = AwardTitle
    AwardJson['investigators'] = []
    for investigator in award_node.getElementsByTagName('Investigator'):
        try:
            FName = investigator.getElementsByTagName('FirstName')[0].firstChild.data
        except:
            FName = ''
        try:
            LName = investigator.getElementsByTagName('LastName')[0].firstChild.data
        except:
            LName = ''
        try:
            email = investigator.getElementsByTagName('EmailAddress')[0].firstChild.data
        except Exception:
            email = ''
        if FName == '' and LName == '':
            continue
        else:
            AwardJson['investigators'].append(
                {'firstName': FName, 'lastName': LName, 'email': email})
    return AwardJson


if __name__ == '__main__':
    # awards = []
    # from tqdm import tqdm
    # for year in tqdm(range(2000, 2021), total=21):
    #     awards = awards + processYearInfo(year)
    # with open('./data/NSF_US_data/2000-2021_dump.json', 'w') as f:
    #     json.dump(awards, f, indent=4)
    with open('./data/NSF_US_data/2000-2021_dump.json', 'r') as f:
        awards = json.load(f)
    print(len(awards))

