import sys

class Logger:

  def __init__(self, logging):
    self.logging = logging

  def write(self, str):
    if self.logging:
      print(str)
