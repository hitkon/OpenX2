import json

if __name__ == '__main__':
    with open("input.json", "r") as read_file:
        data = json.load(read_file)
    sellers = data["sellers"]
    print(len(sellers))
    print(type(sellers[0]))
    print(sellers[2])
    print(sellers[3])



