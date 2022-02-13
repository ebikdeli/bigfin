"""
Remember that the data we send to a Serializer 'data' argument must be JSON-able.
To have a independent app, we defined our Generic serializer here too.
We are following this document to define serializer for Generic serailizer:
https://www.django-rest-framework.org/api-guide/relations/#generic-relationships
https://docs.djangoproject.com/en/4.0/ref/contrib/contenttypes/#methods-on-contenttype-instances

We use nested serializer in this module rather heavily. Read this documents:
https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations

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


def files_upload_create_api(files_upload, parent_instance=False):
    """
    This function get all data in 'files_upload' field in TicketingSerializer and AnswerSerializer and create
    new files for them (if any data received for this optional field). This function used for API.
    'files_upload' is a dictionary consists of data received by FileUploadSerializer from client.
    'parent_instance' is a model instance that could be Answer or Ticketing.
    """
    for file_data in files_upload:
        FileUpload.objects.create(**file_data)


def files_upload_create_gui(files_upload_list, parent_instance):
    """
    This function is comparable to 'files_upload_create_api' but used for DRF GUI
    'file_upload_list' consists of a list that each of its elements is a 2 elements tuple: first argument is
    file obj and second element is the caption for the file.
    """
    for file_data in files_upload_list:
        data = {'file': file_data[0], 'caption': file_data[1]}
        if data['file']:
            parent_instance.files.create(**data)
            parent_instance.save()


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
    """
    To use 'FileUploadSerializer' as a field type in 'TicketingSerializer' or 'AnswerSerializer' we must not use
    'FileUploadRelatedField' in 'FileUploadSerializer' because of 'to_representation' method that uses both
    TicketingSerializer and AnswerSerializer in its body in this causes of circular recursion uses and program stops working.
    To fix the problem we can use below command for 'content_object' field to stops recursion:
    # content_object = serializers.HyperlinkedRelatedField(read_only=True, view_name='ticketing:fileupload-detail')
    """

    class Meta:
        model = FileUpload
        fields = '__all__'


class TicketingSerializer(serializers.HyperlinkedModelSerializer):
# class TicketingSerializer(serializers.ModelSerializer):
    """Serializer for Ticketing."""
    url = serializers.HyperlinkedIdentityField(view_name='ticketing:ticketing-detail')

    # This field only show 'answers' urls that related to current 'ticketing' instance (See 'ticketing' field related_name in the Answer model)
    ticketing_answers = serializers.HyperlinkedRelatedField(view_name='ticketing:answer-detail',read_only=True, many=True)
    """
    Below 'ticketing_answer' field shows all data about 'answers' that related to current 'ticketing' instance. BUT because AnswerSerializer
    is defined under TicketingSerializer we have to use 'serializer inheritance' to do that and currently it is out of
    respect to this work!
    # ticketing_answer = AnswerSerializer(read_only=True, many=True)
    """
    files = serializers.HyperlinkedRelatedField(view_name='ticketing:fileupload-detail', many=True, read_only=True)
    """
    # files = FileUploadSerializer(read_only=True, many=True)
    To use FileUploadSerializer in TicketSerializer or AnswerSerializer we can't let Both of these serializer to
    be used for any reason in FileUploadSerializer. On this matter we use both of these serializer in the
    'to_representation' method of custom field in FileUploadSerializer. So if we use this serializer we get this error:
    RecursionError: maximum recursion depth exceeded while calling a Python object
    """
    user = UserSerializer(read_only=True, many=False)
    # It's better to set 'allow_null=True' fields 'default=None' arguement also
    user_obj = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                                  write_only=True,
                                                  allow_null=True,
                                                  # default=None
                                                  )
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
                                     # default=None
                                     )
    # 'files_upload' field is useing 'nested serializer' as 'child' for the list field. When we send data to this
    # this field, we should put data in a 'list' and the data should be just like the data we send to
    # FileUploadSerializer. In 'test_api' module we done it.
    files_upload = serializers.ListField(child=FileUploadSerializer(),
                                         allow_null=True,
                                         default=None,
                                         write_only=True,
                                         required=False)
    # For better user experience for 'Frontend developer' we can define a new Serializer just like FileUploadSerializer
    # but with better named fields (eg: replace 'content_type' with 'model_name') then in the backend process these fields

    # These fields used for DRF GUI to create files (FileUploadModel) (Because it's not support ListField) #
    file_1 = serializers.FileField(allow_null=True, default=None, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_1 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    file_2 = serializers.FileField(allow_null=True, default=None, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_2 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    file_3 = serializers.FileField(allow_null=True, default=None, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_3 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)

    class Meta:
        model = Ticketing
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Overriding 'create' method to support methods to create Ticketing object with DRF GUI or from
        client side technologies
        """
        # This is a simple example to show how 'serializer context' works!
        # print(self.context)
        # print(self.context.keys())
        # self.context['name'] = 'ehsan'
        # print(self.context)
        # print(self.context.keys())
        # exit()

        # First we should pop additional fields from validated data to prevent 'TypeError'
        files_upload = validated_data.pop('files_upload', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # get all 'files_<number>' and 'caption_<number>' data and process it in 'files_upload_create_gui'
        files_data_list = list()
        file_1 = validated_data.pop('file_1', None)
        caption_1 = validated_data.pop('caption_1', None)
        files_data_list.append((file_1, caption_1))
        file_2 = validated_data.pop('file_2', None)
        caption_2 = validated_data.pop('caption_2', None)
        files_data_list.append((file_2, caption_2))
        file_3 = validated_data.pop('file_3', None)
        caption_3 = validated_data.pop('caption_3', None)
        files_data_list.append((file_3, caption_3))

        # 1- Create ticket from DFR GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            ticket = Ticketing.objects.create(**validated_data)
            # If any 'file_<number>' field is not None, create new file for the field:
            if file_1 or file_2 or file_3:
                files_upload_create_gui(files_data_list, ticket)
            return ticket

        # 2- Create ticket with client-server architecture
        if username:
            q_user = get_user_model().objects.filter(username=username)
            if q_user.exists():
                user = q_user.last()
                validated_data.update({'user': user})
                ticket = Ticketing.objects.create(**validated_data)

                # Before returning newly created answer, we create attached files to the ticket's 'files' field (If any)
                if files_upload:
                    files_upload_create_api(files_upload, parent_instance=ticket)
                return ticket
            else:
                raise ValidationError('Error: There is no user with this username')
        # If no username entered or no user_obj selected, raise this error
        raise ValidationError(detail={'Error': 'No user object or username entered!'})
    
    def update(self, instance, validated_data):
        """
        Overriding 'update' method to support methods to update Ticketing object with DRF GUI or from
        client side technologies
        """
        # First we should pop additional fields from validated data to prevent 'TypeError'
        files_upload = validated_data.pip('files_upload', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # get all 'files_<number>' and 'caption_<number>' data and process it in 'files_upload_create_gui'
        files_data_list = list()
        file_1 = validated_data.pop('file_1', None)
        caption_1 = validated_data.pop('caption_1', None)
        files_data_list.append((file_1, caption_1))
        file_2 = validated_data.pop('file_2', None)
        caption_2 = validated_data.pop('caption_2', None)
        files_data_list.append((file_2, caption_2))
        file_3 = validated_data.pop('file_3', None)
        caption_3 = validated_data.pop('caption_3', None)
        files_data_list.append((file_3, caption_3))

        # 1- Update ticket with DRF GUI
        if user_obj:
            validated_data.update({'user': user_obj})
            Ticketing.objects.filter(id=instance.id).update(**validated_data)
            # https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db
            instance.refresh_from_db()

            # If any 'file_<number>' field is not None, create new file for the field:
            if file_1 or file_2 or file_3:
                files_upload_create_gui(files_data_list, instance)
            return instance

        # 2- Update ticket with client-server architecture
        elif username:
            user_q = get_user_model().objects.filter(username=username)
            if user_q.exists():
                user = user_q.first()
                validated_data.update({'user': user})
                Ticketing.objects.filter(id=instance.id).update(**validated_data)
                instance.refresh_from_db()
                # Before returning updated ticket, we create attached files to the ticket's 'files' field (If any)
                if files_upload:
                    files_upload_create_api(files_upload, parent_instance=instance)
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
    # files = FileUploadRelatedField(#queryset=FileUpload.objects.all(),
    # Below field 'files' only show the FileUpload instances that related to current answer instance. #
    files = serializers.HyperlinkedRelatedField(# queryset=FileUpload.objects.all(),
                                                many=True,
                                                view_name='ticketing:fileupload-detail',
                                                allow_null=True,
                                                default=None,
                                                read_only=True)
    # 'files_upload' field is useing 'nested serializer' as 'child' for the list field. When we send data to this
    # this field, we should put data in a 'list' and the data should be just like the data we send to
    # FileUploadSerializer. In 'test_api' module we done it.
    files_upload = serializers.ListField(child=FileUploadSerializer(),
                                         allow_null=True,
                                         default=None,
                                         write_only=True,
                                         required=False)
    # For better user experience for 'Frontend developer' we can define a new Serializer just like FileUploadSerializer
    # but with better named fields (eg: replace 'content_type' with 'model_name') then in the backend process these fields
    """
    files = serializers.ListField(child=FileUploadRelatedField(queryset=FileUpload.objects.all(), view_name='ticketing:fileupload-detail'),
                                  allow_null=True,
                                  default=None,
                                  )
    """
    # Following three fields used to show or get 'ticket' field on model
    ticketing = TicketingSerializer(read_only=True, many=False)
    ticketing_obj = serializers.PrimaryKeyRelatedField(queryset=Ticketing.objects.all(),
                                                       many=False,
                                                       write_only=True,
                                                       allow_null=True,
                                                       # default=None
                                                       )
    ticket_id = serializers.UUIDField(write_only=True,
                                      allow_null=True,
                                      help_text='For client_server architecture method',
                                      # default=None
                                      )
    # Following three fields used to show or get 'user' field on model
    user = UserSerializer(read_only=True, many=False)
    user_obj = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),
                                                  many=False,
                                                  write_only=True,
                                                  allow_null=True,
                                                  #default=None
                                                  )
    username = serializers.CharField(write_only=True,
                                     allow_null=True,
                                     help_text='Based on authentication method enter username, email or phone',
                                     # default=None
                                     )
    # These fields used for DRF GUI to create files (FileUploadModel) (Because it's not support ListField) #
    file_1 = serializers.FileField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_1 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    file_2 = serializers.FileField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_2 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    file_3 = serializers.FileField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)
    caption_3 = serializers.CharField(allow_null=True, required=False, help_text='Used for DRF GUI (optional)', write_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Overriding 'create' method to support methods to create Answer object with DRF GUI or from
        client side technologies
        """
        # https://docs.djangoproject.com/en/4.0/ref/models/meta/
        # This is how model instance '._meta' works:
        # print(type(Answer._meta))
        # print(type(Answer._meta.fields), '\n',Answer._meta.fields)
        # print(type(Answer._meta.fields[4]))
        # answer = Answer.objects.last()
        # print(answer._meta.fields)

        files_upload = validated_data.pop('files_upload', None)
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        ticket_id = validated_data.pop('ticket_id', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # get all 'files_<number>' and 'caption_<number>' data and process it in 'files_upload_create_gui'
        files_data_list = list()
        file_1 = validated_data.pop('file_1', None)
        caption_1 = validated_data.pop('caption_1', None)
        files_data_list.append((file_1, caption_1))
        file_2 = validated_data.pop('file_2', None)
        caption_2 = validated_data.pop('caption_2', None)
        files_data_list.append((file_2, caption_2))
        file_3 = validated_data.pop('file_3', None)
        caption_3 = validated_data.pop('caption_3', None)
        files_data_list.append((file_3, caption_3))

        # Because we have two foreign keys, we should process two fields:
        # 1/2: PROCESS 'ticket' field:

        # 1- Create Answer with standard DRF GUI - Note that we should not return anything yet:
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            # We set 'ticket' data to 'validation_data' with ticket field and do not return anything
            # before 'user' field would be proccessed

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
            # If any 'file_<number>' field is not None, create new file for the field:
            if file_1 or file_2 or file_3:
                files_upload_create_gui(files_data_list, answer)
            return answer

        # 2- Create Answer with username (client-server architecture)
        elif username:
            queryset = get_user_model().objects.filter(username=username)
            if queryset.exists():
                user = queryset.first()
                validated_data.update({'user': user})
                answer = Answer.objects.create(**validated_data)

                # Before returning newly created answer, we create attached files to the answer's 'files' field (If any)
                if files_upload:
                    files_upload_create_api(files_upload, parent_instance=answer)
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
        files_upload = validated_data.pop('files_upload', None)
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        ticket_id = validated_data.pop('ticket_id', None)
        user_obj = validated_data.pop('user_obj', None)
        username = validated_data.pop('username', None)

        # get all 'files_<number>' and 'caption_<number>' data and process it in 'files_upload_create_gui'
        files_data_list = list()
        file_1 = validated_data.pop('file_1', None)
        caption_1 = validated_data.pop('caption_1', None)
        files_data_list.append((file_1, caption_1))
        file_2 = validated_data.pop('file_2', None)
        caption_2 = validated_data.pop('caption_2', None)
        files_data_list.append((file_2, caption_2))
        file_3 = validated_data.pop('file_3', None)
        caption_3 = validated_data.pop('caption_3', None)
        files_data_list.append((file_3, caption_3))

        # Because we have two foreign keys, we should process two fields:
        # 1/2: PROCESS 'ticket' field:

        # 1- Update Answer with standard DRF GUI - We should not return anything yet:
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            Answer.objects.filter(id=instance.id).update(**validated_data)

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
            validated_data.update({'user': user_obj})
            Answer.objects.filter(id=instance.id).update(**validated_data)
            'https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db'
            instance.refresh_from_db()
            # If any 'file_<number>' field is not None, create new file for the field:
            if file_1 or file_2 or file_3:
                files_upload_create_gui(files_data_list, instance)
            return instance

        # 2- Update Answer with ticket_id (client-server architecture)
        elif username:
            queryset = get_user_model().objects.filter(username=username)
            if queryset.exists():
                user = queryset.first()
                validated_data.update({'user': user})
                Answer.objects.filter(id=instance.id).update(**validated_data)
                instance.refresh_from_db()

                # Before returning newly created answer, we create attached files to the answer's 'files' field (If any)
                if files_upload:
                    files_upload_create_api(files_upload, parent_instance=instance)
                return instance
            else:
                raise ValidationError(detail=f'No user found with this username: {username}')

        # If no user object or username found, raise the following error:
        else:
            raise ValidationError(detail={'error': 'No user found'}, code=HTTP_400_BAD_REQUEST)
