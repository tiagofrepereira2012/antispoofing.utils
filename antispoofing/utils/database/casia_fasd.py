#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""
Abstract class that define some method for the antispoofing databases
"""
import abc
import bob
import xbob.db.casia_fasd

from antispoofing.utils.database import *

class CasiaFASD(Database):

  def __init__ (self,db):
    self.__db = db


  def getTrainData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for training the antispoofing classifier
    """
    types, fold_no = self.__parseArguments(**kargs)

    _,trainReal   = self.__db.cross_valid_foldobjects(cls='real', fold_no=fold_no)
    _,trainAttack = self.__db.cross_valid_foldobjects(cls='attack', types=types, fold_no=fold_no)

    return trainReal,trainAttack


  def getDevelData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for development (supposed to tune the antispoofing classifier)
    """
    types, fold_no = self.__parseArguments(**kargs)

    develReal,_   = self.__db.cross_valid_foldobjects(cls='real', fold_no=fold_no)
    develAttack,_ = self.__db.cross_valid_foldobjects(cls='attack', types=types, fold_no=fold_no)

    return develReal,develAttack


  def getTestData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for test (supposed to report the results)
    """
    types,_ = self.__parseArguments(**kargs)

    testReal    = self.__db.objects(groups='test', cls='real')
    testAttack  = self.__db.objects(groups='test', cls='attack', types=types)

    return testReal,testAttack


  def __parseArguments(self, **kargs):

    #If crashes, return all objects    
    try:
      types = kargs['types']
      if types == '':
        types = ('warped', 'cut','video')
    except:
        types = ('warped', 'cut','video')

    try:
      fold_no = kargs['fold_no']
      if fold_no == '':
        fold_no = 1
    except:
      fold_no = 1

    return types, fold_no



    



