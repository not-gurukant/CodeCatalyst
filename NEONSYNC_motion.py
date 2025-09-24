import cv2
import mediapipe as mp
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# OpenGL + Pygame window size
WIDTH, HEIGHT = 800, 600

# MediaPipe Pose Connections
POSE_CONNECTIONS = mp_pose.POSE_CONNECTIONS

# Initialize Pygame and OpenGL
def init_pygame_opengl():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Pose Skeleton - Fixed Orientation")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

# Convert MediaPipe normalized landmarks to 3D coords for OpenGL
def mp_landmarks_to_3d_coords(landmarks):
    coords = []
    for lm in landmarks:
        x = - (lm.x - 0.5) * 2
        y = - (lm.y - 0.5) * 2
        z = lm.z * 3.0
        coords.append((x * 1.5, y * 1.5, z))
    return coords

# Draw skeleton lines
def draw_skeleton_3d(coords, connections):
    glLineWidth(4)
    glColor3f(0.0, 1.0, 1.0)  # cyan
    glBegin(GL_LINES)
    for (a, b) in connections:
        if a < len(coords) and b < len(coords):
            glVertex3fv(coords[a])
            glVertex3fv(coords[b])
    glEnd()

# Draw joints as spheres on the person in real time
def draw_joints_3d(coords):
    glColor3f(1.0, 0.5, 0.0)  # orange
    for x, y, z in coords:
        glPushMatrix()
        glTranslatef(x, y, z)
        quad = gluNewQuadric()
        gluSphere(quad, 0.05, 12, 8)
        gluDeleteQuadric(quad)
        glPopMatrix()

# Draw 2D overlay
def draw_hologram_2d(image, landmarks, connections):
    h, w, _ = image.shape
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(image, (cx, cy), 6, (0, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(image, (cx, cy), 10, (255, 255, 255), 2, cv2.LINE_AA)

    for (a, b) in connections:
        if a < len(landmarks) and b < len(landmarks):
            start = landmarks[a]
            end = landmarks[b]
            start_pos = (int(start.x * w), int(start.y * h))
            end_pos = (int(end.x * w), int(end.y * h))
            cv2.line(image, start_pos, end_pos, (0, 255, 255), 3, cv2.LINE_AA)

def main():
    init_pygame_opengl()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit()

    clock = pygame.time.Clock()

    while True:
        ret, frame = cap.read()         
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 2D overlay
            draw_hologram_2d(frame, landmarks, POSE_CONNECTIONS)

            # 3D conversion
            coords_3d = mp_landmarks_to_3d_coords(landmarks)

            # Render OpenGL
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -5.0)
            glRotatef(180, 0, 1, 0)

            draw_skeleton_3d(coords_3d, POSE_CONNECTIONS)
            draw_joints_3d(coords_3d)

            pygame.display.flip()
            clock.tick(60)
        else:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -5.0)
            glRotatef(180, 0, 1, 0)
            pygame.display.flip()
            clock.tick(60)

        cv2.imshow("Live Pose Tracking with 2D Hologram", frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                return

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
