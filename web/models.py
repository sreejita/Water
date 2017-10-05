# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class B2S(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    bb_id = models.TextField(primary_key=True)
    site_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'b2s'
        unique_together = (('bb_id', 'site_id', 'bb_id', 'site_id', 'bb_id', 'site_id', 'bb_id', 'site_id'),)


class Boundingbox(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    bb_id = models.TextField(primary_key=True)
    north = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    south = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    west = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    east = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boundingbox'
        unique_together = (('bb_id', 'bb_id', 'bb_id', 'bb_id'),)


class Sites(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    site_id = models.TextField(primary_key=True)
    organizationformalname = models.TextField(blank=True, null=True)
    organizationidentifier = models.TextField(blank=True, null=True)
    monitoringlocationname = models.TextField(blank=True, null=True)
    monitoringlocationtypename = models.TextField(blank=True, null=True)
    monitoringlocationdescriptiontext = models.TextField(blank=True, null=True)
    huceightdigitcode = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    drainageareameasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    drainageareameasure_measureunitcode = models.TextField(blank=True, null=True)
    contributingdrainageareameasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    contributingdrainageareameasure_measureunitcode = models.TextField(blank=True, null=True)
    latitudemeasure = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    longitudemeasure = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sourcemapscalenumeric = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    horizontalaccuracymeasure_measurevalue = models.TextField(blank=True, null=True)
    horizontalaccuracymeasure_measureunitcode = models.TextField(blank=True, null=True)
    horizontalcollectionmethodname = models.TextField(blank=True, null=True)
    horizontalcoordinatereferencesystemdatumname = models.TextField(blank=True, null=True)
    verticalmeasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    verticalmeasure_measureunitcode = models.TextField(blank=True, null=True)
    verticalaccuracymeasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    verticalaccuracymeasure_measureunitcode = models.TextField(blank=True, null=True)
    verticalcollectionmethodname = models.TextField(blank=True, null=True)
    verticalcoordinatereferencesystemdatumname = models.TextField(blank=True, null=True)
    countrycode = models.TextField(blank=True, null=True)
    statecode = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    countycode = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    aquifername = models.TextField(blank=True, null=True)
    formationtypetext = models.TextField(blank=True, null=True)
    aquifertypename = models.TextField(blank=True, null=True)
    constructiondatetext = models.TextField(blank=True, null=True)
    welldepthmeasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    welldepthmeasure_measureunitcode = models.TextField(blank=True, null=True)
    wellholedepthmeasure_measurevalue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sites'
        unique_together = (('site_id', 'site_id', 'site_id', 'site_id'),)


class W2B(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    nhd_lake_id = models.TextField()
    bb_id = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'w2b'
        unique_together = (('bb_id', 'nhd_lake_id', 'bb_id', 'nhd_lake_id', 'bb_id', 'nhd_lake_id', 'bb_id', 'nhd_lake_id'),)


class W2S(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    nhd_lake_id = models.TextField()
    gnis_lake_name = models.TextField(blank=True, null=True)
    site_id = models.TextField(primary_key=True)
    monitoringlocationname = models.TextField(blank=True, null=True)
    isinsidelake = models.NullBooleanField()
    disttoshore_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'w2s'
        unique_together = (('site_id', 'nhd_lake_id', 'site_id', 'nhd_lake_id', 'site_id', 'nhd_lake_id', 'site_id', 'nhd_lake_id'),)


class Waterbodies(models.Model):
    sno = models.IntegerField(blank=True, null=True)
    nhd_lake_id = models.TextField(primary_key=True)
    gnis_name = models.TextField(blank=True, null=True)
    gnis_id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    area_sqkm = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    elevation_feet = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ftype = models.IntegerField(blank=True, null=True)
    fcode = models.IntegerField(blank=True, null=True)
    fdate = models.DateField(blank=True, null=True)
    shape_leng_decimaldegrees = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area_sqdecimaldegrees = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waterbodies'
        unique_together = (('nhd_lake_id', 'nhd_lake_id', 'nhd_lake_id', 'nhd_lake_id'),)
