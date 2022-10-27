from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):

    """ChattingRoom Models Definition"""

    users = models.ManyToManyField(
        "users.USer",
        related_name="chattingrooms",
    )

    def __str__(self) -> str:
        return "Chatting Room"


class Message(CommonModel):

    """Message Model Definition"""

    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    text = models.TextField()
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
