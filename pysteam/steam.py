# encoding: utf-8

import collections
import os
import platform

import paths
import winutils

from model import LocalUserContext, Steam

def _resolve_userdata_path(paths):
  """
  Helper function which checks if the potential userdata directory exists
  and returns a new Steam instance with that userdata directory if it does.
  If the directory doesnt exist it returns None instead
  """
  if not paths: return None
  return next((Steam(path) for path in paths if os.path.exists(path)), None)

def get_steam():
  """
  Returns a Steam object representing the current Steam installation on the
  users computer. If the user doesn't have Steam installed, returns None.
  """
  # For both OS X and Linux, Steam stores it's userdata in a few consistent
  # locations.
  plat = platform.system()
  if plat == 'Darwin':
    return _resolve_userdata_path(paths.default_osx_userdata_paths())
  if plat == 'Linux':
    return _resolve_userdata_path(paths.default_linux_userdata_paths())

  # Windows is a bit trickier. The userdata directory is stored in the Steam
  # installation directory, meaning that theoretically it could be anywhere.
  # Luckily, Valve stores the installation directory in the registry, so its
  # still possible for us to figure out automatically
  if plat == 'Windows':
    possible_dir = winutils.find_userdata_directory()
    return _resolve_userdata_path([possible_dir])
  # This should never be hit. Windows, OS X, and Linux should be the only
  # supported platforms.
  # TODO: Add logging here so that the user (developer) knows that something
  # odd happened.
  return None

def local_user_ids(steam):
  """
  Returns a list of user ids who have logged into Steam on this computer.
  """
  if steam is None:
    return None
  # The userdata directory, at the top level, just contains a single
  # subdirectory for every user which has logged into this system (and
  # therefore that Steam has data for)
  return os.listdir(steam.userdata_directory)
  
def local_user_contexts(steam):
  if steam is None:
    return None
  return map(lambda uid: LocalUserContext(steam, uid), local_user_ids(steam))
