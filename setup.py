from distutils.core import setup

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://dada.pink/horetu/',
      py_modules=['horetu'],
      install_requires = [
          'Sphinx>=1.3.1',
      ],
      tests_require = [
          'pytest>=2.6.4',
      ],
      version='0.0.1',
      license='AGPL',
)
