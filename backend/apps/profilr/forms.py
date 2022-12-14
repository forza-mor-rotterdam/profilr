from django import forms

HANDLE_OPTIONS = (
    ("O", "Opgeruimd"),
    ("N", "Niets aangetroffen"),
    ("N", "De melding is niet voor mij"),
    ("N", "De gemeente gaat hier niet over"),
)


class RadioSelect(forms.RadioSelect):
    template_name = "widgets/radio.html"
    option_template_name = "widgets/radio_option.html"


class HandleForm(forms.Form):

    handle_choice = forms.ChoiceField(
        label="Waarom kan de melding niet worden opgelost?",
        widget=RadioSelect(attrs={"class": "form-check-input"}),
        choices=[[x, HANDLE_OPTIONS[x][1]] for x in range(len(HANDLE_OPTIONS))],
        initial=0,
    )
    external_text = forms.CharField(
        label="Bericht voor de melder",
        widget=forms.Textarea(
            attrs={"class": "form-control", "data-testid": "message", "rows": "4"}
        ),
        required=False,
    )
    internal_text = forms.CharField(
        label="Interne informatie",
        widget=forms.Textarea(
            attrs={"class": "form-control", "data-testid": "information", "rows": "4"}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        handled_type = kwargs.pop("handled_type", None)
        super().__init__(*args, **kwargs)
        if handled_type == "handled":
            self.fields["handle_choice"].widget = forms.HiddenInput()
        else:
            self.fields["handle_choice"].choices = [
                [x, HANDLE_OPTIONS[x][1]]
                for x in range(len(HANDLE_OPTIONS))
                if HANDLE_OPTIONS[x][0] == "N"
            ]
