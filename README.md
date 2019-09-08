# ContentfulORM
***
A Python toolkit for [Contentful](https://www.contentful.com/) to let you create/maintain your Content Type and queries in ORM style.

## Install
***
- To install:
    ```
    pip install git+https://github.com/Phoenix-Chen/ContentfulORM.git
    ```

## Usage
***

### ORM Environment
***
- Create an ORM Environment:
    ```python
    import contentful_management
    from contentful_orm import ORMEnvironment

    # First create an contentful_management.environment.Environment
    client = contentful_management.Client('CONTENTFUL_MANAGEMENT_TOKEN')
    space = client.spaces().find('CONTENTFUL_SPACE_ID')
    environment = space.environments().find('CONTENTFUL_ENVIRONMENT')

    # Then create ORMEnvironment use contentful_management.environment.Environment
    orm_env = ORMEnvironment.from_parent(environment)
    ```

### Content Type Model
***
- Model your content type:
    ```python
    from datetime import datetime
    from contentful_orm.models import Model
    from contentful_orm.fields import ArrayField, BooleanField, DateField, DecimalField, IntegerField, MediaField, ReferenceField, SymbolField, TextField, LocationField
    from contentful_orm.fields.validations import In, Range, Unique, Size, Regex, ImageDimensions, FileSize

    # class name will become content type name
    # class name in camel case will become content type id
    class Person(Model):
        # docstring will become content type description
        """Person model description
        """
        __display_field__ = 'name'

        # Each field need to be a {SomeType}Field from contentful_orm.fields
        # Most of the fields have keyword argument: disabled, localized, omitted, required, validations and default
        # (disabled, localized, omitted and required default to False. validations defaults to []. default defaults to None)
        email = SymbolField(validations=[Unique, Regex('^\\w[\\w.-]*@([\\w-]+\\.)+[\\w-]+$', error_msg='Invalid email address.')], required=True)
        name = SymbolField(localized=True, required=True)
        # ArrayField takes an argument to specify content type
        title = ArrayField(SymbolField(validations=[In(['Manager', 'Seller'], error_msg='Invalid title')]), localized=True)
        age = IntegerField(validations=[Range(min=1, error_msg='age must be a positive integer.')])
        created_date = DateField(default=datetime.now().strftime("%Y-%m-%dT%H:%M-00:00"))

    class Company(Model):
        """Company model description
        """
        __display_field__ = 'name'

        name = SymbolField(validations=[Unique], required=True)
        employees = ArrayField(ReferenceField(model_set={Person}, error_msg='employee has to be a Person entry'))
        address = LocationField()

    class Product(Model):
        """Product model description
        """
        __display_field__ = 'name'

        name = SymbolField(validations=[Unique], required=True)
        description = TextField(localized=True)
        # ReferenceField takes an additional keyword argument model_set to restrict reference content type.
        # (Currently doesn't support reference to the content type itself)
        seller = ReferenceField(model_set={Person, Company}, error_msg="seller has to be a Person or Company entry")
        images = ArrayField(
            MediaField(
                # validations takes a list of contentful_orm.fields.validations
                # See: https://www.contentful.com/r/knowledgebase/validations/ for details
                validations=[
                    ImageDimensions(max_width=12, max_height=12),
                    FileSize(max=40000, error_msg='Maximum file size is 40000 Bytes')
                ]),
            validations=[Size(max=10, error_msg="At most 10 images")]
        )
        sponsored = BooleanField(required=True)
        price = DecimalField(required=True)
    ```
- Create and publish the content type using model:
    ```python
    orm_env.create(Person).publish()
    # Or
    orm_env.create(Person)
    orm_env.publish(Person)
    ```
- Unpublish and delete the content type using model:
    ```python
    orm_env.unpublish(Product)
    orm_env.delete(Product)
    ```
- Add and publish entry:
    ```python
    person1 = orm_env.add(Person(email='a@a.com', name='a', title=['Manager', 'Seller'], age=13)).publish()
    # You can specify entry id or it will randomly generate a UUID
    person2 = orm_env.add(Person(email='b@a.com', name='b', title=['Seller'], age=66), id='S9SN3JWKN3565D').publish()
    person3 = orm_env.add(Person(email='c@a.com', name='c', title=['Manager'], created_date='2019-08-11T00:00-07:00')).publish()
    company1 = orm_env.add(Company(name='Contentful', employees=[person1.to_link().to_json(), person2.to_link().to_json()])).publish()
    # Or
    product1 = Product(
        name='ContentfulORM',
        description='Write your Contentful in ORM style!',
        seller=company1.to_link().to_json(),
        sponsored=True,
        price=0.01
    )
    orm_env.add(product1).publish()
    ```
- Query:
    ```python
    # Query all entries of a content type
    orm_env.query(Person).all()

    # Filter query
    # ORMContentTypeEntriesProxy extends ContentTypeEntriesProxy with additional filter function
    from contentful_orm.operators import all_, limit, select, skip

    # Filter with field names as keyword arguments for exact search
    orm_env.query(Person).filter(email='c@a.com', name='c')

    # Filter with operators, see operators all at: https://github.com/Phoenix-Chen/ContentfulORM/blob/dev/contentful_orm/operators.py
    orm_env.query(Person).filter(all_(title=['Manager', 'seller']), skip(1), limit(100), select('fields.name'))

    # Use combination of both
    orm_env.query(Person).filter(limit(1), name='c')

    ```
- Serialize:
    ```python
    from contentful_orm.serializers import ModelSerializer

    class ProductSerializer(ModelSerializer):
        class Meta:
            model = Product
            # Specify fields to be serialized or use '__all__' for all the fields
            fields = [
                'name',
                'description',
                'price'
            ]

    # Query the entry/entries you want to serialize
    products = orm_env.query(Product).all()

    # Serialize single entry
    serialized_product = ProductSerializer(products[0])

    # Serialize multiple entries
    serialized_products = ProductSerializer(products, many=True)

    # Currently links won't be recursively serialized, in case of circular references.
    ```
