from distutils.core import setup

try:
    from inspect import signature
    ipython = []
except ImportError:
    ipython = ['ipython']

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://dada.pink/horetu/',
      py_modules=['horetu'],
      install_requires = [
          'Sphinx>=1.3.1',
          'inflection>=0.3.1',
      ] + ipython,
      tests_require = [
          'pytest>=2.6.4',
      ],
      version='0.0.3',
      license='AGPL',
)
