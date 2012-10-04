#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Wed 03 Oct 2012 13:36:44 CEST 

import bob
import xbob.db.casia_fasd

from antispoofing.utils.db.files import *

class CasiaFASDFile(File):
  """
  Abstract class that define some methods for the antispoofing File object
  """

  def __init__(self,xbobFile):

    self.__xbobFile = xbobFile



  def videofile(self, directory=None):
    """Returns the path to the database video file for this object

    @param directory An optional directory name that will be prefixed to the returned result.

    @return Returns a string containing the video file path.
    """
    return self.__xbobFile.videofile(directory=directory)


  def facefile(self, directory=None):
    """Returns the path to the companion face bounding-box file

    @param directory An optional directory name that will be prefixed to the returned result.

    @return Returns a string containing the face file path.
    """
    return self.__xbobFile.facefile(directory=directory)


  def bbx(self, directory=None):
    """Reads the file containing the face locations for the frames in the
    current video

    @param directory A directory name that will be prepended to the final filepaths where the
                     face bounding boxes are located, if not on the current directory.

    @return
      A :py:class:`numpy.ndarray` containing information about the located
      faces in the videos. Each row of the :py:class:`numpy.ndarray`
      corresponds for one frame. The five columns of the
      :py:class:`numpy.ndarray` are (all integers):

      * Frame number (int)
      * Bounding box top-left X coordinate (int)
      * Bounding box top-left Y coordinate (int)
      * Bounding box width (int)
      * Bounding box height (int)

      Note that **not** all the frames may contain detected faces.
    """

    return self.__xbobFile.bbx(directory=directory)


  def load(self, directory=None, extension='.hdf5'):
    """Loads the data at the specified location and using the given extension.

    @param data The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    @param directory [optional] If not empty or None, this directory is prefixed to the final
                                file destination

    @param extension [optional] The extension of the filename - this will control the type of
                                output and the codec for saving the input blob.
    """

    return self.__xbobFile.load(directory=directory, extension=extension)


  def save(self, data, directory=None, extension='.hdf5'):
    """Saves the input data at the specified location and using the given
    extension.

    @param data The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    @param directory [optional] If not empty or None, this directory is prefixed to the final file destination

    @param extension [optional] The extension of the filename - this will control the type of
                                output and the codec for saving the input blob.
    """
    
    return self.__xbobFile.save(data, directory=directory, extension=extension)


  def make_path(self, directory=None, extension=None):
    """Wraps the current path so that a complete path is formed

    @param directory An optional directory name that will be prefixed to the returned result.

    @param extension An optional extension that will be suffixed to the returned filename. The
                     extension normally includes the leading ``.`` character as in ``.jpg`` or ``.hdf5``.

    @return Returns a string containing the newly generated file path.
    """

    return self.__xbobFile.make_path(directory=directory, extension=extension)


