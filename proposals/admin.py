# Register your models here.

# proposals/admin.py
from django.contrib import admin
from .models import Profile, Proposal, Contract, Payment, Client, CreditTransaction, CreditRequest
from django.utils.html import format_html
from .models import ProgressReport



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_tone")

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "tone", "created_at")
    list_filter = ("platform", "tone", "created_at")
    search_fields = ("proposal", "job_desc")

admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(Client)
admin.site.register(CreditTransaction)
admin.site.register(CreditRequest)

@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ("user", "month", "year", "platform", "status_filter", "status", "created_at", "download_link")
    list_filter = ("status", "platform")
    actions = ["generate_selected_reports"]

    def download_link(self, obj):
        if obj.generated_report:
            return format_html('<a href="{}" target="_blank">📄 Download</a>', obj.generated_report.url)
        return "—"
    download_link.short_description = "Report"

    def generate_selected_reports(self, request, queryset):
        for report in queryset:
            report.status = "Processing"
            # 🔑 Here you can fetch proposals + conversations, send to LLM, generate PDF, save it
            # Placeholder: just mark as ready
            report.status = "Ready"
            report.generated_report.name = "progress_reports/sample_report.pdf"
            report.save()
        self.message_user(request, "Selected reports marked as ready.")
    generate_selected_reports.short_description = "Generate Selected Reports"
