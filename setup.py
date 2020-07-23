from setuptools import setup

setup(name='repro_eval',
      version='0.1',
      description='A tool to quantify the replicability and reproducibility of system-oriented IR experiments.',
      url='http://github.com/irgroup/repro_eval',
      author='Timo Breuer',
      author_email='timo.breuer@th-koeln.de',
      license='MIT',
      packages=['repro_eval'],
      install_requires=[
          'pytrec_eval',
          'numpy',
          'scipy'
      ],
      zip_safe=False)