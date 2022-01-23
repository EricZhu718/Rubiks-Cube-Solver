# import the opencv library
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

    

    size_percent = 0.5
    # Makes a copy
    overlayImage=np.copy(frame)[int(len(frame) * (1-size_percent) / 2):int(len(frame) * (size_percent + (1-size_percent) / 2)), int(len(frame[0]) * (1-size_percent) / 2):int(len(frame[0]) * (size_percent+(1-size_percent) / 2))]
    
    grayscaleImage=cv.cvtColor(overlayImage, cv.COLOR_BGR2GRAY)
    mean = np.mean(grayscaleImage)


    ret, thresh = cv.threshold(grayscaleImage, min(0.7*mean, 255), 255, cv.THRESH_BINARY)
    cv.imshow('thresh', thresh)

    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contour_img = cv.drawContours(overlayImage, contours, -1, (0,255,0), 6)
    
    
    cv.imshow('contours', contour_img)
    
    
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    



# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()