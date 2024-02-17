import datetime

# Example timezone-aware datetime
aware_dt = datetime.datetime.now(datetime.timezone.utc)

# Example timezone-naive datetime
naive_dt = datetime.datetime.now()

# Convert timezone-naive datetime to timezone-aware
naive_dt_aware = naive_dt.replace(tzinfo=datetime.timezone.utc)

# Now you can compare them
if aware_dt > naive_dt_aware:
    print("The timezone-aware datetime is greater.")
else:
    print("The timezone-naive datetime is greater.")
