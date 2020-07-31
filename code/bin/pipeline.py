import glob

def identity_func(arg):
    def foo():
        return arg
    return foo

class Pipeline:
    """ Defines processing steps, from source to sink"""
    def run(self):
        data_source = self.sections[0]
        # print("FILE NAME SET TO")
        # print(data_source.filename )
        # print("END FILE NAME SET")
        stages = self.sections[1:]
        for item in data_source.items():
            for stage in stages:
                item = stage.process(item)
                if item is None:
                    break
        data_sink = self.sections[-1]
        data_sink.finalize()

class Stage:
    """ One processing step in a pipeline"""
    list_indices = False
    dictionary_keys = False

    def __init__(self,*args,**kw):
        if kw and kw.has_key('list_indices'):
            self.list_indices = kw['list_indices']
        elif kw and kw.has_key('dictionary_keys'):
            self.list_indices = kw['dictionary_keys']


    def extract_sub_items(self,item):
        """ Extracts only sub items to be processed, from item """
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
        """ Puts the processed sub items back into item """
        if self.list_indices:
            for index in self.list_indices:
                item[index]= updated_data.pop(0)
        elif self.dictionary_keys:
            for key in self.dictionary_keys:
                item[key]=updated_data.pop(0)
        else:
            return updated_data
        return item

class FileSource(Stage):
    """ Simple source that yields a file line by line"""
    def __init__(self, *args, **kw):
        if kw and kw.has_key('filename'):
            self.filename = kw['filename']
        else:
            self.filename="input.txt"

    def extra_init(self, func):
        """ Modification of parameters at runtime, for iterating over a pipeline """
        self.filename = func()
        # print("FILE NAME SET TO")
        # print(self.filename )
        # print("END FILE NAME SET")

    def items(self):
        # print("FILE NAME SET TO")
        # print(self.filename )
        # print("END FILE NAME SET")
        file = open(self.filename, 'r')
        first_time = True
        for line in file.readlines():
            if first_time:
                first_time = False
                # print(line[:60])
            yield line
        file.close()

class DirectorySource(Stage):
    """ Yields filenames in a directory, according to glob pattern """
    def __init__(self, *args, **kw):
        self.dirname = kw['directory']
        self.glob= kw['glob']

    def items(self):
        for file in (glob.glob(self.dirname  + '/' + self.glob)):
            yield file

class FileSink(Stage):
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
        fo.writelines(self.data)
        fo.close()
        self.data = []


class Pipelines:
    """ Iterates over a pipeline with whatever source yields """
    def __init__(self,*args,**kw):
        self.source = kw['source']
        self.pipeline = kw['pipeline']
        self.pipeline_init = kw['pipeline_init']
        self.pipeline_sink_init = kw['pipeline_sink_init']


    def run(self):
        for source in self.source.items():
            if self.pipeline_init:
                self.pipeline.sections[0].extra_init(self.pipeline_init(source))
            if self.pipeline_sink_init:
                self.pipeline.sections[-1].extra_init(self.pipeline_sink_init(source))
            self.pipeline.run()

