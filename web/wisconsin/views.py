# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from wisconsin.models import Waterbodies
from wisconsin.models import W2S

# Create your views here.
def index(request):
	#lakes = Waterbodies.objects.filter()
	return render(request, 'wisconsin/index.html', {
		#'lakes' : lakes,
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

