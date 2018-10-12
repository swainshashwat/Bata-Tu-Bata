from django import forms
from django.test import TestCase
from ..templatetags.form_tags import field_type, input_class

class ExampleForm(forms.Form):
    '''
    Sample Form Class.
    '''
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ('name', 'password')

class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        '''
        Checking if the type of Field Types are correct.
        '''
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))

class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        '''
        Testing unbounded Form data.
        '''
        form = ExampleForm() # unbound form
        self.assertEquals('form-control ', input_class(form['name']))

    def test_valid_bound_field(self):
        '''
        Test if the form returns 'is-valid' as True for a valid form.
        '''
        form = ExampleForm({'name':'john', 'password':'123'}) # bound form (field + data)
        self.assertEquals('form-control ', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))

    def test_invalid_bound_field(self):
        form = ExampleForm({'name':'', 'password':'123'}) # bound form (field + data)
        self.assertEquals('form-control is-invalid', input_class(form['name']))
