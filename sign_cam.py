# 카메라 통신 및 표지판 인식
# input: sign_cam
# output: 표지판 종류 (to car_control)

# modes = {'DEFAULT': 0, 'PARKING': 1, 'STATIC_OBS': 2,
#          'MOVING_OBS': 3,'S_CURVE': 4, 'NARROW': 5, 'U_TURN': 6, 'CROSS_WALK': 7}

import cv2
import threading
import numpy as np
import time

crosswalk_stop = 0
narrow_stop = 0
moving_stop = 0
static_stop = 0
s_curve_stop = 0
u_turn_stop = 0
parking_stop = 0

detect_crsosswalk = 0
detect_narrow = 0
detect_moving = 0
detect_static = 0
detect_scurve = 0
detect_uturn = 0
detect_parking = 0

is_in_mission = False

####################### Sign Borad ##########################
try:
    parking_cascade = cv2.CascadeClassifier('./sign_xml_files/parkingdetect.xml')  # 1. 자동 주차
    static_cascade = cv2.CascadeClassifier('./sign_xml_files/static_0514.xml')  # 2. 정적 장애물
    moving_cascade = cv2.CascadeClassifier('./sign_xml_files/moving_0510.xml')  # 3. 동적 장애물
    s_curve_cascade = cv2.CascadeClassifier('./sign_xml_files/scurve_0517.xml')  # 4. S자 주행
    narrow_cascade = cv2.CascadeClassifier('./sign_xml_files/narrowno.xml')  # 5. 협로 주행
    u_turn_cascade = cv2.CascadeClassifier('./sign_xml_files/uturndetect.xml')  # 6. 유턴
    crosswalk_cascade = cv2.CascadeClassifier('./sign_xml_files/crosswalk.xml')  # 7. 횡단보도
except Exception as e:
    print(e)
    exit(1)


def give_delay_for_test():
    global is_in_mission, Mission
    time.sleep(3)
    is_in_mission = False
    Mission = 0


########################## Machine ###########################
def crosswalk_detect():  # 05016 am09  yoon test : 1.07/20 good
    global crosswalk_stop, is_in_mission, Mission, img
    if crosswalk_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 1 Crosswalk is ", crosswalk_stop)
        crosswalk = crosswalk_cascade.detectMultiScale(gray, 1.1, 20)
        for (x, y, w, h) in crosswalk:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        rec1 = np.matrix(crosswalk)

        if np.sum(rec1) >= 1:
            detect_crosswalk = 1
            crosswalk_stop += 1
            if crosswalk_stop == 3:  # 세 프레임 이상 인식하면 미션 시작으로 인식
                Mission = 3
                is_in_mission = True
                give_delay_for_test()  # 테스트 할 때만 쓰는 것. 실제로 쓰려면 이 줄 없애야 함
            print("CrossWalk!!! ", detect_crosswalk)


def narrow_detect():
    global narrow_stop, is_in_mission, Mission, img
    if narrow_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 2 Narrow is ", narrow_stop)
        narrow = narrow_cascade.detectMultiScale(gray, 1.1, 15)
        for (x, y, w, h) in narrow:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        rec2 = np.matrix(narrow)

        if np.sum(rec2) >= 1:
            detect_narrow = 2
            narrow_stop += 1
            if narrow_stop == 3:
                Mission = 2
                is_in_mission = True
            print("Narrow!!!!! ", detect_narrow)


def moving_detect():
    global moving_stop, is_in_mission, Mission, img
    if moving_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 3 Moving is ", moving_stop)
        moving = moving_cascade.detectMultiScale(gray, 1.03, 5)
        for (x, y, w, h) in moving:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 150, 0), 2)
        rec3 = np.matrix(moving)

        if np.sum(rec3) >= 1:
            detect_moving = 3
            moving_stop += 1
            if moving_stop == 3:
                Mission = 1
                is_in_mission = True
                give_delay_for_test()  # 테스트 할 때만 쓰는 것. 실제로 쓰려면 이 줄 없애야 함
            print("Moving!!!! ", detect_moving)


def static_detect():
    global static_stop, is_in_mission, Mission, img
    if static_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 4 Static is ", static_stop)
        static = static_cascade.detectMultiScale(gray, 1.3, 20)
        for (x, y, w, h) in static:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        rec4 = np.matrix(static)

        if np.sum(rec4) >= 1:
            detect_static = 4
            static_stop += 1
            if static_stop == 3:
                Mission = 9
                is_in_mission = True
            print("Static!!!! ", detect_static)


def s_curve_detect():
    global s_curve_stop, is_in_mission, Mission, img
    if s_curve_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 5 Scurve is ", s_curve_stop)
        scurve = s_curve_cascade.detectMultiScale(gray, 1.03, 20)
        for (x, y, w, h) in scurve:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 120), 2)
        rec5 = np.matrix(scurve)

        if np.sum(rec5) >= 1:
            detect_scurve = 5
            s_curve_stop += 1
            if s_curve_stop == 3:
                Mission = 4
                is_in_mission = True
            print("Scurve!!!! ", detect_scurve)


def parking_detect():
    global parking_stop, is_in_mission, Mission, img
    if parking_stop == 3 or is_in_mission:
        pass
    else:
        print("Stop 7 Parking is ", parking_stop)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        parking = parking_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in parking:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        rec7 = np.matrix(parking)

        if np.sum(rec7) >= 1:
            detect_parking = 7
            parking_stop += 1
            if parking_stop == 3:
                Mission = 7
                is_in_mission = True
                give_delay_for_test()  # 테스트 할 때만 쓰는 것. 실제로 쓰려면 이 줄 없애야 함
            print("Parking!!!!! ", detect_parking)


def u_turn_detect():
    global u_turn_stop, is_in_mission, Mission, img
    if u_turn_stop == 3 or is_in_mission:
        pass
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Stop 6 Uturn is ", u_turn_stop)
        uturn = u_turn_cascade.detectMultiScale(gray, 1.06, 5)
        for (x, y, w, h) in uturn:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        rec6 = np.matrix(uturn)

        if np.sum(rec6) >= 1:
            detect_uturn = 6
            u_turn_stop += 1
            if u_turn_stop == 3:
                Mission = 5
                is_in_mission = True
                print("Uturn!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                give_delay_for_test()  # 테스트 할 때만 쓰는 것. 실제로 쓰려면 이 줄 없애야 함
            print("Uturn!!!! ", detect_uturn)


def main():
    U_thread = threading.Thread(target=u_turn_detect())  # 유턴 표지판 탐지
    Cros_thread = threading.Thread(target=crosswalk_detect())  # 횡단보도 표지판 탐지
    Mov_thread = threading.Thread(target=moving_detect())  # 동적장애물 표지판 탐지
    Park_thread = threading.Thread(target=parking_detect())  # 주차 표지판 탐지

    U_thread.start()
    Cros_thread.start()
    Mov_thread.start()
    Park_thread.start()


if __name__ == "__main__":
    # open cam
    cam = cv2.VideoCapture('./Previous Code/0507_one_lap_normal.mp4')

    cam.set(3, 480)
    cam.set(4, 270)

    if (not cam.isOpened()):
        print("cam open failed")
    while True:
        s, img = cam.read()
        main()
        cv2.imshow('cam', img)

        if cv2.waitKey(30) & 0xff == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    cv2.waitKey(0)
