from django.shortcuts import render

from django.core.mail import send_mail

# from django.core.mail import EmailMessage
from aws_backend_project.settings import EMAIL_HOST_USER

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

# Create your views here.


# The `OrderView` class in Python defines API endpoints for retrieving, creating, updating, and
# deleting orders with error handling for various scenarios.
class OrderView(APIView):
    def get(
        self,
        request,
    ):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "message": "Orders data fetched successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(error)
            return Response(
                {"data": {}, "message": "Sorry for this but something went wrong!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        "data": serializer.errors,
                        "message": "Sorry for this but something went wrong!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # implement send mail
            subject = "New order placed"
            customer_name = data["customer_name"]
            message = f"Dear {customer_name}, \nYour order has been placed!"
            email = data["customer_email"]
            recipient_list = [email]
            send_mail(
                subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=False
            )
            serializer.save()

            return Response(
                {
                    "data": serializer.data,
                    "message": "New order created successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as post_error:
            print(post_error)
            return Response(
                {
                    "data": serializer.errors,
                    "message": "Sorry, something went wrong with the creation of order!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request):
        try:
            data = request.data
            order = Order.objects.filter(id=data.get("id"))
            if not order.exists():
                return Response(
                    {
                        "data": {},
                        "message": "Sorry, but order is not found with this ID!",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = OrderSerializer(order[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response(
                    {
                        "data": serializer.errors,
                        "message": "Sorry for this but something went wrong!",
                    },
                    status=status.HTTP_500_BAD_REQUEST,
                )

            serializer.save()

            return Response(
                {
                    "data": serializer.data,
                    "message": "Order is updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as patch_error:
            print(patch_error)
            return Response(
                {
                    "data": serializer.errors,
                    "message": "Sorry for this but something went wrong!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        try:
            data = request.data
            order = Order.objects.filter(id=data.get("id"))

            if not order.exists():
                return Response(
                    {
                        "data": {},
                        "message": "Sorry, but order with this ID was not found !",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            order[0].delete()
            return Response(
                {
                    "data": {},
                    "message": "Order was deleted successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as delete_error:
            print(delete_error)
            return Response(
                {
                    "data": {},
                    "message": "Sorry, something went wrong with the deletion of order!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
