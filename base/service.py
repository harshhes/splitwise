import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib import common

from .serializer import ExpenseGroupSerializer
from .models import User, ExpenseGroup, ExpenseParticipant
from .utils import ExpenseType, HTTPResponse, get_user
from .tasks import send_async_email


class LoginService:
    """Login Service class to handle User Authentication and access token generation"""

    def user_authentication(self, email, password):
        try:
            user = User.objects.get(email=email)
            correct_password = user.check_password(password)
            if correct_password:
                return self.__generate_token(user)
            else:
                return {'status': 'error', 'response': 'Wrong email or password', 'code':400}

        except ObjectDoesNotExist:
            return {'status': 'error', 'response': 'User does not exist', 'code':404}
        except Exception as e:
            traceback.print_exc()
            print('exception at login-->', e)
            return {'status': 'error', 'response': 'Internal server error','code':500}


    def __generate_token(self, user):
        application = Application.objects.all()[:1]
        expires = timezone.now() + timedelta(seconds=3600) # 1 hour
        current_token = common.generate_token()
        refresh_token = common.generate_token()
        access_token = AccessToken(
            user=user,
            scope='',
            expires=expires,
            token=current_token,
            application=application[0]
        )
        access_token.save()
        refresh_token_data = RefreshToken(
            user=user,
            token=refresh_token,
            application=application[0],
            access_token=access_token
        )
        refresh_token_data.save()
        user.last_login=timezone.now()
        user.save(update_fields=['last_login'])
        return {'status': 'success','access_token': current_token, 'refresh_token': refresh_token, 'expiry': expires,'user':user.email,'first_name':user.first_name, "code":200}
    

class ExpenseManager:
    """To Manage Expenses"""

    def __init__(self, data=None):
        self.__data = data
        print(self.__data)

    def add_expense(self):
        name = self.__data.get("name", None)
        payer = self.__data["payer"]
        self.__data["payer"] = get_user(self.__data.get("payer"))
        expense_type = self.__data.get('expense_type')
        amount = self.__data.get('amount')
        image = self.__data.get('image', None)
        notes = self.__data.get('notes', None)
        participants = self.__data.get('participants') 
                

        if expense_type == ExpenseType.equal.value:
            share = amount/(len(participants)+1)
            print(f"per share = {share}")
            pps = self.__data.pop("participants")
            expense = ExpenseGroup.objects.create(**self.__data)

            if type(participants) == list:
                data = [
                    ExpenseParticipant(
                            user=get_user(email),
                            expense=expense,
                            owe_amount=share,
                            final_amount=share
                            ) 
                            for email in participants
                    ]

                expense_participants = ExpenseParticipant.objects.bulk_create(data)
                for i in participants:
                    send_async_email.delay(recipients=i, data={"email":i, "amount":amount, "name":name, "participants": [pps], "payer":payer})
                    print("async email sent")
                return HTTPResponse(200).success_response(f"{name} Expense Added")

        elif expense_type == ExpenseType.exact.value:
            print(sum(participants.values()))
            if sum(participants.values()) != amount - sum(participants.values()):
                return HTTPResponse(400).bad_request(f"please make share smaller than {amount}")
            
            if type(participants) != dict:
                return HTTPResponse(400).bad_request(f"please enter data in dict")
            
            self.__data.pop("participants")
            expense = ExpenseGroup.objects.create(**self.__data)
            
            data = [
                ExpenseParticipant(
                            user=get_user(i),
                            expense=expense,
                            owe_amount=j,
                            final_amount=j
                            ) 
                            for i,j in participants.items() # {participant_name: exact share}
            ]

            expense_participants = ExpenseParticipant.objects.bulk_create(data) 
            for i in participants.keys():
                send_async_email.delay(recipients=i, data={"email":i, "amount":amount, "name":name, "participants": participants.keys(), "payer":payer})
            return HTTPResponse(200).success_response(f"{name} Expense Added")

        else:
            if type(participants) == dict:
                percent_sum = sum(participants.values())
                if percent_sum != (100- (100- percent_sum)):
                    return HTTPResponse(400).bad_request(f"amount exceeds 100%!!!")
                                
                else:
                    self.__data.pop("participants")
                    expense = ExpenseGroup.objects.create(**self.__data)
                    data = [
                        ExpenseParticipant(
                        user=get_user(i),
                        expense=expense,
                        owe_amount=((amount/100)*j),
                        final_amount=((amount/100)*j)
                        ) 
                        for i,j in participants.items() #{participant_name: percent of share}
                    ]
                    expense_participants = ExpenseParticipant.objects.bulk_create(data) 
                    for i in participants.keys():
                        send_async_email.delay(recipients=i, data={"email":i, "amount":amount, "name":name, "participants": participants.keys(), "payer":payer})
                    return HTTPResponse(200).success_response(f"{name} Expense Added")
                
        traceback.print_exc()
        return HTTPResponse(400).bad_request("Something went wrong")

        

        

