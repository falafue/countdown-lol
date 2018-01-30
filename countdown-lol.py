#!/usr/bin/python

import random
import csv
import Image
import ImageDraw
import time
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 4)

matrix.SetWriteCycles(4)

countdown =  15
steps = 30
size=32

digits=len(`countdown`)

class daliDigits:
  def __init__(self,steps):
    self.img = [[0 for step in range(steps)] for digit in range(10)] 
    for digit in range(10):    
      for step in range(steps):
        stepstr="{0:02d}".format(step)
        self.img[digit][step] = Image.open("pgm/"+`digit`+"/dali_digits_"+`digit`+"-"+stepstr+".pbm")
  
  def alldigit(self,num,step):
    numstr=str(num).zfill(digits)
    numlen=len(numstr)
    stepstr=str(step).zfill(digits)
    image = Image.new("RGB", (size*numlen,size))
    for pos in range(digits):
      if pos < digits-1:
        zero=0
        for lower in range(pos+1,digits):
          if numstr[lower] != "9":
            zero=1
        if zero==0:
          #if numstr[pos] == "0":
          #  newnum=str(1)
          #else:
          #  newnum=str(int(numstr[pos])-1)
          numimg = Image.open("pgm/"+numstr[pos]+"/dali_digits_"+numstr[pos]+"-"+stepstr+".pbm")
          numimg.load()
          image.paste(numimg,(pos*size, -1, (pos+1)*size,size-1))
          print "0{0:1s}-{1:02d}".format(numstr[pos],step),
        else:
          numimg = Image.open("pgm/"+numstr[pos]+"/dali_digits_"+numstr[pos]+"-00.pbm")
          numimg.load()
          image.paste(numimg,(pos*size, -1, (pos+1)*size,size-1))
          print "0{0:1s}-{1:02d}".format(numstr[pos],0),
      else:
        numimg = Image.open("pgm/"+numstr[digits-1]+"/dali_digits_"+numstr[digits-1]+"-"+stepstr+".pbm")
        numimg.load()
        image.paste(numimg,(pos*size, -1, (pos+1)*size,size-1))
        print "0{0:1s}-{1:02d}".format(numstr[digits-1],step) 
      matrix.Clear()
      matrix.SetImage(image.im.id, 40, 0)

class CountDown:

  def __init__(self,nseconds,nsteps):
    self.seconds=nseconds
    self.steps=nsteps
    self.dalidigits = daliDigits(steps)

  def countdown(self):
    for count in reversed(range(self.seconds+1)):
      for step in reversed(range(self.steps)):
        print(chr(27) + "[2J") 
        self.dalidigits.alldigit(count,step)
        time.sleep(1.0/self.steps)

  def shownum(self,num,logofile):
    logo=Image.open(logofile)
    logo.load()
    numstr=str(num)
    numlen=len(numstr)
    image = Image.new("RGB", (size*numlen+10+logo.size[0],size))
    matrix.Clear()
    for count in range(len(`num`)):
      numdigit=numstr[count]
      numimg = Image.open("pgm/"+numdigit+"/dali_digits_"+numdigit+"-00.pbm")
      numimg.load()
      image.paste(numimg,(count*size, -2, (count+1)*size,size-2))
    image.paste(logo,((count+1)*size+10, -2, (count+1)*size+10+logo.size[0],logo.size[1]-2))
    image.load()
    for n in range(128, -image.size[0], -1):
      matrix.SetImage(image.im.id, n, 1)
      time.sleep(0.025)
      matrix.Clear()
    

with open('liste.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    myList = list(reader)

counter = CountDown(countdown,steps)

while len(myList) >0:
  element=random.choice(myList)
  counter.shownum(myList.index(element),element["image"])
  myList.remove(element)
  counter.countdown()
