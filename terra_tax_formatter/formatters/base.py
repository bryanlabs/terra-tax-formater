from collections import OrderedDict

class BaseFormatter:
    def __init__(self, headers=[], headers_to_data_keys={}):
        self.headers = headers
        self.headers_to_data_keys = headers_to_data_keys

    def format_data(self, data):
        new_data = []
        for row in data:
            point = OrderedDict()
            for header in self.headers:
                header_value = ""
                try:
                    header_value = row[self.headers_to_data_keys[header]]
                except:
                    pass
                point[header] = header_value
            new_data.append(point)
        return new_data