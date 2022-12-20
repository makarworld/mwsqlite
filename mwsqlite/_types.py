
PY_VAR_TO_SQL_TYPE = {
    int: 'INTEGER',
    float: 'REAL',
    str: 'TEXT',
    bool: 'TEXT',
    list: 'TEXT',
    dict: 'TEXT',
}

DESC = 'DESC'
ASC = 'ASC'    

class Where(dict):
    pass

class Order(dict):
    pass

class Limit(int):
    pass

class Struct:
    def __init__(self, _list=[], **entries):
        if _list:
            self.new_list = []
            for x in _list:
                if isinstance(x, dict):
                    self.new_list.append(Struct(**x))

                elif isinstance(x, list):
                    self.new_list.append(Struct(_list=x).new_list)
                
                else:
                    self.new_list.append(x)
            return

        self.__dict__.update(**entries)
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(**v)

            if isinstance(v, list):
                self.__dict__[k] = Struct(_list=v).new_list

    def __repr__(self):
        return self.__dict__.__repr__()
    
    def __str__(self):
        return self.__dict__.__str__()
    
    def dict(self):
        return self.__dict__ 

    def __getattr__(self, item):
        return None

    def __getitem__(self, item):
        return self.get(item)
    
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    
    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()
    
    def get(self, key):
        return self.__dict__.get(key)

class InvalidColumnNameError(Exception):
    pass