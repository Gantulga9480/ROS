
(cl:in-package :asdf)

(defsystem "robot1-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "board" :depends-on ("_package_board"))
    (:file "_package_board" :depends-on ("_package"))
    (:file "board" :depends-on ("_package_board"))
    (:file "_package_board" :depends-on ("_package"))
  ))