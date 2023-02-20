from nio import (AsyncClient,
                 InviteMemberEvent,
                 MatrixRoom,
                 RoomMessageText,
                 MegolmEvent,)
import logging

logger = logging.getLogger(__name__)


class Callbacks:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def invite(self, room: MatrixRoom, event: InviteMemberEvent) -> None:
        logger.info(f"Got invite to {room.room_id} from {event.sender}.")

        for attempt in range(3):
            result = await self.client.join(room.room_id)
            if type(result) == "JoinError":
                logger.error(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt,
                    result.message,
                )
            else:
                break
        else:
            logger.error("Unable to join room: %s", room.room_id)

        logger.info(f"Joined {room.room_id}")

    async def message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        if event.sender == self.client.user:
            return
        return


    async def decryption_failure(self, room: MatrixRoom, event: MegolmEvent) -> None:
        logger.error(
            f"Failed to decrypt event '{event.event_id}' in room '{room.room_id}'!"
        )

        red_x_and_lock_emoji = "❌ 🔐"

        content = {
            "m.relates_to": {
                "rel_type": "m.annotation",
                "event_id": event.event_id,
                "key": red_x_and_lock_emoji,
            }
        }

        return await self.client.room_send(
            room.room_id,
            "m.reaction",
            content,
            ignore_unverified_devices=True,
        )
