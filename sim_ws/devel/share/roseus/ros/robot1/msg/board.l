;; Auto-generated. Do not edit!


(when (boundp 'robot1::board)
  (if (not (find-package "ROBOT1"))
    (make-package "ROBOT1"))
  (shadow 'board (find-package "ROBOT1")))
(unless (find-package "ROBOT1::BOARD")
  (make-package "ROBOT1::BOARD"))

(in-package "ROS")
;;//! \htmlinclude board.msg.html


(defclass robot1::board
  :super ros::object
  :slots (_robot_x _robot_y ))

(defmethod robot1::board
  (:init
   (&key
    ((:robot_x __robot_x) 0)
    ((:robot_y __robot_y) 0)
    )
   (send-super :init)
   (setq _robot_x (round __robot_x))
   (setq _robot_y (round __robot_y))
   self)
  (:robot_x
   (&optional __robot_x)
   (if __robot_x (setq _robot_x __robot_x)) _robot_x)
  (:robot_y
   (&optional __robot_y)
   (if __robot_y (setq _robot_y __robot_y)) _robot_y)
  (:serialization-length
   ()
   (+
    ;; uint32 _robot_x
    4
    ;; uint32 _robot_y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _robot_x
       (write-long _robot_x s)
     ;; uint32 _robot_y
       (write-long _robot_y s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _robot_x
     (setq _robot_x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _robot_y
     (setq _robot_y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get robot1::board :md5sum-) "3c388db48c5cd0fed06741e9101f00f3")
(setf (get robot1::board :datatype-) "robot1/board")
(setf (get robot1::board :definition-)
      "uint32 robot_x
uint32 robot_y
")



(provide :robot1/board "3c388db48c5cd0fed06741e9101f00f3")


