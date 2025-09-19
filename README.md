# AtomicAds - Notification Service

A Django-based notification and alert management system that enables organizations to create, manage, and deliver alerts to users and teams through multiple channels.

## 🚀 Features

- **Multi-Channel Delivery**: Support for in-app, email, and SMS notifications
- **Flexible Targeting**: Send alerts organization-wide, to specific teams, or individual users
- **Alert Management**: Create alerts with different severity levels (info, warning, critical)
- **User Preferences**: Users can mark alerts as read/unread and snooze notifications
- **Reminder System**: Configurable reminder frequency for persistent alerts
- **Team-Based Organization**: Organize users into teams for targeted notifications
- **Expiry Management**: Set expiration times for time-sensitive alerts
- **Delivery Tracking**: Track notification delivery status and read receipts

## 🏗️ Architecture

The system uses a strategy pattern for notification delivery, allowing easy extension of delivery methods:

- **InAppDelivery**: Creates in-app notifications
- **EmailDelivery**: Sends email notifications (placeholder implementation)
- **SMSDelivery**: Sends SMS notifications (placeholder implementation)

## 📋 Requirements

- Python 3.8+
- Django 5.2.6
- PostgreSQL
- Django REST Framework

See `requirements.txt` for complete dependency list.

## ⚙️ Installation

1. **Clone the repository**
   ```cmd
   git clone <repository-url>
   cd AtomicAds
   ```

2. **Create and activate virtual environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Database Setup**
   ```cmd
   python manage.py migrate
   ```

6. **Seed Sample Data** (Optional)
   ```cmd
   python manage.py seed_data
   ```

7. **Run the Development Server**
   ```cmd
   python manage.py runserver
   ```

## 📊 Data Models

### Alert
- **title**: Alert title
- **message**: Alert content
- **severity**: info, warning, or critical
- **delivery_type**: in_app, email, or sms
- **start_time**: When the alert becomes active
- **expiry_time**: When the alert expires (optional)
- **reminder_frequency**: Frequency for reminders in minutes
- **org_wide**: Whether alert is visible to entire organization
- **teams**: Associated teams
- **users**: Specific users to notify

### Team
- **name**: Team name
- **users**: Team members

### NotificationDelivery
- **alert**: Associated alert
- **user**: Recipient user
- **status**: delivered, read, or unread
- **delivered_at**: Delivery timestamp
- **last_sent_at**: Last reminder timestamp

### UserAlertPreference
- **user**: User
- **alert**: Associated alert
- **read**: Read status
- **snoozed_until**: Snooze expiration date

## 🔌 API Endpoints

### Alerts Management
- `GET /alerts/` - List all alerts with optional filtering
  - Query parameters: `severity`, `status` (active/expired)
- `POST /alerts/` - Create new alert
- `GET /alerts/{id}/` - Get specific alert
- `PUT /alerts/{id}/` - Update alert
- `DELETE /alerts/{id}/` - Delete alert
- `POST /alerts/{id}/trigger/` - Manually trigger alert notifications

### User-Specific Alerts
- `GET /users/{user_id}/alerts/` - Get alerts for specific user
- `POST /users/{user_id}/alerts/{alert_id}/snooze/` - Snooze alert
- `POST /users/{user_id}/alerts/{alert_id}/mark_read/` - Mark alert as read
- `POST /users/{user_id}/alerts/{alert_id}/mark_unread/` - Mark alert as unread

## 🤖 Management Commands

### Seed Data
```cmd
python manage.py seed_data
```
Creates sample teams, users, and alerts for testing.

### Trigger Reminders
```cmd
python manage.py trigger_reminder
```
Manually triggers reminders for all active alerts. This simulates the 2-hour cron job for reminder notifications.

## 🔧 Configuration

### Timezone
The system is configured for Asia/Kolkata timezone. Update `TIME_ZONE` in `settings.py` as needed.

### Database
PostgreSQL is the configured database. Update database settings in `settings.py` or use environment variables.

## 🏃‍♂️ Usage Examples

### Creating an Alert
```python
from core.models import Alert, Team
from django.utils import timezone
from datetime import timedelta

# Create team-specific alert
alert = Alert.objects.create(
    title="System Maintenance",
    message="Scheduled maintenance window from 2-4 AM",
    severity="warning",
    delivery_type="email",
    start_time=timezone.now(),
    expiry_time=timezone.now() + timedelta(days=1),
    reminder_enabled=True,
    reminder_frequency=120  # 2 hours
)

# Assign to specific team
engineering_team = Team.objects.get(name="Engineering")
alert.teams.add(engineering_team)
```

### Triggering Notifications
```python
from core.services import trigger_reminder_for_alert

# Trigger notifications for specific alert
summary = trigger_reminder_for_alert(alert)
print(f"Delivered: {summary['delivered']}, Skipped: {summary['skipped_snoozed']}")
```

## 🔄 Workflow

1. **Alert Creation**: Administrators create alerts with targeting rules
2. **User Notification**: System delivers notifications based on delivery type
3. **User Interaction**: Users can read, snooze, or interact with alerts
4. **Reminder System**: Periodic reminders sent for unread alerts
5. **Expiry Handling**: Expired alerts are automatically filtered out

## 🚀 Future Enhancements

- Integration with real email/SMS providers
- WebSocket support for real-time notifications
- Advanced scheduling and recurring alerts
- Analytics and reporting dashboard
- Mobile app integration
- Custom notification templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support, please create an issue in the repository or contact the development team.