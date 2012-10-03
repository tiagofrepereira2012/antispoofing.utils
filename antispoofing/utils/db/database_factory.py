#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

import abc

import xbob.db.replay
import xbob.db.casia_fasd

import antispoofing
from antispoofing.utils.db import *

class DatabaseFactory:
  """
  Factory of Database objects
  """

  @staticmethod
  def createDatabase(databaseName,args):

    #Searching the objects
    for d in antispoofing.utils.db.Database.__subclasses__():
      if(databaseName == d.name()):
        return d(args)

    raise DatabaseFactoryException("Database " + databaseName + " not registered.")


class DatabaseFactoryException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


