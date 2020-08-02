

from pipeline import Stage
import re

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
                return
        else:
            return
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
            return
        item['text'] = output
        return self.update_item(item, item)

class ReverseItems(Stage):
    accumulator = True

    def __init__(self, *args, **kw):
        print("ReverseItems instantiated")
        self.init()
    
    def init(self):
        self.data =[]

    def process(self, item):
        self.data.append(item)

    def finalize(self):
        print("Finalize being run")
        self.data.reverse()

    def items(self):
        return self.data

    def reset(self):
        self.init()

class ReversedItemsIterator(Stage):
    accumulator = True

    def __init__(self, *args, **kw):
        self.data = []

    def process(self, item):
        self.data.append(item)

    def finalize(self):
        pass

    def items(self):
        return reversed(self.data)

class RemoveDuplicates(Stage):
    def __init__(self, *args, **kw):
        self.newer_text = []
        pass
    
    def process(self, item, *args):
        texts = item['text']
        # if len(texts) > 2:
        #     print(texts)
        if self.newer_text and duplicatish(texts, self.newer_text):
            self.newer_text = texts
            return
        self.newer_text = texts

        return self.update_item(item, item)

def duplicatish(old_text, new_text):
    """ True if old text kind of fits into new text """
    if old_text[0] == new_text[0]:
        # print("same text in first line, %s AND %s" % (old_text[0], new_text[0]))
        return True
    # Take new down to length of old
    # if levenshtein match, remove old
    # if first line matches firs line of old, no reason to use old