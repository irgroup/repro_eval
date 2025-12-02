import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='repro_eval',
      version='0.5.0',
      description='A tool to quantify the replicability and reproducibility of system-oriented IR experiments.',
      long_description=README,
      long_description_content_type="text/markdown",
      url='http://github.com/irgroup/repro_eval',
      author='Timo Breuer',
      author_email='timo.breuer@th-koeln.de',
      license='MIT',
      packages=['repro_eval', 
                'repro_eval.measure'],
      install_requires=[
          'numpy',
          'scipy',
          'tqdm',
          'pytrec_eval_terrier',
          'ir-measures[pytrec_eval]',
          'ruamel.yaml',
          'GitPython',
          'py-cpuinfo'
      ],
      include_package_data=True,
      package_data={'': ['resources/*.json']},
      zip_safe=False)
