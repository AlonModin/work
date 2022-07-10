from os import listdir
from os.path import isfile, join
from pysvtools import status_scope


def run_by_path(path: str):
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    output = "C:\\Temp\\test2"
    for item in all_files:
        status_scope.run(offline_path=path + "\\" + item,
                         analyzers=["ccf", "idp", "ncu", "iop", "cmi", "mc", "pm"],
                         post_processors=["mdat_postprocessor"], output_dir=output + '\\' + item)


if __name__ == '__main__':
    p = "C:\\Temp\\workingTest"
    run_by_path(p)
