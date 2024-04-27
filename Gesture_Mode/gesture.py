import csv
import copy
import itertools

import cv2 as cv
import numpy as np
import mediapipe as mp

from Gesture_Mode.model import KeyPointClassifier
import Helper_Files.spotify_integration as spotify

def start_gesture_mode():
    # Camera preparation ###############################################################
    cap_device = 0
    cap_width = 1260
    cap_height = 780
    
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Model load #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    keypoint_classifier = KeyPointClassifier()
    current_command = ""
    consecutive_command_count = 0

    # Read labels ###########################################################
    with open('Gesture_Mode/model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    #  ########################################################################
    mode = 0

    while True:
        # Process Key (ESC: end) #################################################
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break
        number, mode = select_mode(key, mode)

        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Bounding box calculation
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                # Write to the dataset file
                logging_csv(number, mode, pre_processed_landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                # Spotify Integration 
                current_command, consecutive_command_count = spotify_action(current_command, consecutive_command_count, keypoint_classifier_labels[hand_sign_id])

                # Drawing part
                debug_image = draw_bounding_rect(debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(debug_image, brect, handedness, keypoint_classifier_labels[hand_sign_id])

        debug_image = draw_info(debug_image, mode, number)

        # Screen reflection #############################################################
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    return number, mode


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list



def logging_csv(number, mode, landmark_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'Gesture_Mode/model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    return

def spotify_action(current_command, consecutive_command_count, label):
    # print(current_command)
    if current_command != label:
        consecutive_command_count = 0
        current_command = label
    else:
        consecutive_command_count+=1

    if consecutive_command_count >= 60:
        consecutive_command_count = 0
        spotify.command_to_action(current_command)

    return current_command, consecutive_command_count


def draw_landmarks(image, landmark_point):
    lineColor = (227, 148, 0)
    lineBorderColor = (115,15,3)
    lineInnerBorderSize = 2
    lineOuterBorderSize = 6
    jointColor = (227, 148, 0)
    jointSize = 5
    jointTipSize = 8

    if len(landmark_point) > 0:
        # Thumb
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), lineColor, lineInnerBorderSize)

        # Index finger
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), lineColor, lineInnerBorderSize)

        # Middle finger
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), lineColor, lineInnerBorderSize)

        # Ring finger
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), lineColor, lineInnerBorderSize)

        # Little finger
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), lineColor, lineInnerBorderSize)

        # Palm
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), lineColor, lineInnerBorderSize)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), lineBorderColor, lineOuterBorderSize)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), lineColor, lineInnerBorderSize)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:  # Wrist 1
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 1:  # Wrist 2
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 2:  # Thumb: Base
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 3:  # Thumb: 1st Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 4:  # Thumb: Tip
            cv.circle(image, (landmark[0], landmark[1]), jointTipSize, (247, 158, 74), -1)
        if index == 5:  # Index Finger: Base
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 6:  # Index Finger: 2nd Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 7:  # Index Finger: 1st Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 8:  # Index Finger: Tip
            cv.circle(image, (landmark[0], landmark[1]), jointTipSize, (247, 158, 74), -1)
        if index == 9:  # Middle Finger: Base
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 10:  # Middle Finger: 2nd Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 11:  # Middle Finger: 1st Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 12:  # Middle Finger: Tip
            cv.circle(image, (landmark[0], landmark[1]), jointTipSize, (247, 158, 74), -1)
        if index == 13:  # Ring Finger: Base
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 14:  # Ring Finger: 2nd Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 15:  # Ring Finger: 1st Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 16:  # Ring Finger: Tip
            cv.circle(image, (landmark[0], landmark[1]), jointTipSize, (247, 158, 74), -1)
        if index == 17:  # Little Finger: Base
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 18:  # Little Finger: 2nd Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)   
        if index == 19:  # Little Finger: 1st Joint
            cv.circle(image, (landmark[0], landmark[1]), jointSize, jointColor, -1)
        if index == 20:  # Little Finger: Tip
            cv.circle(image, (landmark[0], landmark[1]), jointTipSize, (247, 158, 74), -1)
    return image


def draw_bounding_rect(image, brect):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (115,15,3), 1)
    return image


def draw_info_text(image, brect, handedness, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1)
    info_text = handedness.classification[0].label[0:]

    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text

    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image


def draw_info(image, mode, number):
    if mode == 1:
        cv.putText(image, "MODE: Logging Key Point", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, "NUM:" + str(number), (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image