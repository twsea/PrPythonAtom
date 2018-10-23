import os
import pickle as pkl

class FileWriter:
    
    def __init__(self, path):
        """path - путь до файла"""
        if self._check_path(path):
            self.path_ = path
            self.file = None
        else:
            print("This directory doen't exist.")
        
    def _check_path(self, path):
        return os.path.exists(os.path.dirname(os.path.abspath(path)))

    @property
    def path(self):
        return self.path_
    @path.setter
    def path(self, path):
        if self._check_path(path):
            self.path_ = path
        else:
            print("This directory doesn't exist.")
    @path.deleter
    def path(self, path):
      del self.path_
    def _check_file_exists(self, path):
        return os.path.exists(path)
    def print_file(self):
        if self._check_file_exists(self.path_):
            f = open(os.path.basename(self.path_))
            return f.read()
        else:
            print("Your file doesn't exist.")
    
    def write(self, some_string):
        with open(self.path) as f_obj:
            f_obj.write(some_string)
        
    def __enter__(self):
        self.file = open(self.path, 'a')
        return self.file
    
    def __exit__(self, type, value, traceback):
        self.file.close()
        self.file = None
        if value:
            raise
    def save_yourself(self, file_name):
        with open(os.path.basename(file_name), 'wb') as f:
            pkl.dump(self,f)
    
    @classmethod
    def load_file_writer(cls, pickle_file):
        with open(pickle_file, 'rb') as f:
            return pkl.load(f)


    # 
    # возможно что то еще.
    # что намеренно упущенно. например что то для контекстного менеджера.
