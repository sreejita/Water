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
	  query_options = forms.ChoiceField(choices=WATER_QUERY_OPTIONS, widget=forms.Select(
	  				attrs={'class':'form-control',
	  						'id' : 'waterbodies-dropdown',
	  				}))
	  lake_id = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter lake id...',
			}
		), label='', required=False,)
	  lake_name = forms.CharField(widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'Enter lake name...',
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
				'placeholder' : 'Enter area...',
			}
		), label='', required=False,)

