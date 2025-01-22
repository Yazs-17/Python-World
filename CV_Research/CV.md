- 一个比较不错的样例：
  ```py
  import cv2
  
  # 加载预训练的人脸级联分类器
  face_cascade = cv2.CascadeClassifier('C:\\Users\\Yazs\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
  # 打开摄像头
  cap = cv2.VideoCapture(0)
  
  while True:
      # 读取一帧
      ret, frame = cap.read()
  
      # 将帧转换为灰度图
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
      # 使用级联分类器检测人脸
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
  
      # 为每个检测到的人脸绘制一个矩形
      for (x, y, w, h) in faces:
          cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
  
      # 显示结果
      cv2.imshow('Faces found', frame)
  
      # 按'q'退出循环
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  
  # 释放摄像头
  cap.release()
  
  # 关闭所有窗口
  cv2.destroyAllWindows()
  
  ```

  