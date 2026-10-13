from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Card
from .serializers import CardSerializer


@extend_schema(
    request=CardSerializer,
    responses={201: CardSerializer},
    tags=["cards"]
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_card(request):

    serializer = CardSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    card = serializer.save(user=request.user)

    return Response(
        CardSerializer(card).data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    responses=CardSerializer(many=True),
    tags=["cards"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_cards(request):

    cards = Card.objects.filter(
        user=request.user
    ).order_by("-id")

    serializer = CardSerializer(cards, many=True)

    return Response(serializer.data)

@extend_schema(
    responses={200: CardSerializer},
    tags=["cards"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_card_by_id(request, card_id):

    card = Card.objects.filter(
        id=card_id,
        user=request.user
    ).first()

    if card is None:
        return Response(
            {"error": "Card not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CardSerializer(card)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@extend_schema(
    request=None,
    responses={204: None},
    tags=["cards"]
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_card(request, card_id):

    card = Card.objects.filter(
        id=card_id,
        user=request.user
    ).first()

    if card is None:
        return Response(
            {"error": "Card not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    card.delete()

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )