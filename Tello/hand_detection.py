import handy
import cv2


def handDetection(img, hist):
    
    # detect the hand
    hand = handy.detect_hand(img, hist)
    
    # plot the fingertips
    for fingertip in hand.fingertips:
        cv2.circle(hand.outline, fingertip, 5, (0, 0, 255), -1)

    return hand
    
