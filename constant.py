import RPi.GPIO as GPIO
import pigpio as pig
import time 

patterns = {
    (0,1,1,1,1,1,1,1):1,
    (0,0,1,1,1,1,1,1):2,
    (1,0,1,1,1,1,1,1):3,
    (1,0,0,1,1,1,1,1):4,
    (1,1,0,1,1,1,1,1):5,
    (1,1,0,0,1,1,1,1):6,
    (1,1,1,0,1,1,1,1):7,
    (1,1,1,0,0,1,1,1):8,
    (1,1,1,1,0,1,1,1):9,
    (1,1,1,1,0,0,1,1):10,
    (1,1,1,1,1,0,1,1):11,
    (1,1,1,1,1,0,0,1):12,
    (1,1,1,1,1,1,0,1):13,
    (1,1,1,1,1,1,0,0):14,
    (1,1,1,1,1,1,1,0):15,
}

patterns_black_line = {
    (0,0,0,0,0,0,0,0):1,
    (1,1,1,0,0,0,0,0):2,
    (0,0,0,0,0,1,1,1):3,
    (1,1,1,0,0,1,1,1):4
}

patterns_Back={
    (0,0):1,
    (1,0):2,
    (0,1):3,
    (1,1):4
}

# senser avg
# avgBlack = 200
# avgGreen = 600
# avgWhite = 900
# avgBlue = 300

#delay
TimeOfRun =0.050#เวลาให้ motor ทำงานสำหรับวิ่งปกติ milisec หมายเหตุยังไม่ใช้ในวันที่ 11/27/2025
TimeOfTurn = 0.050#เวลา ให้ motorทำงานสำหรับการเลี้ยว  milisec
Time_delay = 0.020#delay ให้ เกินเส้นดำ milisec

# speed motor
Speed = 30 # dutycycle 50% 

TurnSpeed = 50
BackSpeed = 20

# PID constants 
Kp = 5
Ki = 0
Kd = 0

# PID variable
Target = 8

# Integral_error = 0 #x หมายถึง error
# previous_error = 0 #x หมายถึง error

# previous_T = 0 # เก็บเวลา us


pid_value = 0
P = 0
I = 0
D = 0

#error = Realposition - target 
error = 0

#-------------------------------------set pinout------------------------------
#set sensor pin 
# กำหนดหมายเลขขา GPIO
sen1 =  17
sen2 = 27
sen3 = 22
sen4 = 23
sen5 = 24
sen6 = 25
sen7 = 5
sen8 = 6
sen9 = 111
sen10 = 111
#ปุ่ม
button = 4

#I2C for LCD
sda = 2 #pin 3  ยังไม่กำหนด IO
scl = 3 #pin 5 ยังไม่กำหนด IO

#set motor

pwm_b = 21 #40
front_right = 12 #32
back_right = 16 #36

pwm_a = 20 #38
front_left = 19 #35
back_left  = 26 #37