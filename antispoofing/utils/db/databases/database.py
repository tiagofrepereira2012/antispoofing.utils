#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

import abc

import antispoofing
from antispoofing.utils.db.databases import *

class Database:
  """
  Abstract class that define some method for the antispoofing databases
  """

  __metaclass__ = abc.ABCMeta

  def __init__ (self,args=None):
    return

  @staticmethod
  @abc.abstractmethod
  def name():
    """
    Defines the name of the object
    """
    return

  @abc.abstractmethod
  def get_train_data(self,**kwargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for training the antispoofing classifier
    """
    return

  @abc.abstractmethod
  def get_devel_data(self,**kwargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for development (supposed to tune the antispoofing classifier)
    """
    return

  @abc.abstractmethod
  def get_test_data(self,**kwargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for test (supposed to report the results)
    """
    return


  @staticmethod
  @abc.abstractmethod
  def create_subparser(subparser):
    """
    Creates a subparser for the central manager taking into consideration the options for every module that can provide those
    """
    return 

  @staticmethod
  def create_parser(parser):
    """
    Defines a sub parser for each database
    """

    subparsers = parser.add_subparsers(help="Database tests available")

    for d in antispoofing.utils.db.databases.Database.__subclasses__():
      d.create_subparser(subparsers)

    return


