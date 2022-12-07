from django import forms

HANDLE_OPTIONS = (
    ("O", "Opgeruimd"),
    ("N", "Kan ik niet oplossen"),
    ("N", "Kan het niet vinden"),
)


class HandleForm(forms.Form):

    handle_choice = forms.ChoiceField(
        label="Hoe wil je de melding afhandelen?",
        widget=forms.RadioSelect(),
        choices=[[x, HANDLE_OPTIONS[x][1]] for x in range(len(HANDLE_OPTIONS))],
    )
