#!/usr/bin/env python
#Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
#Thu Sep 27 17:04:09 CEST 2012

import bob
import numpy


class ScoreNormalization:
  """
  Class that implements some score normalization algorithms
  """

  def __init__(self,scores):
    """
    " Constructor
    " @param scores set of scores to help in the normaliztion
    """
    
    self.mins = min(scores)
    self.maxs = max(scores)
    
    self.avg =  numpy.average(scores)
    self.std  = numpy.std(scores)

    self.totalScores = len(scores)


  def __str__(self):
    string =  "%d Scores \n min=%.2f \n max=%.2f \n Average=%.2f \n Standard Deviation=%.2f " % \
              (self.totalScores, 
              self.mins, 
              self.maxs, 
              self.avg, 
              self.std,
              )
    
    return string


  def calculateZNorm(self,scores):
    """
    Make the ZNorm score normalization
 
    @param scores numpy.array to be normalized
    @return numpy.array with the normalized scores
    """

    if(std==0):
      std = 0.000001

    return numpy.divide((scores - self.avg),self.std)


  def calculateMinMaxNorm(self,scores,lowerBound = -1, upperBound = 1):
    """
    Normalize the score in an specific interval
 
    @param scores numpy.array to be normalized
    @param lowBound The lower bound
    @param upperBound The upper bound

    @return numpy.array with the normalized scores. Will return a array([]) if maxs - mins = 0
    """

    denom = self.maxs - self.mins
    if denom == 0:
      return numpy.array([])
   
    return (upperBound - lowerBound) * (scores - self.mins) / (self.maxs - self.mins) + lowerBound

