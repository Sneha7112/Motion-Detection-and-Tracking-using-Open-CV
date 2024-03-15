import cv2

cap = cv2.VideoCapture('test3.mp4')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (frame_width, frame_height))

ret, frame1 = cap.read()
if not ret:
    print("Error: Could not read the video file.")
    exit()

ret, frame2 = cap.read()
if not ret:
    print("Error: Could not read the video file.")
    exit()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 800:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame1, "Status: {}".format('Movement Detected'), (10, 20), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 3)

    out.write(frame1)
    cv2.imshow("feed", frame1)

    # Update frames
    frame1 = frame2
    ret, frame2 = cap.read()
    if not ret:
        print("End of video.")
        break

    # Check for the close button event
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
out.release()
