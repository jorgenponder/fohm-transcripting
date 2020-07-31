#!/usr/bin/env python3


from pipeline import Pipeline, Pipelines, FileSource, FileSink, Stage, DirectorySource, identity_func

class Printer(Stage):
    def __init__(self, *args, **kw):
        pass
    
    def process(self, item, *args):
        # print(item)
        return self.update_item(item, item)

pipeline = Pipeline()
pipeline.sections = (FileSource(),
                     Printer(),
                     FileSink())

# pipelines take a pipeline specification as input and instructions on what that pipeline wants as input, and how its output should be handled
# input could be a string, in some keyword configuration
# input to sink could be a string in some keyword configuration
# hmm it cannot be revealed until runtime, how do you specify it? with a dictionary?

def output(arg):
    def foo():
        return arg + ".jsonny"
    return foo




pipelines = Pipelines(source = DirectorySource(glob="*.json", directory='.'),
                     pipeline = pipeline,
                     pipeline_init = identity_func,
                     pipeline_sink_init = output)
pipelines.run()