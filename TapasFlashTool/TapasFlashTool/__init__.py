"""
Tapas Flash Tool -- Tool for flashing a Tapas Board via UART

Author: Stefan Steinmueller

BSD 3-Clause License

Copyright (c) 2017, SDI-SoftwareDefinedInverter
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import subprocess
import pkg_resources
_resource_package = __name__
_exe_path = "__main__.py"
exe_path = pkg_resources.resource_filename(_resource_package, _exe_path)



def flash(baud1, port, app_file, kernel_file, dev, baud2=None, debug=False):
    """
    Wrapper function for calling the modules __main__ module.
    """
    args = [
        "python",
        exe_path,
        "-b","{}".format(baud1),
        "-p","{}".format(port),
        "-k","{}".format(kernel_file),
        "-a","{}".format(app_file),
        "-d","{}".format(dev),
        "-b2","{}".format(baud2 or baud1)
        ]
    if debug:
        args.append("-debug")
        
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    log = proc.stdout.read()
    proc.wait()
    if proc.returncode is 0:
        return True, log
    else:
        return False, log
