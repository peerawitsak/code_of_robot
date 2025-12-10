from Set_up_And_Function import *

#-------------------------- main ----------------------------------
if GPIO.input(button)==1:
    time.sleep(60) #รอ 1 นาทีก่อนทำงาน
    Forward_Until_Black(1)
    rb.motor_stop()
#-------------------------- Loop ----------------------------------
    while True():
        
        pass

