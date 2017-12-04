from django import forms

class LakeToSiteForm(forms.Form):
	lake_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'id' : 'l2s_lake_id',
				'class' : 'form-control',
				'placeholder' : 'Enter Lake ID (e.g. 37649095)...',
				'required' : 'true',
			}
		), label='')


class SiteToLakeForm(forms.Form):
	site_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Site ID (e.g. USGS-443840092400301)...',
				'required' : 'true',
			}
		), label='')

WATER_QUERY_OPTIONS = (  
    ('lake_id', 'Lake ID'),
    ('lake_name', 'Lake Name'),
    ('area', 'Area'),
)

AREA_COMPARATORS = (
		('gt', '>'),
    	('lt', '<'),
    	('exact', '='),
    	('gte', '>='),
    	('lte', '<='),
	)

class WaterbodiesForm(forms.Form):
	 
	  lake_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter ID (e.g. 120017988)...',
			}
		), label='', required=False,)
	  lake_name = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Name (e.g. Coon Lake)...',
			}
		), label='', required=False,)
	  area_cmp = forms.ChoiceField(choices=AREA_COMPARATORS, widget=forms.Select(
	  				attrs={'class':'form-control',
	  						'id' : 'waterbodies-area-cmp',
	  						'style' : 'border:none; background-color:#e9ecef;'
	  				}))
	  area = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Area (e.g. 50)...',
			}
		), label='', required=False,)
	  fcode = forms.IntegerField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Feature Code (e.g. 39004)...',
			}
		), label='', required=False,)


class SitesForm(forms.Form):
	 # query_options = forms.ChoiceField(choices=WATER_QUERY_OPTIONS, widget=forms.Select(
	  #				attrs={'class':'form-control',
	  #						'id' : 'waterbodies-dropdown',
	  #				}))
	  site_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Site ID (e.g. USGS-444522093102600)...',
			}
		), required=False,)
	  org_name = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Organization name...',
			}
		), label='', required=False,)
	  org_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Organization ID (e.g. USGS-MN)...',
			}
		), label='', required=False,)
	  huc = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter 8-digit HUC (e.g. 7040001)...',
			}
		), label='', required=False,)


class BoundingBoxForm(forms.Form):
	  east = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter East Longitude (e.g. -91.2427227688)...',
				'required' : 'true',
			}
		), label='', )
	  west = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter West Longitude (e.g. -91.2545777688)...',
				'required' : 'true',
			}
		), label='', )
	  north = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter North Latitude (e.g. 43.4081387326)...',
				'required' : 'true',
			}
		), label='',)
	  south = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter South Latitude (e.g. 43.3915035993)...',
				'required' : 'true',
			}
		), label='', )

