from Set_up_And_Function import *

#-------------------------- main ----------------------------------
ser = serial.Serial('/dev/ttyACM0',115200,timeout=2)# /dev/ttyACM0 = portที่เชื่มต่อ ,115200 =  bitrate ,timeout = เวลาที่จะหยุดทำงานถ้าไม่มีข้อมูลที่ส่งมา
time.sleep(3)
ser.reset_input_buffer()
print("serial is OK")


if GPIO.input(button)==1:
    time.sleep(60) #รอ 1 นาทีก่อนทำงาน
    rb.Forward_Until_Black(1)
    rb.motor_stop()
#-------------------------- Loop ----------------------------------
    try :
        while True:
            #rb.Start_TO_Box()
            try:
                while True:
                    time.sleep(0.01)
                    if ser.in_waiting>0:
                        data = ser.readline().decode('utf-8')
                        print(data)
                        print(type(data))
            except KeyboardInterrupt :
                print("stop ")
                rb.motor_stop()
                ser.close()
                
    except KeyboardInterrupt :
        print("stop ")
        rb.motor_stop()
        ser.close()

