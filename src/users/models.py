from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext
from multiselectfield import MultiSelectField
from dateutil.relativedelta import relativedelta
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from core.fields import PhoneField
from core.helpers import get_absolute_url
from permissions import DEFAULT_GROUP
from permissions.models import MetaPermissions
from schedules.models import Period, Shift
from users.current.tokens import RegisterTokenGenerator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    ROLE_REGISTERED = 'registered'  # registered user
    ROLE_CANDIDATE = 'candidate'    # create user profile
    ROLE_APPROVED = 'approved'      # admin approved user profile
    ROLE_TESTED = 'tested'          # user passed all tests
    ROLE_INTERVIEWED = 'interviewed'  # user passed interview
    ROLE_PREPARED = 'prepared'      # user passed training
    ROLE_MAIN_TEAM = 'main'         # user approved for a specific position
    ROLE_RESERVED = 'reserved'      # user in reserve
    ROLE_CHOICES = (
        (ROLE_REGISTERED, _('Зарегистрированный пользователь')),
        (ROLE_CANDIDATE, _('Кандидат в волонтёры')),
        (ROLE_APPROVED, _('Утверждённый кандидат в волонтёры')),
        (ROLE_TESTED, _('Кандидат в волонтеры, прошедший тестирование')),
        (ROLE_INTERVIEWED,
         _('Кандидат в волонтеры, прошедший отборочные процедуры')),
        (ROLE_PREPARED, _('Подготовленный кандидат в волонтеры')),
        (ROLE_MAIN_TEAM, _('Волонтер основного состава')),
        (ROLE_RESERVED, _('Волонтер резерва')),
    )

    username = models.EmailField(_('электронная почта'), unique=True)
    is_staff = models.BooleanField(
        _('сотрудник'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('активный'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('дата регистрации'),
                                       default=timezone.now)
    role = models.CharField(_('роль'), max_length=12, choices=ROLE_CHOICES,
                            default=ROLE_REGISTERED)
    rating = models.PositiveSmallIntegerField(_('рейтинг пользователя'),
                                              default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta(MetaPermissions):
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.profile:
            full_name = '%s %s' % (self.profile.first_name, self.profile.last_name)
            return full_name.strip()

        return ''

    def set_default_group(self):
        """ Set volunteer group for user by default """
        volunteer_group = Group.objects.get(name=DEFAULT_GROUP)
        self.groups.set([volunteer_group])

    @property
    def full_name(self):
        return self.get_full_name()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        if self.profile:
            return self.profile.first_name

        return ''

    @property
    def short_name(self):
        return self.short_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.username], **kwargs)

    def send_activation_email(self, request=None):
        """
        Send activation code by user email
        """
        token = RegisterTokenGenerator().make_token(self)
        activation_link = reverse(
            'user:activation', kwargs={'user_id': self.id, 'token': token},
            request=request
        )
        if not request:
            activation_link = get_absolute_url(activation_link)

        message = '{0}. {1}'.format(
            _('Для подтверждения регистрации пройдите по ссылке'),
            activation_link
        )
        self.email_user(ugettext('Активация пользователя'), message)

    def get_auth_token(self):
        token, created = Token.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()

        return token

    def activate(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    User profile
    """
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, _('мужчина')),
        (GENDER_FEMALE, _('женщина')),
    )
    ENGLISH_ELEMENTARY = 'elementary'
    ENGLISH_INTERMEDIATE = 'intermediate'
    ENGLISH_UPPER_INTERMEDIATE = 'upper intermediate'
    ENGLISH_FLUENT = 'fluent'
    ENGLISH_CHOICES = (
        (ENGLISH_ELEMENTARY, _('начинающий')),
        (ENGLISH_INTERMEDIATE, _('средний')),
        (ENGLISH_UPPER_INTERMEDIATE, _('выше среднего')),
        (ENGLISH_FLUENT, _('свободно')),
    )
    ATTRACT_EXPERIENCE = 'experience'
    ATTRACT_MEETING = 'meeting'
    ATTRACT_HELPING = 'helping'
    ATTRACT_CONTRIBUTING = 'contributing'
    ATTRACT_NEW_INTERESTING = 'new interesting'
    ATTRACT_DISCOVERY = 'discovery'
    ATTRACTING_CHOICES = (
        (ATTRACT_EXPERIENCE, _('получение нового опыта')),
        (ATTRACT_MEETING, _('встречи с новыми людьми')),
        (ATTRACT_HELPING, _('возможность помогать другим')),
        (ATTRACT_CONTRIBUTING, _('вклад в общее дело')),
        (ATTRACT_NEW_INTERESTING, _('новые интересы')),
        (ATTRACT_DISCOVERY, _('открытие для себя новых сфер')),
    )
    BENEFIT_COMMAND_EXPERIENCE = 'command experience'
    BENEFIT_COMMUNICATION = 'communication'
    BENEFIT_PERSONAL_GROWTH = 'personal growth'
    BENEFIT_KNOWLEDGE = 'knowledge'
    BENEFIT_RELATION = 'relation'
    BENEFIT_FOREIGN_LANGUGE = 'foreign language'
    BENEFIT_SEE_EVENT_INSIDE = 'see event inside'
    BENEFIT_PART_OF = 'part of'
    BENEFIT_OPPORTUNITY = 'opportunity'
    BENEFIT_ACCEPTANCE = 'acceptance'
    BENEFIT_RESPECT = 'respect'
    BENEFIT_CHOICES = (
        (BENEFIT_COMMAND_EXPERIENCE,
         _('получение нового уникального опыта и навыков работы в команде')),
        (BENEFIT_COMMUNICATION, _('расширение круга общения')),
        (BENEFIT_PERSONAL_GROWTH, _('личностный рост и самореализация')),
        (BENEFIT_KNOWLEDGE, _('расширение интересов и знаний')),
        (BENEFIT_RELATION, _('новые связи и потенциальные возможности')),
        (BENEFIT_FOREIGN_LANGUGE,
         _('практика иностранных языков и широкое межкультурное общение')),
        (BENEFIT_SEE_EVENT_INSIDE, _('шанс увидеть мероприятие изнутри')),
        (BENEFIT_PART_OF,
         _('возможность почувствовать себя значимой частью мега-события')),
        (BENEFIT_OPPORTUNITY, _('открытие новых перспектив')),
        (BENEFIT_ACCEPTANCE, _('признание окружающих')),
        (BENEFIT_RESPECT, _('гордость и уважение близких')),
    )
    CLOTHES_SIZE_42 = 42
    CLOTHES_SIZE_44 = 44
    CLOTHES_SIZE_46 = 46
    CLOTHES_SIZE_48 = 48
    CLOTHES_SIZE_50 = 50
    CLOTHES_SIZE_52 = 52
    CLOTHES_SIZE_54 = 54
    CLOTHES_SIZE_56 = 56
    CLOTHES_SIZE_58 = 58
    CLOTHES_SIZE_MALE_CHOICES = (
        (CLOTHES_SIZE_42, _('XXS (42)')), (CLOTHES_SIZE_44, _('XS (44)')),
        (CLOTHES_SIZE_46, _('S (46)')), (CLOTHES_SIZE_48, _('M (48)')),
        (CLOTHES_SIZE_50, _('L (50)')), (CLOTHES_SIZE_52, _('XL (52)')),
        (CLOTHES_SIZE_54, _('XXL (54)')), (CLOTHES_SIZE_56, _('2XL (56)')),
        (CLOTHES_SIZE_58, _('3XL (58)')),
    )
    CLOTHES_SIZE_FEMALE_CHOICES = (
        (CLOTHES_SIZE_42, _('XS (42)')), (CLOTHES_SIZE_44, _('S (44)')),
        (CLOTHES_SIZE_46, _('M (46)')), (CLOTHES_SIZE_48, _('L (48)')),
        (CLOTHES_SIZE_50, _('XL (50)')), (CLOTHES_SIZE_52, _('XXL (52)')),
    )
    SHOE_SIZE_34 = 34
    SHOE_SIZE_35 = 35
    SHOE_SIZE_36 = 36
    SHOE_SIZE_37 = 37
    SHOE_SIZE_38 = 38
    SHOE_SIZE_39 = 39
    SHOE_SIZE_40 = 40
    SHOE_SIZE_41 = 41
    SHOE_SIZE_42 = 42
    SHOE_SIZE_43 = 43
    SHOE_SIZE_44 = 44
    SHOE_SIZE_45 = 45
    SHOE_SIZE_46 = 46
    SHOE_SIZE_47 = 47
    SHOE_SIZE_CHOICES = (
        (SHOE_SIZE_34, _('34')), (SHOE_SIZE_35, _('35')),
        (SHOE_SIZE_36, _('36')), (SHOE_SIZE_37, _('37')),
        (SHOE_SIZE_38, _('38')), (SHOE_SIZE_39, _('39')),
        (SHOE_SIZE_40, _('40')), (SHOE_SIZE_41, _('41')),
        (SHOE_SIZE_42, _('42')), (SHOE_SIZE_43, _('43')),
        (SHOE_SIZE_44, _('44')), (SHOE_SIZE_45, _('45')),
        (SHOE_SIZE_46, _('46')), (SHOE_SIZE_47, _('47')),
    )
    INTERESTING_1 = 1
    INTERESTING_2 = 2
    INTERESTING_3 = 3
    INTERESTING_4 = 4
    INTERESTING_CHOICES = (
        (INTERESTING_1, _('1')),
        (INTERESTING_2, _('2')),
        (INTERESTING_3, _('3')),
        (INTERESTING_4, _('4')),
    )
    EVALUATION_1 = 1
    EVALUATION_2 = 2
    EVALUATION_3 = 3
    EVALUATION_4 = 4
    EVALUATION_5 = 5
    EVALUATION_6 = 6
    EVALUATION_7 = 7
    EVALUATION_8 = 8
    EVALUATION_9 = 9
    EVALUATION_10 = 10
    EVALUATION_CHOICES = (
        (EVALUATION_1, _('1')),
        (EVALUATION_2, _('2')),
        (EVALUATION_3, _('3')),
        (EVALUATION_4, _('4')),
        (EVALUATION_5, _('5')),
        (EVALUATION_6, _('6')),
        (EVALUATION_7, _('7')),
        (EVALUATION_8, _('8')),
        (EVALUATION_9, _('9')),
        (EVALUATION_10, _('10')),
    )
    STATUS_INSPECTION = 'inspection'
    STATUS_WORKING = 'working'
    STATUS_APPROVED = 'approved'
    STATUS_CHOICES = (
        (STATUS_INSPECTION, _('на рассмотрении')),
        (STATUS_WORKING, _('на доработке')),
        (STATUS_APPROVED, _('утверждено')),
    )

    user = models.OneToOneField(
        User, related_name='profile', verbose_name=_('пользователь')
    )
    status = models.CharField(
        _('статус'), choices=STATUS_CHOICES, max_length=10,
        default=STATUS_INSPECTION
    )
    updated_at = models.DateTimeField(_('время обновления'), auto_now=True)
    first_name = models.CharField(_('имя'), max_length=30)
    last_name = models.CharField(_('фамилия'), max_length=30)
    middle_name = models.CharField(_('отчество'), max_length=30)
    gender = models.CharField(_('пол'), choices=GENDER_CHOICES, max_length=8)
    birthday = models.DateField(_('дата рождения'))
    birthplace = models.TextField(_('место рождения'))
    passport_number = models.CharField(_('номер паспорта'), max_length=10)
    passport_issued = models.CharField(_('паспорт выдан'), max_length=256)
    passport_issued_date = models.DateField(_('дата выдачи паспорта'))
    registration_address = models.TextField(_('адрес места жительства'))
    residential_address = models.TextField(_('фактическое место жительства'))
    is_studying = models.BooleanField(_('учусь'))
    place_of_study = models.CharField(
        _('место учёбы'), max_length=265, blank=True, null=True
    )
    speciality = models.CharField(
        _('специальность/направление подготовки, курс'), max_length=256,
        blank=True, null=True
    )
    is_working = models.BooleanField(_('работаю'))
    work_place = models.CharField(
        _('место работы'), max_length=256, blank=True, null=True
    )
    position = models.CharField(
        _('должность'), max_length=128, blank=True, null=True
    )
    employer_phone = PhoneField(
        _('контактный телефон работодателя'), blank=True, null=True,
        max_length=20
    )
    phone = PhoneField(_('контактный телефон'), max_length=20)
    english = models.CharField(
        _('владение английским языком'), choices=ENGLISH_CHOICES, max_length=32
    )
    other_language = models.CharField(
        _('владение другими языками'), max_length=256, blank=True, null=True
    )
    has_experience = models.BooleanField(_('опыт волонтёрской деятельности'))
    experience_in_sport_events = models.TextField(
        _('спортивные мероприятия, в которых принимал участие в качестве '
          'волонтера, описание своих выполняемых функций в каждом из '
          'мероприятий'), blank=True, null=True
    )
    experience_in_other_events = models.TextField(
        _('иные мероприятия, в которых принимал участие в качестве волонтера, '
          'описание своих выполняемых функций в каждом из мероприятий'),
        blank=True, null=True
    )
    attracting = models.CharField(
        _('что привлекает в волонтерской деятельности?'),
        choices=ATTRACTING_CHOICES, max_length=32
    )
    lacking = models.TextField(
        _('каких навыков и знаний в волонтерской деятельности не хватает?')
    )
    benefits = MultiSelectField(
        _('что Вы хотите получить от участия в качестве городского волонтера '
          'в Чемпионате мира по футболу FIFA 2018 в России?'),
        choices=BENEFIT_CHOICES, max_choices=4,
    )
    interesting_tourist_information = models.PositiveSmallIntegerField(
        _('информационно-туристическая служба'), choices=INTERESTING_CHOICES
    )
    interesting_transportation = models.PositiveSmallIntegerField(
        _('транспортная служба'), choices=INTERESTING_CHOICES
    )
    interesting_language = models.PositiveSmallIntegerField(
        _('лингвистическая служба'), choices=INTERESTING_CHOICES
    )
    interesting_festival = models.PositiveSmallIntegerField(
        _('фестиваль болельщиков FIFA'), choices=INTERESTING_CHOICES
    )
    strengths = models.TextField(_('описание своих сильных сторон'))
    weaknesses = models.TextField(_('описание своих слабых сторон'))
    hobby = models.TextField(_('описание хобби'))
    evaluation_responsibility = models.PositiveSmallIntegerField(
        _('ответственность'), choices=EVALUATION_CHOICES
    )
    evaluation_stress_resistance = models.PositiveSmallIntegerField(
        _('стрессоустойчивость'), choices=EVALUATION_CHOICES
    )
    evaluation_communicability = models.PositiveSmallIntegerField(
        _('коммуникабельность'), choices=EVALUATION_CHOICES
    )
    evaluation_diligence = models.PositiveSmallIntegerField(
        _('исполнительность'), choices=EVALUATION_CHOICES
    )
    evaluation_goodwill = models.PositiveSmallIntegerField(
        _('доброжелательность'), choices=EVALUATION_CHOICES
    )
    evaluation_teamwork_skills = models.PositiveSmallIntegerField(
        _('умение работать в команде'), choices=EVALUATION_CHOICES
    )
    has_car = models.BooleanField(_('имею автомобиль'))
    car_detail = models.CharField(
        _('категория водительского удостоверения и стаж вождения'),
        max_length=256, blank=True, null=True
    )
    work_period = models.ForeignKey(
        Period, verbose_name=_('период работы во время чемпионата')

    )
    work_shift = models.ForeignKey(
        Shift, verbose_name=_('смена работы во время чемпионата')
    )
    participate_in_other = models.NullBooleanField(
        _('готовы ли Вы принимать участие в других мероприятиях, '
          'осуществляемых в рамках подготовки и проведения игр ЧМ-2018?'),
        blank=True, null=True
    )
    contraindications = models.TextField(
        _('наличие медицинских противопоказаний к осуществлению работы?'),
    )
    clothes_size_male = models.PositiveSmallIntegerField(
        _('мужской размер одежды'), choices=CLOTHES_SIZE_MALE_CHOICES,
        blank=True, null=True
    )
    clothes_size_female = models.PositiveSmallIntegerField(
        _('женский размер одежды'), choices=CLOTHES_SIZE_FEMALE_CHOICES,
        blank=True, null=True
    )
    shoe_size = models.PositiveSmallIntegerField(
        _('размер обуви'), choices=SHOE_SIZE_CHOICES
    )

    class Meta(MetaPermissions):
        verbose_name = _('анкета пользователя')
        verbose_name_plural = _('анкеты пользователей')

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def age(self):
        return relativedelta(date.today(), self.birthday).years

    @property
    def clothes_size(self):
        if self.gender == self.GENDER_MALE:
            return self.clothes_size_male
        else:
            return self.clothes_size_female


class ProfileAttachment(models.Model):
    """
    User profile attachments
    """
    user = models.OneToOneField(
        User, related_name='profile_attachment',
        verbose_name=_('пользователь')
    )
    photo = models.ImageField(_('фото'), upload_to='user/photo/')

    class Meta(MetaPermissions):
        verbose_name = _('файл анкеты пользователя')
        verbose_name_plural = _('файлы анкет пользователей')

    def __str__(self):
        return str(self.id)


class ProfileComment(models.Model):
    profile = models.ForeignKey(Profile, related_name='comments',
                                verbose_name=_('анкета'))
    text = models.TextField(_('Текст'))
    created_at = models.DateTimeField(_('время создания'), auto_now_add=True)

    class Meta(MetaPermissions):
        verbose_name = _('Комментарий к анкете')
        verbose_name_plural = _('Комментарии к анкете')

    def __str__(self):
        return str(self.id)


class Story(models.Model):
    """
    User story
    """
    profile = models.OneToOneField(
        Profile, related_name='story', verbose_name=_('пользователь')
    )
    text = models.TextField(_('текст'))
    about_yourself = models.CharField(_('о себе'), max_length=1024)
    is_public = models.BooleanField(_('опубликовано'), default=False)
    image = models.ImageField(_('фото'), blank=True, null=True)

    class Meta(MetaPermissions):
        verbose_name = _('волонтёрская история')
        verbose_name_plural = _('волонтёрские истории')

    def __str__(self):
        return str(self.id)


class StoryComment(models.Model):
    """
    Admin story comment
    """
    story = models.ForeignKey(
        Story, related_name='comments', verbose_name=_('волонтёрская история')
    )
    text = models.TextField(_('Текст'))
    created_at = models.DateTimeField(_('время создания'), auto_now_add=True)

    class Meta(MetaPermissions):
        verbose_name = _('комментарий волонтёрской истории')
        verbose_name_plural = _('комментарии волонтёрских историй')

    def __str__(self):
        return str(self.id)
