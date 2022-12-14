from django import forms

HANDLED_OPTIONS = (
    (
        "O",
        "Opgeruimd",
        "De gemeente heeft deze melding in behandeling genomen en gaat ermee aan de slag. De melding is daarom afgesloten.",
    ),
    (
        "N",
        "Niets aangetroffen",
        "In uw melding heeft u een locatie genoemd. Op deze locatie hebben wij echter niets aangetroffen. We sluiten daarom uw meldin.g",
    ),
    (
        "N",
        "De locatie is niet bereikbaar",
        "In uw melding heeft u een locatie genoemd. We kunnen deze locatie echter niet bereiken. We sluiten daarom uw melding.",
    ),
    ("N", "De melding is niet voor mij", ""),
    (
        "N",
        "De gemeente gaat hier niet over",
        "Helaas valt uw melding niet onder verantwoordelijkheid van de gemeente. We sluiten daarom uw melding.",
    ),
)


class RadioSelect(forms.RadioSelect):
    template_name = "widgets/radio.html"
    option_template_name = "widgets/radio_option.html"


class HandleForm(forms.Form):

    handle_choice = forms.ChoiceField(
        label="Waarom kan de melding niet worden opgelost?",
        widget=RadioSelect(attrs={"class": "form-check-input"}),
        choices=[[x, HANDLED_OPTIONS[x][1]] for x in range(len(HANDLED_OPTIONS))],
        initial=0,
    )
    external_text = forms.CharField(
        label="Bericht voor de melder",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "message",
                "rows": "4",
                "data-incidentHandleForm-target": "externalText",
            }
        ),
        required=False,
    )
    internal_text = forms.CharField(
        label="Interne informatie",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "data-testid": "information",
                "rows": "4",
                "data-incidentHandleForm-target": "internalText",
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        handled_type = kwargs.pop("handled_type", None)
        super().__init__(*args, **kwargs)
        if handled_type == "handled":
            self.fields["handle_choice"].widget = forms.HiddenInput()
            self.fields["external_text"].initial = HANDLED_OPTIONS[0][2]
        else:
            self.fields["handle_choice"].choices = [
                [x, HANDLED_OPTIONS[x][1]]
                for x in range(len(HANDLED_OPTIONS))
                if HANDLED_OPTIONS[x][0] == "N"
            ]

        if self.data.get("handle_choice", False) == "3":
            self.fields["external_text"].widget = forms.HiddenInput()
            self.fields["external_text"].required = False
