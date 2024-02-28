# video/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import movenet
# Your existing index view
def index(request):
    return render(request, 'index.html')

# Add the process_frame view below your existing views
@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        frame = request.FILES.get('frame')
        if not frame:
            return JsonResponse({'error': 'No frame provided'}, status=400)
        
        # Save the frame temporarily
        frame_path = 'temp_frame.jpg'  # Consider using a unique path for each request
        with open(frame_path, 'wb+') as destination:
            for chunk in frame.chunks():
                destination.write(chunk)
        
        # Assuming you have a function called process_movenet_single_frame that
        # processes the image and returns keypoints (you need to define or import this)
        keypoints = movenet.process_movenet_single_frame(frame_path)
        
        # Cleanup: remove the temporary file after processing
        os.remove(frame_path)
        
        # Return the keypoints as JSON
        return JsonResponse({'keypoints': keypoints})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

