import pathlib

class PathConstructor(object):

    def __init__(self, *args):
        self.path = pathlib.Path('.')
        for arg in args:
            self.path = self._add_path(self.path, arg)

    def _add_path(
        self,
        path_org: pathlib.PosixPath,
        path_new: str
    ) -> pathlib.PosixPath:
        return path_org / path_new

    def _absolute(self) -> pathlib.PosixPath:
        return self.path.absolute()
    
    def _str_path(self) -> str:
        return str(self._absolute())
