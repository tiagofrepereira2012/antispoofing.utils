#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""
CASIA FASD database layer
"""
import bob
import xbob.db.casia_fasd

from antispoofing.utils.db import *
from antispoofing.utils.db.files import *

class CasiaFASD(Database):

  def __init__ (self,args=None):
    self.__db = xbob.db.casia_fasd.Database()

    self.__kwargs = {}

    if(type(args)!=type(None)):
      self.__kwargs = {
        'types': args.casiaTypes,
        'fold_no': 1,
      }


  @staticmethod
  def create_subparser(subparser,subparserName):
    """
    Creates a parser for the central manager taking into consideration the options for every module that can provide those
    """
    parser_casia = subparser.add_parser(subparserName, help='Casia FASD database')
    parser_casia.add_argument('--types', type=str, choices=('warped', 'cut', 'video', ''), default='', dest='casiaTypes', help='Defines the types of attack videos in the database that are going to be used.')

    parser_casia.set_defaults(which=subparserName)

    return


  def get_train_data(self):
    """
    Will return the real access and the attack File objects (antispoofing.utils.db.files.File) for training the antispoofing classifier
    """
    types, fold_no = self.__parseArguments()

    _,trainReal   = self.__db.cross_valid_foldobjects(cls='real', fold_no=fold_no)
    trainReal   = [CasiaFASDFile(f) for f in trainReal]

    _,trainAttack = self.__db.cross_valid_foldobjects(cls='attack', types=types, fold_no=fold_no)
    trainAttack   = [CasiaFASDFile(f) for f in trainAttack]

    return trainReal,trainAttack


  def get_devel_data(self):
    """
    Will return the real access and the attack File objects (antispoofing.utils.db.files.File) for development (supposed to tune the antispoofing classifier)
    """
    types, fold_no = self.__parseArguments()

    develReal,_   = self.__db.cross_valid_foldobjects(cls='real', fold_no=fold_no)
    develReal   = [CasiaFASDFile(f) for f in develReal]

    develAttack,_ = self.__db.cross_valid_foldobjects(cls='attack', types=types, fold_no=fold_no)
    develAttack   = [CasiaFASDFile(f) for f in develAttack]

    return develReal,develAttack


  def get_test_data(self):
    """
    Will return the real access and the attack File objects (antispoofing.utils.db.files.File) for test (supposed to report the results)
    """
    types,_ = self.__parseArguments()

    testReal    = self.__db.objects(groups='test', cls='real')
    testReal   = [CasiaFASDFile(f) for f in testReal]

    testAttack  = self.__db.objects(groups='test', cls='attack', types=types)
    testAttack   = [CasiaFASDFile(f) for f in testAttack]

    return testReal,testAttack


  def get_all_data(self):
    """
    Will return the real access and the attack File objects (antispoofing.utils.db.files.File) for ALL group sets
    """
    allReal   = self.__db.objects(cls='real',**self.__kwargs)
    allReal   = [CasiaFASDFile(f) for f in allReal]

    allAttacks  = self.__db.objects(cls='attack',**self.__kwargs)
    allAttacks  = [CasiaFASDFile(f) for f in allAttacks]

    return allReal,allAttacks


  def __parseArguments(self):

    #If crashes, return all objects    
    try:
      types = self.__kwargs['types']
      if types == '':
        types = ('warped', 'cut','video')
    except:
        types = ('warped', 'cut','video')

    try:
      fold_no = self.__kwargs['fold_no']
      if fold_no == '':
        fold_no = 1
    except:
      fold_no = 1

    return types, fold_no
