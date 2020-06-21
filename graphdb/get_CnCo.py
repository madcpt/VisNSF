import json

test = '{"result": "true", "ratifyNo": "20001008", "projectAdmin": "271054", "participants": [["583099", "u6768u5149", "u526fu6559u6388", "", "u4e2du5c71u5927u5b66"], ["525545", "u5f20u732eu660e", "u535au58ebu751f", "", "u4e2du5c71u5927u5b66"], ["564362", "u6768u6d0bu6ea2", "u8bb2u5e08", "", "u4e2du5c71u5927u5b66"], ["510213", "u9676u519b", "u535au58ebu751f", "", "u4e2du5c71u5927u5b66"], ["622460", "u90d1u7ecdu826f", "u7855u58ebu751f", "", "u4e2du5c71u5927u5b66"], ["622031", "u4efbu6625u971e", "u7855u58ebu751f", "", "u4e2du5c71u5927u5b66"], ["pj9c4b84a3275a7b8b58a08a24f4bf5bf3", "u6731u6000u521a", "u7855u58ebu751f", "", "u4e2du5c71u5927u5b66"], ["pj264cf996e7a800ee7861f4b9319963f1", "u6d2au60e0u73b2", "u5de5u7a0bu5e08", "", "u4e2du5c71u5927u5b66"]]}'

test2 = '{"result": "true", "ratifyNo": "30170499", "projectAdmin": "271897", "participants": [["100075145", "u5218u6d2au8273", "u7855u58ebu751f", "", "u4e2du56fdu79d1u5b66u9662u6d77u6d0bu7814u7a76u6240"], ["pj1380f7e43ffd3f79eb38295c83e777d4", "u5b59u6d77u5b9d", "u526fu7814u7a76u5458", "", "u4e2du56fdu79d1u5b66u9662u6d77u6d0bu7814u7a76u6240"], ["pj0b4fbb88720f5249a29bff2ca722473e", "u9a6cu5723u5a9b", "u7814u7a76u5b9eu4e60u5458", "", "u4e2du56fdu79d1u5b66u9662u6d77u6d0bu7814u7a76u6240"], ["pjaeba6a37ce1f3901991f79ce7402fb1c", "u5e84u4ef2u534e", "u7855u58ebu751f", "", "u4e2du56fdu79d1u5b66u9662u6d77u6d0bu7814u7a76u6240"], ["pjbc33d511d925bcb45721cbdafd65c63c", "MARIE-FRANCO", "u526fu7814u7a76u5458", "", "TECHN.UNI.BRAN/UNSCHWEIG,GERMANY"]]}'

def loadJson(str):
    load_dict = json.loads(str)

    projectAdmin = load_dict["projectAdmin"] 
    ratifyNo = load_dict["ratifyNo"]
    participatantsList = load_dict["participants"]

    print(projectAdmin)

loadJson(test)
# print(test)