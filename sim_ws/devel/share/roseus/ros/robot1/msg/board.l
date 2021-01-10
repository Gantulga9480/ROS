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
  :slots (_table ))

(defmethod robot1::board
  (:init
   (&key
    ((:table __table) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _table __table)
   self)
  (:table
   (&optional __table)
   (if __table (setq _table __table)) _table)
  (:serialization-length
   ()
   (+
    ;; uint8[] _table
    (* 1    (length _table)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _table
     (write-long (length _table) s)
     (princ _table s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _table
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _table (make-array n :element-type :char))
     (replace _table buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get robot1::board :md5sum-) "8c2595a4679a3b6f30bb5de6a6f5ee2e")
(setf (get robot1::board :datatype-) "robot1/board")
(setf (get robot1::board :definition-)
      "uint8[] table
")



(provide :robot1/board "8c2595a4679a3b6f30bb5de6a6f5ee2e")


