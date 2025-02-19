from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserInfoForm, ImageForm
from .models import OasisInfo, Image, Mandatory_Documents
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse
from datetime import datetime
import json


@login_required
# def home(request, id=None):
#     instance = None
#     images = []

#     if id: 
#         instance = get_object_or_404(OasisInfo, id=id)

#     if request.method == 'POST':
#         form = UserInfoForm(request.POST, request.FILES, instance=instance)

#         if form.is_valid():
#             oasis_info = form.save(commit=False)
#             oasis_info.save()

#             # Save images
#             if request.FILES.getlist('images[]'):
#                 img_des_list = request.POST.getlist('img_descriptions[]')  # Get all descriptions
#                 for i, img in enumerate(request.FILES.getlist('images[]')):
#                     img_des = img_des_list[i] if i < len(img_des_list) else ""  # Match description with image
#                     image_instance = Image(
#                         oasis_info=oasis_info,
#                         img=img,
#                         img_des=img_des
#                     )
#                     image_instance.save()

#             for image in Image.objects.filter(oasis_info=oasis_info):
#                 img_des_key = f'img_des_{image.id}'
#                 updated_description = request.POST.get(img_des_key, image.img_des)
#                 if updated_description != image.img_des:
#                     image.img_des = updated_description
#                     image.save()

#             form_data = form.cleaned_data
#             all_filled = all(bool(value) for value in form_data.values())

#             if all_filled:
#                 messages.success(request, 'The record has been completed successfully!')
#                 return redirect('complete')
#             else:
#                 messages.warning(request, 'Some fields are still pending!')
#                 return redirect('pending')

#     else:
#         form = UserInfoForm(instance=instance)

#     if id:
#         images = Image.objects.filter(oasis_info=instance)

#     return render(request, 'home.html', {
#         'form': form,
#         'images': images,
#     })


def home(request, id=None):
    instance = None
    images = []
    mandatory_documents = None

    if id: 
        instance = get_object_or_404(OasisInfo, id=id)
        mandatory_documents = Mandatory_Documents.objects.filter(oasis_info=instance).first()

    if request.method == 'POST':
        form = UserInfoForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            oasis_info = form.save(commit=False)
            oasis_info.save()

            # Save images
            if request.FILES.getlist('images[]'):
                img_des_list = request.POST.getlist('img_descriptions[]')  # Get all descriptions
                for i, img in enumerate(request.FILES.getlist('images[]')):
                    img_des = img_des_list[i] if i < len(img_des_list) else ""  # Match description with image
                    image_instance = Image(
                        oasis_info=oasis_info,
                        img=img,
                        img_des=img_des
                    )
                    image_instance.save()

            for image in Image.objects.filter(oasis_info=oasis_info):
                img_des_key = f'img_des_{image.id}'
                updated_description = request.POST.get(img_des_key, image.img_des)
                if updated_description != image.img_des:
                    image.img_des = updated_description
                    image.save()

            # Save mandatory documents
            if mandatory_documents:
                mandatory_documents.concent_img = request.FILES.get('concent_img', mandatory_documents.concent_img)
                mandatory_documents.emg_img = request.FILES.get('emg_img', mandatory_documents.emg_img)
                mandatory_documents.med_list_img = request.FILES.get('med_list_img', mandatory_documents.med_list_img)
                mandatory_documents.add_doc_img1 = request.FILES.get('add_doc_img1', mandatory_documents.add_doc_img1)
                mandatory_documents.add_doc_img2 = request.FILES.get('add_doc_img2', mandatory_documents.add_doc_img2)
                mandatory_documents.misc_img = request.FILES.get('misc_img', mandatory_documents.misc_img)
                mandatory_documents.save()
            else:
                mandatory_documents = Mandatory_Documents(
                    oasis_info=oasis_info,
                    concent_img=request.FILES.get('concent_img'),
                    emg_img=request.FILES.get('emg_img'),
                    med_list_img=request.FILES.get('med_list_img'),
                    add_doc_img1=request.FILES.get('add_doc_img1'),
                    add_doc_img2=request.FILES.get('add_doc_img2'),
                    misc_img=request.FILES.get('misc_img'),
                )
                mandatory_documents.save()

            form_data = form.cleaned_data
            all_filled = all(bool(value) for value in form_data.values())

            if all_filled:
                messages.success(request, 'The record has been completed successfully!')
                return redirect('complete')
            else:
                messages.warning(request, 'Some fields are still pending!')
                return redirect('pending')

    else:
        form = UserInfoForm(instance=instance)

    if id:
        images = Image.objects.filter(oasis_info=instance)

    return render(request, 'home.html', {
        'form': form,
        'images': images,
        'mandatory_documents': mandatory_documents,
    })




