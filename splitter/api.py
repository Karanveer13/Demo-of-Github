from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from splitter.authorization import Profile_Authorization, Profile_Friend_Authorization, Group_Authorization, Group_Friend_Authorization, Expense_Authorization, Expense_Total_Authorization, Settle_Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from .models import Profile, Profile_Friend, Group, Group_Friend, Expense, Expense_Total, Settle
from tastypie.exceptions import BadRequest
from django.db.models import Q
#from django.urls import path

class User_Resource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username']
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        filtering = {
            "username":('exact', 'startswith', 'contains','in')
        }

    # def apply_filters(self, request, applicable_filters):
    #     #     """
    #     #     An ORM-specific implementation of ``apply_filters``.
    #     #
    #     #     The default simply applies the ``applicable_filters`` as ``**kwargs``,
    #     #     but should make it possible to do more advanced things.
    #     """
    #     positive_filters = {}
    #     negative_filters = {}
    #     for lookup in applicable_filters.keys():
    #         if lookup.endswith('__not_eq'):
    #             negative_filters[lookup] = applicable_filters[lookup]
    #         else:
    #             positive_filters[lookup] = applicable_filters[lookup]
    #     print(positive_filters)
    #     print(negative_filters)
    #     return self.get_object_list(request).filter(**positive_filters).exclude(**negative_filters)


    # def apply_filters(self, request, applicable_filters):
    #     """
    #     A hook to alter how the filters are applied to the object list.
    #
    #     This needs to be implemented at the user level.
    #
    #     ``ModelResource`` includes a full working version specific to Django's
    #     ``Models``.
    #     """
    #     positive_filters = {}
    #     negative_filters = {}
    #     print("Hi there")
    #     for lookup in applicable_filters.keys():
    #         print (lookup)
    #         print (applicable_filters.keys())
    #         if lookup.endswith('__not_eq'):
    #             negative_filters[lookup] = applicable_filters[lookup]
    #         else:
    #             positive_filters[lookup] = applicable_filters[lookup]
    #     for key in applicable_filters.keys():
    #         value = applicable_filters[key]
    #         if value[0:7] == 'exclude':
    #             negative_filters["pk"] = value[8:]
    #     print ("Outside loop")
    #     print (positive_filters)
    #     print (negative_filters)
    #     print ("Bye Bye")
    #     print (self.get_object_list(request))
    #     newVar = []
    #     for item in self.get_object_list(request):
    #         print (item)
    #         print(type(item))
    #         if applicable_filters["pk"].x != item:
    #             newVar.append(item)
    #     return newVar
    #     # return self.get_object_list(request).exclude(User.username == "Karanveer")
    #         # .filter(**positive_filters).exclude(**negative_filters)

