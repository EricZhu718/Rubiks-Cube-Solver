# import the opencv library
from asyncio.windows_events import NULL
import cv2 as cv
import numpy as np
  
  
# define a video capture object
vid = cv.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv.imshow('unaltered', frame)

    

    size_percent = 1
    # Makes a copy
    overlayImage=np.copy(frame)[int(len(frame) * (1-size_percent) / 2):int(len(frame) * (size_percent + (1-size_percent) / 2)), int(len(frame[0]) * (1-size_percent) / 2):int(len(frame[0]) * (size_percent+(1-size_percent) / 2))]
    
    grayscaleImage=cv.cvtColor(overlayImage, cv.COLOR_BGR2GRAY)

    blue = overlayImage[:,:,0]
    green = overlayImage[:,:,1]
    red = overlayImage[:,:,2]


    mean = np.mean(grayscaleImage)


    ret, thresh = cv.threshold(grayscaleImage, min(0.75*mean, 255), 255, cv.THRESH_BINARY)
    ret, thresh_green = cv.threshold(green, min(0.75*mean, 255), 255, cv.THRESH_BINARY)
    ret, thresh_red = cv.threshold(red, min(0.75*mean, 255), 255, cv.THRESH_BINARY)
    ret, thresh_blue = cv.threshold(blue, min(0.75*mean, 255), 255, cv.THRESH_BINARY)

    final_thresh = np.bitwise_or(thresh, thresh_blue)
    final_thresh = np.bitwise_or(thresh_red, thresh_green)

    cv.imshow('thresh', final_thresh)

    final_contour_img = overlayImage.copy()
    contours_final, _ = cv.findContours(final_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours_final:
        if cv.contourArea(contour) > 300:
            final_contour_img = cv.drawContours(final_contour_img, [contour], -1, (0,255,0), 3)
    cv.imshow('contours', final_contour_img)
    

    copy = frame.copy()

    gray = cv.cvtColor(copy,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,50,150,apertureSize = 3)

    cv.imshow('edges', edges)

    



    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    



# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()