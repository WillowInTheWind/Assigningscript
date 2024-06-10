import math
import dataprocessing as dp
import dhondt as dh
import pandas as pd
import random


# They must always be order of the column with the key and then the value
def run_and_export_dhodnt(
        committee_names_relevant_columns=["COMMITTEE TYPE", "TYPE", "# of Positions"],
        schools_csv_relevant_columns=["School Name","How many delegates would you like to register for FWPMUN VIII? (Delegate counts may be altered as needed.)"],
        schools_csv="Test-Committee-List-fakereg",
        committees_csv="Test-Committee-List-commitees",
        positions_csv="Test-Committee-List-fakepos",
) -> pd.DataFrame:
    # read in schools
    schools_df = dp.read_in_data(schools_csv, schools_csv_relevant_columns)
    df_dict = schools_df.to_dict()
    new_dict = {}
    for k in range(len(df_dict[schools_csv_relevant_columns[0]])):
        number = df_dict[schools_csv_relevant_columns[1]][k]
        try:
            int(number)
            flag = True
        except ValueError:
            print("not int:", df_dict[schools_csv_relevant_columns[0]][k])
            flag = False
        # flag check

        key = df_dict[schools_csv_relevant_columns[0]][k]
        if flag:
            if key in new_dict:
                new_dict[key] += int(number)
            else:
                new_dict[key] = int(number)
    sorted_schools = dict(sorted(new_dict.items(), key=lambda item: item[1]))

    # ---------------------

    # read in committees
    committees_df = dp.read_in_data(committees_csv, committee_names_relevant_columns)
    committees_dict = committees_df.to_dict()
    committees = {}
    for k in range(len(committees_dict[committee_names_relevant_columns[1]])):
        number = committees_dict[committee_names_relevant_columns[2]][k]
        try:
            int(number)
            flag = True
        except ValueError:
            flag = False
        # flag check
        key = committees_dict[committee_names_relevant_columns[1]][k]
        if flag and int(number) <= 100:
            if key in committees:
                committees[key + "(1)"] = int(number)
            else:
                committees[key] = int(number)

    # find total delegates and positions
    total_positions = 0
    for i in committees.values():
        total_positions += i
    total_delegates = 0
    for i in sorted_schools.values():
        total_delegates += i

    # run d'hodnt if there are enough positions
    export_df = {}
    if total_positions < total_delegates:
        print("To few postitions for the " + str(total_delegates) + " delegates")
        print("you need " + str(abs(total_delegates - total_positions)) + " more positions")
    else:
        for school in sorted_schools:
            committee = dh.dhodnt(sorted_schools[school], committees.copy())
            list_of_positions = []
            for i in committee:
                for k in range(committee[i]):
                    list_of_positions.append(i)
            for i in range(max(list(sorted_schools.values())) - len(list_of_positions)):
                list_of_positions.append("")

            export_df[school] = list_of_positions
            for k in committee:
                committees[k] -= committee[k]

    individual_positions = dp.read_in_data(positions_csv, list(committees.keys()))
    individual_positions = individual_positions.to_dict()
    for i in list(individual_positions.keys()):
        for k in list(individual_positions[i].keys()):
            if str(individual_positions[i][k]) == "nan":
                individual_positions[i].pop(k)

    for i in list(individual_positions.keys()):
        individual_positions[i] = list(individual_positions[i].values())
    for school in export_df:
        schools_positions = export_df[school]
        for position in range(len(schools_positions)):
            if schools_positions[position] == "":
                continue
            # print(len(individual_positions[schools_positions[position]]))
            random_pos = int(random.random() * len(individual_positions[schools_positions[position]]))
            # print(random_pos)
            position_name = individual_positions[schools_positions[position]][random_pos]
            individual_positions[schools_positions[position]].pop(random_pos)
            # print(individual_positions[schools_positions[position]])
            # # print(position_name)
            export_df[school][position] = export_df[school][position] + ": " + str(position_name)

    positions_by_school = pd.DataFrame.from_dict(export_df)
    return positions_by_school


if __name__ == "__main__":
    run_and_export_dhodnt().to_csv("output.csv", index=False)