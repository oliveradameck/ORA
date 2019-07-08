
def transform_to_row(data, k2):
    row = []
    for (k1, _k2), value in data:
        if str(k2) == str(_k2):
            row.append(str(value))
    return row

class AmplCodeBuilder:

    @staticmethod
    def param(name, of=None, data=None):
        s = f'param {name}'
        if of:
            s += '{' + of + '}'
        if data:
            s += ' := '
            if type(data) == str:
                s += data
            if type(data) in [int, float]:
                s += str(data)
            if type(data) == list:
                s += '{' + ','.join([str(i) for i in data]) + '}'
        s += ';\n'
        return s

    @staticmethod
    def set(name, data=None):
        s = f'set {name}'
        if data:
            s += ' := '
            if type(data) == str:
                s += data
            if type(data) in [int, float]:
                s += str(data)
            if type(data) == list:
                s += '{' + ','.join([str(i) for i in data]) + '}'
        s += ';\n'
        return s

    @staticmethod
    def fix(name, at, value):
        return f"fix {name}[{at}] := {value};"

    @staticmethod
    def param_datablock(name, data):
        s = f"data;\nparam {name} :="
        for d in data:
            s += '\n' + ' '.join(list(map(str, d)))
        s += ";\nmodel;"
        return s

    @staticmethod
    def param_datablock_3d(name, data):
        key1list = set([str(k1) for (k1, k2), value in data])
        key2list = set([str(k2) for (k1, k2), value in data])

        s = f"data;\nparam {name} : {' '.join(key1list)} :="
        for k2 in key2list:
            s += f'\n {k2} ' +   ' '.join(transform_to_row(data, k2))
        s += ";\nmodel;"
        return s



if __name__ == '__main__':
    d = [((1, 10), 100), ((1, 20), 200), ((2, 10), 200), ((2, 20), 600)]
    a = AmplCodeBuilder.param_datablock_3d( "distance", d)
    print(a)
