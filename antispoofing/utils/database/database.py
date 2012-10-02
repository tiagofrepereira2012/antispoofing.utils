#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

import abc

class Database:
  """
  Abstract class that define some method for the antispoofing databases
  """

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def getTrainData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for training the antispoofing classifier
    """
    return

  @abc.abstractmethod
  def getDevelData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for development (supposed to tune the antispoofing classifier)
    """
    return

  @abc.abstractmethod
  def getTestData(self,**kargs):
    """
    Will return the real access and the attack File objects (xbob.db.<database>.File) for test (supposed to report the results)
    """
    return

