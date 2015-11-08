from distutils.core import setup

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://dada.pink/horetu/',
      py_modules=['horetu'],
      install_requires = [
          'sphinx',
      ],
      version='0.0.1',
      license='AGPL',
)
