# output all print log and save to txt
resultfolder = "logger/"


def clear_all_print_file(players_list):
    with open(resultfolder + "all.txt", "w", encoding='utf-8') as f:
        f.write("")
        f.close()
    for i in players_list:
        with open(resultfolder + f"{i.true_role}.txt", "w", encoding='utf-8') as f:
            f.write("")
            f.close()
    with open(resultfolder + "prompt.txt", "w", encoding='utf-8') as f:
        f.write("")
        f.close()
    with open(resultfolder + "backend.txt", "w", encoding='utf-8') as f:
        f.write("")
        f.close()


def print_to_all(string):
    print(string)
    with open(resultfolder + "all.txt", "a", encoding='utf-8') as f:
        f.write(string + "\n")
        f.close()


def print_to_role(role, string):
    print(string)
    with open(resultfolder + f"{role}.txt", "a", encoding='utf-8') as f:
        f.write(string + "\n")
        f.close()


def print_to_prompt(string):
    print(string)
    with open(resultfolder + f"prompt.txt", "a", encoding='utf-8') as f:
        f.write(string + "\n")
        f.close()


def print_to_backend(string):
    print(string)
    with open(resultfolder + f"backend.txt", "a", encoding='utf-8') as f:
        f.write(string + "\n")
        f.close()
