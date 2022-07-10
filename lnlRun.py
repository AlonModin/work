from svtools import ipypi_testutils as tu
import os
from pysvtools import status_scope

import pysvext.lunarlake_status_scope.post_processors.mdat.mdat_uy_post_process as mdat
from pysvext.lunarlake_status_scope.analyzers.xncu.ver1.xncu_plugin import XNcuPlugin
from pysvext.lunarlake_status_scope.analyzers.noc.ver1.noc_plugin import NocPlugin
from pysvext.lunarlake_status_scope.analyzers.hbo.ver1.hbo_plugin import HboPlugin
from pysvext.lunarlake_status_scope.analyzers.ccf.ver1.ccf_plugin import CcfPlugin
from pysvext.lunarlake_status_scope.analyzers.mempma.ver1.mempma_plugin import MempmaPlugin
from pysvext.lunarlake_status_scope.analyzers.ccfpma.ver1.ccfpma_plugin import CcfpmaPlugin


def mdt_env(path: str, output: str):
    #plugin_xncu = XNcuPlugin()
    #plugin_noc = NocPlugin()
    #plugin_hbo = HboPlugin()
    plugin_ccf = CcfPlugin()
    #plugin_mempma = MempmaPlugin()
    #plugin_ccfpma = CcfpmaPlugin()

    state_dump_file_path = path
    namednodes_file_path = r"C:\pythonsv\src\pysvext-lunarlake_status_scope\tests\test_input\MDAT\A0\snapshot.spkx"
    status_scope.run(
        analyzers=[plugin_ccf, mdat.MdatPostProcessor()],#plugin_hbo, plugin_noc, plugin_xncu, plugin_mempma, plugin_ccfpma, mdat.MdatPostProcessor()],
        offline_dict={"state_dump": state_dump_file_path, "namednodes": namednodes_file_path},
        autoconfig=False,
        output_dir=output,
    )
    pass


if __name__ == '__main__':
    file_path = r"C:\SVSHARE\excel_file\val_files\state_dump.zip"
    mdt_env(file_path,r"C:\SVSHARE\excel_file\val_files")
