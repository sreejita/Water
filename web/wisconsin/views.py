# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from wisconsin.models import Waterbodies
from wisconsin.models import W2S

from wisconsin.forms import LakeToSiteForm
from wisconsin.forms import SiteToLakeForm
from wisconsin.forms import WaterbodiesForm

# Create your views here.
def index(request):
	#lakes = Waterbodies.objects.filter()
	form = LakeToSiteForm()
	forms2l = SiteToLakeForm()
	form_waterbodies = WaterbodiesForm()
	return render(request, 'wisconsin/index.html', {
		#'lakes' : lakes,
		'form' : form,
		'forms2l' : forms2l,
		'form_waterbodies' : form_waterbodies,
	})


def lake_detail(request, id):
	try:
		lakes = Waterbodies.objects.filter(nhd_lake_id=id)
		lake = lakes[0]
	except Waterbodies.DoesNotExist:
		raise Http404('This lake does not exist')
	return render(request, 'wisconsin/lake_detail.html', {
		'lake': lake,
	})

def site_detail(request, id):
	sites = W2S.objects.filter(nhd_lake_id=id)
	lake_name = ''
	if (len(sites) > 0):
		site = sites[0]
		lake_name = site.gnis_lake_name
	return render(request, 'wisconsin/site_detail.html', {
		'sites' : sites,
		'nhd_lake_id' : id,
		'lake_name' : lake_name,
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
		return render(request, 'wisconsin/index.html', {
			'form' : form,
			'forms2l' : forms2l,
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
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
		})

	return render(request, 'wisconsin/site_to_lake.html', {
		'lakes' : lakes,
		'site_id' : id,
		#'lake_name' : lake_name,
	})

def waterbodies(request):
	lakes = ''
	if request.method == 'POST':
		form_waterbodies = WaterbodiesForm(request.POST)
		if form_waterbodies.is_valid():
			cd = form_waterbodies.cleaned_data
			lake_id = cd['lake_id']
			lake_name = cd['lake_name']
			area_cmp = cd['area_cmp']
			area = cd['area']
			if(lake_id) :
				lakes = Waterbodies.objects.filter(nhd_lake_id=lake_id)
			elif(lake_name) :
				lakes = Waterbodies.objects.filter(gnis_name=lake_name)
			elif(area) :
				kwargs = {
				    '{0}__{1}'.format('area_sqkm', area_cmp): area,
				}
				lakes = Waterbodies.objects.filter(**kwargs)

			#if (len(sites) > 0):
			#	site = sites[0]
			#	lake_name = site.gnis_lake_name

	else:
		form = LakeToSiteForm()
		forms2l = SiteToLakeForm()
		form_waterbodies = WaterbodiesForm()
		return render(request, 'wisconsin/index.html', {
			#'lakes' : lakes,
			'form' : form,
			'forms2l' : forms2l,
			'form_waterbodies' : form_waterbodies,
		})

	return render(request, 'wisconsin/waterbodies.html', {
		'lakes' : lakes,
		#'site_id' : id,
		#'lake_name' : lake_name,
	})


