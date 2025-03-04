from django.shortcuts import render
# Create your views here.
from .Upload import Upload
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, FileResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.helper.helper import Helper
from django.db.models import Q
from api.config import webconfig
from ..users.Users import Users
from api.views import Goals
import os
# from PIL import Image
###############33
DEFAULT_LANG = "en"

# init module class
_upload = Upload()
_helper = Helper()
_user = Users()
_goal = Goals()


class uploadVideo(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    #######################
    def get(self, request, lang):
        return JsonResponse({"message": "Invalid request method", "status": "failed"}, status=400)
    def post(self, request, lang):
        helper = Helper()
        if request.FILES:
            file = request.FILES['video']
            video_no = request.POST['video_no']
            ##########################
            if 'video_no' not in request.POST or not request.POST['video_no']:
                return JsonResponse({"message": "Incomplete data request", "status": "failed"}, status=400)
            elif not _videos.videoExists(request, lang, video_no):
                return JsonResponse({"message": "Video doesn't exists", "status": "failed"}, status=400)
            # get video
            _mvideo = _videos.getVideoByNo(request, lang, video_no)
            ######################
            if _mvideo["is_episode"] and int(_mvideo["season_no"]) == 0:
                return JsonResponse({"message": "Please first specify a season to which this episode belongs", "status": "failed"}, status=400)
            elif _mvideo["is_episode"] and int(_mvideo["episode_no"]) == 0:
                return JsonResponse({"message": "Please first specify the episode number", "status": "failed"}, status=400)
            #######
            video_prefix = video_no if not _mvideo["is_episode"] else f"{video_no}_s0{_mvideo['season_no']}e0{_mvideo['episode_no']}"
            video_dir = _mvideo["video_directory"]
            #######################################
            video_path = f"media/{video_dir}/"
            # print(video_path)
            if not os.path.exists(video_path):
                os.mkdir(video_path)
            file_name, file_extension = os.path.splitext(file.name)
            fname = _helper.passwordEncrypt(f"{video_no}") # encrpted file
            video_name = f"{video_no}{file_extension}".replace(" ", "")
            # Upload image
            output = f'{video_path}{video_name}'.strip().replace(" ", "")
            # delete file if it exists
            if os.path.exists(output):
               os.remove(output)
            #########
            if file_extension in webconfig.valid_video_extensions:
                # upload file
                _upload.upload(output, file)
                # get meta data
                _videodata = _upload.getVideoMetaData(output)
                vhieght = _videodata["height"]
                #print(_videodata)
                if _videos.isVideoHeightSupported(request, lang, vhieght):
                    finalfilename = f"{video_prefix}_{vhieght}p{file_extension}".strip()
                    finaloutput = f"{video_path}{finalfilename}"
                    # if file already exist, first delete it
                    if os.path.exists(finaloutput):
                       os.remove(finaloutput)
                    # rename file
                    #print(finaloutput)
                    os.rename(output, finaloutput)
                    _videos.UpdateVideoResolution(request, lang, _videodata, finalfilename, vhieght, video_no)
                    #######
                    return JsonResponse({
                    "message": "Uploaded video successfully",
                    "status": "success"}, status=200)
                else:
                    # first delete file
                    os.remove(output)
                    return JsonResponse({
                    "message": f"Video of {vhieght}p hieght is not supported",
                    "status": "success"}, status=400)
            #     # Check if its the required image
            #     # img = Image.open(output)
            #     # width, height = img.size
            #     # saveImageResolution(
            #     #     output, image_path, image_no_encrypt)
            #     # delete the uploaded director
                
            else:
                valid_ext = ""
                for ext in webconfig.valid_video_extensions:
                    valid_ext += f"{ext}, ".replace(".", "")
                valid_ext = valid_ext[:-2]
                return JsonResponse(
                    {"message": f"Invalid image extension, We only support {valid_ext} files",
                        "status": "failed"},
                    status=400)
        else:
            return JsonResponse({"message": "Please select file to upload", "status": "failed"}, status=400)


class uploadVideoThumbnail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    def get(self, request, lang):
        return JsonResponse({"message": "Invalid request method", "status": "failed"}, status=400)
    def post(self, request, lang):
        helper = Helper()
        if request.FILES:
            file = request.FILES['poster']
            video_no = request.POST['video_no']
            ##########################
            if 'video_no' not in request.POST or not request.POST['video_no']:
                return JsonResponse({"message": "Incomplete data request", "status": "failed"}, status=400)
            elif not _videos.videoExists(request, lang, video_no):
                return JsonResponse({"message": "Video doesn't exists", "status": "failed"}, status=400)
            #######################################
            image_path = f"media/{video_no}/"
            # print(video_path)
            if not os.path.exists(image_path):
                os.mkdir(image_path)
            ###################################
            file_name, file_extension = os.path.splitext(file.name)
            #####################################
            image_name = f"{video_no}{file_extension}".strip()
            # Upload image
            output = f'{image_path}{image_name}'.strip()
            #############################
            if file_extension in webconfig.valid_image_extensions:
                # upload file
                _upload.upload(output, file)
                # Check if its the required image
                img = Image.open(output)
                width, height = img.size
                img.close()
                ###########################
                if width >= webconfig.max_thumbnail_width and height >= webconfig.max_thumbnail_height:
                    self.saveImageResolution(
                        output, image_path, video_no)
                    sizes = webconfig.sizes
                    ##########################################
                    default_poster_size = sizes[0]
                    dwidth = default_poster_size["width"]
                    dheight = default_poster_size["height"]
                    default_poster_image = f"{video_no}_{dwidth}x{dheight}.jpg".strip()
                    _videos.UpdateVideoPoster(default_poster_image, video_no)
                    # delete the uploaded director
                    return JsonResponse({
                        "image_id": video_no,
                        "image_id_encrypt": video_no,
                        "extension": file_extension,
                        "original_image": default_poster_image,
                        "image_output_image": f"{webconfig.VIDEO_THUMBNAIL_ROOT}/{video_no}/{default_poster_image}",
                        "message": "Uploaded image successfully",
                        "status": "success"}, status=200)
                else:
                    os.remove(output)
                    return JsonResponse({"message": f"Invalid image size, your image must be atleast {webconfig.max_thumbnail_width}x{webconfig.max_thumbnail_height} not {width}x{height}", "status": "failed"}, status=400)
            else:
                valid_ext = ""
                for ext in webconfig.valid_image_extensions:
                    valid_ext += f"{ext}, ".replace(".", "")
                valid_ext = valid_ext[:-2]
                return JsonResponse({"message": f"Invalid image extension, We only support {valid_ext}", "status": "failed"}, status=400)
        else:
            return JsonResponse({"message": "Incomplete request data", "status": "failed"}, status=400)

    def upload(self, output, file):
        destination = open(output, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

    def saveImageResolution(self, output, image_path, image_no):
        image = Image.open(output)
        sizes = webconfig.sizes
        for size in sizes:
            width = size["width"]
            height = size["height"]
            path = f"{image_path}{image_no}_{width}x{height}.jpg"
            resize_image = image.resize((width, height))
            resize_image.save(path)
        os.remove(output)


class UploadPhoto(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request, lang):
        photo = request.data['photo']
        userid = request.user.id
        if photo:
            # destination = 'media/profile/'
            # _upload.upload(destination,photo)
            _user.UpdateProfilePhoto(request, lang, userid, photo)
            return Response({"message": "Upload successful", "success": True})
        else:
            return Response({"message": "Incomplete request data", "success": False})


class UploadGoalPhoto(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, lang):
        photo = request.data['photo']
        goalid = request.data['goal_id']
        if photo:
            # destination = 'media/profile/'
            # _upload.upload(destination,photo)
            _goal.UpdateGoalPhoto(goalid, photo)
            return Response({"message": "Upload successful", "success": True})
        else:
            return Response({
                "message": "Incomplete request data",
                "success": False
                })


class UploadFile(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request, lang):
        moa = request.data['moa']
        userid = request.user.id
        if moa:
            # destination = 'media/profile/'
            # _upload.upload(destination,photo)
            _user.UpdateProfilePhoto(request, lang, userid, moa)
            return Response({"message": "Upload successful", "success": True})
        else:
            return Response({"message": "Incomplete request data", "success": False})
