from celery import shared_task


from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from django.conf import settings

from .models import User
from .utils import HTTPResponse

@shared_task
def send_async_email(recipients, data):
    try:
        print(data)
        template = get_template("add_expense.html")
        subject = "New Expense Added | Splitwise"
        message = template.render(data).strip()
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [recipients]
        print(recipient_list)

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = "html" 
        email.send(fail_silently=False)

    except Exception as e:
        print(e)
        return HTTPResponse(500).internal_server_error("something went wrong, please try again later!")