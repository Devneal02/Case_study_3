from abc import ABC, abstractmethod

class Person(ABC):
  def __init__(self, fname, mname, lname, gender, age, email, phonenum, address):
    self.fname = fname
    self.mname = mname
    self.lname = lname
    self.email = email
    self.gender = gender
    self.age = age
    self.phonenum = phonenum
    self.address = address
    self._username = ""
    self.__password = ""
    self.isloggedIn = False

  @abstractmethod
  def LogIn(self):
    pass

  @abstractmethod
  def Profile(self):
    pass