
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Mailer:
    def sendEmail(self, to, subject, message):
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to]
        return send_mail(subject, message, email_from, recipient_list)

    def sendHTMLEmail(self, to, subject, content):
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to]
        return send_mail(subject, strip_tags(content), email_from, recipient_list, html_message=content)

    def sendMultipleEmails(self, to, subject, message):
        email_from = settings.EMAIL_HOST_USER
        return send_mail(subject, message, email_from, to)

    def getEMailTemplateContent(self, template_path, data={}):
        template = get_template(template_path)
        context = Context(data)
        return template.render(data)
