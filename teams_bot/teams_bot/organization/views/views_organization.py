from rest_framework import generics, permissions, status, response

from organization.models import Organization
from organization.serializers.serializer_organization import OrganizationSerializer, OrganizationUser
from lib.drf.permissions import base


class OrganizationViewSet(generics.GenericAPIView):
    # permission_set = {
    #     'GET': ['organization.view'],
    #     'POST': ['organization.add'],
    #     'PUT': ['organization.change'],
    #     'DELETE': ['organization.delete'],
    # }
    # permission_classes = [permissions.IsAuthenticated, base.ValidatePermissionSet]
    permission_classes = []

    serializer_class = OrganizationSerializer

    def get(self, request):
        print(request.user)
        organization_obj = OrganizationUser.objects.filter(user=request.user)
        org_obj = []
        for i in organization_obj:
            org_obj.append(i.organization)
        queryset = org_obj
        serializer = OrganizationSerializer(queryset, many=True)
        res = {"organizations": serializer.data}
        return response.Response(res)
