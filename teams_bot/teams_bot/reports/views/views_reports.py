import datetime
import json

import pytz
from django.conf import settings
from django.db.models import Count
from django.db.models import F

from bot.models.model_bot import Bot
from botData.models import BotRating
from botData.models.model_fallbacks import FallbackMessage
from botData.models.model_feedback_form import Message, FeedbackForm
from botPlatform.models.model_botuser import BotUserInfo
from botPlatform.models.model_platform import Platform
from organization.models.model_organization import Organization
from .views_save_to_xlsx import save_to_xlsx


class ReportData:

    def __init__(
            self,
            organization_id,
            bot_id=None,
            platform=None,
            start_date=None,
            end_date=None,
            report_type=None
    ):
        self.settings_timezone = pytz.timezone(settings.TIME_ZONE)
        # initializing params
        self.organization = organization_id,
        self.bot_id = bot_id
        self.platform = platform
        self.start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time()).astimezone(
            self.settings_timezone
        )
        self.end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time()).astimezone(
            self.settings_timezone
        )

        # initializing organization
        self.organization = Organization.objects.filter(id=organization_id).first()
        if not self.organization:
            raise Exception("Organization Not Found.")

        # initializing bots
        self.org_bots = Bot.objects.filter(organization_id=self.organization).all()
        if bot_id:
            self.bots = Bot.objects.filter(id=bot_id, organization_id=self.organization)
        else:
            self.bots = self.org_bots
        self.org_bot_ids = list(self.org_bots.values_list('id', flat=True))
        self.bot_ids = list(self.bots.values_list('id', flat=True))

        if platform:
            self.platform = Platform.objects.filter(bot_id__in=self.bot_ids, type=platform)
            self.platform_user = list(self.platform.values_list('id', flat=True))
            self.platform_users = BotUserInfo.objects.filter(platform_id__in=self.platform_user)
            self.platform_users = list(self.platform_users.values_list('id', flat=True))
        else:
            self.platform = Platform.objects.filter(bot_id__in=self.bot_ids)

        self.platform_ids = list(self.platform.values_list('id', flat=True))
        self.org_platform = Platform.objects.filter(bot_id__in=self.org_bot_ids)
        self.org_platform_ids = list(self.org_platform.values_list('id', flat=True))

    def fallback_messages(self):
        fallback_msgs = FallbackMessage.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        )
        id_list = []
        date_list = []
        msg_list = []
        user_list = []
        for msgs in fallback_msgs:
            id_list.append(msgs.id)
            date_list.append(msgs.created_at.astimezone(
                self.settings_timezone
            ))
            msg_list.append(msgs.message_id.message)
            user_list.append(msgs.user_id.email)

        data = {
            'ref_id': id_list,
            'last messages reference': msg_list,
            'user': user_list,
            'date': date_list
        }
        excel_file_name = "static/excel_export/fallback_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        print(response)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'

    def new_users(self):
        users_data = BotUserInfo.objects.filter(
            id__in=self.platform_users,
        )
        id_list = []
        date_list = []
        email_list = []
        name_list = []
        info_list = []
        for usr in users_data:
            id_list.append(usr.id)
            date_list.append(usr.created_at.astimezone(
                self.settings_timezone
            ))
            name_list.append(usr.name)
            email_list.append(usr.email)
            info_list.append(json.dumps(usr.info))
        data = {
            'ref_id': id_list,
            'name': name_list,
            'email': email_list,
            'information': info_list,
            'date': date_list
        }
        excel_file_name = "static/excel_export/new_user_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'

    def bot_users(self):
        bot_user = Message.objects.filter(
            type='user', bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).values('user_id').annotate(count=Count('user_id'), email=F('user_id__email'), name=F('user_id__name'))

        id_list = []
        email_list = []
        name_list = []
        count_list = []

        for usr in bot_user:
            id_list.append(usr['user_id'])
            email_list.append(usr['email'])
            name_list.append(usr['name'])
            count_list.append(usr['count'])

        data = {
            'ref_id': id_list,
            'name': name_list,
            'email': email_list,
            'message count': count_list,
        }
        excel_file_name = "static/excel_export/bot_user_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'

    def total_messages(self):
        total_messages = Message.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        )
        id_list = []
        date_list = []
        msg_list = []
        user_list = []
        type_list = []
        for msgs in total_messages:
            id_list.append(msgs.id)
            date_list.append(msgs.created_at.astimezone(
                self.settings_timezone
            ))
            msg_list.append(msgs.message)
            user_list.append(msgs.user_id.email)
            type_list.append(msgs.type)
        data = {
            'ref_id': id_list,
            'message': msg_list,
            'user': user_list,
            'by': type_list,
            'date': date_list
        }
        excel_file_name = "static/excel_export/messages_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'

    def feedback_forms(self):
        feedback_forms = FeedbackForm.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        )

        id_list = []
        date_list = []
        msg_list = []
        user_list = []
        user_msg_list = []
        for msgs in feedback_forms:
            id_list.append(msgs.id)
            date_list.append(msgs.created_at.astimezone(
                self.settings_timezone
            ))
            msg_list.append(msgs.message_id.message)
            user_list.append(msgs.user_id.email)
            user_msg_list.append(msgs.user_message)
        data = {
            'ref_id': id_list,
            'last messages reference': msg_list,
            'user': user_list,
            'feedback': user_msg_list,
            'date': date_list
        }
        excel_file_name = "static/excel_export/feedback_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'

    def bot_ratings(self):
        bot_ratings = BotRating.objects.filter(bot_id__in=self.bots,
                                               user_id__in=self.platform_users,
                                               created_at__range=(self.start_date, self.end_date))
        id_list = []
        date_list = []
        rating_list = []
        user_list = []

        for bot_rating in bot_ratings:
            id_list.append(bot_rating.id)
            date_list.append(bot_rating.created_at.astimezone(
                self.settings_timezone
            ))
            rating_list.append(bot_rating.rating)
            user_list.append(bot_rating.user_id.email)

        data = {
            'ref_id': id_list,
            'rating': rating_list,
            'user': user_list,
            'date': date_list
        }
        excel_file_name = "static/excel_export/ratings_report.xlsx"
        response = save_to_xlsx(data, excel_file_name)
        if response == 'success':
            return excel_file_name
        else:
            return 'Error'
