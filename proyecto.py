import cv2
import time
import mediapipe as mp   
import numpy as np
from math import acos, degrees

# Inicializar los mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicializar la camara
cap = cv2.VideoCapture(0)

# Inicializar el contador
contador=0


# Inicializar el modelo de pose
with mp_pose.Pose(static_image_mode=False) as pose:

     while True:
          ret, frame = cap.read()
          if ret == False:
               break
          
          # Sacar el height y width del frame
          height, width, _ = frame.shape
          # Convertir la imagen de BGR a RGB
          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          results = pose.process(frame_rgb)

          # Dibujar los landmarks
          if results.pose_landmarks is not None:
               
               # Puntos de interes

               # Lado izquierdo
               x1 = int(results.pose_landmarks.landmark[0].x * width)
               y1 = int(results.pose_landmarks.landmark[0].y * height)

               x2 = int(results.pose_landmarks.landmark[11].x * width)
               y2 = int(results.pose_landmarks.landmark[11].y * height)

               x3 = int(results.pose_landmarks.landmark[23].x * width)
               y3 = int(results.pose_landmarks.landmark[23].y * height)

               # Lado derecho
               x4= int(results.pose_landmarks.landmark[12].x * width)
               y4 = int(results.pose_landmarks.landmark[12].y * height)

               x5 = int(results.pose_landmarks.landmark[24].x * width)
               y5 = int(results.pose_landmarks.landmark[24].y * height)

               # Transformacion de puntos de interes
               p1= np.array([x1,y1])
               p2= np.array([x2,y2])
               p3= np.array([x3,y3])
               p4= np.array([x4,y4])
               p5= np.array([x5,y5])

               # Calcular el angulo
               L1= np.linalg.norm(p2-p3)
               L2= np.linalg.norm(p1-p3)
               L3= np.linalg.norm(p1-p2)

               L4= np.linalg.norm(p4-p5)
               L5= np.linalg.norm(p1-p5)
               L6= np.linalg.norm(p1-p4)

               # Ley de cosenos
               angulo1= degrees(acos((L1**2+L2**2-L3**2)/(2*L1*L2)))
               angulo2= degrees(acos((L4**2+L5**2-L6**2)/(2*L4*L5)))

               #Visualizar los puntos de interes
               cv2.circle(frame, (x1,y1), 5, (0,255,0), 4)
               cv2.circle(frame, (x2,y2), 5, (0,255,0), 4)
               cv2.circle(frame, (x3,y3), 5, (0,255,0), 4)
               cv2.circle(frame, (x4,y4), 5, (0,255,0), 4)
               cv2.circle(frame, (x5,y5), 5, (0,255,0), 4)

               # Lineas entre puntos de interes
               cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 2)
               cv2.line(frame, (x2,y2), (x3,y3), (0,255,0), 2)
               cv2.line(frame, (x1,y1), (x3,y3), (0,255,0), 2)
               contours1= np.array([[[x1,y1],[x2,y2],[x3,y3]]])
               cv2.fillPoly(frame, pts =contours1, color=(0,255,0))

               cv2.line(frame, (x1,y1), (x4,y4), (0,255,0), 2)
               cv2.line(frame, (x4,y4), (x5,y5), (0,255,0), 2)
               cv2.line(frame, (x1,y1), (x5,y5), (0,255,0), 2)
               contours2= np.array([[[x1,y1],[x4,y4],[x5,y5]]])
               cv2.fillPoly(frame, pts =contours2, color=(0,255,0))

               # Mostrar el angulos
               cv2.putText(frame, str(int(angulo1)), (x2+30,y2), 1, 1, (255,255,255), 2)
               cv2.putText(frame, str(int(angulo2)), (x4+30,y4), 1, 1, (0,0,0), 2)
               
               #Posiciones correctas
               if angulo1<angulo2 and angulo1<12 and angulo2>13:
                    contador=0
                    cv2.putText(frame, "Posicion Correcta Boca arriba", (10,50), 1, 2, (0,255,0), 2)
               elif angulo1>angulo2 and (angulo1-angulo2)>4  and angulo2<10 and angulo2>3 and angulo1<15:
                    contador=0
                    cv2.putText(frame, "Posicion Correcta Frente camara", (10,50), 1, 2, (0,255,0), 2)
               elif angulo1>angulo2 and (angulo1-angulo2)<6:
                    contador=0
                    cv2.putText(frame, "Posicion Correcta Espaldas camara", (10,50), 1, 2, (0,255,0), 2)
               else:
                    cv2.putText(frame, "Posicion Incorrecta", (10,50), 1, 2, (0,0,255), 2)
                    contador=contador+1
                    cv2.putText(frame, str(contador), (20,400), 1, 2, (0,255,0), 2)
                    if contador>400:
                         cv2.putText(frame, "Pitido", (400,50), 1, 2, (0,255,0), 2)
                         if contador>600:
                              contador=0
                    
          # Mostrar el frame
          cv2.imshow('Frame', frame)

          #Cerrar la ventana con la tecla q
          if cv2.waitKey(1) & 0xFF == ord('q'):
               break
cap.release()
cv2.destroyAllWindows()