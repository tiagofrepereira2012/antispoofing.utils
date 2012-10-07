#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
# Tue 01 Oct 2012 16:48:44 CEST 

"""Replay attack database implementation as antispoofing.utils.db.Database"""

import xbob.db.replay
from . import File as FileBase
from . import Database as DatabaseBase

class File(FileBase):

  def __init__(self, f):
    """Initializes this File object with the xbob.db.replay.File equivalent"""

    self.__f = f

  def videofile(self, directory=None):
    return self.__f.videofile(directory=directory)
  videofile.__doc__ = FileBase.videofile.__doc__

  def facefile(self, directory=None):
    return self.__f.facefile(directory=directory)
  facefile.__doc__ = FileBase.facefile.__doc__

  def bbx(self, directory=None):
    return self.__f.bbx(directory=directory)
  bbx.__doc__ = FileBase.bbx.__doc__

  def load(self, directory=None, extension='.hdf5'):
    return self.__f.load(directory=directory, extension=extension)
  load.__doc__ = FileBase.bbx.__doc__

  def save(self, data, directory=None, extension='.hdf5'):
    return self.__f.save(data, directory=directory, extension=extension)
  save.__doc__ = FileBase.save.__doc__

  def make_path(self, directory=None, extension=None):
    return self.__f.make_path(directory=directory, extension=extension)
  make_path.__doc__ = FileBase.make_path.__doc__

class Database(DatabaseBase):
  __doc__ = xbob.db.replay.__doc__

  def __init__ (self, args=None):
    self.__db = xbob.db.replay.Database()

    self.__kwargs = {}
    if args is not None:

      self.__kwargs = {
        'protocol': args.replay_protocol,
        'support' : args.replay_support,
        'light'   : args.replay_light,
       }
  __init__.__doc__ = DatabaseBase.__init__.__doc__

  def create_subparser(self, subparser, entry_point_name):
    p = subparser.add_parser(entry_point_name, help=self.long_description())

    protocols = [p.name for p in xbob.db.replay.Database().protocols()]

    p.add_argument('--protocol', type=str, dest="replay_protocol", default='grandtest', help='The REPLAY-ATTACK protocol type may be specified   instead of the id switch to subselect a smaller number of files to operate on', choices=protocols)

    p.add_argument('--support', type=str, choices=('fixed', 'hand'), default='', dest='replay_support', help='One of the valid supported attacks (fixed, hand) (defaults to "%(default)s")')

    p.add_argument('--light', type=str, choices=('controlled', 'adverse'), default='', dest='replay_light', help='Types of illumination conditions (controlled,adverse) (defaults to "%(default)s")')
  
    p.set_defaults(name=entry_point_name)
    p.set_defaults(cls=Database)
    
    return
  create_subparser.__doc__ = DatabaseBase.create_subparser.__doc__
  
  def short_description(self):
    return "Anti-Spoofing database with 1300 videos produced at Idiap, Switzerland"
  short_description.__doc__ = DatabaseBase.short_description.__doc__
 
  def long_description(self):
    return Database.__doc__
  long_description.__doc__ = DatabaseBase.long_description.__doc__
 
  def get_data(self, group):
    """Returns either all objects or objects for a specific group"""
    
    real = dict(self__kwargs)
    real.update({'groups': group, 'cls': 'real'})
    attack = dict(self__kwargs)
    attack.update({'groups': group, 'cls': 'attack'})
    return [File(k) for k in self.__db.objects(**real)], \
        [File(k) for k in self.__db.objects(**attack)]

  def get_train_data(self):
    return get_data('train')
  get_train_data.__doc__ = DatabaseBase.get_train_data.__doc__

  def get_devel_data(self):
    return get_data('devel')
  get_devel_data.__doc__ = DatabaseBase.get_devel_data.__doc__

  def get_test_data(self):
    return get_data('test')
  get_test_data.__doc__ = DatabaseBase.get_test_data.__doc__

  def get_all_data(self):
    return get_data(None)
  get_all_data.__doc__ = DatabaseBase.get_all_data.__doc__
