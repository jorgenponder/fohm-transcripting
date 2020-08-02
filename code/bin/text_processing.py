

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
        item['text'] = output
        return self.update_item(item, item)