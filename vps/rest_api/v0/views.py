from pickle import FALSE
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

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

# TODO https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#adding-optional-format-suffixes-to-our-urls
from django.db import IntegrityError
from vps.models import (Arrestee, ChargeSheet, ChargeSheet_Person, Country, CourtFile, Evidence, EvidenceCategory, EvidenceImage, FingerPrints, Gender, IPRS_Person, MugShots, Next_of_keen, Occurrence, OccurrenceCategory, Offense, PoliceCell, Rank, PoliceStation, PoliceOfficer,
ItemCategory, Item, Warrant_of_arrest
)
from helpers.file_system_manipulation import delete_folder_in_media
from vps.rest_api.v0.common.views import BaseDetailView, BaseListView, ImageBaseDetailView, ImageBaseListView
from .serializers import (ArresteeSerializer, ChargeSheetPersonSerializer, ChargeSheetSerializer, CountrySerializer, CourtFileSerializer, EvidenceCategorySerializer, EvidenceImageSerializer, EvidenceSerializer, FingerPrintsSerializer, GenderSerializer, IPRS_PersonSerializer, ItemCategorySerializer, ItemSerializer, MugShotsSerializer, NextofkeenSerializer, OccurrenceCategorySerializer, OccurrenceSerializer, OffenseSerializer, PoliceCellSerializer, 
RankSerializer, PoliceStationSerializer, PoliceOfficerSerializer, WarrantofarrestSerializer
)

import yaml
import json

import glob
import os
from . import name_prefix

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

    swagger_json = json.dumps(swagger)

    context = {
        'name_prefix': name_prefix,
        "swagger_json": swagger_json
    }
    return render(request, 'vps/swagger.html', context)

# GENDER
@api_view(['GET', 'POST'])
def gender_list(request, format=None):
    """
    List all genders, or create a gender.
    """
    if request.method == 'GET':
        resources = Gender.objects.all()
        serializer = GenderSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def gender_detail(request, pk, format=None):
    """
    Retrieve, update or delete a gender.
    """
    try:
        resource = Gender.objects.get(pk=pk)
    except Gender.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenderSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GenderSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

# COUNTRY
@api_view(['GET', 'POST'])
def country_list(request, format=None):
    """
    List all countries, or create a new country.
    """
    if request.method == 'GET':
        resources = Country.objects.all()
        serializer = CountrySerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def country_detail(request, pk, format=None):
    """
    Retrieve, update or delete a country.
    """
    try:
        resource = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CountrySerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CountrySerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

