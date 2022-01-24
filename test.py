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
    
    copy = frame.copy()

    gray = cv.cvtColor(copy,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize = 3)

    cv.imshow('edges', edges)

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
    
    combined_img = np.bitwise_and(np.bitwise_not(edges), final_thresh)
    cv.imshow('thresh and canny', combined_img)


    contours_final, _ = cv.findContours(combined_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours_final:
        if cv.contourArea(contour) > 300:
            final_contour_img = cv.drawContours(final_contour_img, [contour], -1, (0,255,0), 3)
    
    
    cv.imshow('contours normal', final_contour_img)
    


    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 10  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments
    line_image = np.copy(copy)  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv.line(line_image, (x1,y1), (x2,y2), (255,0,0), 3)

    cv.imshow('lines', line_image)




    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    



# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()