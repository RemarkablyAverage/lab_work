from distutils.core import setup, Extension

module1 = Extension('spam',
                    sources=['spmodule.c'],
                    include_dirs=[],
                    libraries=['m'])

setup(name = "SpamModule",
      version='1.0',
      description="Guido likes spam",
      ext_modules = [module1])
