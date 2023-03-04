from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder


class UserActivities:
    def run(user_handle):
        segment = xray_recorder.begin_segment('user-activities.segment')
        model = {
            'errors': None,
            'data': None
        }

        now = datetime.now(timezone.utc).astimezone()

        dict = {
            "now": now.isoformat(),
            "user_handle": user_handle,
        }

        # Add metadata or annotation here if necessary
        segment.put_metadata('user_metadata_key', dict, 'namespace')
        with xray_recorder.in_subsegment('subsegment_name') as subsegment:
            subsegment.put_annotation('user.name', 'mquanit')

        if user_handle == None or len(user_handle) < 1:
            model['errors'] = ['blank_user_handle']
        else:
            now = datetime.now()
            results = [{
                'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
                'handle':  'M Quanit',
                'message': 'Cloud is fun!',
                'created_at': (now - timedelta(days=1)).isoformat(),
                'expires_at': (now + timedelta(days=31)).isoformat()
            }]
            model['data'] = results
        return model
