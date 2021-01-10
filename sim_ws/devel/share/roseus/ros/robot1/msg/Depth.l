;; Auto-generated. Do not edit!


(when (boundp 'robot1::Depth)
  (if (not (find-package "ROBOT1"))
    (make-package "ROBOT1"))
  (shadow 'Depth (find-package "ROBOT1")))
(unless (find-package "ROBOT1::DEPTH")
  (make-package "ROBOT1::DEPTH"))

(in-package "ROS")
;;//! \htmlinclude Depth.msg.html


(defclass robot1::Depth
  :super ros::object
  :slots (_encoding _is_bigendian _data ))

(defmethod robot1::Depth
  (:init
   (&key
    ((:encoding __encoding) "")
    ((:is_bigendian __is_bigendian) 0)
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _encoding (string __encoding))
   (setq _is_bigendian (round __is_bigendian))
   (setq _data __data)
   self)
  (:encoding
   (&optional __encoding)
   (if __encoding (setq _encoding __encoding)) _encoding)
  (:is_bigendian
   (&optional __is_bigendian)
   (if __is_bigendian (setq _is_bigendian __is_bigendian)) _is_bigendian)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; string _encoding
    4 (length _encoding)
    ;; uint8 _is_bigendian
    1
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _encoding
       (write-long (length _encoding) s) (princ _encoding s)
     ;; uint8 _is_bigendian
       (write-byte _is_bigendian s)
     ;; uint8[] _data
     (write-long (length _data) s)
     (princ _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _encoding
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _encoding (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _is_bigendian
     (setq _is_bigendian (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8[] _data
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _data (make-array n :element-type :char))
     (replace _data buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get robot1::Depth :md5sum-) "d92edb9cf281cc6148c6af12ac4ac794")
(setf (get robot1::Depth :datatype-) "robot1/Depth")
(setf (get robot1::Depth :definition-)
      "string encoding
uint8 is_bigendian
uint8[] data
")



(provide :robot1/Depth "d92edb9cf281cc6148c6af12ac4ac794")


