from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import User, ExpenseGroup, ExpenseParticipant
from .service import LoginService, ExpenseManager

from .serializer import (
    RegisterUserSerializer,
    LoginUserSerializer,
    ExpenseGroupSerializer
)


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()



class LoginUserView(APIView):
    def post(self, request, *args):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        __service = LoginService().user_authentication(email=email, password=password)

        return Response(__service, __service['code'])
    

class AddExpenseView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args):
        data = request.data
        __service = ExpenseManager(data=data)
        return __service.add_expense()
