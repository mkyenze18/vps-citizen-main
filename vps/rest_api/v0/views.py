from http.client import responses
from pickle import FALSE
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from reportlab.pdfgen import canvas


# Create your views here.

# TODO https://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from .serializers import SnippetSerializer

# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)

# TODO https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#pulling-it-all-together
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timezone, date
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer


# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework import generics

# TODO https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#adding-optional-format-suffixes-to-our-urls
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mass_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator


from vps.models import (
    Gender, Country, IPRS_Person, PoliceStation, Rank, PoliceOfficer,
    OccurrenceCategory, OccurrenceCategoryInput, Occurrence, OccurrenceDetail, Reporter, UnregisteredReporter,
    PoliceCell, Warrant_of_arrest, Arrestee, Accomplice, Gang, Next_of_kin,
    MugShots, FingerPrints,
    Offense, ChargeSheet_Person, ChargeSheet, CourtFile,
    EvidenceCategory, Evidence, EvidenceItemCategory, EvidenceItemImage,
    RegisteredVehicle, InsurancePolicy, DrivingLicense, TrafficOffender, Vehicle, Inspection, TrafficSubject,
    UnregisteredTrafficSubject,
    OccurrenceCounter
)
from helpers.file_system_manipulation import delete_file_in_media, delete_folder_in_media
from vps.rest_api.v0.common.views import BaseDetailView, BaseListView, ImageBaseDetailView, ImageBaseListView
from .serializers import (UserSerializer,
    CountrySerializer, GenderSerializer, IPRS_PersonSerializerRead, IPRS_PersonSerializerWrite, RankSerializer,
    PoliceStationSerializer, PoliceOfficerReadSerializer, PoliceOfficerWriteSerializer,
    OccurrenceCategorySerializer, OccurrenceCategoryInputSerializer, OccurrenceReadSerializer, OccurrenceWriteSerializer,
    OccurrenceDetailSerializer, ReporterSerializer, UnregisteredReporterSerializer,
    PoliceCellSerializer, WarrantofarrestSerializer, ArresteeReadSerializer, ArresteeWriteSerializer, AccompliceSerializer, GangSerializer,
    NextofkinSerializer, MugShotsSerializer, FingerPrintsSerializer,
    OffenseSerializer, ChargeSheetSerializer, ChargeSheetPersonSerializer, CourtFileSerializer,
    EvidenceCategorySerializer, EvidenceItemCategorySerializer, EvidenceReadSerializer, EvidenceWriteSerializer, EvidenceItemImageSerializer,
    RegisteredVehicleSerializer, InsurancePolicySerializer, DrivingLicenseSerializer, TrafficOffenderReadSerializer, TrafficOffenderWriteSerializer, 
    VehicleSerializer, InspectionSerializer, TrafficSubjectSerializer, UnregisteredTrafficSubjectSerializer
)

import yaml
import json

import glob
import os
from . import name_prefix

from rest_framework import filters

from .smile_identity import enhanced_kyc
import requests
from smile_id_core import ServerError

from .pagination import VariableResultsSetPagination, CustomPagination

# SWAGGER
def swagger(request):
    # TODO https://adamtheautomator.com/yaml-to-json/
    ## Import the modules to handle JSON & YAML
    # import yaml
    # import json
    
    ## Create a variable to hold the data to import
    swagger = {}

    # TODO https://stackoverflow.com/questions/28218174/current-directory-os-getcwd-from-within-django-determined-how
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # TODO https://linuxize.com/post/python-get-change-current-working-directory/#:~:text=To%20find%20the%20current%20working,chdir(path)%20.
    os.chdir(root_dir)

    yaml_path = [os.path.normpath(i) for i in glob.glob("swagger.yaml")]

    if len(yaml_path):
        ## Read the YAML file
        # with open("c:\temp\operating-systems.yml") as infile:
        with open(yaml_path[0]) as infile:
            # Marshall the YAML into the variable defined above
            swagger = yaml.load(infile, Loader=yaml.FullLoader)

            swagger['host'] = request.get_host() # chaning the host dynamically

    swagger_json = json.dumps(swagger)

    context = {
        'name_prefix': name_prefix,
        "swagger_json": swagger_json
    }
    return render(request, 'vps/swagger.html', context)

# USER
class UserListView(BaseListView):
    """
    List all items, or create a new item.
    """
    model = User
    serializer_class = UserSerializer
    read_serializer_class = UserSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

#GENDER
class GenderListView(BaseListView):
    """
    list all genders or create a new gender
    """
    
    model = Gender
    serializer_class = GenderSerializer
    read_serializer_class = GenderSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Gender.objects.all()

        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name=name)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class GenderDetailView(BaseDetailView):
    """
    Retrieve , updates and delete a gender
    """
    model = Gender
    serializer_class = GenderSerializer
    read_serializer_class = GenderSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

#COUNTRY
class CountryListView(BaseListView):
    """
    list all countries or create a new country
    """

    model = Country
    serializer_class = CountrySerializer
    read_serializer_class = CountrySerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Country.objects.all()

        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name=name)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class CountryDetailView(BaseDetailView):
    """
    Retrieve , updates and delete a country
    """

    model = Country
    serializer_class = CountrySerializer
    read_serializer_class = CountrySerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

