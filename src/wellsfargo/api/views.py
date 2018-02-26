from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework import views, generics, status, serializers
from oscarapi.basket import operations
from ..core.constants import (
    US, CA,
    INDIVIDUAL, JOINT
)
from ..models import PreQualificationResponse
from .serializers import (
    AppSelectionSerializer,
    USCreditAppSerializer,
    USJointCreditAppSerializer,
    CACreditAppSerializer,
    CAJointCreditAppSerializer,
    FinancingPlanSerializer,
    AccountInquirySerializer,
    PreQualificationRequestSerializer,
    PreQualificationResponseSerializer,
)
from ..utils import list_plans_for_basket

PREQUAL_SESSION_KEY = 'wfrs-prequal-request-id'


class SelectCreditAppView(generics.GenericAPIView):
    serializer_class = AppSelectionSerializer

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'url': self._get_app_url(request, **serializer.validated_data),
        })

    def _get_app_url(self, request, region, app_type):
        routes = {
            US: {
                INDIVIDUAL: reverse_lazy('wfrs-api-apply-us-individual', request=request),
                JOINT: reverse_lazy('wfrs-api-apply-us-join', request=request),
            },
            CA: {
                INDIVIDUAL: reverse_lazy('wfrs-api-apply-ca-individual', request=request),
                JOINT: reverse_lazy('wfrs-api-apply-ca-joint', request=request),
            },
        }
        return routes.get(region, {}).get(app_type)


class BaseCreditAppView(generics.GenericAPIView):
    def post(self, request):
        request_ser = self.get_serializer_class()(data=request.data, context={'request': request})
        request_ser.is_valid(raise_exception=True)
        result = request_ser.save()
        response_ser = AccountInquirySerializer(instance=result, context={'request': request})
        return Response(response_ser.data)


class USCreditAppView(BaseCreditAppView):
    serializer_class = USCreditAppSerializer


class USJointCreditAppView(BaseCreditAppView):
    serializer_class = USJointCreditAppSerializer


class CACreditAppView(BaseCreditAppView):
    serializer_class = CACreditAppSerializer


class CAJointCreditAppView(BaseCreditAppView):
    serializer_class = CAJointCreditAppSerializer


class FinancingPlanView(views.APIView):
    def get(self, request):
        basket = operations.get_basket(request)
        plans = list_plans_for_basket(basket)
        ser = FinancingPlanSerializer(plans, many=True)
        return Response(ser.data)


class SubmitAccountInquiryView(generics.GenericAPIView):
    serializer_class = AccountInquirySerializer

    def post(self, request):
        request_ser = self.get_serializer_class()(data=request.data, context={'request': request})
        request_ser.is_valid(raise_exception=True)
        result = request_ser.save()
        response_ser = self.get_serializer_class()(instance=result, context={'request': request})
        return Response(response_ser.data)


class PreQualificationRequestView(generics.GenericAPIView):
    serializer_class = PreQualificationRequestSerializer

    def get(self, request):
        prequal_request_id = request.session.get(PREQUAL_SESSION_KEY)
        if not prequal_request_id:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            prequal_response = PreQualificationResponse.objects.get(request__id=prequal_request_id)
        except PreQualificationResponse.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_ser = PreQualificationResponseSerializer(instance=prequal_response, context={'request': request})
        return Response(response_ser.data)


    def post(self, request):
        request_ser = self.get_serializer_class()(data=request.data, context={'request': request})
        request_ser.is_valid(raise_exception=True)
        prequal_request = request_ser.save()
        try:
            prequal_response = prequal_request.response
        except PreQualificationResponse.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        request.session[PREQUAL_SESSION_KEY] = prequal_request.pk
        response_ser = PreQualificationResponseSerializer(instance=prequal_response, context={'request': request})
        return Response(response_ser.data)


class PreQualificationCustomerResponseView(views.APIView):
    serializer_class = PreQualificationResponseSerializer

    def post(self, request):
        prequal_request_id = request.session.get(PREQUAL_SESSION_KEY)
        if not prequal_request_id:
            raise serializers.ValidationError('No pre-qualification response was found for this session.')
        try:
            prequal_response = PreQualificationResponse.objects.get(request__id=prequal_request_id)
        except PreQualificationResponse.DoesNotExist:
            raise serializers.ValidationError('No pre-qualification response was found for this session.')
        serializer = self.get_serializer_class()(
            instance=prequal_response,
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
