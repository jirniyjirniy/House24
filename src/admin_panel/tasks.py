from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML

from House24.celery import app


@app.task(bind=True)
def send_invitation(self, to='info@example.com'):
    html_template = 'invitation/invitation_email.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Приглашение в House24', html_message, 'faceit_kawai@gmail.com', [to])
    message.content_subtype = 'html'
    message.send()


@app.task(bind=True)
def notification_password_changed(self, to='info@example.com'):
    html_template = 'accounts/password_changed.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Смена паролья House24', html_message, 'faceit_kawai@gmail.com', [to])
    message.content_subtype = 'html'
    message.send()


@app.task(bind=True)
def send_receipt(self, html_to_pdf, base_url, to='somebody@gmail.com'):
    pdf_file = HTML(string=html_to_pdf, base_url=base_url).write_pdf()

    html_template = 'admin_panel/receipt_email.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Электронная квитанция House24', html_message, 'faceit_kawai@gmail.com', [to])

    message.attach('квитанция.pdf', pdf_file, 'application/pdf')

    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()
