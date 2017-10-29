from django import forms

class LakeToSiteForm(forms.Form):
	lake_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter lake id...',
			}
		), label='')


class SiteToLakeForm(forms.Form):
	site_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter site id...',
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
				'placeholder' : 'Enter Lake ID...',
			}
		), label='', required=False,)
	  lake_name = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Lake Name...',
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
				'placeholder' : 'Enter Area...',
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
				'placeholder' : 'Enter Site ID...',
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
				'placeholder' : 'Enter Organization ID...',
			}
		), label='', required=False,)
	  monitoring_location = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter Monitoring Location...',
			}
		), label='', required=False,)
	  huc = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter HUC...',
			}
		), label='', required=False,)


class BoundingBoxForm(forms.Form):
	  east = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter East Longitude...',
			}
		), label='', )
	  west = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter West Longitude...',
			}
		), label='', )
	  north = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter North Latitude...',
			}
		), label='',)
	  south = forms.DecimalField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter South Latitude...',
			}
		), label='', )

