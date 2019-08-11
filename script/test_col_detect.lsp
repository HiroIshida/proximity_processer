(load "package://pr2eus/pr2-interface.l")
(ros::load-ros-manifest "proximity_processer")
(ros::load-ros-manifest "force_proximity_ros")

(defun warning-message (hoge hogen &rest hoenn) nil) ;; overriden

(setq init-angle-vector #f(179.821 51.0643 25.1347 83.4318 -82.9128 52.5284 -59.2714 -20.2535 -74.8208 -19.4982 -38.4855 -110.41 19.994 -10.9107 -9.78539 5.2327 74.2702))

(ros::roseus "col_detect_tester" :anonymous t)
(pr2-init)
(setq *robot* *pr2*)
(send *robot* :angle-vector init-angle-vector)
(send *ri* :angle-vector (send *robot* :angle-vector))
(send *ri* :wait-interpolation)

(ros::set-logger-level "ros.roseus" ros::*rosfatal*)

(defun stick-loop nil
  (let ((counter 0))
    (loop
      (print "a")
      (send *robot* :larm :move-end-pos #f(0 -10 0) :world)
      (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
      (when (> counter 20)
          (send *ri* :cancel-angle-vector)
          (return))
      (incf counter))))

(setq *diff_val* 0)
(setq *prox* 0)

(ros::subscribe "test" proximity_processer::FloatHeader
                #'(lambda (msg) 
                    (setq *diff_val* (send msg :data :data))))

(ros::subscribe "/proximity_sensor" force_proximity_ros::ProximityStamped
                #'(lambda (msg)
                    (setq *prox* (send msg :proximity :average))))

(send *robot* :larm :move-end-pos 
      #f(0 -300 0)
      :world)

(send *ri* :angle-vector (send *robot* :angle-vector) 30000)

(let ((time-begin (send (ros::time-now) :sec))
      (time-maximam 20);sec
      (value-pre 0))
  (loop 
    (setq time-now (send (ros::time-now) :sec))
    (when (> (- time-now time-begin) time-maximam)
      (return))
    (ros::spin-once)
    (print "-------------------------")
    (print *diff_val*)
    (unix:usleep 5000)
    (when (and (< (- *diff_val* value-pre) -40000) (> *diff_val* 100000))
      (speak-jp "あ")
      (print "result")
      (print value-pre)
      (print *diff_val*)
      (send *ri* :cancel-angle-vector)
      (send *ri* :wait-interpolation)
      (return))
    (setq value-pre *diff_val*))
  )








