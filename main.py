import cv2
import mediapipe as mp
import pygame
import sys
import random
import threading
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

index_x, index_y = 0, 0
initial_hand_detected = False
stop_capture = False  #

def capture_hand():
    global index_x, index_y, initial_hand_detected, stop_capture
    cap = cv2.VideoCapture(0)
    
    while not stop_capture:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)  
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            initial_hand_detected = True
            
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = img.shape
                index_x = int(hand_landmarks.landmark[8].x * w)  
                index_y = int(hand_landmarks.landmark[8].y * h)
                min_x = min([lm.x for lm in hand_landmarks.landmark]) * w
                min_y = min([lm.y for lm in hand_landmarks.landmark]) * h
                max_x = max([lm.x for lm in hand_landmarks.landmark]) * w
                max_y = max([lm.y for lm in hand_landmarks.landmark]) * h
                cv2.rectangle(img, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 255, 0), 2)

                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)

        cv2.imshow("Hand Tracker", img)
        if cv2.waitKey(1) == ord('q') or stop_capture:
            break

    cap.release()
    cv2.destroyAllWindows()

def snake_game():
    global index_x, index_y, initial_hand_detected, stop_capture

    pygame.init()
    width, height = 640, 480
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hand-Controlled Snake")

    clock = pygame.time.Clock()
    snake_block = 20
    snake_speed = 4

    font_style = pygame.font.SysFont(None, 40)

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        win.blit(mesg, [width / 6, height / 3])

    def gameLoop():
        game_over = False
        x1 = width / 2
        y1 = height / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
        foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

        print("Waiting for hand...")
        
        while not initial_hand_detected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop_capture = True
                    sys.exit()
            time.sleep(0.1)

        print("Hand detected! Starting game...")

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop_capture = True
                    sys.exit()

            center_x, center_y = width // 2, height // 2
            dx = index_x - center_x
            dy = index_y - center_y

            threshold = 40  
            
            if abs(dx) > abs(dy):
                if dx > threshold:
                    x1_change = snake_block
                    y1_change = 0
                elif dx < -threshold:
                    x1_change = -snake_block
                    y1_change = 0
            else:
                if dy > threshold:
                    y1_change = snake_block
                    x1_change = 0
                elif dy < -threshold:
                    y1_change = -snake_block
                    x1_change = 0

            x1 += x1_change
            y1 += y1_change

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_over = True

            win.fill((0, 0, 0))
            pygame.draw.rect(win, (255, 0, 0), [foodx, foody, snake_block, snake_block])
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True

            for x in snake_list:
                pygame.draw.rect(win, (0, 255, 0), [x[0], x[1], snake_block, snake_block])

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
                length_of_snake += 1

            clock.tick(snake_speed)

        win.fill((0, 0, 0))
        message("Game Over!", (255, 255, 255))
        pygame.display.update()
        pygame.time.wait(2000)

    gameLoop()
    stop_capture = True
    pygame.quit()
    sys.exit()

t1 = threading.Thread(target=capture_hand)
t1.start()

snake_game()
