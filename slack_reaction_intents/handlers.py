from gateway.platforms.base import MessageEvent, MessageType

from .config import EVENT_FLAGS, REACTION_PROMPT_MAP


async def handle_slack_reaction_added(adapter, event, **kwargs):
    """Addon hook: convert supported Slack reactions into synthetic MessageEvents."""
    reaction = str((event or {}).get("reaction") or "").strip()
    prompt = REACTION_PROMPT_MAP.get(reaction)
    if not prompt:
        return None

    event_ts = str((event or {}).get("event_ts") or "")
    if event_ts and getattr(adapter, "_reaction_dedup", None) and adapter._reaction_dedup.is_duplicate(event_ts):
        return {"handled": True}

    user_id = str((event or {}).get("user") or "")
    bot_user_id = getattr(adapter, "_bot_user_id", None)
    if not user_id or user_id == bot_user_id:
        return {"handled": True}

    item = (event or {}).get("item") or {}
    if item.get("type") != "message":
        return {"handled": True}

    channel_id = str(item.get("channel") or "")
    message_ts = str(item.get("ts") or "")
    if not channel_id or not message_ts:
        return {"handled": True}

    team_id = str((event or {}).get("item_team") or (event or {}).get("team") or (event or {}).get("team_id") or "")
    if team_id and channel_id:
        adapter._channel_team[channel_id] = team_id
    bot_uid = adapter._team_bot_user_ids.get(team_id, bot_user_id)
    item_user = str((event or {}).get("item_user") or "")
    if item_user and bot_uid and item_user != bot_uid:
        return {"handled": True}

    client = adapter._get_client(channel_id)
    result = await client.conversations_history(
        channel=channel_id,
        latest=message_ts,
        oldest=message_ts,
        inclusive=True,
        limit=1,
    )
    messages = result.get("messages", [])
    if not messages:
        reaction_item = await client.reactions_get(
            channel=channel_id,
            timestamp=message_ts,
            full=True,
        )
        if reaction_item.get("type") == "message" and reaction_item.get("message"):
            messages = [reaction_item["message"]]
        else:
            return {"handled": True}

    message = messages[0]
    message_user = str(message.get("user") or "")
    if not message.get("bot_id"):
        if bot_uid and message_user != bot_uid:
            return {"handled": True}
        if item_user and message_user and message_user != item_user:
            return {"handled": True}

    thread_ts = str(message.get("thread_ts") or message_ts)
    user_name = await adapter._resolve_user_name(user_id, chat_id=channel_id)
    is_dm = channel_id.startswith("D")
    source = adapter.build_source(
        chat_id=channel_id,
        chat_name=channel_id,
        chat_type="dm" if is_dm else "group",
        user_id=user_id,
        user_name=user_name,
        thread_id=thread_ts,
    )
    reply_to_message_id = thread_ts if thread_ts != message_ts else None
    dispatch_event = MessageEvent(
        text=prompt,
        message_type=MessageType.TEXT,
        source=source,
        raw_message=event,
        message_id=str((event or {}).get("event_ts") or f"reaction:{channel_id}:{message_ts}:{reaction}:{user_id}"),
        reply_to_message_id=reply_to_message_id,
        reply_to_text=str(message.get("text") or "") or None,
        flags=dict(EVENT_FLAGS),
    )
    return {"dispatch_event": dispatch_event, "handled": True}