# IPRS PERSON
@api_view(['GET', 'POST'])
def iprsPerson_list(request, format=None):
    """
    List all IPRS persons, or create a new IPRS person.
    """
    if request.method == 'GET':
        resources = IPRS_Person.objects.all()

        id_no = request.query_params.get('id_no', None)
        if id_no:
            resources = resources.filter(id_no__icontains=id_no)
            if resources.count() < 1:
                try:
                    success = save_iprs_person_from_smile_identity(request, id_no, "NATIONAL_ID")
                    if success:
                        resources = IPRS_Person.objects.filter(id_no__icontains=id_no)
                except ValueError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_400_BAD_REQUEST)
                    return []
                except ServerError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return []
                except:
                    return []
                # + https://docs.python.org/3/tutorial/errors.html#handling-exceptions
                # except BaseException as err:
                #     print(err)
                #     raise
                
        passport_no = request.query_params.get('passport_no', None)
        if passport_no:
            resources = resources.filter(passport_no__icontains=passport_no)
            if resources.count() < 1:
                try:
                    success = save_iprs_person_from_smile_identity(request, passport_no, "PASSPORT")
                    if success:
                        resources = IPRS_Person.objects.filter(passport_no__icontains=passport_no)
                except ValueError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_400_BAD_REQUEST)
                    return []
                except ServerError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return []
                except:
                    return []
                # + https://docs.python.org/3/tutorial/errors.html#handling-exceptions
                # except BaseException as err:
                #     print(err)
                #     raise

        serializer = IPRS_PersonSerializerRead(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IPRS_PersonSerializerWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class IPRS_PersonList(APIView):
#     """
#     List all IPRS Persons, or create a new IPRS Person.
#     """
#     def get(self, request, format=None):
#         items = IPRS_Person.objects.all()
#         serializer = IPRS_PersonSerializerRead(items, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = IPRS_PersonSerializerWrite(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class IPRS_PersonList(generics.GenericAPIView):
#     """
#     List all IPRS Persons, or create a new IPRS Person.
#     """

#     queryset = IPRS_Person.objects.all()
#     pagination_class = CustomPagination

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return IPRS_PersonSerializerWrite
#         return IPRS_PersonSerializerRead

#     def get(self, request, format=None):
#         items = self.get_queryset()
#         serializer = self.get_serializer_class()(items, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = self.get_serializer_class()(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IPRS_PersonList(generics.ListCreateAPIView):
    """
    List all IPRS Persons, or create a new IPRS Person.
    """

    # queryset = IPRS_Person.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IPRS_PersonSerializerWrite
        return IPRS_PersonSerializerRead

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = IPRS_Person.objects.all()

        country_isoCode = self.request.query_params.get('country_isoCode', "KE")
        if country_isoCode:
            queryset = queryset.filter(nationality__iso_code=country_isoCode)

        id_no = self.request.query_params.get('id_no', None)
        if id_no:
            # queryset = queryset.filter(id_no__icontains=id_no)
            queryset = queryset.filter(id_no=id_no)
            if queryset.count() < 1:
                try:
                    success = save_iprs_person_from_smile_identity(self.request, id_no, "NATIONAL_ID", country_isoCode)
                    if success:
                        queryset = IPRS_Person.objects.filter(id_no__icontains=id_no)
                except ValueError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_400_BAD_REQUEST)
                    return []
                except ServerError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return []
                except:
                    return []
                # + https://docs.python.org/3/tutorial/errors.html#handling-exceptions
                # except BaseException as err:
                #     print(err)
                #     raise
                
        passport_no = self.request.query_params.get('passport_no', None)
        if passport_no:
            # queryset = queryset.filter(passport_no__icontains=passport_no)
            queryset = queryset.filter(passport_no=passport_no)
            if queryset.count() < 1:
                try:
                    success = save_iprs_person_from_smile_identity(self.request, passport_no, "PASSPORT", country_isoCode)
                    if success:
                        queryset = IPRS_Person.objects.filter(passport_no__icontains=passport_no)
                except ValueError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_400_BAD_REQUEST)
                    return []
                except ServerError:
                    # return Response('Error getting IPRS Person', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return []
                except:
                    return []
                # + https://docs.python.org/3/tutorial/errors.html#handling-exceptions
                # except BaseException as err:
                #     print(err)
                #     raise

        return queryset

class IprsPersonDetailView(BaseDetailView):
    """
    """
    model = IPRS_Person
    serializer_class = IPRS_PersonSerializerWrite
    read_serializer_class = IPRS_PersonSerializerRead
    permission_class = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

@api_view(['GET', 'PUT', 'DELETE'])
def iprsPerson_restMug(request, pk, format=None):
    """
    Retrieve, update or delete a IPRS person.
    """
    try:
        resource = IPRS_Person.objects.get(pk=pk)
    except IPRS_Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = IPRS_PersonSerializerWrite(resource)
        resource.mug_shot.delete()
        return Response(serializer.data)
        

