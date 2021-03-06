import os
from datetime import datetime
from texttable import Texttable
import hashlib
from tqdm import tqdm


def listdir_nohidden(path, args):
    dirList = []
    for f in os.listdir(path):
        if not f.startswith('.') or args.hidden:
            dirList.append(f'{path}/{f}')
    return dirList

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.creationTime = datetime.fromtimestamp(os.path.getmtime(path))
        self.nameLower = self.name.lower()

class Folder:
    fileList = []
    folderList = []
    def __init__(self, path, args):
        self.path = path
        for item in listdir_nohidden(path, args):
            if os.path.isdir(item):
                self.folderList.append(Folder(f'{path}/{os.path.basename(item)}', args))
            elif os.path.isfile(item):
                self.fileList.append(File(f'{path}/{os.path.basename(item)}'))

    def Alex(self, args):
        self.res = {}
        if not args.silent:
            print('looking for all dubles started')
            for item in tqdm(range(len(self.fileList) - 1)):
                if self.res.get(self.fileList[item].nameLower):
                    self.res[self.fileList[item].nameLower].append(self.fileList[item])
                else:
                    self.res[self.fileList[item].nameLower] = [self.fileList[item]]
            print('All dubles found')
        else:
            for item in range(len(self.fileList) - 1):
                if self.res.get(self.fileList[item].nameLower):
                    self.res[self.fileList[item].nameLower].append(self.fileList[item])
                else:
                    self.res[self.fileList[item].nameLower] = [self.fileList[item]]

    def default_output(self, args):
        for value in self.res.values():
            if len(value) > 2:
                for i in value:
                    print(i.name, args.delimiter, i.path, args.delimiter, md5(i.path), args.delimiter, i.creationTime)

    def output(self):
        t = Texttable()
        t.set_cols_width([15, 50, 40, 20])
        t.add_row(["File name", "Path", "Md5", "Creation Time"])
        for value in self.res.values():
            if len(value) > 2:
                for i in value:
                    t.add_row([i.name, i.path, md5(i.path), i.creationTime])
        print(t.draw())

