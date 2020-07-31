#!/usr/bin/env python3


from pipeline import Pipeline, FileSource, FileSink, Stage

class Printer(Stage):
    def __init__(self, *args, **kw):
        pass
    
    def process(self, item, *args):
        print(item)
        self.update_item(item, item)

pipeline = Pipeline()
pipeline.sections = (FileSource(),
                     Printer(),
                     FileSink())
pipeline.run()