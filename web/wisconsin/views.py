# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import csv

from wisconsin.models import Waterbodies
from wisconsin.models import W2S
from wisconsin.models import Sites
from wisconsin.models import Boundingbox
from wisconsin.models import W2B
from wisconsin.models import B2S

from wisconsin.forms import LakeToSiteForm
from wisconsin.forms import SiteToLakeForm
from wisconsin.forms import WaterbodiesForm
from wisconsin.forms import SitesForm
from wisconsin.forms import BoundingBoxForm
import decimal

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
# Create your views here.
def index(request):
	#lakes = Waterbodies.objects.filter()
	form = LakeToSiteForm()
	forms2l = SiteToLakeForm()
	form_waterbodies = WaterbodiesForm()
	form_sites = SitesForm()
	form_bb= BoundingBoxForm()
	return render(request, 'wisconsin/index.html', {
		#'lakes' : lakes,
		'form' : form,
		'forms2l' : forms2l,
		'form_waterbodies' : form_waterbodies,
		'form_sites' : form_sites,
		'form_bb' : form_bb,
	})


'''def lake_detail(request, id):
	try:
		lakes = Waterbodies.objects.filter(nhd_lake_id=id)
		lake = lakes[0]
	except Waterbodies.DoesNotExist:
		raise Http404('This lake does not exist')
	return render(request, 'wisconsin/lake_detail.html', {
		'lake': lake,
	}) '''

def lake_detail(request, id):
	lakes = Waterbodies.objects.filter(nhd_lake_id=id)
	
	return render(request, 'wisconsin/lake_detail.html', {
		'lakes' : lakes,
	})

def site_detail(request, id):
	sites = Sites.objects.filter(site_id=id)
	geo = {}
	geo["lat"] = str(sites[0].latitudemeasure);
	geo["lng"] = str(sites[0].longitudemeasure);
	return render(request, 'wisconsin/site_detail.html', {
		'sites' : sites,
		'geo' : json.dumps(geo),
	})


def bb_detail(request, id):
	lake_id = W2B.objects.filter(bb_id=id)[0]
	site_ids = B2S.objects.filter(bb_id=id)
	sites = []
	lake = Waterbodies.objects.filter(nhd_lake_id=lake_id.nhd_lake_id)
	if(site_ids):
		for sid in site_ids:
			site = Sites.objects.filter(site_id=sid.site_id)[0]
			sites.append(site)
			
	return render(request, 'wisconsin/bb_detail.html', {
		#'lake_id' : lake_id.nhd_lake_id,
		'lake' : lake,
		'lake_id' : lake_id.nhd_lake_id,
		'sites' : sites,
		'bb_id' : id,
	})

def lake_to_site_download(request, id):
	sites = ''

	sites = W2S.objects.filter(nhd_lake_id=id)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="sitesForLake_' + id + '.csv"'
	writer = csv.writer(response)
	writer.writerow(["Site ID", "Monitoring Location", "Is Inside Lake", "Distance from shore(in m.)"])
	for s in sites:
		writer.writerow([s.site_id, s.monitoringlocationname, s.isinsidelake, s.disttoshore_m])
	return response


def lake_to_site(request, id):
	lake_name = ''
	sites = ''
	
	sites = W2S.objects.filter(nhd_lake_id=id)
	geoArr = []
	if (len(sites) > 0):
		site = sites[0]
		lake_name = site.gnis_lake_name
		for s in sites:
			site = Sites.objects.filter(site_id=s.site_id)[0];
			geo = {}
			geo["lat"] = str(site.latitudemeasure)
			geo["lng"] = str(site.longitudemeasure)
			geo['title'] = site.site_id
			geo['monitor_loc'] = site.monitoringlocationname
			geo['inside_lake'] = s.isinsidelake
			geo['dist_shore'] = str(round(s.disttoshore_m , 5))
			geoArr.append(geo);

	return render(request, 'wisconsin/lake_to_site.html', {
		'sites' : sites,
		'nhd_lake_id' : id,
		'lake_name' : lake_name,
		'geo_arr' : json.dumps(geoArr),
	})

