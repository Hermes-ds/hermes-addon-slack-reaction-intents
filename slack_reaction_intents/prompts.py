APPROVE_PROMPT = "방금 제안한 구체 작업을 승인합니다. 반응이 달린 직전 답변의 제안을 그대로 수행해줘."
QUESTION_PROMPT = (
    "더 진행하면 좋을 작업이 있을까? 꼭 필요한 것만 제안해주고, "
    "오히려 얻는 것보다 잃을 것이 많거나, 굳이 안해도 되는건 제안 안해줘도 돼."
)

REACTION_PROMPT_MAP = {
    "+1": APPROVE_PROMPT,
    "thumbsup": APPROVE_PROMPT,
    "question": QUESTION_PROMPT,
}
