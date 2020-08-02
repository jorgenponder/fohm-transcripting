from __future__ import unicode_literals
import simplejson
from pipeline import FileSink


class JSONDataSink(FileSink):

    """Writes a JSON file with the items as an array """

    def __init__(self, *args, **kw):
        self.data = []
        if kw and kw.has_key('filename'):
            self.filename = kw['filename']
        else:
            self.filename="output.json"

    def extra_init(self, func):
        """ Modification of parameters at runtime, for iterating over a pipeline """
        self.filename = func()
        self.data = []
        # print("FILE NAME SET TO")
        # print(self.filename )
        # print("END FILE NAME SET")

    def process(self, item):
        self.data.append(item)

    def finalize(self):
        fo = open('w', self.filename)
        json.dump(self.data, fo)
        fo.close()



