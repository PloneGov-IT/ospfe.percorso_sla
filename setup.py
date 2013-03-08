from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ospfe.percorso_sla',
      version=version,
      description="Modulo Plone per il monotoraggio dei pazienti SLA",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov sla form',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://github.com/PloneGov-IT/ospfe.percorso_sla',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ospfe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PloneFormGen',
          'uwosh.pfg.d2c',
          'plone.app.registry',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
