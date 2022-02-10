"""
To have a independent app, we defined our Generic serailizer here too.
We are following this document to define serializer for Generic serailizer:
https://www.django-rest-framework.org/api-guide/relations/#generic-relationships

In 'FileUploadRelatedField we get 'request' object from serializer context. Read this document:
https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context
"""
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import FileUpload, Ticketing, Answer
from accounts.serializers import UserSerializer


class FileUploadRelatedField(serializers.HyperlinkedRelatedField):
    """
    A custom field to use for the `FileUpload_object` generic relationship.
    """
    def to_representation(self, value):
        """We are using serializer context to get 'request' that we need."""
        request = self.context.get('request', None)
        if isinstance(value, Ticketing):
            serializer = TicketingSerializer(value, context={'request': request})
        elif isinstance(value, Answer):
            serializer = AnswerSerializer(value, context={'request': request})
        else:
            return {'error': 'This object is not Json serializer'}
        return serializer.data


class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
# class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for FileUpload"""
    url = serializers.HyperlinkedIdentityField(view_name='ticketing:fileupload-detail')
    # If we don't set 'content_type' field we won't have any problem!
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), many=False)
    # Only if we had ManyToMany relations we have to set 'many=True'. Otherwise it's not neccessary but not wrong either #
    # content_object = FileUploadRelatedField(read_only=True)
    content_object = FileUploadRelatedField(read_only=True, view_name='ticketing:fileupload-detail')
    class Meta:
        model = FileUpload
        fields = '__all__'


