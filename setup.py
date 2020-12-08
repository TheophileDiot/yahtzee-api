from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='yahtzee_api',
      version='0.1.0',
      description='API offering basic functionality for the classic dice game Yahtzee.',
      long_description=readme(),
      url='https://github.com/tomarbeiter/yahtzee_api',
      author='Tom Arbeiter',
      license='Apache 2.0',
      packages=['yahtzee_api'],
      install_requires=[]
)