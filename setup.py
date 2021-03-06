# @file    setup.py
# @brief   Python distutils code for libSBML Python
#          module (including dependencies)
# @author  Michael Hucka
# @author  Ben Bornstein
# @author  Ben Kovitz
# @author  Frank Bergmann (fbergman@caltech.edu)
#
# <!---------------------------------------------------------------------------
# This file is part of libSBML.  Please visit http://sbml.org for more
# information about SBML, and the latest version of libSBML.
#
# Copyright (C) 2013-2016 jointly by the following organizations:
#     1. California Institute of Technology, Pasadena, CA, USA
#     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
#     3. University of Heidelberg, Heidelberg, Germany
#
# Copyright 2005-2010 California Institute of Technology.
# Copyright 2002-2005 California Institute of Technology and
#                     Japan Science and Technology Corporation.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.  A copy of the license agreement is provided
# in the file named "LICENSE.txt" included with this software distribution
# and also available online as http://sbml.org/software/libsbml/license.html
# ----------------------------------------------------------------------- -->*/

import glob
import os
import sys
import shutil
import platform
from sysconfig import get_config_vars
from setuptools import setup, Extension

current_dir = os.path.dirname(os.path.realpath(__file__))

# remove -Wstrict-prototypes
(opt,) = get_config_vars('OPT')
if opt is not None:
    os.environ['OPT'] = " ".join(
        flag for flag in opt.split() if flag != '-Wstrict-prototypes'
    )

# we need to switch the __init__.py file based on the python version
# as python 3 uses a different syntax for metaclasses
if sys.version_info >= (3, 0):
    # this is python 3.x
    if os.path.exists(current_dir + '/libsbml/__init__.py'):
        os.remove(current_dir + '/libsbml/__init__.py')
    shutil.copyfile(current_dir + '/script/libsbml3.py',
                    current_dir + '/libsbml/__init__.py')
else:
    # this is an older python
    if os.path.exists(current_dir + '/libsbml/__init__.py'):
        os.remove(current_dir + '/libsbml/__init__.py')
    shutil.copyfile(current_dir + '/script/libsbml2.py',
                    current_dir + '/libsbml/__init__.py')

# figure out the os
basepath = './base/'
current_os = 'LINUX'
package_name = '"libsbml"'
inc_dirs = []
lib_dirs = []
libs = []
definitions = []
packages = [
    ('USE_COMP', None),
    ('USE_QUAL', None),
    ('USE_FBC', None),
    ('USE_LAYOUT', None)
]
if platform.system() == 'Darwin':
    current_os = 'DARWIN'
elif platform.system() == 'Windows':
    current_os = 'WIN32'
    package_name = '\\"libsbml\\"'
    definitions = [
        ('LIBSBML_EXPORTS', None),
        ('LIBLAX_STATIC', None)
    ]

definitions = definitions + [
    ('BZIP2_STATIC', None),
    ('HAVE_MEMMOVE', None),
    ('_LIB', None)
]

cfiles = [basepath + 'libsbml_wrap.cpp']

# add dependencies
cfiles = cfiles + glob.glob(basepath + "*.c")

for root, dirs, files in os.walk(basepath + 'sbml'):
    for file in files:
        if file.endswith('.c') or file.endswith('.cpp'):
            cfiles.append(os.path.join(root, file))


setup(name="python-libsbml",
      version="5.12.1",
      description="LibSBML Python API",
      long_description=("LibSBML is a library for reading, writing and "
                        "manipulating the Systems Biology Markup Language "
                        "(SBML).  It is written in ISO C and C++, supports "
                        "SBML Levels 1, 2 and 3, and runs on Linux, Microsoft "
                        "Windows, and Apple MacOS X.  For more information "
                        "about SBML, please see http://sbml.org."),
      license="LGPL",
      author="SBML Team",
      author_email="libsbml-team@caltech.edu",
      url="http://sbml.org",
      packages=["libsbml"],
      package_dir={'libsbml': 'libsbml'},
      # data_files       = [('lib/site-packages', ['libsbml.pth'])],
      ext_package="libsbml",
      ext_modules=[Extension("_libsbml", sources=cfiles,
                             define_macros=definitions + [
                                 (current_os, None),
                                 ('USE_EXPAT', None),
                                 ('USE_ZLIB', None),
                                 ('USE_BZ2', None)
                             ] + packages,
                             include_dirs=inc_dirs + [
                                 basepath + "/",
                                 basepath + "/sbml",
                                 basepath + "/sbml/compress",
                                 basepath + "/sbml/validator/constraints",
                                 basepath + "/sbml/packages/comp/validator",
                                 basepath +
                                 "/sbml/packages/comp/validator/constraints",
                                 "."],
                             libraries=libs,
                             library_dirs=lib_dirs
                             )
                   ]
      )
