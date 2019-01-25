from django import forms

from applications.firewalls.models import firewalls


class FirewallsForm(forms.ModelForm):

	class Meta:
		model = firewalls

		fields = [
			'geom',
			'type',
			'descript',
		]
		labels = {
			'geom': 'Geometry',
			'type': 'Type of Firewall',
			'descript': 'Description',
		}