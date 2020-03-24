# PasswordParsing

This is a Python utility to parse /etc/passwd and /etc/group files to combine the user data and return a JSON output containing fields and groups.

### Pre-requisites:
1. Python 3.x installed on the system

### Steps to run:
1. In terminal, change directory to file location.
2. Execute command: python3 PasswordParsing.py -h (This command will provide you help regarding how to provide command line arguments)
3. Use -pwd and -grp arguments in the command to provide Password file and Group file path.
    Eg: python3 PasswordParsing.py -pwd /home/desktop/passwd -grp /home/desktop/group
4. These are optional arguments and by default /etc/passwd and /etc/group paths are set for Password and Group file respectively.
    Eg: python3 PasswordParsing.py
5. The utility prints whole JSON output on the terminal. But it also creates a Results.json file in the same location which contains the output.

Thank you.

Kindly let me know in case of any concerns.
