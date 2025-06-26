def emit_trade_event(user_id: int):
    # In real Kafka: publish to topic
    print(f"[EVENT] Trade completed for user {user_id}")
