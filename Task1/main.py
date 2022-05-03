""" Task 1 description
The program has two arguments --max-depth(default = 2) and --tree-path if tree of relation already exists.
And you want only to show te tree of relations.
Algorythm consists of two functions build_tree() and show_tree().
The first one build a tree of domain relations of set depth starting from domain openx.com, and then tree will be represented by
the second one.
"""

import os.path
import sys
import contextlib
import json
import requests
import treelib
import argparse

def CreateParser():
    """The function creates parser for input arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-depth', default="2")
    parser.add_argument('--tree-path', default="NoFile")
    return parser

def build_tree(max_depth = 2, first_request = 'openx.com'):
    """ This function creates file tree.txt, which contains all dependencies between domains.
    Make it by recursion requests to domains sellers files, which seller_type is INTERMEDIARY or BOTH until depth less
    than defined max.
    """
    if not os.path.exists("json"):  # Create directory json for downloaded json files
        os.mkdir("json")

    if not os.path.exists("json/" + first_request + ".json"):   # Download and save the first sellers file.
        try:
            r = requests.get('https://' + first_request + '/sellers.json')
            if r.status_code == 200:
                BUFFILE = open("json/" + first_request + ".json", "w")
                BUFFILE.write(json.dumps(r.json()))
                BUFFILE.close()
        except:
            print("Can't upload the first file")
            return
    used_dict = {first_request: 1}  # Dictionary of used domains, consist of pairs of domain and its depth
    queue = [first_request]         # Queue of not PUBLISHER domains
    FILE = open("tree.txt", "w")
    while len(queue) != 0:

        cur_domain = queue.pop(0)           # Take the first domain in queue
        cur_depth = used_dict[cur_domain]

        if cur_depth == -1:    # Depth is -1 if domain was not response
            continue

        try:  # Try to open json file of current domain
            if used_dict.get(cur_domain) == -1:    # Do not take domains without appropriate file of sellers
                continue

            with open("json/" + cur_domain + ".json", "r") as read_file:
                data = json.load(read_file)     # Read appropriate downloaded json file for current domain
            sellers = data['sellers']

            for seller in sellers:
                lower_domain = seller['domain']

                if lower_domain[0:4] == 'www.':
                    lower_domain = lower_domain[4:]     # Standardizing domains which start from www.
                if lower_domain[0:8] == 'https://':
                    lower_domain = lower_domain[12:-1]   # Standardizing domains which start from https//www.

                if used_dict.get(lower_domain) is not None:  # Process only not used domains
                    continue

                FILE.write(lower_domain + " " + cur_domain + "\n")  # Add to tree relation
                FILE.flush()

                lower_level = cur_depth + 1
                if lower_level >= max_depth:    # If depth more than maks or equal, not process the domain
                    continue




                if seller['seller_type'] != 'PUBLISHER':
                    if not os.path.exists("json/" + lower_domain + ".json"):
                        try:  # Trying to download and write sellers file of domain
                            r = requests.get('https://' + lower_domain + '/sellers.json')
                            if r.status_code == 200:
                                BUFFILE = open("json/" + lower_domain + ".json", "w")
                                BUFFILE.write(json.dumps(r.json()))
                                BUFFILE.close()
                        except Exception as ex:
                            lower_level = -1  # Mark if domain is unresponsive
                            pass
                    queue.append(lower_domain)  # If domain is not PUBLISHER, add domain to recursion queue.
                used_dict[lower_domain] = lower_level   # Then mark the domain as used and add depth of the domain.
        except Exception as ex:
            pass

    FILE.close()


def show_tree(path = ""):
    """The function creates tree of domains by using file tree.txt and library treelib
        Result saves in file answer.txt"""

    tree = treelib.Tree()   # Using the treelib library make a tree that represent relations of domains
    tree.create_node('openx.com', 'openx.com')
    with open(path + "tree.txt", 'r') as tree_file:  # Open the file with a tree
        for line in tree_file:
            try:
                edge = line.strip().split(" ")
                if len(edge) > 1:   # There are maybe some broken empty relations if one of sellers files was incorrect
                    tree.create_node(edge[0], edge[0], parent=edge[-1])
            except Exception as ex:
                pass

    with open("answer.txt", "w", encoding='utf-8') as f:  # Write the answer tree to the file "answer.txt"
        with contextlib.redirect_stdout(f):
            print("Max depth: " + str(tree.depth()))
            tree.show()


if __name__ == '__main__':
    parser = CreateParser()
    namespace = parser.parse_args(sys.argv[1:])  # Parse the arguments

    # Decide if program needs to make tree.
    if namespace.tree_path == "NoFile" or not os.path.exists(namespace.tree_path):
        build_tree(max_depth=int(namespace.max_depth) + 1)
        show_tree()
    else:
        show_tree(namespace.tree_path)



