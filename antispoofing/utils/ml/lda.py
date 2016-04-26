#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Mon 19 Sep 2011 15:01:44 CEST 

"""LDA training for the anti-spoofing library
"""

import bob.learn.linear
import numpy

def make_lda(train, use_pinv=False):
  """Creates a new linear machine and train it using LDA.

  Keyword Parameters:

  train
    An iterable (list) containing two ndarray: the first contains the real
    accesses and the second contains the attacks.

  Returns the machine
  """

  print(use_pinv)
  T = bob.learn.linear.FisherLDATrainer(use_pinv=use_pinv)
  machine, eig_vals = T.train(train)
  return machine

def get_scores(machine, data):
  """Gets the scores for the data"""

  #return numpy.vstack(data.foreach(machine))[:,0]

  return machine(data)
