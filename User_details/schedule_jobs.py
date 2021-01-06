'''
from datetime import datetime, timedelta, timezone
from .models import DeactivateUser
#from django.contrib.auth import get_user_model

from .model import User 

# run every 23h.
def schedule_deactivate_user():
    deactivates = DeactivateUser.objects.all()
    now = datetime.now(timezone.utc)
    # 2592000 = 30 day
    for deactive in deactivates:
        user_deactivate = deactive.user.deactivate.deactive
        created = deactive.user.deactivate.created
        last_login = deactive.user.last_login
        if user_deactivate == True and (now - created).total_seconds() > 2592000:
            if (now - last_login).total_seconds() < 2592000:
                user_deactivate = False
                deactive.user.deactivate.save()
            deactive.user.is_active = False
            deactive.user.save()
            # TODO send mail for user tell him his account not active

'''