#RANK 
class RankListView(BaseListView):
    """
    list all ranks or create a n
    """
    model = Rank
    serializer_class = RankSerializer
    read_serializer_class = RankSerializer
    Permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class RankDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an item
    """
    model = Rank
    serializer_class = RankSerializer
    read_serializer_class = RankSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

#POLICE STATION
class PoliceStationListView(BaseListView):
    """
    List all police stations or create new one
    """

    model = PoliceStation
    serializer_class = PoliceStationSerializer
    read_serializer_class = PoliceStationSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = PoliceStation.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)

        queryset = queryset.order_by('id')

        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(location=location)

        queryset = queryset.order_by('id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class PoliceStationDetailView(BaseDetailView):
    """
    Retrieve , updates and delete a police station
    """

    model = PoliceStation
    serializer_class = PoliceStationSerializer
    read_serializer_class = PoliceStationSerializer
    permission_classes = ()


    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

# POLICE OFFICER
@api_view(['GET', 'POST'])
def policeOfficer_list(request, format=None):
    """
    List all police officers, or create a new police officer.
    """
    if request.method == 'GET':
        resources = PoliceOfficer.objects.all()

        user = request.query_params.get('user', None)
        if user:
            resources = resources.filter(user=user)

        serializer = PoliceOfficerReadSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PoliceOfficerWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PoliceOfficerList(generics.ListCreateAPIView):
    """
    List all Police Officers, or create a new Police Officer.
    """

    queryset = PoliceOfficer.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PoliceOfficerWriteSerializer
        return PoliceOfficerReadSerializer

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = PoliceOfficer.objects.all()

        user = self.request.query_params.get('user', None)
        if user:
            queryset = queryset.filter(user=user)

        service_number = self.request.query_params.get('service_number', None)
        if service_number:
            queryset = queryset.filter(service_number=service_number)

        return queryset

class PoliceOfficerDetailView(BaseDetailView):
    """
    """
    model = PoliceOfficer
    serializer_class = PoliceOfficerWriteSerializer
    read_serializer_class = PoliceOfficerReadSerializer
    permission_class = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

@api_view(['GET', 'PUT', 'DELETE'])
def policeOfficer_restMug(request, pk, format=None):
    """
    Retrieve, update or delete a IPRS person.
    """
    try:
        resource = PoliceOfficer.objects.get(pk=pk)
    except PoliceOfficer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PoliceOfficerReadSerializer(resource)
        resource.mug_shot.delete()
        return Response(serializer.data)

# ! Focus on OB (report) module
class OccurrenceCategoryListView(BaseListView):
    """
    List all Occurrencecategory, or create a new Occurrencecategory.
    """
    model = OccurrenceCategory
    serializer_class = OccurrenceCategorySerializer
    read_serializer_class = OccurrenceCategorySerializer
    permission_classes = ()

    pagination_class = VariableResultsSetPagination # TODO https://www.django-rest-framework.org/api-guide/pagination/#configuration

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OccurrenceCategory.objects.all()

        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name=name)

        module = self.request.query_params.get('module', None)
        if module:
            queryset = queryset.filter(module=module)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class OccurrenceCategoryDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an Occurrencecategory.
    """
    model = OccurrenceCategory
    serializer_class = OccurrenceCategorySerializer
    read_serializer_class = OccurrenceCategorySerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class OccurrenceCategoryInputListView(BaseListView):
    """
    List all occurrence category inputs, or create a new occurrence category input.
    """
    model = OccurrenceCategoryInput
    serializer_class = OccurrenceCategoryInputSerializer
    read_serializer_class = OccurrenceCategoryInputSerializer
    permission_classes = ()
    # SUSPENDED
    # # TODO https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
    # # TODO https://www.django-rest-framework.org/api-guide/filtering/#specifying-which-fields-may-be-ordered-against
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['occurrence_category']
    # ordering_fields = ['order']
    # ordering = ['order'] # https://www.django-rest-framework.org/api-guide/filtering/#specifying-a-default-ordering

    pagination_class = VariableResultsSetPagination # TODO https://www.django-rest-framework.org/api-guide/pagination/#configuration

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OccurrenceCategoryInput.objects.all()
        occurrence_category = self.request.query_params.get('occurrence_category')
        if occurrence_category is not None:
            queryset = queryset.filter(occurrence_category=occurrence_category)

        queryset = queryset.order_by('order')
        return queryset

    def get(self, request):
        layout = self.request.query_params.get('layout')
        if layout == 'nested':
            query_string = ''
            for key, value in self.request.query_params.items():
                if key == 'page':
                    continue
                query_string += f'{key}={value}&'
            # query_string = query_string[:-1] # remove ampersand (&)

            limit = self.request.query_params.get('limit', 10)

            queryset = self.get_queryset()
            queryset = queryset.filter(dependency__isnull=True)
            # TODO https://docs.djangoproject.com/en/4.1/topics/pagination/#using-paginator-in-a-view-function
            input_list = []
            for input in queryset:
                nested_dict = build_nested_input_dict(input, True)
                input_list.append(nested_dict)

            paginator = Paginator(input_list, limit) # Show 25 contacts per page.

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            reverse_url = reverse(f'{app_name}:{pre}-occurrence-category-input-list')

            next = None
            if page_obj.has_next():
                next = f'{request.scheme}://{request.get_host()}{reverse_url}?{query_string}page={page_obj.next_page_number()}'

            previous = None
            if page_obj.has_previous():
                previous = f'{request.scheme}://{request.get_host()}{reverse_url}?{query_string}page={page_obj.previous_page_number()}'

            response = {
                "count": paginator.count,
                "next": next,
                "previous": previous,
                "results": page_obj.object_list,
            }

            return Response(response)
            
        return super().get(request)

    def post(self, request):
        return super().post(request)

class OccurrenceCategoryInputDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an occurrence category input.
    """
    model = OccurrenceCategoryInput
    serializer_class = OccurrenceCategoryInputSerializer
    read_serializer_class = OccurrenceCategoryInputSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        layout = self.request.query_params.get('layout')
        if layout == 'nested':
            item = self.get_object(request, pk)
            nested_dict = build_nested_input_dict(item, True)
            return Response(nested_dict)

        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

def build_nested_input_dict(input, include_occurrence_category=False):
    input_dict = {
        "id": input.id
    }

    if include_occurrence_category:
        input_dict['occurrence_category'] = input.occurrence_category.id

    input_dict["label"] = input.label
    input_dict["type"] = input.type
    input_dict["name"] = input.name
    input_dict["choices"] = input.choices
    input_dict["order"] = input.order
    input_dict["required"] = input.required

    for dependency in input.dependencies.all():
        input_dict[dependency.dependency_value] = build_nested_input_dict(dependency)
    return input_dict
# ================================================
class OccurrenceListView(BaseListView):
    """
    List all Occurrence, or create a new Occurrence.
    """
    model = Occurrence
    serializer_class = OccurrenceWriteSerializer
    read_serializer_class = OccurrenceReadSerializer
    permission_classes = ()
    # TODO https://www.django-rest-framework.org/api-guide/filtering/#specifying-a-default-ordering
    # "...Typically you'd instead control this by setting order_by on the initial queryset,"
    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Occurrence.objects.all()
        police_station = self.request.query_params.get('police_station')
        if police_station is not None:
            queryset = queryset.filter(police_station=police_station)

        police_officer = self.request.query_params.get('police_officer')
        if police_officer is not None:
            queryset = queryset.filter(police_officer=police_officer)

        ob_no = self.request.query_params.get('ob_no')
        if ob_no is not None:
            queryset = queryset.filter(ob_no=ob_no)

        id_no = self.request.query_params.get('id_no')
        if id_no is not None:
            queryset = queryset.filter(reporters__iprs_person__id_no=id_no)

        module = self.request.query_params.get('module')
        if module is not None:
            queryset = queryset.filter(module=module)

        is_closed = self.request.query_params.get('is_closed')
        if is_closed is not None:
            is_closed = is_closed.lower() in ['true',] # + https://stackoverflow.com/a/715455
            queryset = queryset.filter(is_closed=is_closed)

        lastSyncedOccurrenceId = self.request.query_params.get('lastSyncedOccurrenceId')
        if lastSyncedOccurrenceId is not None:
            queryset = queryset.filter(id__gt=lastSyncedOccurrenceId)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        # return super().post(request)
        # Excerpt from "BaseListView.post"
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                counter = OccurrenceCounter.objects.get(date=date.today())
            except:
                counter = OccurrenceCounter.objects.create()
            # instance.ob_no = f'OB/{instance.id}/{instance.posted_date.strftime("%d/%m/%Y")}'
            instance.ob_no = f'OB/{counter.ob_no + 1}/{instance.posted_date.strftime("%d/%m/%Y")}'
            instance.save()

            counter.ob_no = counter.ob_no + 1
            counter.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OccurrenceDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an Occurrence.
    """
    model = Occurrence
    serializer_class = OccurrenceWriteSerializer
    read_serializer_class = OccurrenceReadSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class OccurrenceDetailListView(BaseListView):
    """
    List all occurrence category inputs, or create a new occurrence category input.
    """
    model = OccurrenceDetail
    serializer_class = OccurrenceDetailSerializer
    read_serializer_class = OccurrenceDetailSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = OccurrenceDetail.objects.all()
        occurrence = self.request.query_params.get('occurrence')
        if occurrence is not None:
            queryset = queryset.filter(occurrence=occurrence)

        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class OccurrenceDetailDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an occurrence category input.
    """
    model = OccurrenceDetail
    serializer_class = OccurrenceDetailSerializer
    read_serializer_class = OccurrenceDetailSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class ReporterListView(BaseListView):
    """
    List all items, or create a new item.
    """
    model = Reporter
    serializer_class = ReporterSerializer
    read_serializer_class = ReporterSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Reporter.objects.all()
        occurrence = self.request.query_params.get('occurrence')
        if occurrence is not None:
            queryset = queryset.filter(occurrence=occurrence)

        id_no = self.request.query_params.get('id_no')
        if id_no is not None:
            queryset = queryset.filter(iprs_person__id_no=id_no)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ReporterDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an item
    """
    model = Reporter
    serializer_class = ReporterSerializer
    read_serializer_class = ReporterSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class UnregisteredReporterListView(BaseListView):
    """
    List all items, or create a new item.
    """
    model = UnregisteredReporter
    serializer_class = UnregisteredReporterSerializer
    read_serializer_class = UnregisteredReporterSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = UnregisteredReporter.objects.all()
        occurrence = self.request.query_params.get('occurrence')
        if occurrence is not None:
            queryset = queryset.filter(occurrence=occurrence)

        id_no = self.request.query_params.get('id_no')
        if id_no is not None:
            queryset = queryset.filter(id_no=id_no)

        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class UnregisteredReporterDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an item
    """
    model = UnregisteredReporter
    serializer_class = UnregisteredReporterSerializer
    read_serializer_class = UnregisteredReporterSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

# TODO https://docs.djangoproject.com/en/4.0/howto/outputting-pdf/#write-your-view
import io
# from django.http import FileResponse
from reportlab.pdfgen import canvas

@api_view(['PUT'])
def occurrence_emailAbstract(request, pk, format=None):
    """
    Retrieve, update or delete a IPRS person.
    """
    try:
        resource = Occurrence.objects.get(pk=pk)
        # police_officer = PoliceOfficer.objects.get(iprs_person=resource.pollice_officer.iprs_person_id).user
        police_officer = resource.police_officer
    except Occurrence.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        from .OBReport.report import generate_report

        media_folder = f'{settings.MEDIA_ROOT}/abstract'
        os.makedirs(media_folder, exist_ok=True)

        # TODO https://docs.djangoproject.com/en/4.0/howto/outputting-pdf/#write-your-view
        # Create a file-like buffer to receive PDF data.
        # buffer = io.BytesIO()
        # + https://docs.python.org/3/library/io.html#binary-i-o
        # f = open("myfile.jpg", "rb")
        buffer = open(f'{media_folder}/Abstract_{resource.id}.pdf', "w+b")

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # p.drawString(100, 100, "Hello world.")
        p.drawString(100, 100, f'Abstract {resource.id}')        

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
        url = f'{request.scheme}://{request.get_host()}/vps/abstract/{resource.id}/view'
        # ! Peter & Mutuku using ReportLab
        file_name = f'{media_folder}/Abstract_{resource.id}.pdf'
        generate_report(file_name, resource, police_officer, url)

        # TODO https://docs.djangoproject.com/en/4.0/topics/email/#send-mass-mail
        # message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
        # message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
        # send_mass_mail((message1, message2), fail_silently=False)

        instance = resource

        # subject = f'Police Absract #{resource.id}'
        subject = f'Police Absract No. {resource.ob_no}'

        message = f"see attachment for the abstract"

        reporters = instance.reporters.all()
        reporters_email_array = list(map(lambda recipient: recipient.email_address, reporters))

        unregistered_reporters = instance.unregistered_reporters.all()
        unregistered_reporters_email_array = list(map(lambda recipient: recipient.email_address, unregistered_reporters))

        traffic_offenders = instance.traffic_offenders.all()
        traffic_offenders_email_array = list(map(lambda recipient: recipient.email, traffic_offenders))

        recipient_list_email = reporters_email_array + unregistered_reporters_email_array + traffic_offenders_email_array
        
#         message1 = (subject, message, 'not-reply@task_manager.vps', recipient_list_email)
#         send_mass_mail((message1,), fail_silently=False)

        # TODO https://docs.djangoproject.com/en/4.0/topics/email/#the-emailmessage-class
        # email = EmailMessage(
        #     'Hello',
        #     'Body goes here',
        #     'from@example.com',
        #     ['to1@example.com', 'to2@example.com'],
        #     ['bcc@example.com'],
        #     reply_to=['another@example.com'],
        #     headers={'Message-ID': 'foo'},
        # )
        # message.attach_file('/images/weather_map.png')
        email = EmailMessage(
            subject,
            message,
            'no-reply@virtualpolicestation.com',
            recipient_list_email,
            [],
            # reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )
        email.attach_file(file_name)
        email.send(fail_silently=False)

        return Response({'status': 'successful'})
        
# ! Focus on arrest module
class PoliceCellListView(BaseListView):
    """
    List all PoliceCell, or create a new PoliceCell.
    """
    model = PoliceCell
    serializer_class = PoliceCellSerializer
    read_serializer_class = PoliceCellSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class PoliceCellDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an PoliceCell.
    """
    model = PoliceCell
    serializer_class = PoliceCellSerializer
    read_serializer_class = PoliceCellSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class WarrantofarrestListView(BaseListView):
    """
    List all Warrantofarrest, or create a new Warrantofarrest.
    """
    model = Warrant_of_arrest
    serializer_class = WarrantofarrestSerializer
    read_serializer_class = WarrantofarrestSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Warrant_of_arrest.objects.all()
        arrestee = self.request.query_params.get('arrestee')
        if arrestee is not None:
            queryset = queryset.filter(arrestee=arrestee)

        reference_no = self.request.query_params.get('reference_no')
        if reference_no is not None:
            queryset = queryset.filter(reference_no=reference_no)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class WarrantofarrestDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an Warrantofarrest.
    """
    model = Warrant_of_arrest
    serializer_class = WarrantofarrestSerializer
    read_serializer_class = WarrantofarrestSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class ArresteeListView(BaseListView):
    """
    List all arrestee, or create a new arrestee.
    """
    model = Arrestee
    serializer_class = ArresteeWriteSerializer
    read_serializer_class = ArresteeReadSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Arrestee.objects.all()
        police_station = self.request.query_params.get('police_station')
        if police_station is not None:
            queryset = queryset.filter(police_station=police_station)

        arresting_officer = self.request.query_params.get('arresting_officer')
        if arresting_officer is not None:
            queryset = queryset.filter(arresting_officer=arresting_officer)

        ob_no = self.request.query_params.get('ob_no')
        if ob_no is not None:
            queryset = queryset.filter(occurrence__ob_no=ob_no)

        id_no = self.request.query_params.get('id_no')
        if id_no is not None:
            queryset = queryset.filter(iprs_person__id_no=id_no)

        is_closed = self.request.query_params.get('is_closed')
        if is_closed is not None:
            is_closed = is_closed.lower() in ['true',] # + https://stackoverflow.com/a/715455
            queryset = queryset.filter(occurrence__is_closed=is_closed)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ArresteeDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an arrestee.
    """
    model = Arrestee
    serializer_class = ArresteeWriteSerializer
    read_serializer_class = ArresteeReadSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class AccompliceListView(BaseListView):
    """
    List all accomplice, or create a new accomplice.
    """
    model = Accomplice
    serializer_class = AccompliceSerializer
    read_serializer_class = AccompliceSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Accomplice.objects.all()
        arrestee = self.request.query_params.get('arrestee')
        if arrestee is not None:
            queryset = queryset.filter(arrestee=arrestee)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class AccompliceDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an accomplice.
    """
    model = Accomplice
    serializer_class = AccompliceSerializer
    read_serializer_class = AccompliceSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class GangListView(BaseListView):
    """
    List all gang, or create a new gang.
    """
    model = Gang
    serializer_class = GangSerializer
    read_serializer_class = GangSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Gang.objects.all()
        arrestee = self.request.query_params.get('arrestee')
        if arrestee is not None:
            queryset = queryset.filter(arrestee=arrestee)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class GangDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an gang.
    """
    model = Gang
    serializer_class = GangSerializer
    read_serializer_class = GangSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class NextofkinListView(BaseListView):
    """
    List all next of kins, or create a new next of kin,.
    """
    model = Next_of_kin
    serializer_class = NextofkinSerializer
    read_serializer_class = NextofkinSerializer
    permission_classes = ()

    # TODO https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Next_of_kin.objects.all()
        arrestee = self.request.query_params.get('arrestee')
        if arrestee is not None:
            queryset = queryset.filter(arrestee=arrestee)

        queryset = queryset.order_by('-id')
        return queryset

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class NextofkinDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an next of kin.
    """
    model = Next_of_kin
    serializer_class = NextofkinSerializer
    read_serializer_class = NextofkinSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class MugShotsListView(ImageBaseListView):
    """
    List all mugshots, or create a new mugshots.
    """
    model = MugShots
    serializer_class = MugShotsSerializer
    read_serializer_class = MugShotsSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class MugShotsDetailView(ImageBaseDetailView):

    """
    Retrieve , updates and delete an mugshots.
    """
    model = MugShots
    serializer_class = MugShotsSerializer
    read_serializer_class = MugShotsSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class FingerPrintsListView(ImageBaseListView):
    """
    List all FingerPrints, or create a new FingerPrints.
    """
    model = FingerPrints
    serializer_class = FingerPrintsSerializer
    read_serializer_class = FingerPrintsSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class FingerPrintsDetailView(ImageBaseDetailView):

    """
    Retrieve , updates and delete an FingerPrints.
    """
    model = FingerPrints
    serializer_class = FingerPrintsSerializer
    read_serializer_class = FingerPrintsSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

# ! Focus on charge sheet module
class OffenseListView(BaseListView):
    """
    List all Offense, or create a new Offense.
    """
    model = Offense
    serializer_class = OffenseSerializer
    read_serializer_class = OffenseSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class OffenseDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an Offense.
    """
    model = Offense
    serializer_class = OffenseSerializer
    read_serializer_class = OffenseSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class ChargeSheetPersonListView(BaseListView):
    """
    List all ChargeSheetPerson, or create a new ChargeSheetPerson
    """
    model = ChargeSheet_Person
    serializer_class = ChargeSheetPersonSerializer
    read_serializer_class = ChargeSheetPersonSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ChargeSheetPersonDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an ChargeSheetPerson
    """
    model = ChargeSheet_Person
    serializer_class = ChargeSheetPersonSerializer
    read_serializer_class = ChargeSheetPersonSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class ChargeSheetListView(BaseListView):
    """
    List all ChargeSheet, or create a new ChargeSheet
    """
    model = ChargeSheet
    serializer_class = ChargeSheetSerializer
    read_serializer_class = ChargeSheetSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ChargeSheetDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an ChargeSheet.
    """
    model = ChargeSheet
    serializer_class = ChargeSheetSerializer
    read_serializer_class = ChargeSheetSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class CourtFileListView(BaseListView):
    """
    List all CourtFile, or create a new CourtFile.
    """
    model = CourtFile
    serializer_class = CourtFileSerializer
    read_serializer_class = CourtFileSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class CourtFileDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an CourtFile.
    """
    model = CourtFile
    serializer_class = CourtFileSerializer
    read_serializer_class = CourtFileSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

# ! Focus on evidence module
class EvidenceCategoryListView(BaseListView):
    """
    List all evidencecategory, or create a new evidencecategory.
    """
    model = EvidenceCategory
    serializer_class = EvidenceCategorySerializer
    read_serializer_class = EvidenceCategorySerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class EvidenceCategoryDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an evidencecategory.
    """
    model = EvidenceCategory
    serializer_class = EvidenceCategorySerializer
    read_serializer_class = EvidenceCategorySerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class EvidenceListView(BaseListView):
    """
    List all evidence, or create a new evidence.
    """
    model = Evidence
    serializer_class = EvidenceWriteSerializer
    read_serializer_class = EvidenceReadSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        # return super().post(request)
        # Excerpt from "BaseListView.post"
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.evidence_no = f'EV/{instance.id}/{instance.posted_date.strftime("%m/%d/%Y")}'
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvidenceDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an evidence.
    """
    model = Evidence
    serializer_class = EvidenceWriteSerializer
    read_serializer_class = EvidenceReadSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class EvidenceItemCategoryListView(BaseListView):
    """
    List all evidencecategory, or create a new evidence item category.
    """
    model = EvidenceItemCategory
    serializer_class = EvidenceItemCategorySerializer
    read_serializer_class = EvidenceItemCategorySerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class EvidenceItemCategoryDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an evidence item category.
    """
    model = EvidenceItemCategory
    serializer_class = EvidenceItemCategorySerializer
    read_serializer_class = EvidenceItemCategorySerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
