from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, UserProfileSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={201: UserProfileSerializer},
    tags=["auth"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
        {
            "message": "User registered successfully",
            "user": UserProfileSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    responses=UserProfileSerializer,
    tags=["auth"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):

    serializer = UserProfileSerializer(request.user)

    return Response(serializer.data)