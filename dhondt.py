import dataprocessing as dp
import pandas as pd


def dhodnt(schools, committeelist):
    school_committees = committeelist.copy()
    for committee in school_committees.keys():
        school_committees[committee] = 0
    for i in range(schools):
        greatest = max(committeelist, key = committeelist.get)
        school_committees[greatest] += 1
        committeelist[greatest] *= (school_committees[greatest])/(1+school_committees[greatest])
    # print(school_committees)
    # print(committeelist)
    return school_committees

# if __name__ == "__main__":
#     test_committees = {"UNSC": 20, "UNHRC": 45, "Adhoc": 15}
#     # df = dp.load_data_as_dataframe("testcsv2")
#     comitee = dhodnt(11,test_committees.copy())
#     print("------------")
#     print(comitee)
#     print(test_committees)
#     print("------------")
#     for committee in comitee.keys():
#         test_committees[committee] -= comitee[committee]
#     print(comitee)
#     print(test_committees)