from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *


class User_Resource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = (
            'UserID', 'Name', 'Email', 'Password', 'Phone', 'SSN', 'AddressLine1', 'AddressLine2', 'City', 'Country',
            'Longitude', 'Latitude', 'TimeZone', 'MotionDetection',
            'MotionAlert', 'MotionSensitivity', 'CrimeDetection', 'CrimeAlert',
            'CrimeSensitivity',)


class User_Admin(ImportExportModelAdmin):
    resource_class = User_Resource


class Feed_Resource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = (
            'UserID', 'CameraID', 'CameraLocation', 'Url', 'UserName', 'Password',)


class Feed_Admin(ImportExportModelAdmin):
    resource_class = Feed_Resource


class Threat_Resource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ('ThreatID', 'CameraID', 'ReportTo')


class Threat_Admin(ImportExportModelAdmin):
    resource_class = Threat_Resource


class ThreatLog_Resource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = (
            'ThreatID', 'UserID', 'CameraID', 'File', 'TimeStamp', 'Category', 'Duration', 'Confidence', 'Type')


class ThreatLog_Admin(ImportExportModelAdmin):
    resource_class = ThreatLog_Resource
