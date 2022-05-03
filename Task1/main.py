import os.path
import json
import requests
import treelib
import threading

# queueLock = threading.Lock()
# dictLock = threading.Lock()
# FILELock = threading.Lock()
# thread_activity = threading.Lock()
#
# thread_activity_count = [0]
#
# exitFlag = 0
#
# class myThread(threading.Thread):
#     def __init__(self, id, name, queue, used_dict, FILE, thread_activity_count):
#         threading.Thread.__init__(self)
#         self.id = id
#         self.name = name
#         self.queue = queue
#         self.used_dict = used_dict
#         self.FILE = FILE
#         self.thread_activity_count = thread_activity_count
#
#     def run(self):
#         while not exitFlag:
#
#             while True:
#                 queueLock.acquire()
#                 size = len(self.queue)
#                 if size == 0:
#                     queueLock.release()
#                     break
#                 self.thread_activity_count[0] += 1
#                 print(self.name)
#                 cur_node = self.queue.pop(0)
#                 queueLock.release()
#
#                 try:
#                     with open("json/" + cur_node + ".json", "r") as read_file:
#                         data = json.load(read_file)
#                     sellers = data['sellers']
#                     for seller in sellers:
#                         domain = seller['domain']
#                         if domain[0:4] == 'www.':
#                             domain = domain[4:]
#                         if domain[0:8] == 'https://':
#                             domain = domain[12:-1]
#
#                         dictLock.acquire()
#                         domain_used_dict = self.used_dict.get(domain)
#                         dictLock.release()
#                         if domain_used_dict is not None:
#                             continue
#
#                         FILELock.acquire()
#                         self.FILE.write(domain + " " + cur_node + "\n")
#                         self.FILE.flush()
#                         FILELock.release()
#                         if seller['seller_type'] != 'PUBLISHER':
#                             data2 = 'Not Publisher'
#                             try:
#                                 r = requests.get('https://' + domain + '/sellers.json')
#                                 if r.status_code == 200:
#                                     if not os.path.exists("json/"+domain + ".json"):
#                                         BUFFILE = open("json/"+domain + ".json", "w")
#                                         BUFFILE.write(json.dumps(r.json()))
#                                         BUFFILE.close()
#                                     #queueLock.acquire()
#                                     self.queue.append(domain)
#                                     #queueLock.release()
#                                     print(domain)
#                             except Exception as ex:
#                                 print(ex)
#                             #dictLock.acquire()
#                             self.used_dict[domain] = data2
#                             #dictLock.release()
#                         else:
#                             #dictLock.acquire()
#                             self.used_dict[domain] = 'Publisher'
#                             #dictLock.release()
#
#                 except Exception as ex:
#                     if dictLock.locked():
#                         dictLock.release()
#                     if FILELock.locked():
#                         FILELock.release()
#                     print(ex)
#                 self. thread_activity_count[0] -= 1
#
#
# def build_tree(num_thread = 3):
#     with open("input.json", "r") as read_file:
#         data = json.load(read_file)
#     threadList = []
#     for i in range(num_thread):
#         threadList.append("Thread-" + str(i))
#     threadId = 1
#     threads = []
#
#     used_dict = {"openx.com": data['sellers']}
#     queue = ["openx.com"]
#     FILE = open("tree.txt", "w")
#     for name in threadList:
#         thread = myThread(threadId, name, queue, used_dict, FILE, thread_activity_count)
#         thread.start()
#         threads.append(thread)
#         threadId += 1
#
#     while True:
#         thread_activity.acquire()
#         count = thread_activity_count[0]
#         thread_activity.release()
#         if count == 0:
#             break
#     exitFlag = 1
#     print(exitFlag)
#
#     for t in threads:
#         t.join()
#     FILE.close()


def build_tree():
    with open("input.json", "r") as read_file:
        data = json.load(read_file)
    used_dict = {"openx.com": data['sellers']}
    queue = ["openx.com"]
    FILE = open("tree.txt", "w")
    while len(queue) != 0:
        cur_node = queue.pop(0)
        try:
            with open("json/" + cur_node + ".json", "r") as read_file:
                data = json.load(read_file)
            sellers = data['sellers']
            for seller in sellers:
                domain = seller['domain']
                if domain[0:4] == 'www.':
                    domain = domain[4:]
                if domain[0:8] == 'https://':
                    domain = domain[12:-1]

                if used_dict.get(domain) is not None:
                    continue


                FILE.write(domain + " " + cur_node + "\n")
                FILE.flush()

                if seller['seller_type'] != 'PUBLISHER':
                    data2 = 'Not Publisher'
                    if not os.path.exists("json/" + domain + ".json"):
                        try:
                            r = requests.get('https://' + domain + '/sellers.json')
                            if r.status_code == 200:

                                BUFFILE = open("json/" + domain + ".json", "w")
                                BUFFILE.write(json.dumps(r.json()))
                                BUFFILE.close()


                                print(domain)
                        except Exception as ex:
                            print(ex)
                    queue.append(domain)
                    used_dict[domain] = data2
                else:
                    used_dict[domain] = 'Publisher'
        except Exception as ex:
            print(ex)

    FILE.close()

def show_tree(nodes = 1000):
    tree = treelib.Tree()
    tree.create_node('openx.com', 'openx.com')
    with open('tree.txt', 'r') as tree_file:
        i = 0
        for line in tree_file:
            if i == nodes:
                break
            try:
                edge = line.strip().split(" ")
                if len(edge) > 1:
                    tree.create_node(edge[0], edge[0], parent=edge[-1])
                    i+=1
            except:
                pass
    print("Max depth: " + str(tree.depth()))
    tree.show()


if __name__ == '__main__':
    build_tree()
    #show_tree(nodes=10000)
