#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Wed Sep 12 11:43:19 CET 2012

import bob
import numpy

from .. import ml
from ..ml import pca, lda, norm

"""
Implement the train flow to a LDA based countermeasure
"""

"""
Train the countermeasure
"""
def train(train_real_plane, train_attack_plane, normalize=False,pca_reduction=False,copy=True):

  pca_machine = None

  if(copy):
    train_real_plane   = numpy.copy(train_real_plane)
    train_attack_plane = numpy.copy(train_attack_plane)

  if normalize:  # zero mean unit variance data normalziation
    mean, std = norm.calc_mean_std(train_real_plane, train_attack_plane)

  # PCA dimensionality reduction of the data
  if pca_reduction:
    train = bob.io.Arrayset() # preparing the train data for PCA (putting them altogether into bob.io.Arrayset)
    train.extend(train_real_plane); train.extend(train_attack_plane)
    pca_machine = pca.make_pca(train, energy, False) # performing PCA

    #Storing the normaliation factors in PCA machine
    if normalize:
      pca_machine.input_subtract = mean
      pca_machine.input_divide = std

    train_real_plane = pca.pcareduce(pca_machine, train_real_plane); train_attack_plane = pca.pcareduce(pca_machine, train_attack_plane)

  lda_machine = lda.make_lda((train_real_plane, train_attack_plane)) # training the LDA
  lda_machine.shape = (lda_machine.shape[0], 1) #only use first component!

  #Storing the normaliation factors in Linear machine
  if(not pca_reduction and normalize):
    lda_machine.input_subtract = mean
    lda_machine.input_divide   = std

  return [lda_machine,pca_machine]



"""
Compute scores
"""
def computeScores(train_real_plane, train_attack_plane,devel_real_plane, devel_attack_plane,test_real_plane, test_attack_plane, ldaMachine,pcaMachine, copy=True):

  if(copy):
    train_real   = numpy.copy(train_real)
    train_attack = numpy.copy(train_attack)

    devel_real   = numpy.copy(devel_real)
    devel_attack = numpy.copy(devel_attack)
  
    test_real   = numpy.copy(test_real)
    test_attack = numpy.copy(test_attack)


  if(pcaMachine != None):
    train_real = pca.pcareduce(pca_machine, train_real); train_attack = pca.pcareduce(pca_machine, train_attack)
    devel_real = pca.pcareduce(pca_machine, devel_real); devel_attack = pca.pcareduce(pca_machine, devel_attack)
    test_real  = pca.pcareduce(pca_machine, test_real); test_attack = pca.pcareduce(pca_machine, test_attack)


  train_real_scores   = lda.get_scores(lda_machine, train_real)
  train_attack_scores = lda.get_scores(lda_machine, train_attack)

  devel_real_scores   = lda.get_scores(lda_machine, devel_real)
  devel_attack_scores = lda.get_scores(lda_machine, devel_attack)

  test_real_scores    = lda.get_scores(lda_machine, test_real)
  test_attack_scores  = lda.get_scores(lda_machine, test_attack)

  # it is expected that the scores of the real accesses are always higher then the scores of the attacks. Therefore, a check is first made, if the   average of the scores of real accesses is smaller then the average of the scores of the attacks, all the scores are inverted by multiplying with -1.
  if numpy.mean(devel_real_scores) < numpy.mean(devel_attack_scores):
    train_real_scores = train_real_scores * -1; train_attack_scores = train_attack_scores * -1
    devel_real_scores = devel_real_scores * -1; devel_attack_scores = devel_attack_scores * -1
    test_real_scores = test_real_scores * -1; test_attack_scores = test_attack_scores * -1


  return [train_real_scores,train_attack_scores,devel_real_scores,devel_attack_scores,test_real_scores,test_attack_scores]






