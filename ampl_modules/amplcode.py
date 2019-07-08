from .amplcodebuilder import AmplCodeBuilder


class AmplCode:
    """
    Assumptions:
        - max. one command per line
        - no double spaces as delimiter
    """

    def __init__(self, code):
        self.code = code
        self.lines = self.code.split('\n')

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as f:
            code = f.read()
        return AmplCode(code)

    def _update_lines_from_code(self):
        self.lines = self.code.split('\n')

    def _update_code_from_lines(self):
        self.code = '\n'.join(self.lines)

    def __repr__(self):
        s = ""
        for i, line in enumerate(self.lines, start=1):
            s += ('%i:\t' % i, line) + '\n'
        return s

    def export(self, filename):
        with open(filename, 'w') as f:
            f.write(self.code)

    def get_params(self):
        params = []
        for line in self.lines:
            if line.startswith("param"):
                name = line.split(' ')[1]
                if '{' in name:
                    name = name.split('{')[0]
                if ':' in name:
                    name = name.split(':')[0]
                if '{' in line and ':=' in line and line.index('{') < line.index(':='):
                    of = line[line.index('{') + 1:line.index('}')]
                else:
                    of = ""
                data = line.split(':=')[-1].strip()[:-1]
                params.append((name, of, data))
        return params

    def set_param(self, name, data):
        for i, line in enumerate(self.lines):
            if line.startswith(f"param {name}"):
                break
        _, of, data_old = next(filter(lambda x: x[0] == name, self.get_params()))
        self.lines[i] = AmplCodeBuilder.param(name, of, data=data)
        self._update_code_from_lines()

    def get_sets(self):
        sets = []
        for line in self.lines:
            if line.startswith("set"):
                name = line.split(' ')[1]
                if ':' in name:
                    name = name.split(':')[0]
                data = line.split(':=')[-1].strip()[:-1]
                sets.append((name, data))
        return sets

    def set_set(self, name, data):
        for i, line in enumerate(self.lines):
            if line.startswith(f"set {name}"):
                break
        self.lines[i] = AmplCodeBuilder.set(name, data)
        self._update_code_from_lines()

    def fix_var(self, name, at, value):
        for i, line in enumerate(self.lines):
            if line.startswith(f"var {name}"):
                break
        self.lines.insert(i + 1, AmplCodeBuilder.fix(name, at, value))
        self._update_code_from_lines()

    def delete_fixed(self):
        """
        delete all fix commands
        :return:
        """
        for i, line in enumerate(self.lines):
            if line.startswith("fix"):
                self.lines[i] = ''
        self._update_code_from_lines()

    def set_param_data(self, name, data):
        """

        :return:
        """
        for i, line in enumerate(self.lines):
            if line.startswith(f"param {name}"):
                break
        _, of, data_old = next(filter(lambda x: x[0] == name, self.get_params()))

        self.lines.insert(i+1, AmplCodeBuilder.param_datablock(name, data=data))
        self._update_code_from_lines()

    def set_param_data_3d(self, name, data):
        """

        :return:
        """
        for i, line in enumerate(self.lines):
            if line.startswith(f"param {name}"):
                break
        _, of, data_old = next(filter(lambda x: x[0] == name, self.get_params()))

        self.lines.insert(i+1, AmplCodeBuilder.param_datablock_3d(name, data=data))
        self._update_code_from_lines()
