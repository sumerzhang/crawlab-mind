from setuptools import setup

setup(
    name='crawlab-mind',
    version='0.0.1',
    packages=['crawlab_mind', 'crawlab_mind.core'],
    url='https://github.com/crawlab-team/crawlab-mind',
    license='BSD-3',
    author='Marvin Zhang',
    author_email='tikazyq@163.com',
    description='Crawlab Mind',
    install_requires=['scikit-learn', 'numpy', 'lxml'],
)
