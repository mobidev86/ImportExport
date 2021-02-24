from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file', required=False)
    url = forms.URLField(label='Enter url of G-sheet', required=False)

    def clean(self):
        file = self.cleaned_data.get('file')
        url = self.cleaned_data.get('url')

        if file:
            if not file.name.endswith('.csv') and not file.name.endswith('.xlsx'):
                raise forms.ValidationError("Only CSV and XLSX files are accepted.")

        if url:
            if url.find('spreadsheets') == -1:
                raise forms.ValidationError("Please provide Google sheet URL.")
        if not url and not file:
            raise forms.ValidationError("You have to Upload File or Enter URL. ")


