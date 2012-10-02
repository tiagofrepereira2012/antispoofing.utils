#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""
Abstract class that define some method for the antispoofing databases
"""
import abc
import bob
import xbob.db.replay

from antispoofing.utils.database import *

class Replay(Database):

  def __init__ (self,db):
    self.__db = db    


  def getTrainData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for training the antispoofing classifier
    """

    protocol, support, light = self.__parseArguments(**kargs)

    trainReal   = self.__db.objects(groups='train', cls='real',protocol=protocol, support=support, light=light)
    trainAttack = self.__db.objects(groups='train', cls='attack',protocol=protocol, support=support, light=light)

    return trainReal,trainAttack


  def getDevelData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for development (supposed to tune the antispoofing classifier)
    """
    protocol, support, light = self.__parseArguments(**kargs)

    develReal   = self.__db.objects(groups='devel', cls='real',protocol=protocol, support=support, light=light)
    develAttack = self.__db.objects(groups='devel', cls='attack',protocol=protocol, support=support, light=light)

    return develReal,develAttack


  def getTestData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for test (supposed to report the results)
    """
    protocol, support, light = self.__parseArguments(**kargs)

    testReal    = self.__db.objects(groups='test', cls='real',protocol=protocol, support=support, light=light)
    testAttack  = self.__db.objects(groups='test', cls='attack',protocol=protocol, support=support, light=light)

    return testReal,testAttack


  def __parseArguments(self, **kargs):

    #If crashes, return all objects    
    try:
      protocol = kargs['protocol']
    except:
      protocol = 'grandtest'

    try:
      support  = kargs['support']
    except:
      support  = ''

    try:
      light    = kargs['light']
    except:
      light    = ''

    return protocol, support, light

