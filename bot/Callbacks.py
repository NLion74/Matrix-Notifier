import asyncio
from nio import AsyncClient, InviteMemberEvent, MatrixRoom, RoomMessageText


class Callbacks():
    def __init__(self, client: AsyncClient):
        self.client = client

    async def invite(self, room: MatrixRoom, event: InviteMemberEvent) -> None:
        print(f"Got invite to {room.room_id} from {event.sender}.")

        for attempt in range(3):
            result = await self.client.join(room.room_id)
            if type(result) == "JoinError":
                print(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt,
                    result.message,
                )
            else:
                break
        else:
            print("Unable to join room: %s", room.room_id)

        print(f"Joined {room.room_id}")

    async def message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        if event.sender == self.client.user:
            return
        return