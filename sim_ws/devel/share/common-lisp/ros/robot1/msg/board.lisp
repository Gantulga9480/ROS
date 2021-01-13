; Auto-generated. Do not edit!


(cl:in-package robot1-msg)


;//! \htmlinclude board.msg.html

(cl:defclass <board> (roslisp-msg-protocol:ros-message)
  ((table
    :reader table
    :initarg :table
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass board (<board>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <board>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'board)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot1-msg:<board> is deprecated: use robot1-msg:board instead.")))

(cl:ensure-generic-function 'table-val :lambda-list '(m))
(cl:defmethod table-val ((m <board>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot1-msg:table-val is deprecated.  Use robot1-msg:table instead.")
  (table m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <board>) ostream)
  "Serializes a message object of type '<board>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'table))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) ele) ostream))
   (cl:slot-value msg 'table))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <board>) istream)
  "Deserializes a message object of type '<board>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'table) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'table)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<board>)))
  "Returns string type for a message object of type '<board>"
  "robot1/board")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'board)))
  "Returns string type for a message object of type 'board"
  "robot1/board")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<board>)))
  "Returns md5sum for a message object of type '<board>"
  "f4fc566b67f0715ec037ec3bb197f924")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'board)))
  "Returns md5sum for a message object of type 'board"
  "f4fc566b67f0715ec037ec3bb197f924")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<board>)))
  "Returns full string definition for message of type '<board>"
  (cl:format cl:nil "uint32[] table~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'board)))
  "Returns full string definition for message of type 'board"
  (cl:format cl:nil "uint32[] table~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <board>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'table) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <board>))
  "Converts a ROS message object to a list"
  (cl:list 'board
    (cl:cons ':table (table msg))
))
