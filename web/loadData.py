import psycopg2
import csv
import sys

db = "waterqualitydb"
uname = "postgres"
pwd = ""
hostname = "localhost"
filePath = ""
fileSeparator = "/"
tableList = ["WATERBODIES", "BOUNDINGBOX", "SITES", "W2B", "B2S", "W2S"]
#schemaList = ["WISCONSIN", "MICHIGAN", "INDIANA", "MINNESOTA"]
schemaList = ["WISCONSIN"]

conn = psycopg2.connect (database = db, user=uname, password=pwd, host=hostname, port="5432")
cursor = conn.cursor();
conn.set_client_encoding('Latin1')

def createSchemas():
    for s in schemaList:
        createSchema(s)

def createSchema(schema):
    sql = """CREATE SCHEMA %s"""
    cursor.execute(sql % schema)
    #conn.commit() 

def createTables(schema_name):
    column_separator = "_" 

    B2S_table = """CREATE TABLE %s.B2S(SNO integer,BB_ID text,SITE_ID text,PRIMARY KEY (BB_ID , SITE_ID))""" % schema_name

    BOUNDINGBOX_table = """CREATE TABLE %s.BOUNDINGBOX(SNO integer,BB_ID text,North numeric,South numeric,West numeric,East numeric,PRIMARY KEY (BB_ID))""" % schema_name

    SITES_table = """CREATE TABLE %s.SITES(SNO integer,SITE_ID text,OrganizationFormalName text,OrganizationIdentifier text,MonitoringLocationName text,MonitoringLocationTypeName text,MonitoringLocationDescriptionText text,HUCEightDigitCode numeric,DrainageAreaMeasure%sMeasureValue numeric,DrainageAreaMeasure%sMeasureUnitCode text,ContributingDrainageAreaMeasure%sMeasureValue numeric,ContributingDrainageAreaMeasure%sMeasureUnitCode text,LatitudeMeasure numeric,LongitudeMeasure numeric,SourceMapScaleNumeric numeric,HorizontalAccuracyMeasure%sMeasureValue text,HorizontalAccuracyMeasure%sMeasureUnitCode text,HorizontalCollectionMethodName text,HorizontalCoordinateReferenceSystemDatumName text,VerticalMeasure%sMeasureValue numeric,VerticalMeasure%sMeasureUnitCode text,VerticalAccuracyMeasure%sMeasureValue numeric,VerticalAccuracyMeasure%sMeasureUnitCode text,VerticalCollectionMethodName text,VerticalCoordinateReferenceSystemDatumName text,CountryCode text,StateCode numeric,CountyCode numeric,AquiferName text,FormationTypeText text,AquiferTypeName text,ConstructionDateText text,WellDepthMeasure%sMeasureValue numeric,WellDepthMeasure%sMeasureUnitCode text,WellHoleDepthMeasure%sMeasureValue numeric, PRIMARY KEY (SITE_ID))""" % (schema_name,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator,column_separator)

    W2B_table = """CREATE TABLE %s.W2B(SNO integer,NHD_LAKE_ID text,BB_ID text,PRIMARY KEY (BB_ID , NHD_LAKE_ID))""" % schema_name

    W2S_table = """CREATE TABLE %s.W2S(SNO integer,NHD_LAKE_ID text,GNIS_LAKE_NAME text,SITE_ID text,MonitoringLocationName text,IsInsideLake BOOLEAN,DistToShore%sm numeric,PRIMARY KEY (SITE_ID , NHD_LAKE_ID))""" % (schema_name, column_separator)

    WATERBODIES_table = """CREATE TABLE %s.WATERBODIES(SNO integer,NHD_LAKE_ID text,GNIS_NAME text,GNIS_ID numeric,AREA%ssqkm numeric,ELEVATION%sfeet numeric,FTYPE integer,FCODE integer,FDATE date,SHAPE_LENG%sdecimaldegrees numeric,SHAPE_AREA%ssqdecimaldegrees numeric,PRIMARY KEY (NHD_LAKE_ID))""" % (schema_name, column_separator, column_separator, column_separator, column_separator)
    
    print "Creating b2s\n"
    cursor.execute(B2S_table)
    print "Creating coundingbox\n"
    cursor.execute(BOUNDINGBOX_table)
    print "Creating sites\n"
    cursor.execute(SITES_table)
    print "Creating w2b\n"
    cursor.execute(W2B_table)
    print "Creating w2s\n"
    cursor.execute(W2S_table)
    print "Creating waterbodies\n"
    cursor.execute(WATERBODIES_table)
    #conn.commit()

def loadCsv(fileObject, tableName):
    sql = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """
    cursor.copy_expert(sql % tableName, fileObject)
    #conn.commit()

def loadFiles(schema):
    for t in tableList:
        print "%s :\n"%(t)
        tableName = schema + "." + t
        csvFile = schema + fileSeparator + t + ".csv"
        fileObject = open(csvFile)
        loadCsv(fileObject, tableName)


try:
    createSchemas()
    print "Schemas created..."
    for s in schemaList:
        print "create tables for %s :"%(s)
        createTables(s)
        print "Tables created for schema %s"%(s)

    for s in schemaList:
        print "load data for %s :"%(s)
        loadFiles(s)
        print "data loaded for schema %s"%(s)
    print "Data Loaded!"
    conn.commit()
finally:
    conn.close()
   
