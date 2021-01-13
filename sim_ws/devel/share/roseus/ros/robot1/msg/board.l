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
    ((:table __table) (make-array 0 :initial-element 0 :element-type :integer))
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
    ;; uint32[] _table
    (* 4    (length _table)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32[] _table
     (write-long (length _table) s)
     (dotimes (i (length _table))
       (write-long (elt _table i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32[] _table
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _table (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _table i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get robot1::board :md5sum-) "f4fc566b67f0715ec037ec3bb197f924")
(setf (get robot1::board :datatype-) "robot1/board")
(setf (get robot1::board :definition-)
      "uint32[] table
")



(provide :robot1/board "f4fc566b67f0715ec037ec3bb197f924")


