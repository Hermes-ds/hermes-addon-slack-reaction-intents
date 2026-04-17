from .handlers import handle_slack_reaction_added


def register(ctx):
    """Register Hermes addon hooks for Slack reaction intent handling.

    Note: this addon uses the official Hermes plugin API under the hood.
    """

    def gateway_pre_handle_event(event, adapter=None, runner=None, **kwargs):
        # Reserved for future add-on-specific event normalization.
        return None

    ctx.register_hook("slack_reaction_added", handle_slack_reaction_added)
    ctx.register_hook("gateway_pre_handle_event", gateway_pre_handle_event)
