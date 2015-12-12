from distutils.core import setup

backwards_compatibility = []

# This works from Python 2.7 and 3.3 on
try:
    from inspect import signature
except ImportError:
    backwards_compatibility.append('ipython>=4.0.1')

# This is needed to support Python 2.6 and below.
try:
    import argparse
except ImportError:
    backwards_compatibility.append('argparse>=1.4.0')

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://dada.pink/horetu/',
      py_modules=['horetu'],
      install_requires = [
          'Sphinx>=1.3.1',
          'inflection>=0.3.1',
      ] + backwards_compatibility,
      tests_require = [
          'pytest>=2.6.4',
      ],
      classifiers = [
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      version='0.0.4',
      license='AGPL',
)