# ================================================
class EvidenceImageListView(ImageBaseListView):
    """
    List all evidenceimage, or create a new evidenceimage.
    """
    model = EvidenceItemImage
    serializer_class = EvidenceItemImageSerializer
    read_serializer_class = EvidenceItemImageSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        # return super().post(request)
        # Excerpt from "BaseListView.post"
        serializer = self.get_serializer_class()(data={"evidence": request.data['evidence']})
        if serializer.is_valid():
            evidence_item_image = serializer.save()
            evidence_item_image.image = request.data['image']
            evidence_item_image.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvidenceImageDetailView(ImageBaseDetailView):
    """
    Retrieve , updates and delete an evidenceimage.
    """
    model = EvidenceItemImage
    serializer_class = EvidenceItemImageSerializer
    read_serializer_class = EvidenceItemImageSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        # return super().delete(request, pk)
        # Excerpt from "BaseDetailView.delete"
        item = self.get_object(request, pk)
        if hasattr(item, "is_deleted"):
            item.is_deleted = True
            item.deleted_at = datetime.datetime.now(tz=timezone.utc)
            item.modified_by = request.user
            item.save()
        else:
            try:
                # delete_file_in_media(item.image.name)
                item.image.delete() # TODO https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.fields.files.FieldFile.delete
            except OSError:
                return Response({"message": "Evidence files not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                pass
            
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def save_iprs_person_from_smile_identity(request, id_number, id_type, country="KE"):
    iprs_person = enhanced_kyc(id_number, id_type, country) # TODO https://docs.smileidentity.com/supported-id-types/for-individuals-kyc/backed-by-id-authority#know-your-customer-kyc
    iprs_person = iprs_person.json() # TODO https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content
    # print(iprs_person)
    if iprs_person['ResultCode'] != "1012":
        return
    
    # nationality = get_object_or_404(Country, nationality__iexact=iprs_person["FullData"]['Citizenship'])
    nationality = get_object_or_404(Country, iso_code=iprs_person["Country"])

    GENDER_CHOICES = {
        "M": "male",
        "F": "female"
    }
    if iprs_person['FullData'].get('Gender'):
        gender = get_object_or_404(Gender, name__iexact=GENDER_CHOICES[iprs_person['FullData']['Gender']])
    else:
        gender = get_object_or_404(Gender, name__iexact=GENDER_CHOICES[iprs_person['FullData']['sex']])

    id_no = None
    passport_no = None
    if 'NATIONAL_ID' in id_type:
        id_no = id_number
    
    if id_type == 'PASSPORT':
        passport_no = id_number
        
    county_of_birth = None
    district_of_birth = None
    division_of_birth = None
    location_of_birth = None

    if iprs_person['FullData'].get('Place_of_Birth'):
        place_of_birth = iprs_person['FullData']['Place_of_Birth'] # KISUMU EAST\nDISTRICT - KISUMU EAST
        place_of_birth = place_of_birth.split("\n")
        for place_entry in place_of_birth:
            place = place_entry.split('-')
            if len(place) > 1:
                # ['DISTRICT ', ' NOT INDICATED']
                if place[1].strip().lower() == 'not indicated':
                    continue

                if place[0].strip().lower() == 'county':
                    county_of_birth = place[1].strip().title()
                elif place[0].strip().lower() == 'district':
                    district_of_birth = place[1].strip().title()
                elif place[0].strip().lower() == 'division':
                    division_of_birth = place[1].strip().title()
                elif place[0].strip().lower() == 'location':
                    location_of_birth = place[1].strip().title()

    # TODO https://www.programiz.com/python-programming/examples/string-to-datetime
    if iprs_person['FullData'].get('Date_of_Birth'):
        my_date_string = iprs_person['FullData']['Date_of_Birth'] # 6/1/1998 12:00:00 AM
        datetime_object = datetime.strptime(my_date_string, '%m/%d/%Y %I:%M:%S %p')
    else:
        my_date_string = iprs_person['FullData']['dateOfBirth'] # "1978-02-10T00:00:00"
        datetime_object = datetime.strptime(my_date_string, '%Y-%m-%dT%H:%M:%S')

    first_name = None
    middle_name = None
    surname = None

    if iprs_person['FullData'].get('First_Name'):
        first_name = iprs_person['FullData']['First_Name'].capitalize()
    else:
        first_name = iprs_person['FullData']['givenNames'].capitalize()

    if iprs_person['FullData'].get('Other_Name'):
        middle_name = iprs_person['FullData']['Other_Name'].title()

    if iprs_person['FullData'].get('Surname'):
        surname = iprs_person['FullData']['Surname'].capitalize()
    else:
        surname = iprs_person['FullData']['surname'].capitalize()

    # + https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests
    payload = {
        # 'id_no': iprs_person['FullData']['ID_Number'],
        # 'passport_no': iprs_person['FullData']['value2'],
        'id_no': id_no,
        'passport_no': passport_no,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': surname,
        'nationality': nationality.id,
        'gender': gender.id,
        'county_of_birth': county_of_birth,
        'district_of_birth': district_of_birth,
        'division_of_birth': division_of_birth,
        'location_of_birth': location_of_birth,
        'date_of_birth': datetime_object.isoformat(),
    }

    r = requests.post(f"{request.scheme}://{request.get_host()}/vps/api/v0/iprs-persons", data=payload)
    # print(r.text)
    # + https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes
    r.raise_for_status()
    return True

# ! Focus on traffic module
# REGISTRED VEHICLE
class RegisteredVehicleList(generics.ListCreateAPIView):
    """
    List all regsitered vehicles, or create a new regsitered vehicle.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = RegisteredVehicle.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(reg_no=reg_no)

        chassis_no = self.request.query_params.get('chassis_no', None)
        if chassis_no:
            queryset = queryset.filter(chassis_no=chassis_no)

        return queryset

    def get_serializer_class(self):
        return RegisteredVehicleSerializer

class RegisteredVehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a RegisteredVehicle
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return RegisteredVehicleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = RegisteredVehicle.objects.all()
        return queryset

# INSURANCE POLICY
class InsurancePolicyList(generics.ListCreateAPIView):
    """
    List all insurance policies, or create a new insurance policies.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = InsurancePolicy.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        policy_no = self.request.query_params.get('policy_no', None)
        if policy_no:
            queryset = queryset.filter(policy_no=policy_no)

        certificate_no = self.request.query_params.get('certificate_no', None)
        if certificate_no:
            queryset = queryset.filter(certificate_no=certificate_no)

        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(reg_no=reg_no)

        return queryset

    def get_serializer_class(self):
        return InsurancePolicySerializer

class InsurancePolicyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a InsurancePolicy
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return InsurancePolicySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = InsurancePolicy.objects.all()
        return queryset

# DRIVING LICENSE
class DrivingLicenseList(generics.ListCreateAPIView):
    """
    List all driving license, or create a new driving licenses.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = DrivingLicense.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        license_no = self.request.query_params.get('license_no', None)
        if license_no:
            queryset = queryset.filter(license_no=license_no)

        id_no = self.request.query_params.get('id_no', None)
        if id_no:
            queryset = queryset.filter(iprs_person__id_no=id_no)

        passport_no = self.request.query_params.get('passport_no', None)
        if passport_no:
            queryset = queryset.filter(iprs_person__passport_no=passport_no)

        return queryset

    def get_serializer_class(self):
        return DrivingLicenseSerializer

class DrivingLicenseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a DrivingLicense
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return DrivingLicenseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = DrivingLicense.objects.all()
        return queryset

# TRAFFIC OFFENDER
class TrafficOffenderList(generics.ListCreateAPIView):
    """
    List all traffic offender, or create a new traffic offenders.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = TrafficOffender.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        id_no = self.request.query_params.get('id_no', None)
        if id_no:
            queryset = queryset.filter(iprs_person__id_no=id_no)

        passport_no = self.request.query_params.get('passport_no', None)
        if passport_no:
            queryset = queryset.filter(iprs_person__passport_no=passport_no)

        return queryset

    # def get_serializer_class(self):
    #     return TrafficOffenderSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrafficOffenderWriteSerializer
        return TrafficOffenderReadSerializer

class TrafficOffenderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a TrafficOffender
    """

    # permission_classes = [IsStaffOrReadOnly]

    # def get_serializer_class(self):
    #     return TrafficOffenderSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TrafficOffenderWriteSerializer
        return TrafficOffenderReadSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TrafficOffender.objects.all()
        return queryset

# VEHICLE
class VehicleList(generics.ListCreateAPIView):
    """
    List all vehicles, or create a new vehicle.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(reg_no=reg_no)

        chassis_no = self.request.query_params.get('chassis_no', None)
        if chassis_no:
            queryset = queryset.filter(chassis_no=chassis_no)

        inspection = self.request.query_params.get('inspection', None)
        if inspection:
            queryset = queryset.filter(inspection=inspection)

        return queryset

    def get_serializer_class(self):
        return VehicleSerializer

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a Vehicle
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return VehicleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Vehicle.objects.all()
        return queryset

# INSPECTION
class InspectionList(generics.ListCreateAPIView):
    """
    List all inspections, or create a new inspection.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Inspection.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(vehicle__reg_no=reg_no)

        police_officer = self.request.query_params.get('police_officer', None)
        if police_officer:
            queryset = queryset.filter(police_officer__service_number=police_officer)

        penal_code = self.request.query_params.get('penal_code', None)
        if penal_code:
            queryset = queryset.filter(penal_code=penal_code)

        return queryset

    def get_serializer_class(self):
        return InspectionSerializer

class InspectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a Inspection
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return InspectionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Inspection.objects.all()
        return queryset

# TRAFFIC SUBJECT
class TrafficSubjectList(generics.ListCreateAPIView):
    """
    List all traffic subjects, or create a new traffic subject.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = TrafficSubject.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(vehicle__reg_no=reg_no)

        police_officer = self.request.query_params.get('police_officer', None)
        if police_officer:
            queryset = queryset.filter(police_officer__service_number=police_officer)

        penal_code = self.request.query_params.get('penal_code', None)
        if penal_code:
            queryset = queryset.filter(penal_code=penal_code)

        return queryset

    def get_serializer_class(self):
        return TrafficSubjectSerializer

class TrafficSubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a TrafficSubject
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return TrafficSubjectSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TrafficSubject.objects.all()
        return queryset

# UNREGISTERED TRAFFIC SUBJECT
class UnregisteredTrafficSubjectList(generics.ListCreateAPIView):
    """
    List all unregistered traffic subjects, or create a new unregistered traffic subject.
    """

    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = UnregisteredTrafficSubject.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        reg_no = self.request.query_params.get('reg_no', None)
        if reg_no:
            queryset = queryset.filter(vehicle__reg_no=reg_no)

        police_officer = self.request.query_params.get('police_officer', None)
        if police_officer:
            queryset = queryset.filter(police_officer__service_number=police_officer)

        penal_code = self.request.query_params.get('penal_code', None)
        if penal_code:
            queryset = queryset.filter(penal_code=penal_code)

        return queryset

    def get_serializer_class(self):
        return UnregisteredTrafficSubjectSerializer

class UnregisteredTrafficSubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Update, Delete, or View a unregistered traffic subject
    """

    # permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        return UnregisteredTrafficSubjectSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = UnregisteredTrafficSubject.objects.all()
        return queryset

# class TrafficOffenderListView(BaseListView):
#     """
#     List all TrafficOffenderDetails, or create a new trafficOffenderDetails.
#     """
#     model = TrafficOffender
#     serializer_class = TrafficOffenderDetailsSerializer
#     read_serializer_class = TrafficOffenderDetailsSerializer
#     permission_classes = ()

#     def get(self, request):
#         return super().get(request)

#     def post(self, request):
#         return super().post(request)

# class TrafficOffenderDetailsView(BaseDetailView):

#     """
#     Retrieve , updates and delete an TrafficOffenderDetails.
#     """
#     model = TrafficOffender
#     serializer_class = TrafficOffenderDetailsSerializer
#     read_serializer_class = TrafficOffenderDetailsSerializer
#     permission_classes = ()

#     def get(self, request, pk=None):
#         return super().get(request, pk)

#     def put(self, request, pk=None):
#         return super().put(request, pk)

#     def delete(self, request, pk=None):
#         return super().delete(request, pk)

# class DriverListView(BaseListView):
#     """
#     List all DriverDetails, or create a new DriverDetails.
#     """
#     model = Driver
#     serializer_class = DriverSerializer
#     read_serializer_class = DriverSerializer
#     permission_classes = ()

#     def get(self, request):
#         return super().get(request)

#     def post(self, request):
#         return super().post(request)

# class DriverDetailsView(BaseDetailView):

#     """
#     Retrieve DriverDetails.
#     """
#     model = Driver
#     serializer_class = DriverSerializer
#     read_serializer_class = DriverSerializer
#     permission_classes = ()

#     def get(self, request, pk=None):
#         return super().get(request, pk)

#     def put(self, request, pk=None):
#         return super().put(request, pk)

#     def delete(self, request, pk=None):
#         return super().delete(request, pk)

# class VehicleListView(BaseListView):
#     """
#     List all VehicleDetails, or create a new VehicleDetails.
#     """
#     model = Vehicle
#     serializer_class = VehicleSerializer
#     read_serializer_class = VehicleSerializer
#     permission_classes = ()

#     def get(self, request):
#         return super().get(request)

#     def post(self, request):
#         return super().post(request)

# class VehicleDetailsView(BaseDetailView):

#     """
#     Retrieve vehicleDetails.
#     """
#     model = Vehicle
#     serializer_class = VehicleSerializer
#     read_serializer_class = VehicleSerializer
#     permission_classes = ()

#     def get(self, request, pk=None):
#         return super().get(request, pk)

#     def put(self, request, pk=None):
#         return super().put(request, pk)

#     def delete(self, request, pk=None):
#         return super().delete(request, pk)

# TODO https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/#creating-an-endpoint-for-the-root-of-our-api
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from vps.urls import app_name
from . import name_prefix as pre

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'swagger': reverse(f'{app_name}:{pre}-swagger', request=request, format=format),

        'Login & Registration' : '================',
        'Token Auth': reverse(f'user:token-auth', request=request, format=format),

        'Core System' : '================',
        'users': reverse(f'{app_name}:{pre}-user-list', request=request, format=format),

        'genders': reverse(f'{app_name}:{pre}-gender-list', request=request, format=format),
        'countries': reverse(f'{app_name}:{pre}-country-list', request=request, format=format),
        'IPRS persons': reverse(f'{app_name}:{pre}-iprs-person-list', request=request, format=format),
        'police stations': reverse(f'{app_name}:{pre}-police-station-list', request=request, format=format),
        'ranks': reverse(f'{app_name}:{pre}-rank-list', request=request, format=format),
        'police officers': reverse(f'{app_name}:{pre}-police-officer-list', request=request, format=format),

        # ! Focus on OB (report) module
        'OB' : '================',
        'occurrence categories': reverse(f'{app_name}:{pre}-occurrence-category-list', request=request, format=format),
        'occurrence categories inputs': reverse(f'{app_name}:{pre}-occurrence-category-input-list', request=request, format=format),
        'occurrences': reverse(f'{app_name}:{pre}-occurrence-list', request=request, format=format),
        'occurrences details': reverse(f'{app_name}:{pre}-occurrence-detail-list', request=request, format=format),
        'reporters': reverse(f'{app_name}:{pre}-reporter-list', request=request, format=format),
        'unregistered-reporters': reverse(f'{app_name}:{pre}-unregistered-reporter-list', request=request, format=format),

        # ! Focus on arrest module
        'ARREST' : '================',
        'police cells': reverse(f'{app_name}:{pre}-police-cell-list', request=request, format=format),
        'warrants of arrest': reverse(f'{app_name}:{pre}-warrant-of-arrest-list', request=request, format=format),
        'arrestees': reverse(f'{app_name}:{pre}-arrestee-list', request=request, format=format),
        'accomplices': reverse(f'{app_name}:{pre}-accomplice-list', request=request, format=format),
        'gangs': reverse(f'{app_name}:{pre}-gang-list', request=request, format=format),
        'next of kins': reverse(f'{app_name}:{pre}-next-of-kin-list', request=request, format=format),
        'mugshots': reverse(f'{app_name}:{pre}-mugshot-list', request=request, format=format),
        'fingerprints': reverse(f'{app_name}:{pre}-fingerprint-list', request=request, format=format),

        # ! Focus on charge sheet module
        'CHARGE SHEET' : '================',
        'offenses': reverse(f'{app_name}:{pre}-offence-list', request=request, format=format),
        'chargesheet persons': reverse(f'{app_name}:{pre}-charge-sheet-person-list', request=request, format=format),
        'chargesheets': reverse(f'{app_name}:{pre}-charge-sheet-list', request=request, format=format),
        'court files': reverse(f'{app_name}:{pre}-court-file-list', request=request, format=format),

        # ! Focus on evidence module
        'EVIDENCE' : '================',
        'evidence categories': reverse(f'{app_name}:{pre}-evidence-category-list', request=request, format=format),
        'evidences': reverse(f'{app_name}:{pre}-evidence-list', request=request, format=format),
        'evidence item categories': reverse(f'{app_name}:{pre}-evidence-item-category-list', request=request, format=format),
        'evidence images': reverse(f'{app_name}:{pre}-evidence-item-image-list', request=request, format=format),


        # !Focus on traffic module
        'TRAFFIC' : '================',
        'registered-vehicles': reverse(f'{app_name}:{pre}-registered-vehicle-list', request=request, format=format),
        'insurance-policies': reverse(f'{app_name}:{pre}-insurance-policy-list', request=request, format=format),
        'driving-licenses': reverse(f'{app_name}:{pre}-driving-license-list', request=request, format=format),
        'traffic-offenders': reverse(f'{app_name}:{pre}-traffic-offender-list', request=request, format=format),
        'vehicle': reverse(f'{app_name}:{pre}-vehicle-list', request=request, format=format),
        'inspection': reverse(f'{app_name}:{pre}-inspection-list', request=request, format=format),
        'traffic-subject': reverse(f'{app_name}:{pre}-traffic-subject-list', request=request, format=format),
        'unregistered-traffic-subject': reverse(f'{app_name}:{pre}-unregistered-traffic-subject-list', request=request, format=format),
        # 'traffic offenders': reverse(f'{app_name}:{pre}-trafficoffenders', request=request, format=format),
        # 'drivers': reverse(f'{app_name}:{pre}-driver', request=request, format=format),
    })
