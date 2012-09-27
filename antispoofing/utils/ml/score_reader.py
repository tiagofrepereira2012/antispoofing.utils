#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Thu 27 Sep 2011 13:01:44 CEST 

"""
Class that work with the scores

"""

import bob
import numpy

class ScoreReader:

  def __init__(self,files,inputDir):
    """
    " Receive a list of xbob.db.replay.File to return the scores
    """

    self.files = files
    self.inputDir = inputDir
  

  def __str__(self):
    return "%d video files " % len(self.files)


  def getScores(self,onlyValidScores=True):
    """
    Return a numpy.array with the scores of all xbob.db.replay.File

    @param onlyValidScores Will return only the valid scores
    """

    allScores = numpy.array([])

    for f in self.files:
      fileName = str(f.make_path(self.inputDir,extension='.hdf5'))

      scores = bob.io.load(fileName)

      allScores=numpy.concatenate((allScores,scores))


    if(onlyValidScores):
      allScores = allScores[(numpy.where(numpy.isnan(allScores)==False))[0]]

    return allScores