'''def lake_to_site(request):
	lake_name = ''
	id = ''
	sites = ''
	if request.method == 'POST':
		form = LakeToSiteForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			id = cd['lake_id']
			sites = W2S.objects.filter(nhd_lake_id=id)
			geoArr = []
			if (len(sites) > 0):
				site = sites[0]
				lake_name = site.gnis_lake_name
				for s in sites:
					site = Sites.objects.filter(site_id=s.site_id)[0];
					geo = {}
					geo["lat"] = str(site.latitudemeasure)
					geo["lng"] = str(site.longitudemeasure)
					geo['title'] = site.site_id
					geoArr.append(geo);

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		form_bb = BoundingBoxForm()
		return render(request, 'wisconsin/index.html', {
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
			'form_bb' : form_bb,
		})

	return render(request, 'wisconsin/lake_to_site.html', {
		'sites' : sites,
		'nhd_lake_id' : id,
		'lake_name' : lake_name,
		'geo_arr' : json.dumps(geoArr),
	})
'''
def site_to_lake(request):
	lakes = ''
	id = ''
	writer = ''
	if request.method == 'POST':
		forms2l = SiteToLakeForm(request.POST)
		if forms2l.is_valid():
			cd = forms2l.cleaned_data
			id = cd['site_id']
			lakes = W2S.objects.filter(site_id=id)

			#if (len(sites) > 0):
			#	site = sites[0]
			#	lake_name = site.gnis_lake_name

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		form_bb= BoundingBoxForm()
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
			'form_bb' : form_bb,
		})

	return render(request, 'wisconsin/site_to_lake.html', {
		'lakes' : lakes,
		'site_id' : id,
		#'lake_name' : lake_name,
	})

def waterbodies(request, page):
	lakes = ''
	lake_list = ''
	get_params = '?'
	pg_range = ''
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="waterbodies.csv"'
	writer = csv.writer(response)
	#lake_name = ''
	if request.method == 'GET':
		print "IN view"
		form_waterbodies = WaterbodiesForm(request.GET)
		if form_waterbodies.is_valid():
			cd = form_waterbodies.cleaned_data
			lake_id = request.GET.get('lake_id', '')
			lake_name = request.GET.get('lake_name', '')
			area_cmp = request.GET.get('area_cmp')
			area = request.GET.get('area')
			fcode = request.GET.get('fcode')
			
			kwargs = { }
			if(lake_id) :
				kwargs['nhd_lake_id'] = lake_id
				get_params += 'lake_id=' + lake_id + '&'
			if(lake_name) :
				kwargs['{0}__{1}'.format('gnis_name', 'icontains')] = lake_name
				get_params += 'lake_name=' + lake_name + '&'
			if(area_cmp) :
				get_params += 'area_cmp=' + area_cmp + '&'
			if(area) :
				kwargs['{0}__{1}'.format('area_sqkm', area_cmp)] = area
				get_params += 'area=' + area + '&'
			if(fcode) :
				kwargs['fcode'] = fcode
				get_params += 'fcode=' + fcode + '&'
			
			lake_list = Waterbodies.objects.filter(**kwargs)
			if(page == "0"):
				print "Download"
				lakes = lake_list
				writer.writerow(["ID", "GNIS Name", "GNIS_ID", "Area(sq. km.)" , "Elevation(ft.)", "FType", "FCode", "FDate", "Shape Length(dec. deg.)", "Shape Area(sq. dec. deg."])
				for l in lakes:
					writer.writerow([l.nhd_lake_id, l.gnis_name, l.gnis_id, l.area_sqkm, l.elevation_feet, l.ftype, l.fcode, l.fdate, l.shape_leng_decimaldegrees, l.shape_area_sqdecimaldegrees])
				return response
			else: 
				print "table"
				paginator = Paginator(lake_list, 20)

				try:
					lakes = paginator.page(page)
				except PageNotAnInteger:
					lakes = paginator.page(1)
				except EmptyPage:
					lakes = paginator.page(paginator.num_pages)

	'''else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		form_bb = BoundingBoxForm()
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
			'form_bb' : form_bb,
		})'''

	return render(request, 'wisconsin/waterbodies.html', {
		'lakes' : lakes,
		'params' : get_params,
		#'range' : pg_range,
		#'site_id' : id,
		#'lake_name' : lake_name,
	})

