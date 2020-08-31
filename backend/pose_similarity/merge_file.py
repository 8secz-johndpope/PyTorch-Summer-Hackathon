import json
import glob

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def main():
    dictionary = dict()

    for filename in glob.glob(r'./jsons/*.json'):
        with open(filename) as json_file:
            data = json.load(json_file)
            dictionary = merge_two_dicts(dictionary, data)

    ret = json.dumps(dictionary)
    with open('4database.json', 'w') as fp:
        fp.write(ret)

if __name__ == "__main__":
    main()