@login_required
def remove_image(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            image_id = body.get('image_id')

            if not image_id:
                raise ValueError("Image ID is required")

            image = Image.objects.get(id=image_id)
            image.img.delete()
            image.delete()

            return JsonResponse({'success': True})

        except Image.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Image not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})



@login_required
# def about(request):
#     oasis_info_id = request.GET.get('id', None)
#     if oasis_info_id:
#         oasis_info = get_object_or_404(OasisInfo, pk=oasis_info_id)
#         oasis_info_form = UserInfoForm(request.POST or None, request.FILES or None, instance=oasis_info)
#     else:
#         oasis_info_form = UserInfoForm(request.POST or None, request.FILES or None)

#     if request.method == 'POST' and oasis_info_form.is_valid():
#         oasis_info = oasis_info_form.save(commit=False)
#         oasis_info.save()

#         if request.FILES.getlist('images[]'):
#             img_des_list = request.POST.getlist('img_descriptions[]')  # Get all descriptions
            
#             for i, img in enumerate(request.FILES.getlist('images[]')):
#                 img_des = img_des_list[i] if i < len(img_des_list) else ""  # Match description with image

#                 image_instance = Image(
#                     oasis_info=oasis_info,
#                     img=img,
#                     img_des=img_des  # Correctly save the description
#                 )
#                 image_instance.save()

#         form_data = oasis_info_form.cleaned_data
#         all_filled = all(bool(value) for value in form_data.values())

#         if all_filled:
#             messages.success(request, 'The record has been completed successfully!')
#             return redirect('complete')
#         else:
#             messages.warning(request, 'Some fields are still pending!')
#             return redirect('pending')

#     user = request.user
#     cli_name = f"{user.last_name}, {user.first_name}" if user.last_name and user.first_name else user.username

#     return render(request, 'about.html', {
#         'oasis_info_form': oasis_info_form,
#         'cli_name': cli_name,
#     })

def about(request):
    oasis_info_id = request.GET.get('id', None)
    if oasis_info_id:
        oasis_info = get_object_or_404(OasisInfo, pk=oasis_info_id)
        oasis_info_form = UserInfoForm(request.POST or None, request.FILES or None, instance=oasis_info)

        # Get or create Mandatory_Documents instance
        mandatory_documents, _ = Mandatory_Documents.objects.get_or_create(oasis_info=oasis_info)

    else:
        oasis_info_form = UserInfoForm(request.POST or None, request.FILES or None)
        mandatory_documents = None

    if request.method == 'POST' and oasis_info_form.is_valid():
        oasis_info = oasis_info_form.save(commit=False)
        oasis_info.save()

        # Save Images with Descriptions
        if request.FILES.getlist('images[]'):
            img_des_list = request.POST.getlist('img_descriptions[]')  

            for i, img in enumerate(request.FILES.getlist('images[]')):
                img_des = img_des_list[i] if i < len(img_des_list) else ""  

                image_instance = Image(
                    oasis_info=oasis_info,
                    img=img,
                    img_des=img_des
                )
                image_instance.save()

        # Save Mandatory Documents if uploaded
        if mandatory_documents:
            if 'concent_img' in request.FILES:
                mandatory_documents.concent_img = request.FILES['concent_img']
            if 'emg_img' in request.FILES:
                mandatory_documents.emg_img = request.FILES['emg_img']
            if 'med_list_img' in request.FILES:
                mandatory_documents.med_list_img = request.FILES['med_list_img']
            if 'add_doc_img1' in request.FILES:
                mandatory_documents.add_doc_img1 = request.FILES['add_doc_img1']
            if 'add_doc_img2' in request.FILES:
                mandatory_documents.add_doc_img2 = request.FILES['add_doc_img2']
            if 'misc_img' in request.FILES:
                mandatory_documents.misc_img = request.FILES['misc_img']

            mandatory_documents.save()

        # Check if all fields are filled
        form_data = oasis_info_form.cleaned_data
        all_filled = all(bool(value) for value in form_data.values())

        if all_filled:
            messages.success(request, 'The record has been completed successfully!')
            return redirect('complete')
        else:
            messages.warning(request, 'Some fields are still pending!')
            return redirect('pending')

    user = request.user
    cli_name = f"{user.last_name}, {user.first_name}" if user.last_name and user.first_name else user.username

    return render(request, 'about.html', {
        'oasis_info_form': oasis_info_form,
        'mandatory_documents': mandatory_documents,
        'cli_name': cli_name,
    })



