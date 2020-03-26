from django.contrib.auth.models import User
from authentication.models import UserProfile
from factory import DjangoModelFactory, Faker, SubFactory


class UserFactory(DjangoModelFactory):
    email = Faker('email')
    username = Faker('text')
    password = 'a-fake-password'
    is_superuser = Faker('boolean')
    is_staff = False
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    class Meta:
        model = User


class UserProfileFactory(DjangoModelFactory):
    uuid = Faker('uuid4')
    user = SubFactory(UserFactory)
    address = Faker('text')
    description = Faker('text')
    resident_country = Faker('text')
    origin_country = Faker('text')
    phone = Faker('text')
    profile_image = Faker('text')
    national_id = Faker('text')
    is_verified = True
    passport = Faker('text')
    is_active = True
    is_admin = True
    created_at = Faker('date_time')
    modified_at = Faker('date_time')

    class Meta:
        model = UserProfile
