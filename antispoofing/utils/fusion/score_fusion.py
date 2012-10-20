#!/usr/bin/env python
#Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
#Oct 01 20:50:00 CEST 2012

"""
This script run the score fusion

"""

import bob
import numpy

from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *

class ScoreFusion:
  """
  Class that run different Score level fusion with different normalization score algorithm
  """

  def __init__(self,scoreNormalizationAlg,realScoreReader,attackScoreReader):
    """
    Constructor

    @param scoresNormalization Name of the score Normalizatio algorithm (TODO: THIS IS CRAP. PLEASE THINK IN A BETTER SOLUTION)

    @param scoresReaderRealAccess ScoreReader with real access scores
    @param scoresReaderAttackAccess ScoreReader with real attack scores
    """

    #Checking if the number of countermeasures has a match
    self.__checkCounterMeasureNumbers(realScoreReader,attackScoreReader)

    self.__realScoreReader   = realScoreReader
    self.__attackScoreReader = attackScoreReader

    self.__llrMachine = None
    self.__llrTrained = False

    self.__scoreNormalizationAlg = scoreNormalizationAlg

    self.__scoreNormalization = ScoreNormalization(numpy.concatenate((realScoreReader.getConcatenetedScores(), attackScoreReader.getConcatenetedScores()), axis=0))



  def __checkCounterMeasureNumbers(self,scoreReaderA,scoreReaderB):
    """
    Checking if the number of countermeasures has a match
    """
    if(scoreReaderA.getNumberCountermeasures() != scoreReaderB.getNumberCountermeasures()):
      raise ScoreFusionException("Number of countermeasures between real access and attacks does not match")
    

  def __normalizeData(self,data):
    """
    Apply the score normalization set by __scoreNormalizationAlg
    """
    if(self.__scoreNormalizationAlg=="minmax"):
      return self.__scoreNormalization.calculateMinMaxNorm(data)
    else:
      raise ScoreFusionException("Normalization algorithm " + self.__scoreNormalizationAlg + " invalid.")


  def __normalizeOutput(self,normalizationFactor,data):
    """
    Helper that normalize some data between -1 and 1
    """

    scoreNorm = ScoreNormalization(normalizationFactor)
    return scoreNorm.calculateMinMaxNorm(data)


  def getLLRScores(self,scoreReader, normalizeOutput=True):
    """
    Get the fusion of scores using the LLR machine

    @param scoreReader Score reader with the scores to be fused. If the LLR Machine was not trained the method will train
    @param normalizeOutput Normalize the output between -1 and 1
   
    @return A numpy.array with the scores
    """

    self.__checkCounterMeasureNumbers(self.__realScoreReader,scoreReader)

    #Applying normalization
    normalizedData = self.__normalizeData(scoreReader.getConcatenetedScores())
    normalizedReal   = None
    normalizedAttack = None

    #Trainning the LLR if not trained
    if(not self.__llrTrained):
      self.__llrTrained = True
      llrTrainer = bob.trainer.LLRTrainer()
      self.__llrMachine = bob.machine.LinearMachine()

      normalizedReal   = self.__normalizeData(self.__realScoreReader.getConcatenetedScores())
      normalizedAttack = self.__normalizeData(self.__attackScoreReader.getConcatenetedScores())
      llrTrainer.train(self.__llrMachine, normalizedReal,normalizedAttack)

    #Applying the LLR in the input data
    outputData = self.__llrMachine(normalizedData)

    #Normalizing the output
    if(normalizeOutput):
      #Getting the scores for the trainning data
      if(normalizedReal == None):
        normalizedReal   = self.__normalizeData(self.__realScoreReader.getConcatenetedScores())
        normalizedAttack = self.__normalizeData(self.__attackScoreReader.getConcatenetedScores())

      normalizedReal   = self.__llrMachine(normalizedReal)
      normalizedAttack = self.__llrMachine(normalizedAttack)

      #Normalizing the output
      normalizationFactor  = numpy.concatenate((normalizedReal,normalizedAttack),axis=0)
      outputData = self.__normalizeOutput(normalizationFactor,outputData)  

    outputData = numpy.reshape(outputData,(len(outputData)))
    return outputData



  def getSUMScores(self,scoreReader, normalizeOutput=True):
    """
    Get the fusion of scores using the SUM rule. The countermeasures scores has the same weight.

    @param scoreReader Score reader with the scores to be fused. If the LLR Machine was not trained the method will train
    @param normalizeOutput Normalize the output between 0 and 1
   
    @return A numpy.array with the scores
    """

    self.__checkCounterMeasureNumbers(self.__realScoreReader,scoreReader)


    #Applying the score normalization
    normalizedData = self.__normalizeData(scoreReader.getConcatenetedScores())
    normalizedReal   = None
    normalizedAttack = None


    #Applying the SUM rule in the input data
    outputData = numpy.sum(normalizedData,axis=1)

    #Normalizing the output
    if(normalizeOutput):
      #Getting the scores for the trainning data
      if(normalizedReal == None):
        normalizedReal   = self.__normalizeData(self.__realScoreReader.getConcatenetedScores())
        normalizedAttack = self.__normalizeData(self.__attackScoreReader.getConcatenetedScores())

      normalizedReal   = numpy.sum(normalizedReal,axis=1)
      normalizedAttack = numpy.sum(normalizedAttack,axis=1)

      #Normalizing the output
      normalizationFactor  = numpy.concatenate((normalizedReal,normalizedAttack),axis=0)
      outputData = self.__normalizeOutput(normalizationFactor,outputData)  

    outputData = numpy.reshape(outputData,(len(outputData)))
    return outputData




class ScoreFusionException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


