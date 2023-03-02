from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode


tracer = trace.get_tracer("notifications.activities")

class NotificationsActivities:
  def run():
    with tracer.start_as_current_span("notification-mock-span") as span:
      # Set attributes on the span
      span.set_attribute("notification", "cruddr")
    
      # Set the status of the span
      span.set_status(Status(StatusCode.OK, "Notification Initialized."))
      now = datetime.now(timezone.utc).astimezone()
      results = [{
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Coco Melon',
        'message': 'I am a youtube channel',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [{
          'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
          'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'Worf',
          'message': 'This post has no honor!',
          'likes_count': 0,
          'replies_count': 0,
          'reposts_count': 0,
          'created_at': (now - timedelta(days=2)).isoformat()
        }],
      }]
      return results