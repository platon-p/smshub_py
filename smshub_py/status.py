"""
**Just after getting number these actions allowed:**

`CANCEL` - Cancel activation

`SMS_SENT` - Say that SMS was sent (optional)

**If status is SMS_SENT:**

`CANCEL` - Cancel activation

**Just after getting SMS code:**

`SMS_RETRY` - Request for another SMS

`SMS_ACCEPTED` - Accept SMS code and finish activation

**If status is SMS_RETRY:**

`SMS_ACCEPTED` - Accept SMS code and finish activation
"""

SMS_SENT = 1
CANCEL = 8
SMS_RETRY = 3
SMS_ACCEPTED = 6
