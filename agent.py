def agent_reply(history_len: int):
    if history_len < 2:
        return "Why is my account being suspended?"
    if history_len < 4:
        return "I am confused. What do you need from me?"
    if history_len < 6:
        return "It is asking for beneficiary details. Can you share?"
    return "Payment failed. Please resend the details."
