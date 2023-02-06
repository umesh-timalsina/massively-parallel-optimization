import pathlib
import pickle


class Result:
    def __init__(self, algorithm_result):
        self.algorithm_result = algorithm_result

    def save(self, save_dir: pathlib.Path):
        with open(save_dir / "result.pkl", "wb") as res:
            pickle.dump(self.algorithm_result, res)

