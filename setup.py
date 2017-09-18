#!/bin/python3

from setuptools.command.test import test as TestCommand
from setuptools import setup
from distutils.util import convert_path
import sys


class Tox(TestCommand):
    """
    This is a special command class that runs tox from setup.py
    """
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def get_version():
    main_ns = {}
    ver_path = convert_path('django_voldemort/version.py')
    with open(ver_path) as ver_file:
        exec(ver_file.read(), main_ns)
    return main_ns['__version__']


def readme():
    with open('README.rst') as f:
        return f.read()

config = dict(
    name='django_voldemort',
    description='',
    long_description=readme(),
    url='http://localhost.test',
    author='Mirko Lelansky',
    author_email='mlelansky@mail.de',
    version=get_version(),
    license='Apache',
    classifiers=[
    ],
    keywords='',
    packages=['django_voldemort'],
    platforms=['any'],
    install_requires=['Django', 'voldemort-client'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    include_package_data=True,
    package_data=dict(
    )
)

if __name__ == "__main__":
    setup(**config)