# IPRS PERSON
@api_view(['GET', 'POST'])
def iprsPerson_list(request, format=None):
    """
    List all IPRS persons, or create a new IPRS person.
    """
    if request.method == 'GET':
        resources = IPRS_Person.objects.all()
        serializer = IPRS_PersonSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IPRS_PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def iprsPerson_detail(request, pk, format=None):
    """
    Retrieve, update or delete a IPRS person.
    """
    try:
        resource = IPRS_Person.objects.get(pk=pk)
    except IPRS_Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IPRS_PersonSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IPRS_PersonSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():

            if serializer.validated_data.get("mug_shot", None):
                resource.mug_shot.delete() # delete the existing mug shot first

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            delete_folder_in_media(f'iprs_person_{resource.id}', False)
        except OSError:
            return Response({"message": "User files not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pass

        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        serializer = IPRS_PersonSerializer(resource)
        resource.mug_shot.delete()
        return Response(serializer.data)
        
# RANK
@api_view(['GET', 'POST'])
def rank_list(request, format=None):
    """
    List all ranks, or create a new rank.
    """
    if request.method == 'GET':
        resources = Rank.objects.all()
        serializer = RankSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def rank_detail(request, pk, format=None):
    """
    Retrieve, update or delete a rank.
    """
    try:
        resource = Rank.objects.get(pk=pk)
    except Rank.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RankSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RankSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

# POLICE STATION
@api_view(['GET', 'POST'])
def policeStation_list(request, format=None):
    """
    List all police stations, or create a new police station.
    """
    if request.method == 'GET':
        resources = PoliceStation.objects.all()
        serializer = PoliceStationSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PoliceStationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def policeStation_detail(request, pk, format=None):
    """
    Retrieve, update or delete a police station.
    """
    try:
        resource = PoliceStation.objects.get(pk=pk)
    except PoliceStation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PoliceStationSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PoliceStationSerializer(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

# POLICE OFFICER
@api_view(['GET', 'POST'])
def policeOfficer_list(request, format=None):
    """
    List all police officers, or create a new police officer.
    """
    if request.method == 'GET':
        resources = PoliceOfficer.objects.all()
        serializer = PoliceOfficerSerializer(resources, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PoliceOfficerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def policeOfficer_detail(request, pk, format=None):
    """
    Retrieve, update or delete a police officer.
    """
    try:
        resource = PoliceOfficer.objects.get(pk=pk)
    except PoliceOfficer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PoliceOfficerSerializer(resource)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PoliceOfficerSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            resource.delete()
        except IntegrityError:
            return Response({"message": "Deleting action not allowed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemListView(BaseListView):
    """
    List all items, or create a new item.
    """
    model = Item
    serializer_class = ItemSerializer
    read_serializer_class = ItemSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ItemDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an item
    """
    model = Item
    serializer_class = ItemSerializer
    read_serializer_class = ItemSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

class ItemCategoryListView(BaseListView):
    """
    List all Itemcategory, or create a new Itemcategory.
    """
    model = ItemCategory
    serializer_class = ItemCategorySerializer
    read_serializer_class = ItemCategorySerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ItemCategoryDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an Itemcategory.
    """
    model = ItemCategory
    serializer_class = ItemCategorySerializer
    read_serializer_class = ItemCategorySerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

class EvidenceListView(BaseListView):
    """
    List all evidence, or create a new evidence.
    """
    model = Evidence
    serializer_class = EvidenceSerializer
    read_serializer_class = EvidenceSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class EvidenceDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an evidence.
    """
    model = Evidence
    serializer_class = EvidenceSerializer
    read_serializer_class = EvidenceSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

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
    model = Evidence
    serializer_class = EvidenceSerializer
    read_serializer_class = EvidenceSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

class EvidenceImageListView(ImageBaseListView):
    """
    List all evidenceimage, or create a new evidenceimage.
    """
    model = EvidenceImage
    serializer_class = EvidenceImageSerializer
    read_serializer_class = EvidenceImageSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request) 

class EvidenceImageDetailView(ImageBaseDetailView):
    """
    Retrieve , updates and delete an evidenceimage.
    """
    model = EvidenceImage
    serializer_class = EvidenceImageSerializer
    read_serializer_class = EvidenceImageSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk) 

class OccurrenceListView(BaseListView):
    """
    List all Occurrence, or create a new Occurrence.
    """
    model = Occurrence
    serializer_class = OccurrenceSerializer
    read_serializer_class = OccurrenceSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class OccurrenceDetailView(BaseDetailView):
    """
    Retrieve , updates and delete an Occurrence.
    """
    model = Occurrence
    serializer_class = OccurrenceSerializer
    read_serializer_class = OccurrenceSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

class OccurrenceCategoryListView(BaseListView):
    """
    List all Occurrencecategory, or create a new Occurrencecategory.
    """
    model = OccurrenceCategory
    serializer_class = OccurrenceCategorySerializer
    read_serializer_class = OccurrenceCategorySerializer
    permission_classes = ()

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

class ArresteeListView(BaseListView):
    """
    List all arrestee, or create a new arrestee.
    """
    model = Arrestee
    serializer_class = ArresteeSerializer
    read_serializer_class = ArresteeSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class ArresteeDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an arrestee.
    """
    model = Arrestee
    serializer_class = ArresteeSerializer
    read_serializer_class = ArresteeSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

class NextofkeenListView(BaseListView):
    """
    List all Nextofkeen, or create a new Nextofkeen.
    """
    model = Arrestee
    serializer_class = ArresteeSerializer
    read_serializer_class = ArresteeSerializer
    permission_classes = ()

    def get(self, request):
        return super().get(request)

    def post(self, request):
        return super().post(request)

class NextofkeenDetailView(BaseDetailView):

    """
    Retrieve , updates and delete an Nextofkeen.
    """
    model = Next_of_keen
    serializer_class = NextofkeenSerializer
    read_serializer_class = NextofkeenSerializer
    permission_classes = ()

    def get(self, request, pk=None):
        return super().get(request, pk)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)

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

class WarrantofarrestListView(BaseListView):
    """
    List all Warrantofarrest, or create a new Warrantofarrest.
    """
    model = Warrant_of_arrest
    serializer_class = WarrantofarrestSerializer
    read_serializer_class = WarrantofarrestSerializer
    permission_classes = ()

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
        'genders': reverse(f'{app_name}:{pre}-gender-list', request=request, format=format),
        'countries': reverse(f'{app_name}:{pre}-country-list', request=request, format=format),
        'IPRS persons': reverse(f'{app_name}:{pre}-iprs-person-list', request=request, format=format),
        'ranks': reverse(f'{app_name}:{pre}-rank-list', request=request, format=format),
        'police stations': reverse(f'{app_name}:{pre}-police-station-list', request=request, format=format),
        'police offices': reverse(f'{app_name}:{pre}-police-officer-list', request=request, format=format),
        'items': reverse(f'{app_name}:{pre}-item-list', request=request, format=format),
        'item/categories': reverse(f'{app_name}:{pre}-item-categories', request=request, format=format),
        'evidences': reverse(f'{app_name}:{pre}-evidence', request=request, format=format),
        'evidenceimages': reverse(f'{app_name}:{pre}-evidenceimage', request=request, format=format),
        'occurrences': reverse(f'{app_name}:{pre}-occurrences', request=request, format=format),
        'occurrence/categories': reverse(f'{app_name}:{pre}-occurrence-categories', request=request, format=format),
        'arrestees': reverse(f'{app_name}:{pre}-arrestees', request=request, format=format),
        'Next_of_keen_list': reverse(f'{app_name}:{pre}-Next_of_keen_list', request=request, format=format),
        'mugshots': reverse(f'{app_name}:{pre}-mugshots', request=request, format=format),
        'offenses': reverse(f'{app_name}:{pre}-offences', request=request, format=format),
        'chargesheets': reverse(f'{app_name}:{pre}-chargesheets', request=request, format=format),
        'chargesheetpersons': reverse(f'{app_name}:{pre}-chargesheetpersons', request=request, format=format),
        'courtfiles': reverse(f'{app_name}:{pre}-courtfiles', request=request, format=format),
        'fingerprints': reverse(f'{app_name}:{pre}-fingerprints', request=request, format=format),
        'policecells': reverse(f'{app_name}:{pre}-policecells', request=request, format=format),
        'warrant_of_arrests': reverse(f'{app_name}:{pre}-warrantofarrests', request=request, format=format),
    })
