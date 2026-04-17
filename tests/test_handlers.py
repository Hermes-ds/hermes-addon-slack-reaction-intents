from unittest.mock import AsyncMock, MagicMock

from slack_reaction_intents.handlers import handle_slack_reaction_added


async def test_handle_slack_reaction_added_builds_dispatch_event():
    adapter = MagicMock()
    adapter._reaction_dedup = MagicMock()
    adapter._reaction_dedup.is_duplicate.return_value = False
    adapter._bot_user_id = "U_BOT"
    adapter._team_bot_user_ids = {}
    adapter._channel_team = {}
    adapter._get_client.return_value = MagicMock(
        conversations_history=AsyncMock(return_value={
            "messages": [{
                "ts": "2000.2",
                "thread_ts": "1000.1",
                "text": "Original bot reply",
                "user": "U_BOT",
            }]
        }),
        reactions_get=AsyncMock(),
    )
    adapter._resolve_user_name = AsyncMock(return_value="DS")
    adapter.build_source.return_value = MagicMock(thread_id="1000.1")

    result = await handle_slack_reaction_added(adapter, {
        "type": "reaction_added",
        "user": "U_USER",
        "reaction": "thumbsup",
        "item": {"type": "message", "channel": "C123", "ts": "2000.2"},
        "item_user": "U_BOT",
        "event_ts": "3000.3",
    })

    assert result["handled"] is True
    dispatch_event = result["dispatch_event"]
    assert dispatch_event.text.startswith("방금 제안한 구체 작업을 승인합니다")
    assert dispatch_event.flags["suppress_busy_ack"] is True
