from django.contrib import admin
from .models import Customer


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ("username", "email", "date_of_birth", "is_superuser", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "date_of_birth",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
    )

    # if user is only a staff enable read-only for highlighted fields
    if not Customer.is_superuser:
        readonly_fields = ["is_superuser", "is_staff"]
    else:
        readonly_fields = []

    def has_view_permission(self, request, obj=None) -> bool:
        return True

    def has_add_permission(self, request) -> bool:
        return True

    def has_change_permission(self, request, obj=None) -> bool:
        return True

    def has_delete_permission(self, request, obj=None) -> bool:
        assert isinstance(request.user, Customer), "request.user must be a Customer"
        return request.user.is_superuser
