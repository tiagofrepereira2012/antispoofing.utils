#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Sat 22 11:43:19 CET 2012

import bob
import numpy

from . import *

"""
PLEASE DO NOT USE THIS FILE BECAUSE IS NOT WORKING


Implement the logistic regression to a set of data
"""

"""
Train the countermeasure
"""
def train(realData, attackData, copy=True):

  if(copy):
    realData   = numpy.copy(realData)
    attackData = numpy.copy(attackData)


  #Creating the arrayset
  realDataArraySet = bob.io.Arrayset()
  realDataArraySet.append(realData)
  #for data in realData:
    #realDataArraySet.append(data)

  attackDataArraySet = bob.io.Arrayset()
  attackDataArraySet.append(attackData)
  #for data in attackData:
    #attackDataArraySet.append(data)

  #print(attackDataArraySet.shape)
  #print(realDataArraySet.shape)
  #exit()

  #Training
  trainer = bob.trainer.LLRTrainer()
  machine = bob.machine.LinearMachine()
  trainer.train(machine, realDataArraySet,attackDataArraySet)

  return machine
