# -*- coding: utf-8 -*-
from django.urls import path

from .views.application import ApplicationListView, ApplicationFilteredListView, ApplicationCreateView, \
    ApplicationDetailView, ApplicationUpdateView, ApplicationDeleteView
from .views.clients import (
    ClientDetailView,
    ClientsFilteredListView,
    ClientSignUpView,
    ClientsListView,
    ClientUpdateView,
)
from .views.flat import (
    FlatCreateView,
    FlatDeleteView,
    FlatDetailView,
    FlatFilteredListView,
    FlatListView,
    FlatUpdateView, SendInvitation,
)
from .views.house import (
    CreateHouseView,
    DeleteHouseView,
    GetHouseInfoView,
    HouseDetailView,
    HouseFilteredListView,
    HouseListView,
    UpdateHouseView, GetSectionInfoView, GetAllFlatsView, GetFlatOwnerView, GetFlatsForMail, GetFlatInfoView,
    GetTariffInfoView, GetServiceInfoView, GetIndicationInfoView,
)
from .views.indications import (
    CounterIndicationsFilteredList,
    CounterIndicationsList,
    CreateIndication,
    CreateIndicationForFlat,
    CreateNewIndication,
    IndicationDetail,
    IndicationsFilteredList,
    IndicationsList,
    UpdateIndication, CounterFilteredList, FlatIndicationsList,
)
from .views.mail import MailListView, MailFilteredListView, MailDeleteView, MailCreateView, MailDetailView, \
    MailDebtorsCreateView
from .views.other import GetRoleView
from .views.paybox import PayboxList, PayboxFilteredList, PayboxDetail, UpdatePaybox, CreatePaybox, CopyPaybox, \
    DeletePaybox
from .views.personal_account import PersonalAccountListView, CreatePersonalAccountView, PersonalAccountFilteredListView, \
    PersonalAccountDetailView, DeletePersonalAccount, UpdatePersonalAccountView
from .views.receipts import ReceiptList, ReceiptsFilteredList, CreateReceipt, UpdateReceipt, CopyReceipt, ReceiptDetail, \
    DeleteReceipt, ReceiptPrint, ReceiptDownloadExcel, ReceiptPrintingSettings, ReceiptPrintingSettingsDelete, \
    ReceiptPrintingSettingsDefault, SendReceiptEmail, GetIndicationsSortedList
from .views.statistic import StatisticView
from .views.system_settings import (
    CopyTariffView,
    CreatePaymentArticleView,
    CreateTariffView,
    DeletePaymentArticleView,
    DeleteTariffView,
    GetMeasureView,
    ListPaymentArticleView,
    PaymentDetailView,
    PersonalDeleteView,
    PersonalDetailView,
    PersonalFilterView,
    PersonalListView,
    PersonalSignUpView,
    PersonalUpdateView,
    RolesListView,
    ServicesView,
    TariffDetail,
    TariffListView,
    UpdatePaymentArticleView,
    UpdateTariffView,
    get_measure_options,
)
from .views.website import (
    AboutUsView,
    ContactSiteView,
    DeleteDocsView,
    DeletePhotoView,
    MainPageView,
    SiteServicesView,
    TariffSiteView,
)
from ..cabinet.views import CabinetStatisticView, Profile, UpdateProfileView, ReceiptListCabinet, FlatReceiptList, \
    FlatReceiptFilteredList, CabinetReceiptsFilteredList, CabinetReceiptDetail, Invoice, ReceiptPDF, ReceiptPDF2, \
    CabinetTariffDetail, CabinetMailboxList, CabinetMailboxFilteredList, CabinetMailboxDetail, CabinetDeleteMailbox, \
    CabinetApplicationList, CabinetCreateApplication

