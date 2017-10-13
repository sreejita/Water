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