@login_required
def pending(request):
    user = request.user
    if user.is_superuser:
        rows = OasisInfo.objects.all().order_by('-modified_date', '-created_date')
    else:
        cli_name = f"{user.last_name}, {user.first_name}" if user.last_name and user.first_name else user.username
        rows = OasisInfo.objects.filter(cli_name=cli_name).order_by('-modified_date', '-created_date')

    for row in rows:
        if row.visit_date:
            try:
                row.visit_date = datetime.strptime(row.visit_date, "%Y-%m-%d")
            except ValueError:
                row.visit_date = None
    
    return render(request, 'pending.html', {'rows': rows})


@login_required
def complete(request):
    user = request.user
    if user.is_superuser:
        rows = OasisInfo.objects.all().order_by('-modified_date', '-created_date')
    else:
        cli_name = f"{user.last_name}, {user.first_name}" if user.last_name and user.first_name else user.username
        rows = OasisInfo.objects.filter(cli_name=cli_name).order_by('-modified_date', '-created_date')

    for row in rows:
        if row.visit_date:
            try:
                row.visit_date = datetime.strptime(row.visit_date, "%Y-%m-%d")
            except ValueError:
                row.visit_date = None
                
    return render(request, 'completed.html', {'rows': rows})

@login_required
def pending_oasis_forms(request):
    search_query = request.GET.get('search', '')
    if search_query:
        rows = OasisInfo.objects.filter(name__icontains=search_query) | OasisInfo.objects.filter(mrn__icontains=search_query)
    else:
        rows = OasisInfo.objects.all()
    
    return render(request, 'pending_oasis_forms.html', {'rows': rows})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def capture_and_edit(request):
    return render(request, 'test.html')







# from django.utils.timezone import now
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import User
# from .utils import send_otp
# from django.views.decorators.csrf import csrf_exempt
# import json
# import random
# from twilio.rest import Client
# from django.contrib.auth.hashers import make_password




# otp_store = {}

# @csrf_exempt
# def send_otp(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         mobile_number = data.get('mobile_number')

#         if not mobile_number:
#             return JsonResponse({'error': 'Mobile number is required'}, status=400)
#         otp = str(random.randint(100000, 999999))

#         try:
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#             message = client.messages.create(
#                 body=f"Your OTP is: {otp}",
#                 from_=TWILIO_PHONE_NUMBER,
#                 to=mobile_number
#             )
#             otp_store[mobile_number] = otp
#             return JsonResponse({'message': 'OTP sent successfully'}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# def verify_otp(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             mobile_number = data.get('mobile_number')
#             otp = data.get('otp')
#             redirect_url = data.get('redirect_url')  # Capture the redirect URL from the request body