urlpatterns = [
    path("services/", ServicesView.as_view(), name="services"),
    path("tariffs/", TariffListView.as_view(), name="tariffs"),
    path("tariffs/<int:pk>/", TariffDetail.as_view(), name="tariff_detail"),
    path("tariffs/create/", CreateTariffView.as_view(), name="tariff_create"),
    path("tariffs-update/<int:pk>/", UpdateTariffView.as_view(), name="tariffs_update"),
    path("tariffs-copy/<int:pk>/", CopyTariffView.as_view(), name="tariffs_copy"),
    path("tariff-delete/<int:pk>/", DeleteTariffView.as_view(), name="tariff_delete"),
    path("get-measure/<int:pk>/", GetMeasureView.as_view(), name="get_measure"),
    path("get-role/<int:pk>/", GetRoleView.as_view(), name="get_role"),
    path("get_measure/", get_measure_options, name="get_measure_ajax"),
    path("personals/", PersonalListView.as_view(), name="personals"),
    path("personal-add/", PersonalSignUpView.as_view(), name="personal_add"),
    path("personal-detail/<int:pk>/", PersonalDetailView.as_view(), name="personal_detail"),
    path("personal-update/<int:pk>/", PersonalUpdateView.as_view(), name="personal_update"),
    path("personal-delete/<int:pk>/", PersonalDeleteView.as_view(), name="personal_delete"),
    path("personal-filter/", PersonalFilterView.as_view(), name="personal_filter"),
    path("payment/", PaymentDetailView.as_view(), name="payment"),

    path("articel-payments/", ListPaymentArticleView.as_view(), name="article_payments"),
    path("articel-payments/create/", CreatePaymentArticleView.as_view(), name="article_payment_create"),
    path("articel-payments/update/<int:pk>/", UpdatePaymentArticleView.as_view(), name="article_payment_update"),
    path("articel-payments/delete/<int:pk>/", DeletePaymentArticleView.as_view(), name="article_payment_delete"),

    path("roles/", RolesListView.as_view(), name="roles"),

    path("manage-site/main-page/", MainPageView.as_view(), name="main_page_update"),
    path("manage-site/about-page/", AboutUsView.as_view(), name="about_us"),
    path("manage-site/delete-photo/<int:pk>/", DeletePhotoView.as_view(), name="delete_photo"),
    path("manage-site/delete-document/<int:pk>/", DeleteDocsView.as_view(), name="delete_docs"),
    path("manage-site/services-page/", SiteServicesView.as_view(), name="services_page"),
    path("manage-site/tariffs-page/", TariffSiteView.as_view(), name="tariffs_page"),
    path("manage-site/contacts-page/", ContactSiteView.as_view(), name="contacts_page"),

    path("indicators/", IndicationsList.as_view(), name="indicators"),
    path("indicators/filtered_indicators/", IndicationsFilteredList.as_view(), name="indicators_filtered"),
    path("indicators/counter-indicators/<str:flat>/<str:service>/", CounterIndicationsList.as_view(),
         name="counter_indicators"),
    path("indicators/filtered-counter/<str:flat>/", CounterFilteredList.as_view(),
         name="filtered_counters"),
    path("indicators/filtered-counter-indicators/<str:flat>/", CounterIndicationsFilteredList.as_view(),
         name="filtered_counter_indicators"),
    path("indicators/add", CreateIndication.as_view(), name="add_indicator"),
    path("indicators/add_new/<str:flat>/<str:service>/", CreateNewIndication.as_view(), name="add_new_indicator"),
    path("indicators/add_to_flat/<int:flat>/", CreateIndicationForFlat.as_view(), name="add_indication_to_flat"),
    path("indicators/update/<int:pk>/", UpdateIndication.as_view(), name="update_indication"),
    path("indicators/detail/<int:pk>/", IndicationDetail.as_view(), name="detail_indication"),
    path("indicators/flat/<str:flat>/", FlatIndicationsList.as_view(), name="flat_indication"),

    path("houses/", HouseListView.as_view(), name="houses"),
    path("houses/filtered-house/", HouseFilteredListView.as_view(), name="filtered_houses"),
    path("houses/add/", CreateHouseView.as_view(), name="create_house"),
    path("houses/detail/<int:pk>/", HouseDetailView.as_view(), name="house_detail"),
    path("houses/delete/<int:pk>/", DeleteHouseView.as_view(), name="house_delete"),
    path("houses/update/<int:pk>/", UpdateHouseView.as_view(), name="house_update"),
    path("houses/get-house-info/<int:pk>/", GetHouseInfoView.as_view(), name="get_house_info"),
    path('houses/get-section-info/<int:pk>/', GetSectionInfoView.as_view(), name="get_section_info"),
    path('houses/get-all-flats/', GetAllFlatsView.as_view(), name="get_all_flats"),
    path('houses/get-flat-owner/<int:pk>/', GetFlatOwnerView.as_view(), name="get_flat_owner"),
    path('houses/get-flat-for-mail/<int:section_id>/<int:floor_id>/', GetFlatsForMail.as_view(),
         name="get_flat_for_mail"),
    path("houses/get-flat-info/<str:pk>", GetFlatInfoView.as_view(), name='get_flat-info'),
    path("houses/get-tariff-info/<str:pk>", GetTariffInfoView.as_view(), name='get_tariff-info'),
    path("houses/get-service-info/<str:pk>", GetServiceInfoView.as_view(), name='get_service-info'),
    path("houses/get-indication-info/<int:flat_id>/<int:service_id>/", GetIndicationInfoView.as_view(),
         name='get_service-info'),
    path("houses/get-indication-sorted-list/<int:flat_id>", GetIndicationsSortedList.as_view(),
         name='get_indication-sorted-list'),

    path("clients/", ClientsListView.as_view(), name="clients"),
    path("clients/filtered/", ClientsFilteredListView.as_view(), name="clients_filtered"),
    path("clients/add/", ClientSignUpView.as_view(), name="clients_add"),
    path("clients/detail/<int:pk>/", ClientDetailView.as_view(), name="clients_detail"),
    path("clients/update/<int:pk>/", ClientUpdateView.as_view(), name="clients_update"),
    path("clients/delete/<int:pk>/", ClientSignUpView.as_view(), name="clients_delete"),

    path("flats/", FlatListView.as_view(), name="flats"),
    path("flats/filtered/", FlatFilteredListView.as_view(), name="flats_filtered"),
    path("flats/create/", FlatCreateView.as_view(), name="flats_create"),
    path("flats/detail/<int:pk>/", FlatDetailView.as_view(), name="flats_detail"),
    path("flats/update/<int:pk>/", FlatUpdateView.as_view(), name="flats_update"),
    path("flats/delete/<int:pk>/", FlatDeleteView.as_view(), name="flats_delete"),
    path('flats/send-invitation/', SendInvitation.as_view(), name='send_invitation'),

    path('applications/', ApplicationListView.as_view(), name='applications'),
    path('applications/filtered/', ApplicationFilteredListView.as_view(), name='applications_filtered'),
    path('applications/add/', ApplicationCreateView.as_view(), name='application_add'),
    path('applications/detail/<int:pk>/', ApplicationDetailView.as_view(), name='applications_detail'),
    path('applications/update/<int:pk>/', ApplicationUpdateView.as_view(), name='applications_update'),
    path('applications/delete/<int:pk>/', ApplicationDeleteView.as_view(), name='applications_delete'),

    path('mailbox/', MailListView.as_view(), name='mailbox'),
    path('mailbox/create/', MailCreateView.as_view(), name='create_mail'),
    path('mailbox/detail/<int:pk>/', MailDetailView.as_view(), name='detail_mail'),
    path('mailbox/search_row/', MailFilteredListView.as_view(), name='filtered_mailbox'),
    path('mailbox/delete/<int:pk>/', MailDeleteView.as_view(), name='delete_mail'),
    path('mailbox/debtors/', MailDebtorsCreateView.as_view(), name='add_debtors_mailbox'),

    path('personal-accounts/', PersonalAccountListView.as_view(), name='personal_accounts'),
    path('personal-accounts/add/', CreatePersonalAccountView.as_view(), name='personal_account_add'),
    path('personal-accounts/update/<int:pk>/', UpdatePersonalAccountView.as_view(), name='personal_account_update'),
    path('personal-accounts/detail/<int:pk>/', PersonalAccountDetailView.as_view(), name='personal_account_detail'),
    path('personal-accounts/delete/', DeletePersonalAccount.as_view(), name='personal_account_delete'),
    path('personal-accounts/filtered-list/', PersonalAccountFilteredListView.as_view(),
         name='personal_accounts_filtered'),

    path('paybox/', PayboxList.as_view(), name='paybox'),
    path('paybox/filtered/', PayboxFilteredList.as_view(), name='paybox_filtered'),
    path('paybox/create/<str:income>/', CreatePaybox.as_view(), name='paybox_create'),
    path('paybox/update/<int:pk>/', UpdatePaybox.as_view(), name='paybox_update'),
    path('paybox/copy/<int:pk>/', CopyPaybox.as_view(), name='paybox_copy'),
    path('paybox/detail/<int:pk>/', PayboxDetail.as_view(), name='paybox_details'),
    path('paybox/delete/<int:pk>/', DeletePaybox.as_view(), name='paybox_delete'),

    path('statistic/', StatisticView.as_view(), name='statistic'),

    path("receipts", ReceiptList.as_view(), name='receipts'),
    path("receipts/filtered_receipts", ReceiptsFilteredList.as_view(),
         name='filtered_receipts'),
    path("receipts/add", CreateReceipt.as_view(), name='add_receipt'),
    path("receipts/update/<str:pk>/", UpdateReceipt.as_view(), name='update_receipt'),
    path("receipts/copy/<str:pk>/", CopyReceipt.as_view(), name='copy_receipt'),
    path("receipts/detail/<str:pk>/", ReceiptDetail.as_view(), name='read_receipt'),
    path("receipts/delete/<str:pk>/", DeleteReceipt.as_view(), name='delete_receipt'),
    path("receipts/print/<str:pk>/", ReceiptPrint.as_view(), name='receipt_print'),
    path("receipts/download_excel/<str:excel_id>/<str:receipt_id>/", ReceiptDownloadExcel.as_view(),
         name='receipt_download'),
    path("receipts/print_settings", ReceiptPrintingSettings.as_view(), name='receipt_print_settings'),
    path("receipts/print_settings/delete/<str:pk>", ReceiptPrintingSettingsDelete.as_view(),
         name='receipt_print_settings_delete'),
    path("receipts/print_settings/default/<str:pk>", ReceiptPrintingSettingsDefault.as_view(),
         name='receipt_print_settings_default'),
    path("receipts/send_receipt_email/<str:receipt_id>", SendReceiptEmail.as_view(),
         name='send_receipt_email'),

    path('cabinet/statistic/<int:flat_id>/', CabinetStatisticView.as_view(), name='flat_statistic_cabinet'),

    path('cabinet/profile/', Profile.as_view(), name='profile'),
    path('cabinet/profile/update/<str:pk>/', UpdateProfileView.as_view(), name='update_profile'),

    path('cabinet/receipts/', ReceiptListCabinet.as_view(), name='receipts_cabinet'),
    path("cabinet/flat_receipts/<str:flat_id>", FlatReceiptList.as_view(), name='get_flat_receipts_cabinet'),
    path("cabinet/flat_filtered_receipts/<str:flat_id>", FlatReceiptFilteredList.as_view(),
         name='flat_filtered_receipts_cabinet'),
    path("cabinet/filtered_receipts", CabinetReceiptsFilteredList.as_view(),
         name='filtered_receipts_cabinet'),
    path('cabinet/receipt/detail/<int:pk>/', CabinetReceiptDetail.as_view(), name='read_receipt_cabinet'),
    path("cabinet/receipt_to_pdf_print/<str:receipt_id>", ReceiptPDF.as_view(), name='receipt_to_pdf_print'),
    path("cabinet/receipt_to_pdf2/<str:receipt_id>", ReceiptPDF2.as_view(), name='receipt_to_pdf2'),

    path('cabinet/invoice/', Invoice.as_view(), name='invoice'),
    path("cabinet/tariff/detail/<str:flat_id>", CabinetTariffDetail.as_view(), name='get_tariff_cabinet'),

    path("cabinet/mailbox", CabinetMailboxList.as_view(), name='mailboxes_cabinet'),
    path("cabinet/filtered_messages", CabinetMailboxFilteredList.as_view(),
         name='filtered_messages_cabinet'),
    path("cabinet/mailbox/detail/<str:pk>", CabinetMailboxDetail.as_view(), name='mailbox_detail_cabinet'),
    path("cabinet/mailbox/delete/<str:pk>", CabinetDeleteMailbox.as_view(),
         name='delete_mailbox_cabinet'),

    path("cabinet/applications", CabinetApplicationList.as_view(), name='applications_cabinet'),
    path("cabinet/application/add", CabinetCreateApplication.as_view(), name='add_application_cabinet'),
]
