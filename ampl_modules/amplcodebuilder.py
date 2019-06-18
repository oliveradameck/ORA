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
