import datetime

import pytz
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate

from bot.models.model_bot import Bot
from botData.models.model_bot_ratings import BotRating
from botData.models.model_fallbacks import FallbackMessage
from botData.models.model_feedback_form import Message, FeedbackForm
from botPlatform.models.model_botuser import BotUserInfo
from botPlatform.models.model_platform import Platform
from organization.models.model_organization import Organization


class Kpi:
    def __init__(
            self,
            organization_id,
            bot_id=None,
            platform=None,
            start_date=None,
            end_date=None,
    ):
        settings_timezone = pytz.timezone(settings.TIME_ZONE)
        # initializing params
        self.organization = organization_id,
        self.bot_id = bot_id
        self.platform = platform
        self.start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time()).astimezone(
            settings_timezone
        )
        self.end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time()).astimezone(
            settings_timezone
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

        self.data = {
            "counts": {},
        }

    def counts(self):
        counts = dict()
        counts['bots'] = Bot.objects.filter(organization_id=self.organization).count()
        counts['platforms'] = Platform.objects.filter(bot_id__in=self.org_bot_ids).distinct('type').count()
        counts['users'] = BotUserInfo.objects.filter(
            platform_id__in=self.org_platform_ids,
        ).distinct('email').count()
        counts['messages'] = Message.objects.filter(
            bot_id__in=self.org_bot_ids,
        ).count()

        self.data['counts'] = counts

    def fallback_messages(self):
        fallback_msgs = FallbackMessage.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id'))
        print("fallback messages", fallback_msgs)
        self.data['fallback_messages'] = fallback_msgs

    def new_users(self):
        users_data = BotUserInfo.objects.filter(
            id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id'))

        self.data['new_users'] = users_data

    def bot_users(self):
        users_data = Message.objects.filter(
            type='user', bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(
            count=Count('user_id', distinct=True)
        )
        self.data['bot_users'] = users_data

    def bot_ratings(self):
        bot_ratings = BotRating.objects.filter(bot_id__in=self.bots,
                                               user_id__in=self.platform_users,
                                               created_at__range=(self.start_date, self.end_date)).values(
            'rating').annotate(count=Count('rating'))
        bot_rating = [0, 0, 0, 0, 0]
        for ratings in bot_ratings:
            if ratings['rating'] in ['1', '2', '3', '4', '5']:
                bot_rating[int(ratings['rating']) - 1] = ratings['count']

        self.data['bot_ratings'] = bot_rating

    def total_messages(self):
        total_messages = Message.objects.filter(bot_id=self.bot_id).count()
        user_messages = Message.objects.filter(
            type='user', bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')
        )

        bot_messages = Message.objects.filter(
            type='bot', bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')
        )

        self.data['bot_messages'] = bot_messages
        self.data['user_messages'] = user_messages

    def feedback_forms(self):
        feedback_forms = FeedbackForm.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            created_at__range=(self.start_date, self.end_date),
        ).annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id'))

        self.data['feedback_forms'] = feedback_forms

    def get_top_queries(self):
        input_messages = Message.objects.filter(
            bot_id__in=self.bots,
            user_id__in=self.platform_users,
            type='user',
            created_at__range=(self.start_date, self.end_date),
        )
        words = []
        for input_message in input_messages:
            if input_message.message:
                common_words = ['hi', 'yes', 'hello', 'thanks', 'ok', 'okay', 'it operations', 'hms', 'no', 'crm']
                if input_message.message.lower() not in common_words:
                    words.append(input_message.message)
        words_with_weigth = {}
        for word in words:
            words_with_weigth[word] = words_with_weigth.get(word, 1) + 1
        data = [[k, v] for k, v in sorted(words_with_weigth.items(), key=lambda item: item[1])]
        data.reverse()

        self.data['top_queries_words'] = data[:10]
