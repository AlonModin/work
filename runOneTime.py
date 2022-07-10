import sys
from pysvtools import status_scope


print(sys.argv)
path = sys.argv[1]
output = sys.argv[2]
status_scope.run(offline_path=path,
            analyzers=["ccf", "idp", "ncu", "iop", "cmi", "mc", "pm"],
            post_processors=["mdat_postprocessor"], output_dir=output)
status_scope =""
