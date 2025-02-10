from datetime import datetime, timedelta

current_time = datetime.utcnow()
future_time = current_time + timedelta(minutes=15)

print(f"Current Time: {current_time}")
print(f"Future Time: {future_time}")