constant.py = เก็บตัวแปรพื้นฐาน กำหนดpin import libary

ClassMain.py = เก็บคลาสหลัก มีฟังชั้นย่อย 
    class Robot(kp,ki,kd,Speed,target) = หมายเหตุ rb คือ object สร้างใน set_up_and_function.py
        update() จะไม่มีการ return แต่จะมีการ update ค่า
                rb.position = sensorหน้า 15 แบบ 
                rb.black_line = เส้นดำ 4 แบบ 1:เส้นดำทั้งเส้น 2:เส้นดำขวา 3:เส้นดำซ้าย 4:เจอเส้นดำตรงกลางเฉยๆ and 0 ถ้าไม่เจอ
                rb.Backposition = sensorหลัง 4 แบบ 1:เส้นดำทั้งเส้น 2:เส้นดำขวา 3:เส้นดำซ้าย 4:ไม่เจอ
                rb._error =  rb.position - rb.target เก็บค่า error 
            และเรียกใช้
                rb.PID_cal()

        rb.PID_cal() จะนำค่า rb._error มาคำนวณ มีการ update ค่า
                                        rb.previous_T = ค่าเวลาล่าสุดที่เรียกใช้
                rb.pid_value = ค่าpid
                                        rb.Integral_error = ผลรวมerrorตามเวลา
                                        rb.previous_error = ค่าerrorล่าสุด
            และเรียกใช้
                rb.Motor_Control()

        rb.Motor_Control() จะนำค่า rb.pid_value มาคำนวณ มีการ update ค่า
                rb.leftspeed = int 
                rb.rightspeed = int 
        
        rb.Track_forward(+-speed) เดินไปข้างหน้าด้วยการ tag แบบ pid แต่ ถ้าไม่ใส่  +-speed จะ +-speed = 0
            เรียก rb.update ก่อนและนำค่า (rb.leftspeed ,rb.rightspeed) มาขับ motor 
        
        rb.Track_backward(+-speed) ถอยหลัง tag แบบ pid แต่ ถ้าไม่ใส่  +-speed จะ +-speed = 0
            เรียก rb.update ก่อนและนำค่า (rb.leftspeed ,rb.rightspeed) มาขับ motor 
                แต่ จะทำการใส่ rb.leftspeed ,rb.rightspeed สลับกัน 
        
        rb.motor_stop() สั่ง motor หยุดทำงาน

        rb.Turn_Right(speed)  แต่ ถ้าไม่ใส่ speed = 30 สั่งเลี้ยวขวา
            จนกว่า sensorหลังซ้าย จะเจอเส้นดำ 1 ครั้ง และ จน ไม่เจอเส้นดำ
            และสั่ง motor_stop

        rb.Turn_Left(speed)  แต่ ถ้าไม่ใส่ speed = 30 สั่งเลี้ยวขวา
            จนกว่า sensorหลังขวา จะเจอเส้นดำ 1 ครั้ง และ จน ไม่เจอเส้นดำ
            และสั่ง motor_stop

        rb.UTurn(speed) แต่ ถ้าไม่ใส่ speed = 30 สั่งเลี้ยวขวา
            จนกว่า sensorหลังซ้าย จะเจอเส้นดำ และ จนไม่เจอเส้นดำ 2 ครั้ง 
            และสั่ง motor_stop