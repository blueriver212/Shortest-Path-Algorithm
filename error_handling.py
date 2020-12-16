#An object storing all of the error handling
import os


class Errors:

    def json_input():
        """
        User inputs their json file. It needs to be located in the relative path of
        'Materials/itn/'
        :return: A file path for the JSON file
        """
        cwd = os.getcwd()
        root = os.path.dirname(cwd)
        file_list = os.listdir(os.path.join(root, 'Material', 'itn'))
        while True:
            try:
                # remove when submitting
                # path = 'solent_itn.json'
                path = input('Filename of ITN network:')
                file = os.path.join(root, 'Material', 'itn', path)
                if ".json" not in path:
                    raise ValueError
                if path not in file_list:
                    raise FileNotFoundError
            except ValueError:
                print('File must be .json')
            except FileNotFoundError:
                print('This file does not exist')
                continue
            else:
                break
        return file