class Profile_Resource(ModelResource):
    profile_user = fields.ForeignKey(User_Resource, attribute='profile_user', null=True)
    profile_friends = fields.ToManyField(User_Resource, attribute = 'profile_friends', null = True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Profile_Authorization()
        always_return_data = True
        filtering = {
            'profile_user': ALL_WITH_RELATIONS,
            'profile_friends': ALL_WITH_RELATIONS,
        }

class Profile_Friend_Resource(ModelResource):
    profile = fields.ForeignKey(Profile_Resource, attribute='profile', null=True)
    p_friend = fields.ForeignKey(User_Resource, attribute='p_friend', null=True)

    class Meta:
        queryset = Profile_Friend.objects.all()
        resource_name = 'profile_friend'
        allowed_methods = ['get', 'post', 'delete']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Profile_Friend_Authorization()
        always_return_data = True
        filtering = {
            'profile': ALL_WITH_RELATIONS,
            'p_friend': ALL_WITH_RELATIONS,
        }


class Group_Resource(ModelResource):
    creator = fields.ForeignKey(User_Resource, attribute = 'creator', null = True)
    group_friends = fields.ToManyField(Profile_Friend_Resource, attribute = 'group_friends', null = True)
    #group_friends = fields.ToManyField(User_Resource, attribute='group_friends', null=True)
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'group'
        allowed_methods = ['get', 'post', 'put','delete']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Group_Authorization()
        always_return_data = True
        filtering = {
            'creator': ALL_WITH_RELATIONS,
            'group_friends': ALL_WITH_RELATIONS,
            'name': ['exact'],
        }



class Group_Friend_Resource(ModelResource):
    group = fields.ForeignKey(Group_Resource, attribute='group', null=True)
    #friend = fields.ToManyField(User_Resource, attribute='friend', null=True)
    friend = fields.ForeignKey(Profile_Friend_Resource, attribute='friend', null=True)

    class Meta:
        queryset = Group_Friend.objects.all()
        resource_name = 'group_friend'
        allowed_methods = ['get', 'post', 'put','delete']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Group_Friend_Authorization()
        filtering = {
            'group': ALL_WITH_RELATIONS,
            'friend': ALL_WITH_RELATIONS,
            #'user': ALL_WITH_RELATIONS,
        }


class Expense_Resource(ModelResource):
    group = fields.ForeignKey(Group_Resource, attribute='group', null=True)
    payer = fields.ForeignKey(Group_Friend_Resource, attribute='payer', null=True)
    splitters = fields.ToManyField(Group_Friend_Resource, attribute='splitters', null=True)

    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        allowed_methods = ['get', 'post', 'put','delete']
        excludes = ['created_at']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Expense_Authorization()
        filtering = {
            'group': ALL_WITH_RELATIONS,
            'payer': ALL_WITH_RELATIONS,
            'splitters': ALL_WITH_RELATIONS,
        }
    #pass


class Expense_Total_Resource(ModelResource):
    sender = fields.ForeignKey(User_Resource, attribute='sender', null=True)
    receiver = fields.ForeignKey(User_Resource, attribute='receiver', null=True)

    class Meta:
        queryset = Expense_Total.objects.all()
        resource_name = 'expense_total'
        allowed_methods = ['get', 'post', 'put','delete']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Expense_Total_Authorization()
        filtering = {
            'sender': ALL_WITH_RELATIONS,
            'receiver': ALL_WITH_RELATIONS,
        }
    #pass


class Settle_Resource(ModelResource):
    group = fields.ForeignKey(Group_Resource, attribute='group', null=True)
    expense = fields.ForeignKey(Expense_Resource, attribute='expense', null=True)
    sender = fields.ForeignKey(Group_Friend_Resource, attribute='sender', null=True)
    receiver = fields.ForeignKey(Group_Friend_Resource, attribute='receiver', null=True)

    class Meta:
        queryset = Settle.objects.all()
        resource_name = 'settle'
        allowed_methods = ['get', 'post', 'put','delete']
        authentication = ApiKeyAuthentication()
        #authorization = Authorization()
        authorization = Settle_Authorization()
        filtering = {
            'group': ALL_WITH_RELATIONS,
            'expense': ALL_WITH_RELATIONS,
            'sender': ALL_WITH_RELATIONS,
            'receiver': ALL_WITH_RELATIONS,
        }
    #pass



   #     def obj_create(self, bundle, **kwargs):
    #         creater_data = User.objects.get(user=bundle.request.user)
    #         name_data = bundle.data.get('name')
    #         if name_data = '':
    #             raise BadRequest("Group name missing")
    #
    #         group_exist = Group.objects.filter((creater=creater_data) & (queryset['name']=name_data))
    #         if group_exist:
    #             raise BadRequest('Group already present')
    #         Group.objects.create(creater = creater_data, name)
    #
    #         user_prof = Profile.objects.get(user=bundle.request.user)
    #         receiver_data = bundle.data.get('receiver', '')
    #         if receiver_data == '':
    #             raise BadRequest(f"Include receiver.")
    #         receiver_prof = Profile.objects.filter(user__username=receiver_data)
    #         if receiver_prof:
    #             # Check if the FriendRequest exist or not
    #             frnd_req = FriendRequest.objects.filter((Q(sender=user_prof) & Q(receiver=receiver_prof[0])) | (
    #                         Q(sender=receiver_prof[0]) & Q(receiver=user_prof)))
    #             if frnd_req:
    #                 raise BadRequest(f"Already {frnd_req[0].status}")
    #             new_frnd_req = FriendRequest.objects.create(sender=user_prof, receiver=receiver_prof[0])
    #             bundle.obj = new_frnd_req
    #             return bundle
    #         else:
    #             raise BadRequest(f"Invalid username.")
    #
    #     def get_list(self, request, **kwargs):
    #         self.method_check(request, allowed=['get'])
    #         data = self.deserialize(request, request.body)
    #         username = data.get('username')
    #         password = data.get('password')
    #         if username is None or password is None:
    #             raise BadRequest('Please enter a value.')
    #
    #         # Check if the user exists
    #         user = authenticate(username=username, password=password)
    #         if user:
    #             login(request, user)
    #             # Getting the API key,create if doesn't exist
    #             try:
    #                 api_key = ApiKey.objects.get(user=user)
    #                 if not api_key.key:
    #                     api_key.save()
    #             except ApiKey.DoesNotExist:
    #                 # raise BadRequest('Please enter correct details.')
    #                 api_key = ApiKey.objects.create(user=user)
    #
    #             return self.create_response(request, {
    #                 'success': True,
    #                 'username': username,
    #                 'token': api_key.key
    #             })
    #         else:
    #             raise BadRequest("Please enter correct details.")
    #
    # def is_authenticatmycustoed_m(self, request, body):
    #     # "hhdd"
    #     print("sdfs")

    # def prepend_urls(self):
    #     return [
    #         path('haha/', self.wrap_view('new_me'), name="new_me"),
    #     ]
    #
    # def obj_create(self, bundle, **kwargs):
    #     bundle = self.full_hydrate(bundle)
    #     # return super(Group_Resource, self).obj_create(bundle, creator=bundle.request.user)
    #     bundle.obj = self._meta.object_class()
    #
    #     for key, value in kwargs.items():
    #         setattr(bundle.obj, key, value)
    #
    #     bundle = self.full_hydrate(bundle)
    #     return self.save(bundle)
    #
    # def hydrate(self, bundle):
    #     "AUTH"
    #     return bundle

    #pass

    # def obj_get(self, bundle, **kwargs):
    #     print(bundle)
    #     print(bundle.request)
    #     print(bundle.request.headers)
    #     return 123
    #
    # def new_me(self, bundle, **kwargs):
    #     self.is_authenticatmycustoed_m(bundle.headers, bundle.body)
    #     print ("Me hu na");