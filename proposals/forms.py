from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Proposal, TONE_CHOICES, PLATFORM_CHOICES, Client
from .models import FreelancerDirectoryProfile
from .models import ProgressReport
import datetime



# proposals/forms.py

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "portfolio", "skills", "preferred_tone"]

class ProposalForm(forms.ModelForm):
    job_url = forms.URLField(required=False, label="Job URL (Upwork/Fiverr/LinkedIn)")

    class Meta:
        model = Proposal
        fields = ("job_title","platform", "tone", "job_description")
        widgets = {
            "platform": forms.Select(choices=PLATFORM_CHOICES),
            "tone": forms.Select(choices=TONE_CHOICES),
            "job_description": forms.Textarea(attrs={"rows": 8}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "notes"]

class FreelancerDirectoryProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerDirectoryProfile
        exclude = ["user"]

    profession = forms.ChoiceField(
        choices=FreelancerDirectoryProfile.PROFESSION_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )

class AdminAdjustCreditsForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    delta = forms.IntegerField(help_text="Positive to add, negative to deduct", widget=forms.NumberInput(attrs={"class": "form-control"}))
    reason = forms.ChoiceField(
        choices=[("manual_topup", "Manual Top-up"), ("admin_adjust", "Admin Adjust"), ("refund", "Refund")],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    method = forms.ChoiceField(
        choices=[("cash", "Cash"), ("upi", "UPI"), ("bank", "Bank Transfer"), ("other", "Other / NA")],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    note = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

class CreditRequestForm(forms.Form):
    amount = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g., 100"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Any note for our team (optional)"}))


class ProgressReportRequestForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ["month", "year", "platform", "status_filter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate year dynamically
        current_year = datetime.date.today().year
        self.fields["year"].widget = forms.Select(choices=[(y, y) for y in range(current_year-2, current_year+1)])
        self.fields["month"].widget = forms.Select(choices=[(i, datetime.date(2000, i, 1).strftime("%B")) for i in range(1, 13)])

        self.fields["platform"].widget.attrs.update({"placeholder": "Upwork, Fiverr, LinkedIn, or leave blank for all"})
        self.fields["status_filter"].widget.attrs.update({"placeholder": "Won, Lost, or leave blank for all"})