def sites(request, page):
	sites = ''
	site_list = ''
	get_params = '?'
	pg_range = ''
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="sites.csv"'
	writer = csv.writer(response)
	if request.method == 'GET':
		form_sites = SitesForm(request.GET)
		if form_sites.is_valid():
			cd = form_sites.cleaned_data
			site_id = request.GET.get('site_id', '')
			org_name = request.GET.get('org_name', '')
			org_id = request.GET.get('org_id', '')
			#monitoring_location = cd['monitoring_location']
			huc = request.GET.get('huc', '')
			kwargs = { }
			
			if(site_id) :
				kwargs['site_id'] = site_id
				get_params += 'site_id=' + site_id + '&'
			if(org_name) :
				kwargs['{0}__{1}'.format('organizationformalname', 'icontains')] = org_name
				get_params += 'org_name=' + org_name + '&'
			if(org_id) :
				kwargs['organizationidentifier'] = org_id
				get_params += 'org_id=' + org_id + '&'
			if(huc) :
				kwargs['huceightdigitcode'] = huc
				get_params += 'huc=' + huc + '&'
			site_list = Sites.objects.filter(**kwargs)

			if(page == "0"):
				print "Download Sites"
				sites = site_list
				writer.writerow(["SITE_ID", "OrganizationFormalName", "OrganizationIdentifier", "MonitoringLocationName", "MonitoringLocationTypeName", "MonitoringLocationDescriptionText",	"HUCEightDigitCode", "DrainageAreaMeasure/MeasureValue", "DrainageAreaMeasure/MeasureUnitCode", "ContributingDrainageAreaMeasure/MeasureValue", "ContributingDrainageAreaMeasure/MeasureUnitCode", "LatitudeMeasure", "LongitudeMeasure", "SourceMapScaleNumeric", "HorizontalAccuracyMeasure/MeasureValue", "HorizontalAccuracyMeasure/MeasureUnitCode", "HorizontalCollectionMethodName", "HorizontalCoordinateReferenceSystemDatumName", "VerticalMeasure/MeasureValue", "VerticalMeasure/MeasureUnitCode", "VerticalAccuracyMeasure/MeasureValue", "VerticalAccuracyMeasure/MeasureUnitCode", "VerticalCollectionMethodName", "VerticalCoordinateReferenceSystemDatumName", "CountryCode", "StateCode", "CountyCode", "AquiferName", "FormationTypeText", "AquiferTypeName", "ConstructionDateText", "WellDepthMeasure/MeasureValue", "WellDepthMeasure/MeasureUnitCode", "WellHoleDepthMeasure/MeasureValue"])
				for s in sites:
					writer.writerow([s.site_id, s.organizationformalname, s.organizationidentifier, s.monitoringlocationname, s.monitoringlocationtypename, s.monitoringlocationdescriptiontext, s.huceightdigitcode, s.drainageareameasure_measurevalue, s.drainageareameasure_measureunitcode, s.contributingdrainageareameasure_measurevalue, s.contributingdrainageareameasure_measureunitcode, s.latitudemeasure, s.longitudemeasure, s.sourcemapscalenumeric, s.horizontalaccuracymeasure_measurevalue, s.horizontalaccuracymeasure_measureunitcode, s.horizontalcollectionmethodname, s.horizontalcoordinatereferencesystemdatumname, s.verticalmeasure_measurevalue, s.verticalmeasure_measureunitcode, s.verticalaccuracymeasure_measurevalue, s.verticalaccuracymeasure_measureunitcode, s.verticalcollectionmethodname, s.verticalcoordinatereferencesystemdatumname, s.countrycode, s.statecode, s.countycode, s.aquifername, s.formationtypetext, s.aquifertypename, s.constructiondatetext, s.welldepthmeasure_measurevalue, s.welldepthmeasure_measureunitcode, s.wellholedepthmeasure_measurevalue])
				return response
			else:
				paginator = Paginator(site_list, 20)
				try:
					sites = paginator.page(page)
				except PageNotAnInteger:
					sites = paginator.page(1)
				except EmptyPage:
					sites = paginator.page(paginator.num_pages)

	return render(request, 'wisconsin/sites.html', {
		'sites' : sites,
		'params' : get_params,
		#'site_id' : id,
		#'lake_name' : lake_name,
	})


def bb(request):
	bbs = ''
	if request.method == 'POST':
		form_bb = BoundingBoxForm(request.POST)
		if form_bb.is_valid():
			cd = form_bb.cleaned_data
			n = cd['north']
			s = cd['south']
			e = cd['east']
			w = cd['west']
			
			bbs = Boundingbox.objects.filter(south__lte=n, north__gte=s, east__lte=e, west__gte=w)

			#for bb in bbs:
				#bb.lake_id = W2B.objects.filter(bb_id=bb.bb_id)[0].nhd_lake_id

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		form_bb = BoundingBoxForm()
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
			'form_bb' : form_bb,
		})

	return render(request, 'wisconsin/bb.html', {
		'bbs' : bbs,
		#'site_id' : id,
		#'lake_name' : lake_name,
	})


