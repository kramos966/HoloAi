from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
#build with python3 setpup.py build_ext -i
setup(
    ext_modules = cythonize([Extension("camwire", ["camwire.pyx"],
        libraries=["camwire", "dc1394"])],
    compiler_directives={"language_level" : "3"},
))

