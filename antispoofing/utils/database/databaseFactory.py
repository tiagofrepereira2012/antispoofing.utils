#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

import abc

import xbob.db.replay
import xbob.db.casia_fasd

import antispoofing
from antispoofing.utils.database import *

class DatabaseFactory:
  """
  Factory of Database objects
  """

  @staticmethod
  def createDatabase(databaseName):
    avaliableDatabases = {'replay':'replay','casia_fasd':'casia_fasd'}  #Dictionary of avaliable databases

    try:
      #I do not know if it is stupid
      databaseName = avaliableDatabases[databaseName]
    except:
      raise DatabaseFactoryException("Database " + databaseName + " not registered.")

    if(databaseName=='replay'):
      return antispoofing.utils.database.Replay(xbob.db.replay.Database())
    elif(databaseName=='casia_fasd'):
      return antispoofing.utils.database.CasiaFASD(xbob.db.casia_fasd.Database())


class DatabaseFactoryException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


