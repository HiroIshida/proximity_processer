(ros::load-ros-manifest "roseus")
(ros::load-ros-manifest "proximity_processer")

(defun proximity-processer-init ()
  (ros::wait-for-service "proximity_processer/init")
  (let ((req (instance std_srvs::EmptyRequest :init)))
    (ros::service-call "proximity_processer/init" req)))

(defun proximity-processer-append ()
  (ros::wait-for-service "proximity_processer/append")
  (let ((req (instance std_srvs::EmptyRequest :init)))
    (ros::service-call "proximity_processer/append" req)))

(defun proximity-processer-judge ()
  (ros::wait-for-service "proximity_processer/judge")
  (let* ((req (instance proximity_processer::IsCollisionRequest :init))
         (res (ros::service-call "proximity_processer/judge" req))
         (msg (send res :isCollision))
         (bool (send msg :data)))
    bool))

;; alias
(defun pp-init () (proximity-processer-init))
(defun pp-append () (proximity-processer-append))
(defun pp-judge () (proximity-processer-judge))

