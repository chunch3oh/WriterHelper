from django import forms

class InputForm(forms.Form):
    field1 = forms.CharField(label='文風',max_length=200)
    field2 = forms.CharField(label='時代',max_length=200)
    field3 = forms.CharField(label='場景',max_length=200)
    field4 = forms.CharField(label='其他你認為文章內要出現的資訊',max_length=200)

