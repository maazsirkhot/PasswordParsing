import argparse
import json
passwordFields = ["username", "encryptedPassword", "uid", "groupId", "full_name", "homeDir", "shell"]
groupFields = ["groupName", "password", "groupId", "groupList"]
defaultPasswordPath = "/etc/passwd"
defaultGroupPath = "/etc/group"


def process_files(file_path1=defaultPasswordPath, file_path2=defaultGroupPath):
    password_data = read_file_data(file_path1)
    group_data = read_file_data(file_path2)
    return password_data, group_data


def read_file_data(file_path):
    data = []
    with open(file_path) as file:
        lines = file.readlines()
    for line in lines:
        data.append(line.strip().split(":"))
    return data


def compute_password_data(password_data):
    user_dict = {}
    user_data = {}
    for lvalues in password_data:
        for i in range(len(lvalues)):
            if i == 0:
                user_dict[lvalues[i]] = None
            else:
                user_data[passwordFields[i]] = lvalues[i]
        user_data["groups"] = []
        user_dict[lvalues[0]] = user_data
        user_data = {}
    return user_dict


def compute_group_data(group_data):
    group_dict = {}
    group_list = []
    for lvalues in group_data:
        for i in range(len(lvalues)):
            if i == 3:
                if len(lvalues[i]) > 0:
                    group_dict[groupFields[i]] = lvalues[i].split(",")
                else:
                    group_dict[groupFields[i]] = []
            else:
                group_dict[groupFields[i]] = lvalues[i]
        group_list.append(group_dict)
        group_dict = {}
    return group_list


def compute_combined_data(user_dict, group_list):
    for element in group_list:
        if len(group_list) > 0:
            for value in element["groupList"]:
                if value in user_dict.keys():
                    user_dict[value]["groups"].append(element["groupName"])
    return user_dict


def remove_fields(user_dict):
    for key, value in user_dict.items():
        del value["encryptedPassword"]
        del value["groupId"]
        del value["homeDir"]
        del value["shell"]
    return user_dict


def main():
    try:
        parser = argparse.ArgumentParser(description='Add Password and Group File paths as arguments.')
        parser.add_argument("-pwd", action="store", default=defaultPasswordPath, help="Password File Path (Default : " + defaultPasswordPath + ")")
        parser.add_argument("-grp", action="store", default=defaultGroupPath, help="Group File Path (Default : " + defaultGroupPath + ")")
        args = parser.parse_args()

        # Begin Parsing
        password_data, group_data = process_files(args.pwd, args.grp)
        user_dict = compute_password_data(password_data)
        group_list = compute_group_data(group_data)
        combined_data = compute_combined_data(user_dict, group_list)

        # Remove extra field and convert output to JSON
        final_data = remove_fields(combined_data)
        final_data_json = json.dumps(final_data, indent=4)

        # Display JSON output
        print(final_data_json)

        # Write Results to a JSON file in the same location
        with open("results.json", "w") as outfile:
            outfile.write(final_data_json)
    except FileNotFoundError:
        print("Error: Invalid File Location")
    except TypeError:
        print("Error: Invalid Data Format in the files")
    except Exception:
        print("Exception Occurred: Please Try again")


if __name__ == "__main__":
    main()
