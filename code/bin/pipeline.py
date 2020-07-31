

class Pipeline:

    def run(self):
        data_source = self.sections[0]
        stages = self.sections[1:]
        previous_item = None
        previous_item_processed = None
        for item in data_source.items():
            for stage in stages:
                previous_item = item
                item = stage.process(item, previous_item, previous_item_processed)
                previous_item_processed = item
                if item is None:
                    break
        data_sink = self.sections[-1]
        data_sink.finalize()

class Stage:
    list_indices = False
    dictionary_keys = False

    def __init__(self,*args,**kw):
        if kw and kw.has_key('list_indices'):
            self.list_indices = kw['list_indices']
        elif kw and kw.has_key('dictionary_keys'):
            self.list_indices = kw['dictionary_keys']


    def extract_sub_items(self,item):
        """Extracts sub items to be processed, from item"""
        parsed_item = []
        if self.list_indices:
            for index in self.list_indices:
                parsed_item.append(item[index])
            return parsed_item
        elif self.dictionary_keys:
            for key in self.dictionary_keys:
                parsed_item.append(item[key])
            return parsed_item
        else:
            return item

    def update_item(self,updated_data, item):
        """Puts the processed sub items back into item"""
        if self.list_indices:
            for index in self.list_indices:
                item[index]= updated_data.pop(0)
        elif self.dictionary_keys:
            for key in self.dictionary_keys:
                item[key]=updated_data.pop(0)
        else:
            return updated_data
        return item

class FileSource:
    def __init__(self, *args, **kw):
        if kw and kw.has_key('filename'):
            filename = kw['filename']
        else:
            filename="input.txt"
        fo = open(filename, 'r')
        self.file = fo

    def items(self):
        for line in self.file.readlines():
            yield line
        self.file.close()

class FileSink:
    def __init__(self, *args, **kw):
        self.data = []
        if kw and kw.has_key('filename'):
            filename = kw['filename']
        else:
            filename="output.txt"
        fo = open(filename, 'w')
        self.file = fo



    def process(self, item):
        # this needs to accumulate data
        self.data.append(item)

    def finalize(self):
        self.file.writelines(self.data)
        self.file.close()