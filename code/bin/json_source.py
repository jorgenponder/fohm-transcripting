
import json
from pipeline import Stage


class JSONDataSource:

    def __init__(self, *args, **kw):
        if kw and kw.has_key('filename'):
            self.filename = kw['filename']
        else:
            self.filename="input.json"

    def extra_init(self, func):
        """ Modification of parameters at runtime, for iterating over a pipeline """
        self.filename = func()
        # print("FILE NAME SET TO")
        # print(self.filename )
        # print("END FILE NAME SET")

    def items(self):
        fo = open(self.filename)
        struct = json.load(fo)
        return struct

class JSONSink(Stage):
    """ Simple sink that writes lines to a file """
    def __init__(self, *args, **kw):
        self.data = []

        if kw and kw.has_key('filename'):
            self.filename = kw['filename']
        else:
            self.filename="output.txt"

    def process(self, item):
        """ Accumulates data"""
        # print("HERE'S DATA")
        # print(item)
        # print("END DATA")
        self.data.append(item)

    def extra_init(self, func):
        """ Modification of parameters at runtime, for iterating over a pipeline """
        self.filename = func()


    def finalize(self):
        fo = open(self.filename, 'w')
        json.dump(self.data, fo)
        fo.close()
        self.data = []
