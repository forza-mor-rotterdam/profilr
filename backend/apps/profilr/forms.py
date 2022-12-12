from django import forms

HANDLE_OPTIONS = (
    ("O", "Opgeruimd"),
    ("N", "Kan ik niet oplossen"),
    ("N", "Kan het niet vinden"),
)


class RadioSelect(forms.RadioSelect):
    template_name = "widgets/radio.html"
    option_template_name = "widgets/radio_option.html"


class HandleForm(forms.Form):

    handle_choice = forms.ChoiceField(
        label="Hoe wil je de melding afhandelen?",
        widget=RadioSelect(attrs={"class": "form-check-input"}),
        choices=[[x, HANDLE_OPTIONS[x][1]] for x in range(len(HANDLE_OPTIONS))],
    )
