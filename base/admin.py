from django.contrib import admin
from .models import User, ExpenseGroup, ExpenseParticipant

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined',)



@admin.register(ExpenseGroup)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'payer', 'expense_type', 'amount', '_get_participants', 'created_at', )


    def _get_participants(self, obj):
        return ", ".join([str(i.first_name) for i in obj.users.all()])
    

    _get_participants.short_description = "Participants"


@admin.register(ExpenseParticipant)
class ExpenseParticipantAdmin(admin.ModelAdmin):
    list_display = ('expense', 'user', 'owe_amount', 'final_amount', 'created_at', )
