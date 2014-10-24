from distutils.core import setup

setup(
  name='barleycorn',
  version='0.1.0',
  packages=['env.lib.python2.7.distutils', 'env.lib.python2.7.encodings', 'env.lib.python2.7.site-packages.pip',
            'env.lib.python2.7.site-packages.pip.vcs', 'env.lib.python2.7.site-packages.pip.vendor',
            'env.lib.python2.7.site-packages.pip.vendor.distlib',
            'env.lib.python2.7.site-packages.pip.vendor.distlib._backport',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib.trie',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib.filters',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib.serializer',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib.treewalkers',
            'env.lib.python2.7.site-packages.pip.vendor.html5lib.treebuilders',
            'env.lib.python2.7.site-packages.pip.commands', 'env.lib.python2.7.site-packages.pip.backwardcompat',
            'env.lib.python2.7.site-packages._markerlib', 'env.lib.python2.7.site-packages.setuptools',
            'env.lib.python2.7.site-packages.setuptools.tests', 'env.lib.python2.7.site-packages.setuptools.command',
            'env.lib.python2.7.site-packages.setuptools._backport',
            'env.lib.python2.7.site-packages.setuptools._backport.hashlib', 'barleycorn', 'barleycorn.toolkits'],
  url='https://bitbucket.org/jjpr/barleycorn',
  license='',
  author='jjpr',
  author_email='jjprescottroy@gmail.com',
  description='A domain-specific language for constructive solid geometry'
)
