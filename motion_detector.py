from datetime import date, datetime
import cv2, time, pandas

from cv2 import threshold

first_frame = None
status_list = [None, None]
times = []
data_frame = pandas.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = False
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Applies gaussian blur, this increases accuracy of detection.
    current_frame_blurred = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = current_frame_blurred
        continue

    delta_frame = cv2.absdiff(first_frame, current_frame_blurred)

    threshold_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    threshold_frame = cv2.dilate(threshold_delta, None, iterations=2)

    (cnts, _) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = True

        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1]==True and status_list[-2]==False:
        times.append(datetime.now())
    if status_list[-1]==False and status_list[-2]==True:
        times.append(datetime.now())

    cv2.imshow("Gray Frame", current_frame_blurred)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Color Frame", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == True:
            times.append(datetime.now())
        break

print(status_list)

for i in range(0, len(times),2):
    data_frame = data_frame.append({"Start":times[i], "End":times[i + 1]},ignore_index=True)

data_frame.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()