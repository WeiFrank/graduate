#!/usr/bin/env python2
#coding:utf-8

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist

IMP_VERSION = ['2012', '8', None]
def canonical_version_string():
    return '.'.join(filter(None, IMP_VERSION))

#import config

#install_manage = config.InstallManage()
#install_manage.run()


class local_sdist(sdist):
    """Customized sdist hook - builds the ChangeLog file from VC first"""
    def run(self):
        print "hello"
        sdist.run(self)

setup(
    name='application',
    version=canonical_version_string(),
    #version=__version__,
    description='application',
    license='zhuwei License',
    author='zhuwei',
    scripts=[],
    )

