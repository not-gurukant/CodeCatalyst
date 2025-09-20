import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

# --- Matplotlib 3D setup ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
connections = mp_pose.POSE_CONNECTIONS

# --- Realtime hologram overlay colors ---
holo_color = (255, 0, 255)  # Neon magenta lines
dot_color = (0, 255, 255)   # Cyan dots

def update(frame):
    ret, img = cap.read()
    if not ret:
        return

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    # ========== (1) REALTIME HOLOGRAM ON CAMERA ==========
    if results.pose_landmarks:
        h, w, _ = img.shape
        landmarks = results.pose_landmarks.landmark

        # Draw keypoints & skeleton on camera feed
        for id, lm in enumerate(landmarks):
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 4, dot_color, -1)

        for conn in connections:
            start = landmarks[conn[0]]
            end = landmarks[conn[1]]
            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)
            cv2.line(img, (x1, y1), (x2, y2), holo_color, 2)

    cv2.imshow("HOLOGRAM VIEW", img)

    # ========== (2) 3D SKELETON MODEL ==========
    ax.cla()
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(0, 2)

    if results.pose_landmarks:
        points = [(lm.x - 0.5, -lm.z, -lm.y + 1) for lm in results.pose_landmarks.landmark]
        xs, ys, zs = zip(*points)
        ax.scatter(xs, ys, zs, c='cyan', s=30)

        for conn in connections:
            x1, y1, z1 = points[conn[0]]
            x2, y2, z2 = points[conn[1]]
            ax.plot([x1, x2], [y1, y2], [z1, z2], c='magenta')

    ax.set_xlabel("X")
    ax.set_ylabel("Depth")
    ax.set_zlabel("Height")
    ax.view_init(elev=15, azim=-70)

    # Exit when "q" is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        plt.close()

ani = FuncAnimation(fig, update, interval=30, cache_frame_data=False)
plt.show()
