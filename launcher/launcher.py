from abstract_launcher import LauncherBase

class Launcher:
    def __init__(self) -> None:
        pass
    
    def input_data(self, path: str):
        self._input_data = path

    def check_data(self) -> str:
        return self._input_data