class TicketingSerializer(serializers.HyperlinkedModelSerializer):
# class TicketingSerializer(serializers.ModelSerializer):
    """Serializer for Ticketing."""
    url = serializers.HyperlinkedIdentityField(view_name='ticketing:ticketing-detail')

    user = UserSerializer(read_only=True, many=False)
    # It's better to set 'allow_null=True' fields 'default=None' arguement also
    user_obj = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                                  write_only=True,
                                                  allow_null=True,
                                                  default=None)
    # We can also write above command as HyperlinkedRelatedField like below line (but no recommended!):
    # user_obj = serializers.HyperlinkedRelatedField(queryset=get_user_model().objects.all(), write_only=True, view_name='accounts:user-detail', allow_null=True, default=None)
    """
    If we don't want to have INNER RELATIONS in our serializer, we just need to define our serializer like below line
    and completly igonre 'user_obj' field:
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=False, allow_null=True)
    """
    username = serializers.CharField(allow_null=True,
                                     write_only=True,
                                     help_text='Based on authentication method enter username, email or phone',
                                     default=None)

    class Meta:
        model = Ticketing
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Overriding 'create' method to support methods to create Ticketing object with DRF GUI or from
        client side technologies
        """

        # This is a simple example to show how 'serializer context work!S
        # print(self.context)
        # print(self.context.keys())
        # self.context['name'] = 'ehsan'
        # print(self.context)
        # print(self.context.keys())
        # exit()

        # First we should pop additional fields from validated data to prevent 'TypeError'
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)
        # 1- Create ticket from DFR GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            ticket = Ticketing.objects.create(**validated_data)
            return ticket
        # 2- Create ticket with client-server architecture
        if username:
            q_user = get_user_model().objects.filter(username=username)
            if q_user.exists():
                user = q_user.last()
                validated_data.update({'user': user})
                ticket = Ticketing.objects.create(**validated_data)
                return ticket
            else:
                raise ValidationError('Error: There is no user with this username')
        raise ValidationError(detail={'Error': 'No user object or username entered!'})
    
    def update(self, instance, validated_data):
        """
        Overriding 'update' method to support methods to update Ticketing object with DRF GUI or from
        client side technologies
        """
        # First we should pop additional fields from validated data to prevent 'TypeError'
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # 1- Update ticket with DRF GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            Ticketing.objects.filter(id=instance.id).update(**validated_data)
            # https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db
            instance.refresh_from_db()
            return instance

        # 2- Update ticket with client-server architecture
        elif username:
            user_q = get_user_model().objects.filter(username=username)
            if user_q.exists():
                user = user_q.first()
                validated_data.update({'user': user})
                Ticketing.objects.filter(id=instance.pk).update(**validated_data)
                instance.refresh_from_db()
                return instance
            else:
                raise ValidationError(detail=f'No user found with this username: {username}')

        # If No username or user_obj selected to update the instance
        raise ValidationError({'Error': 'No username or user object found!'})


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
# class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Answer model
    https://www.django-rest-framework.org/api-guide/fields/#write_only
    """
    url = serializers.HyperlinkedIdentityField(view_name='ticketing:answer-detail')
    """
    # This field used for ListField
    files = serializers.ListField(
                                  child=serializers.FileField(
                                                              max_length=100000,
                                                              allow_empty_file=False,
                                                              use_url=False)
                                 )
    """
    # file = serializers.FileField()
    # caption = serializers.CharField()
    # files = FileUploadRelatedField(queryset=FileUpload.objects.all())

    # Following three fields used to show or get 'ticket' field on model
    ticketing = TicketingSerializer(read_only=True, many=False)
    ticketing_obj = serializers.PrimaryKeyRelatedField(queryset=Ticketing.objects.all(),
                                                       many=False,
                                                       write_only=True,
                                                       allow_null=True,
                                                       default=None)
    ticket_id = serializers.UUIDField(write_only=True,
                                      allow_null=True,
                                      help_text='For client_server architecture method',
                                      default=None)
    # Followin three fields used to show or get 'user' field on model
    user = UserSerializer(read_only=True, many=False)
    user_obj = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                                  many=False,
                                                  write_only=True,
                                                  allow_null=True,
                                                  default=None)
    username = serializers.CharField(write_only=True,
                                     allow_null=True,
                                     help_text='Based on authentication method enter username, email or phone',
                                     default=None)


    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Overriding 'create' method to support methods to create Answer object with DRF GUI or from
        client side technologies
        """
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        ticket_id = validated_data.pop('ticket_id', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # Because we have two foreign keys, we should process two fields:
        # 1/2: PROCESS 'ticket' field:

        # 1- Create Answer with standard DRF GUI - Note that we should not return anything yet:
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            # We set 'ticket' data to 'validation_data' with ticket field and do not return anything
            # before 'user' field would be proccessed.
               
        # 2- Create Answer with ticket_id (client-server architecture)
        elif ticket_id:
            queryset = Ticketing.objects.filter(ticket_id=ticket_id)
            if queryset.exists():
                ticketing = queryset.first()
                validated_data.update({'ticketing': ticketing})
            else:
                raise ValidationError(detail=f'No ticket found with this id: {ticket_id}')

        # If there is no ticket_id or ticket object raise Error:
        else:
            raise ValidationError(detail={'error': 'No Ticket found'}, code=HTTP_400_BAD_REQUEST)
        
        # 2/2: Proccess 'user' field

        # 1- Create Answer with standard DRF GUI:
        if user_obj:
            validated_data.update({'user': user_obj})
            answer = Answer.objects.create(**validated_data)
            return answer
            
        # 2- Create Answer with username (client-server architecture)
        elif username:
            queryset = get_user_model().objects.filter(username=username)
            if queryset.exists():
                user = queryset.first()
                validated_data.update({'user': user})
                answer = Answer.objects.create(**validated_data)
                return answer
            else:
                raise ValidationError(detail=f'No user found with this username: {username}')
        
        # If there is no username or user object raise Error:
        else:
            raise ValidationError(detail={'error': 'No user found'}, code=HTTP_400_BAD_REQUEST)
    
    def update(self, instance, validated_data):
        """
        Overriding 'update' method to support methods to update Answer object with DRF GUI or from
        client side technologies
        """
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        ticket_id = validated_data.pop('ticket_id', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # Because we have two foreign keys, we should process two fields:
        # 1/2: PROCESS 'ticket' field:

        # 1- Update Answer with standard DRF GUI - We should not return anything yet:
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            Answer.objects.filter(id=instance.pk).update(**validated_data)

        # 2- Update Answer with ticket_id (client-server architecture) - We should not return anything yet:
        elif ticket_id:
            queryset = Ticketing.objects.filter(ticket_id=ticket_id)
            if queryset.exists():
                ticketing = queryset.first()
                validated_data.update({'ticketing': ticketing})
            else:
                raise ValidationError(detail=f'No ticket found with this id: {ticket_id}')

        # If no ticket object or ticket_id found, raise the following error:
        else:
            raise ValidationError(detail={'error': 'No Ticket found'}, code=HTTP_400_BAD_REQUEST)

        # 2/2: PROCESS 'user' field:

        # 1- Update Answer with standard DRF GUI
        if user_obj:
            validated_data.update({'uesr': user_obj})
            Answer.objects.filter(id=instance.pk).update(**validated_data)
            'https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db'
            instance.refresh_from_db()
            return instance

        # 2- Update Answer with ticket_id (client-server architecture)
        elif username:
            queryset = get_user_model().objects.filter(username=username)
            if queryset.exists():
                user = queryset.first()
                validated_data.update({'user': user})
                Answer.objects.filter(id=instance.pk).update(**validated_data)
                instance.refresh_from_db()
                return instance
            else:
                raise ValidationError(detail=f'No user found with this username: {username}')

        # If no user object or username found, raise the following error:
        else:
            raise ValidationError(detail={'error': 'No user found'}, code=HTTP_400_BAD_REQUEST)

    """
    # This method used for ListField
    def create(self, validated_data):
        files=validated_data.pop('files')
        answer=Answer.objects.create(**validated_data)
        for f in files:
            file=FileUpload.objects.create(f)
            answer.files.add = file
        answer.save()
        return answer
    """
