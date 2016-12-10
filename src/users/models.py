from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from volunteer.fields import PhoneField


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
    username = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.profile.first_name, self.profile.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.profile.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.username], **kwargs)

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


    user = models.OneToOneField(User, related_name='profile')
    first_name = models.CharField(_('имя'), max_length=30)
    last_name = models.CharField(_('фамилия'), max_length=30)
    middle_name = models.CharField(_('отчество'), max_length=30)
    gender = models.CharField(_('пол'), choices=GENDER_CHOICES, max_length=8)
    birthday = models.DateField(_('дата рождения'))
    birthplace = models.TextField(_('место рождения'))
    passport_number = models.PositiveSmallIntegerField(_('номер паспорта'))
    passport_issued = models.CharField(_('паспорт выдан'), max_length=256)
    passport_issued_date = models.DateField(_('дата выдачи паспорта'))
    registration = models.TextField(_('адрес места жительства'))
    residence = models.TextField(_('фактическое место жительства'))
    place_of_study = models.CharField(_('место учёбы'), max_length=265)
    speciality = models.CharField(
        _('специальность/направление подготовки, курс'), max_length=256
    )
    working = models.BooleanField(_('работаю'))
    work_place = models.CharField(_('место работы'), max_length=256)
    position = models.CharField(_('должность'), max_length=128)
    employer_phone = PhoneField(
        _('контактный телефон работодателя'), blank=True
    )
    phone = PhoneField(_('контактный телефон'))
    english = models.CharField(
        _('владение английским языком'), choices=ENGLISH_CHOICES, max_length=32
    )
    # TODO: may be blank
    other_language = models.CharField(
        _('владение другими языками'), max_length=256
    )
    has_volunteer_experience = models.BooleanField(
        _('опыт волонтёрской деятельности')
    )
    # TODO: may be blank if has_volunteer_experience field is false
    experience_in_sport_events = models.TextField(
        _('Спортивные мероприятия, в которых принимал участие в качестве '
          'волонтера, описание своих выполняемых функций в каждом из '
          'мероприятий')
    )
    # TODO: may be blank
    experience_in_other_events = models.TextField(
        _('Иные мероприятия, в которых принимал участие в качестве волонтера, '
          'описание своих выполняемых функций в каждом из мероприятий')
    )
    attracting = models.CharField(
        _('Что привлекает в волонтерской деятельности?'),
        choices=ATTRACTING_CHOICES, max_length=32
    )


    # photo = models.ImageField('Фото', upload_to='user/photo/')
    # accredited_photo = models.ImageField('Фото', upload_to='user/acc_photo/')


    # Пол* (тип: select)
    # Почтовый индекс* (тип: input) (ссылка на возможность найти по адресу свой индекс)
    # Место учебы* (тип: input + select) (возможность выбрать из списка или если их заведение не представлено, самостоятельно заполнить)
    # Специальность/направление подготовки* (тип: input)
    # Не работаю (тип: checkbox, в случае выбора скрываются поля “место работы”, “должность”, “адрес места работы”)
    # Место работы* (тип: input)
    # Должность* (тип: input)
    # Контактные телефоны работодателя (тип: input)
    # Ссылка на профиль в “Вконтакте” (тип: input)
    # Ссылка на профиль в “Одноклассники” (тип: input)
    # Ссылка на профиль в “Facebook” (тип: input)
    # Ссылка на профиль в “Twitter” (тип: input)
    # Владение английским языком* (тип: select) (с пояснением уровня подготовки)
    # Владение другими иностранными языками* (тип: textarea)
    # Спортивные мероприятия, в которых принимал участие в качестве волонтера, описание своих выполняемых функций в каждом из мероприятий * (тип: textarea)
    # Иные мероприятия, в которых принимал участие в качестве волонтера, описание своих выполняемых функций в каждом из мероприятий * (тип: textarea)
    # Что именно привлекает в волонтерской деятельности?* (тип: select)
    # Каких навыков и знаний в волонтерской деятельности не хватает?* (тип: textarea)
    # Что Вы хотите получить от участия в качестве городского волонтера в Чемпионате мира по футболу FIFA 2018 в России? (укажите не более 4-х вариантов)* (тип: select)
    # Описание своих сильных сторон* (тип: textarea)
    # Описание своих слабых сторон* (тип: textarea)
    # Описание хобби? * (тип: textarea)
    # Оценить себя по шкале от 1 до 10 по указанным качествам * (тип: select)
    # Выбор желаемого функционального направления деятельности волонтера на ЧМ 2018* :(тип: select)
    # (со справкой по каждому направлению, не более трех вариантов)
    # Выбор периода работы во время Чемпионата* (тип: select)
    # Выбор смены работы во время Чемпионата* (тип: select)
    # Наличие каких-либо медицинских противопоказаний по состоянию здоровья к осуществлению работы? * (тип: textarea)
    # Иные значимые сведения (тип: textarea)
    # Сведения о ближайших родственниках* (множественный тип)
    # Указание размера одежды (жен) * (тип: select)
    # Указание размера одежды (муж) * (тип: select)
    # Указание размера обуви * (тип: textarea)

    class Meta:
        verbose_name = _('профиль пользователя')
        verbose_name_plural = _('профили пользователей')

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
