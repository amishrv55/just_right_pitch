# proposals/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import os

def validate_image_size(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Image file too large (max 2 MB).")

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

TONE_CHOICES = [
    ("Formal", "Formal"),
    ("Friendly", "Friendly"),
    ("Bold", "Bold"),
]

PLATFORM_CHOICES = [
    ("Upwork", "Upwork"),
    ("Fiverr", "Fiverr"),
    ("LinkedIn", "LinkedIn"),
    ("Generic", "Generic"),
]

class Proposal(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Sent", "Sent"),
        ("Won", "Won"),
        ("Lost", "Lost"),
    ]
    CONFIDENCE_CHOICES = [
        ("High", "High Confidence"),
        ("Medium", "Medium Confidence"),
        ("Low", "Low Confidence"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200, default="Untitled Proposal")
    job_description = models.TextField()
    platform = models.CharField(max_length=50)
    tone = models.CharField(max_length=20)
    proposal_text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Draft")
    confidence = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES, default="Medium")
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    last_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.platform} - {self.status}"


class Contract(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name="contract")
    contract_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    signed_by_client = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract for {self.proposal.id}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Received", "Received"),
    ]
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    due_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Proposal {self.proposal.id} - {self.status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ai_credits = models.PositiveIntegerField(default=0)
    full_name = models.CharField(max_length=100, blank=True)
    portfolio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    preferred_tone = models.CharField(
        max_length=20,
        choices=TONE_CHOICES,
        default="Formal"
    )

    def __str__(self):
        return self.full_name or self.user.username

#class Proposal(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    job_description = models.TextField(default = "", blank = True)
#    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
#    tone = models.CharField(max_length=20, choices=TONE_CHOICES)
#    proposal_text = models.TextField(default = "Sorry!something went wrong.")
#    created_at = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return f"Proposal for {self.platform} ({self.created_at:%Y-%m-%d})"


# --- Validator for file size ---
def validate_image_size(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Image file too large (max 2 MB).")

class FreelancerDirectoryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="directory_profile")
    is_visible = models.BooleanField(default=False)  # toggle to appear in directory

    # Basic info
    display_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        upload_to="freelancer_photos/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )
    tagline = models.CharField(max_length=150, blank=True)

    PROFESSION_CHOICES = [
        ("Law", [
            ("corporate_lawyer", "Corporate Lawyer"),
            ("criminal_lawyer", "Criminal Lawyer"),
            ("family_lawyer", "Family Lawyer"),
            ("immigration_lawyer", "Immigration Lawyer"),
            ("intellectual_property_lawyer", "Intellectual Property Lawyer"),
            ("tax_lawyer", "Tax Lawyer"),
        ]),
        ("Tech", [
            ("data_scientist", "Data Scientist"),
            ("machine_learning_engineer", "Machine Learning Engineer"),
            ("mobile_app_developer", "Mobile App Developer"),
            ("software_developer", "Software Developer"),
            ("web_developer", "Web Developer"),
        ]),
        ("Design", [
            ("graphic_designer", "Graphic Designer"),
            ("ux_designer", "UX / UI Designer"),
            ("video_editor", "Video Editor"),
        ]),
        ("Marketing", [
            ("seo_specialist", "SEO Specialist"),
            ("social_media_manager", "Social Media Manager"),
        ]),
        ("Writing", [
            ("content_writer", "Content Writer"),
            ("copywriter", "Copywriter"),
        ]),
        ("Business", [
            ("accountant", "Accountant"),
            ("business_consultant", "Business Consultant"),
        ]),
        ("Education", [
            ("tutor", "Tutor / Educator"),
        ]),
        ("Health & Wellness", [
            ("fitness_trainer", "Fitness Trainer"),
            ("nutritionist", "Nutritionist"),
        ]),
        ("Other", [
            ("other", "Other"),
        ]),
    ]
    profession = models.CharField(max_length=100, choices=PROFESSION_CHOICES, default="other")

    # Professional info
    skills = models.TextField(help_text="Comma-separated list of skills")
    qualifications = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    portfolio_link = models.URLField(blank=True)

    # Experience
    projects_completed = models.PositiveIntegerField(default=0)
    testimonials = models.TextField(blank=True)  # free text or JSON structure for MVP

    # Preferences
    preferred_platforms = models.CharField(max_length=200, blank=True)
    preferred_tone = models.CharField(max_length=50, blank=True)  # reuse your existing tone field

    # Optional meta
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.user.username

    # --- Auto resize/compress on save ---
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save normally first

        if self.profile_photo:
            img_path = os.path.join(settings.MEDIA_ROOT, self.profile_photo.name)
            try:
                img = Image.open(img_path)

                # Resize: max 600x600
                max_size = (600, 600)
                img.thumbnail(max_size)

                # Convert to RGB if image has transparency
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Save compressed JPEG (quality=85)
                img.save(img_path, format="JPEG", quality=85)
            except Exception as e:
                print(f"⚠️ Image processing failed: {e}")


class CreditTransaction(models.Model):
    REASON_CHOICES = [
        ("manual_topup", "Manual Top-up"),
        ("voucher", "Voucher Redeem"),
        ("generation", "AI Generation Charge"),
        ("refund", "Refund"),
        ("admin_adjust", "Admin Adjust"),
    ]
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank", "Bank Transfer"),
        ("other", "Other / NA"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credit_transactions")
    delta = models.IntegerField(help_text="Positive for credit, negative for deduction")
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="other")
    note = models.CharField(max_length=255, blank=True)
    balance_after = models.IntegerField()  # snapshot after this transaction
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="credit_actions",
        help_text="Admin/staff who performed the action; null for system"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        sign = "+" if self.delta >= 0 else ""
        return f"{self.user.username}: {sign}{self.delta} ({self.reason})"


class CreditRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_requested = models.PositiveIntegerField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.amount_requested} credits ({self.status})"


# proposals/models.py
class Conversation(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="conversations")
    sender = models.CharField(max_length=50, choices=[("freelancer", "Freelancer"), ("client", "Client")])
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"Conversation ({self.sender}) - {self.proposal.id}"


class ProgressReport(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending (Awaiting Payment)"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress_reports")
    month = models.PositiveIntegerField()  # 1-12
    year = models.PositiveIntegerField()
    platform = models.CharField(max_length=50, blank=True, help_text="Upwork, Fiverr, LinkedIn, etc.")
    status_filter = models.CharField(max_length=10, blank=True, help_text="Won, Lost, or All")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    token_count = models.PositiveIntegerField(default=0)

    generated_report = models.FileField(upload_to="progress_reports/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True, help_text="Admin notes or comments.")

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} ({self.status})"
