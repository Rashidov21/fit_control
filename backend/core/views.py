"""
API views for authentication and core functionality.
"""
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login
from .serializers import UserSerializer, LoginSerializer, QRCodeSerializer
from .models import User, QRCode


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response({
            'user': user_serializer.data,
            'is_superuser': user.is_superuser,
            'is_gym_admin': user.is_gym_admin,
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user."""
    serializer = UserSerializer(request.user)
    return Response({
        'user': serializer.data,
        'is_superuser': request.user.is_superuser,
        'is_gym_admin': request.user.is_gym_admin,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """User logout endpoint."""
    from django.contrib.auth import logout
    logout(request)
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class QRCodeDetailView(generics.RetrieveAPIView):
    """Get QR code for gym."""
    serializer_class = QRCodeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Get QR code for current user's gym."""
        try:
            if self.request.user.is_superuser:
                gym_id = self.request.query_params.get('gym_id')
                if gym_id:
                    try:
                        from gyms.models import Gym
                        gym = Gym.objects.get(id=gym_id)
                    except Gym.DoesNotExist:
                        from rest_framework.exceptions import NotFound
                        raise NotFound('Gym not found.')
                else:
                    from rest_framework.exceptions import ValidationError
                    raise ValidationError('gym_id parameter is required for superuser.')
            else:
                gym = self.request.user.gym
            
            if not gym:
                from rest_framework.exceptions import NotFound
                raise NotFound('No gym associated with this user.')
            
            qr_code, created = QRCode.objects.get_or_create(gym=gym)
            return qr_code
        except Exception as e:
            from rest_framework.exceptions import APIException
            raise APIException(f'Error retrieving QR code: {str(e)}')


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_qr_token(request, token):
    """Verify QR token for Telegram bot."""
    try:
        if not token:
            return Response({
                'valid': False,
                'error': 'Token is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        qr_code = QRCode.objects.get(token=token)
        return Response({
            'valid': True,
            'gym_id': qr_code.gym.id,
            'gym_name': qr_code.gym.name,
        }, status=status.HTTP_200_OK)
    except QRCode.DoesNotExist:
        return Response({
            'valid': False,
            'error': 'Invalid QR token'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'valid': False,
            'error': f'Error verifying token: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)