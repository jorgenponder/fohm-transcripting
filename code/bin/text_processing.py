from pipeline import Stage
import re
from difflib import SequenceMatcher

secs = re.compile(r'\d+')
empty = re.compile(r'^[ \n\f]*$')


class Itemizer(Stage):
    def __init__(self, *args, **kw):
        pass
    
    def process(self, item, *args):
        parts = item.split("\n")
        obj = {}
        if len(parts) > 1:
            try:
                obj['timestamp'] =  secs.match(parts[1]).group()
            except AttributeError:
                return None
        else:
            return None
        if len(parts) > 2:
            obj['text'] = parts[2:]
        return self.update_item(obj, obj)

class RemoveEmpties(Stage):
    def __init__(self, *args, **kw):
        pass
    
    def process(self, item, *args):
        texts = item['text']
        output = []
        for text in texts:
            if not empty.match(text):
                output.append(text)
        if not output:
            return None
        item['text'] = output
        return self.update_item(item, item)

class ReverseItems(Stage):
    accumulator = True

    def __init__(self, *args, **kw):
        # print("ReverseItems instantiated")
        self.init()
    
    def init(self):
        self.data =[]

    def process(self, item):
        self.data.append(item)

    def finalize(self):
        # print("Finalize being run")
        self.data.reverse()

    def items(self):
        return self.data

    def reset(self):
        self.init()

class RemoveDuplicates(Stage):
    def __init__(self, *args, **kw):
        self.newer_text = []
        pass
    
    def process(self, item, *args):
        texts = item['text']
        if not item['text']:
            return None

        # if len(texts) > 2:
        #     print(texts)
        if self.newer_text and duplicatish(texts[0], self.newer_text[0]):
            self.newer_text = texts
            return None # text is duplicatish
        
        if self.newer_text and duplicatish(texts[-1], self.newer_text[0]):
            item['text'].pop()

        self.newer_text = texts

        return self.update_item(item, item)

def duplicatish(old_text, new_text):
    """ True if old text kind of fits into new text """
    if old_text == new_text:
        # print("same text in first line, %s AND %s" % (old_text[0], new_text[0]))
        return True

    s = SequenceMatcher(None, old_text, new_text)
    ratio = s.ratio()
    if ratio > 0.6:
        # print("%s %.2f\n%s\n" % (old_text[0], ratio, new_text[0]))
        return True
    
    return False

def webvtt_timestamp(timestamp):
    timestamp = int(timestamp)
    end_timestamp = timestamp + 1
    hours = int(timestamp/3600)
    mins = int(timestamp/60)
    secs = timestamp - hours * 3600 - mins * 60
    end_hours = int(end_timestamp/3600)
    end_mins = int(end_timestamp/60)
    end_secs = end_timestamp - end_hours * 3600 - end_mins * 60
    return "{:0>2d}:{:0>2d}.{:0>2d}.000 --> {:0>2d}:{:0>2d}.{:0>2d}.000".format(hours, mins, secs, end_hours, end_mins, end_secs)

class WebVTTSink(Stage):
    """ Write to WbVTT file """
    def __init__(self, *args, **kw):
        self.data = []

        if kw and kw.has_key('filename'):
            self.filename = kw['filename']
        else:
            self.filename="output.scr"

    def process(self, item):
        """ Accumulates data"""
        # print("HERE'S DATA")
        # print(item)
        # print("END DATA")
        text = webvtt_timestamp(item['timestamp']) + "\n"
        text += "\n".join(item['text'])
        self.data.append(text + "\n\n")

    def extra_init(self, func):
        """ Modification of parameters at runtime, for iterating over a pipeline """
        self.filename = func()


    def finalize(self):
        fo = open(self.filename, 'w')
        fo.writelines(self.data)
        fo.close()
        self.data = []

   