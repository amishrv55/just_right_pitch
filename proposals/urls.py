# proposals/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from proposals import views as pviews
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


urlpatterns = [
    path("", lambda request: redirect("dashboard"), name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path("proposals/new/", views.create_proposal, name="create_proposal"),  # NEW
    path("proposals/<int:proposal_id>/", views.proposal_detail, name="proposal_detail"),
    path("proposals/<int:proposal_id>/download/", views.download_proposal_pdf, name="download_proposal_pdf"),
    path('proposal/<int:proposal_id>/delete/', views.delete_proposal, name='delete_proposal'),
    path("proposal/<int:proposal_id>/update_tracking/", views.update_proposal_tracking, name="update_proposal_tracking"),
    path('analytics/', views.analytics, name='analytics'),
    path('contract/view/<int:proposal_id>/', views.view_contract, name='view_contract'),
    path("payment/add/<int:proposal_id>/", views.add_payment, name="add_payment"),
    path("proposal/<int:proposal_id>/update-status/", views.update_proposal_status, name="update_proposal_status"),
    path("proposal/<int:proposal_id>/update-confidence/", views.update_proposal_confidence, name="update_proposal_confidence"),
    path('payments/track/<int:proposal_id>/', views.track_payments, name='track_payments'),
    path('contract/form/<int:proposal_id>/', views.contract_form, name='contract_form'),
    path('contract/generate/', views.generate_contract_pdf_simple, name='generate_contract_pdf_simple'),
    # proposals/urls.py
    path("proposal/<int:proposal_id>/add-client/", views.add_client_to_proposal, name="add_client_to_proposal"),
    path("clients/", views.my_clients, name="my_clients"),
    path("client/<int:client_id>/edit/", views.edit_client, name="edit_client"),
    path("client/<int:client_id>/delete/", views.delete_client, name="delete_client"), 
    # Exports
    path("export/proposals/csv/", views.export_proposals_csv, name="export_proposals_csv"),
    path("export/proposals/excel/", views.export_proposals_excel, name="export_proposals_excel"),
    path("export/clients/csv/", views.export_clients_csv, name="export_clients_csv"),
    path("export/clients/excel/", views.export_clients_excel, name="export_clients_excel"),
    path("export/payments/csv/", views.export_payments_csv, name="export_payments_csv"),
    path("export/payments/excel/", views.export_payments_excel, name="export_payments_excel"),
    path("export/all-data/", views.export_all_data_zip, name="export_all_data_zip"),
    path("freelancers/", views.freelancer_list, name="freelancer_list"),
    path("freelancers/<int:pk>/", views.freelancer_detail, name="freelancer_detail"),
    path("freelancer/profile/edit/", views.edit_freelancer_profile, name="edit_freelancer_profile"),
    path("invoice/<int:proposal_id>/", views.generate_invoice_pdf, name="generate_invoice_pdf"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("billing/", pviews.credits_overview, name="credits_overview"),
    path("billing/request/", pviews.credits_request, name="credits_request"),
    path("billing/admin/adjust/", pviews.credits_admin_adjust, name="credits_admin_adjust"),
    path("requests/", views.credit_requests_list, name="credit_requests_list"),
    path("requests/<int:request_id>/<str:action>/", views.credit_request_action, name="credit_request_action"),
    path("proposals/<int:proposal_id>/add-conversation/", views.add_conversation, name="add_conversation"),
    path("proposals/<int:proposal_id>/track-conversations/", views.track_conversations, name="track_conversations"),
    path("proposals/<int:proposal_id>/conversations/pdf/", views.download_conversations_pdf, name="download_conversations_pdf"),
    path("request-progress-report/", views.request_progress_report, name="request_progress_report"),
    path("progress-requests/", views.progress_report_requests_list, name="progress_report_requests_list"),
    path("progress-requests/<int:report_id>/generate/", views.admin_generate_progress_report, name="admin_generate_progress_report"),
    path("progress-requests/<int:report_id>/reject/", views.admin_reject_progress_report, name="admin_reject_progress_report"),
    path("my-requests/", views.my_requests, name="my_requests"),
    path("admin-workspace/", views.admin_workspace, name="admin_workspace"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)