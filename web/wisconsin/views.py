# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

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
	
	return render(request, 'wisconsin/site_detail.html', {
		'sites' : sites,
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
		'sites' : sites,
		'bb_id' : id,
	})

def lake_to_site(request):
	lake_name = ''
	id = ''
	sites = ''
	if request.method == 'POST':
		form = LakeToSiteForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			id = cd['lake_id']
			sites = W2S.objects.filter(nhd_lake_id=id)

			if (len(sites) > 0):
				site = sites[0]
				lake_name = site.gnis_lake_name

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		return render(request, 'wisconsin/index.html', {
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
		})

	return render(request, 'wisconsin/lake_to_site.html', {
		'sites' : sites,
		'nhd_lake_id' : id,
		'lake_name' : lake_name,
	})

def site_to_lake(request):
	lakes = ''
	id = ''
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
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
		})

	return render(request, 'wisconsin/site_to_lake.html', {
		'lakes' : lakes,
		'site_id' : id,
		#'lake_name' : lake_name,
	})

def waterbodies(request):
	lakes = ''
	#lake_name = ''
	if request.method == 'POST':
		form_waterbodies = WaterbodiesForm(request.POST)
		if form_waterbodies.is_valid():
			cd = form_waterbodies.cleaned_data
			lake_id = cd['lake_id']
			lake_name = cd['lake_name']
			area_cmp = cd['area_cmp']
			area = cd['area']
			fcode = cd['fcode']
			
			kwargs = { }
			if(lake_id) :
				kwargs['nhd_lake_id'] = lake_id
			if(lake_name) :
				kwargs['gnis_name'] = lake_name
			if(area) :
				kwargs['{0}__{1}'.format('area_sqkm', area_cmp)] = area
			if(fcode) :
				kwargs['fcode'] = fcode
			
			lakes = Waterbodies.objects.filter(**kwargs)

			#if (len(sites) > 0):
			#	site = sites[0]
			#	lake_name = site.gnis_lake_name

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

	return render(request, 'wisconsin/waterbodies.html', {
		'lakes' : lakes,
		#'site_id' : id,
		#'lake_name' : lake_name,
	})

def sites(request):
	sites = ''
	if request.method == 'POST':
		form_sites = SitesForm(request.POST)
		if form_sites.is_valid():
			cd = form_sites.cleaned_data
			site_id = cd['site_id']
			org_name = cd['org_name']
			org_id = cd['org_id']
			#monitoring_location = cd['monitoring_location']
			huc = cd['huc']
			kwargs = { }
			if(site_id) :
				kwargs['site_id'] = site_id
			if(org_name) :
				kwargs['organizationformalname'] = org_name
			if(org_id) :
				kwargs['organizationidentifier'] = org_id
			'''if(monitoring_location) :
				kwargs['monitoringlocationname'] = monitoring_location'''
			if(huc) :
				kwargs['huceightdigitcode'] = huc
			sites = Sites.objects.filter(**kwargs)

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		form_sites = SitesForm()
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
			'form_sites' : form_sites,
		})

	return render(request, 'wisconsin/sites.html', {
		'sites' : sites,
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


