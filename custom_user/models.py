from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not phone:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            phone = phone,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            phone = phone,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'010\d{7,8}', message=_('010으로 시작하는 10자리 혹시 11자리 숫자'))
    phone = models.CharField(
        verbose_name=_('핸드폰 번호'),
        max_length=11,
        unique=True,
        validators=[phone_regex,]
    )
    name = models.CharField(
        verbose_name=_('이름'),
        max_length=10,
    )
    is_active = models.BooleanField(
        verbose_name=_('활성'),
        default=False,
    )
    is_admin = models.BooleanField(
        verbose_name=_('관리자'),
        default=False,
    )
    date_joined = models.DateTimeField(
        verbose_name=_('가입시간'),
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name',]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Dose the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Dose the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_admin

    get_full_name.short_description = _('Full name')
