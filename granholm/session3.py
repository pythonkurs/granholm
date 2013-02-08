import os

class repoDir(object):
    '''Context manager that temporarily moves to a different directory'''
    def __init__(self, temp_path):
        self.original_path = os.getcwd()
        self.temp_path = temp_path

    def __enter__(self):
        os.chdir(self.temp_path)

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_path)

class courseRepo(object):
    '''Class to check whether all files are there'''
    def __init__(self, surname):
        self.surname = surname
        self.required = ['.git',
            'setup.py',
            'README.md',
            'scripts/getting_data.py',
            'scripts/check_repo.py',
            self.surname+'/__init__.py',
            self.surname+'/session3.py']

    def check(self):
        return all([os.path.exists(i) for i in self.required])

    
