 
from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, AltAz
from astroplan import Observer

@python_2_unicode_compatible  # to support Python 2
class Observatory(models.Model):
   
   name = models.CharField(max_length=100, default='')
   
   # latitude in degrees
   latitude = models.FloatField(default=0)
   
   # longitude in degrees
   longitude = models.FloatField(default=0)
   
   # altitude in meter
   altitude = models.FloatField(default=0)
   
   
   url = models.URLField(default='')
   
   note = models.CharField(max_length=300, default='')
   
   #-- bookkeeping
   added_on = models.DateTimeField(auto_now_add=True)
   last_modified = models.DateTimeField(auto_now=True)
   
   
   def get_EarthLocation(self):
      """
      Returns the astropy earthlocation of this observatory
      """
      return EarthLocation(lat=self.latitude*u.deg, lon=self.longitude*u.deg, height=self.altitude*u.m)
      
   def get_sunset_sunrise(self, time):
      """
      Returns the sunset and sunrise times of the night containing the time provided
      time is a astropy Time object
      The sunset and sunrise times are returns as an astropy Time object with the same 
      settings as the provided Time object. 
      """
      observer = Observer(location=self.get_EarthLocation())
      sunset = observer.sun_set_time(time, which='nearest')
      sunrise = observer.sun_rise_time(time, which='nearest')
      
      return sunset, sunrise
   
   #-- representation of self
   def __str__(self):
      return "{}: lat={}, lon={}, alt={}".format(self.name, self.latitude, self.longitude, self.altitude)
