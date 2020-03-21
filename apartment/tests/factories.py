from factory import DjangoModelFactory, Faker, SubFactory
from ..models import Apartment, Category
from authentication.tests.factories import UserProfileFactory


class CategoryFactory(DjangoModelFactory):
    uuid = Faker('uuid4')
    category = Faker('text')

    class Meta:
        model = Category


class ApartmentFactory(DjangoModelFactory):
    uuid = Faker('uuid4')
    title = Faker('text')
    owner = SubFactory(UserProfileFactory)
    title = Faker('text')
    # Stores image url which is store on a cloud
    main_image = Faker('text')
    total_rooms = 1
    available_rooms = 2
    max_guest_number = 5
    description = Faker('text')
    type = SubFactory(CategoryFactory)
    space = Faker('text')
    address = Faker('text')
    city = Faker('text')
    province = Faker('text')
    country = Faker('text')
    number_of_bathrooms = 5
    price = 45
    discount = 0.85
    amenities = Faker('text')  # String separated by ,
    extras = Faker('text')     # String separated by ,
    rules = Faker('text')      # String separated by ,
    is_active = True
    is_verified = False  # Used for commercial properties
    unavailable_from = Faker('date')
    unavailable_to = Faker('date')
    min_nights = 4
    max_nights = 6
    check_in = Faker('text')   # Timezone is Africa/Kigali
    check_out = Faker('text')  # Timezone is Africa/Kigali
    is_available = Faker('boolean')
    created_at = Faker('date_time')

    class Meta:
        model = Apartment