#             if not mobile_number or not otp:
#                 return JsonResponse({'error': 'Mobile number and OTP are required'}, status=400)
#             if otp_store.get(mobile_number) == otp:
#                 del otp_store[mobile_number] 
#                 request.session['verified_mobile_number'] = mobile_number
                
#                 # If a redirect URL is provided, use it
#                 if redirect_url:
#                     return JsonResponse({'message': 'OTP verified successfully', 'redirect_url': redirect_url}, status=200)
#                 else:
#                     return JsonResponse({'message': 'OTP verified successfully, no redirect URL found'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid OTP'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



# def reset_password(request):
#     verified_mobile_number = request.session.get('verified_mobile_number')
#     if not verified_mobile_number:
#         return redirect('login')  # Redirect to login if the session is not verified
#     return render(request, 'reset_password.html')

# @csrf_exempt
# def update_password(request):
#     if request.method == 'GET':
#         # Render the password update form
#         return render(request, 'update_password.html')

#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')

#         # Retrieve the verified phone number from the session
#         verified_phone_number = request.session.get('verified_mobile_number')
#         if not verified_phone_number:
#             return JsonResponse({'error': 'Session expired. Please verify OTP again.'}, status=400)

#         # Update the password
#         try:
#             user = User.objects.get(phone_number=verified_phone_number)
#             user.set_password(new_password)  # Use set_password to hash and save the password
#             user.save()

#             # Clear the session and redirect to login
#             del request.session['verified_mobile_number']
#             return redirect('login')  # Replace 'login' with the name of your login route

#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found.'}, status=404)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)




# from django.contrib.auth.forms import PasswordResetForm
# from django.shortcuts import render, redirect
# from twilio.rest import Client
# from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.auth import get_user_model

# def send_sms_reset(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         user = get_user_model().objects.filter(profile__phone_number=phone_number).first()

#         if user:
#             # Generate token
#             uid = urlsafe_base64_encode(user.pk.encode('utf-8'))
#             token = default_token_generator.make_token(user)

#             reset_link = f"{request.build_absolute_uri('/reset-password/')}?uid={uid}&token={token}"
#             send_sms(phone_number, reset_link)

#             return redirect('password_reset_done')

#     return render(request, 'send_sms_reset.html')

# def send_sms(phone_number, reset_link):
#     # Twilio client setup
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     client.messages.create(
#         body=f"Password reset link: {reset_link}",
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )

# def send_reset_link(request):
#     if request.method == 'POST':
#         try:
#             # Parse the incoming JSON data
#             data = json.loads(request.body)
#             mobile_number = data.get('mobile_number')

#             # Check if mobile number is provided
#             if not mobile_number:
#                 return JsonResponse({'error': 'Mobile number is required'}, status=400)

#             try:
#                 # Retrieve the user associated with the mobile number
#                 user = User.objects.get(profile__mobile_number=mobile_number)  # Adjust if needed for your model

#                 # Generate the reset token using Django's password reset token generator
#                 token = default_token_generator.make_token(user)

#                 # Create the reset link using the generated token
#                 reset_link = f'http://127.0.0.1:8000/accounts/reset/{user.pk}/{token}/'

#                 # Construct the message like the email content
#                 message_body = f'''
#                 You're receiving this SMS because you requested a password reset for your user account at 127.0.0.1:8000.

#                 Please go to the following page and choose a new password:

#                 {reset_link}

#                 Your username, in case you’ve forgotten: {user.username}

#                 Thanks for using our site!

#                 The 127.0.0.1:8000 team
#                 '''

#                 # Send the message using Twilio
#                 client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#                 # Send the SMS
#                 message = client.messages.create(
#                     body=message_body,
#                     from_=TWILIO_PHONE_NUMBER,
#                     to=mobile_number
#                 )

#                 return JsonResponse({'message': 'Reset link sent successfully via SMS'}, status=200)

#             except User.DoesNotExist:
#                 return JsonResponse({'error': 'User not found for this mobile number'}, status=404)
#             except Exception as e:
#                 return JsonResponse({'error': f'Failed to send reset link: {str(e)}'}, status=500)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)



