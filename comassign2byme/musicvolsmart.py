import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# กำหนด Universe of Discourse
input_current_volume = ctrl.Antecedent(np.arange(0, 101, 1), 'current_volume')
input_desired_volume = ctrl.Antecedent(np.arange(0, 101, 1), 'desired_volume')
output_controlled_volume = ctrl.Consequent(np.arange(0, 101, 1), 'controlled_volume')

# กำหนด Membership Functions (ในที่นี้ควรปรับแต่งตามความต้องการ)
input_current_volume['low'] = fuzz.trimf(input_current_volume.universe, [0, 0, 40])
input_current_volume['medium'] = fuzz.trimf(input_current_volume.universe, [20, 50, 80])
input_current_volume['high'] = fuzz.trimf(input_current_volume.universe, [60, 100, 100])

input_desired_volume['low'] = fuzz.trimf(input_desired_volume.universe, [0, 0, 40])
input_desired_volume['medium'] = fuzz.trimf(input_desired_volume.universe, [20, 50, 80])
input_desired_volume['high'] = fuzz.trimf(input_desired_volume.universe, [60, 100, 100])

output_controlled_volume['low'] = fuzz.trimf(output_controlled_volume.universe, [0, 0, 40])
output_controlled_volume['medium'] = fuzz.trimf(output_controlled_volume.universe, [20, 50, 80])
output_controlled_volume['high'] = fuzz.trimf(output_controlled_volume.universe, [60, 100, 100])

# กำหนดกฎ (ในที่นี้ควรปรับแต่งตามความต้องการ)
rule1 = ctrl.Rule(input_current_volume['low'] & input_desired_volume['low'], output_controlled_volume['low'])
rule2 = ctrl.Rule(input_current_volume['low'] & input_desired_volume['medium'], output_controlled_volume['medium'])
rule3 = ctrl.Rule(input_current_volume['low'] & input_desired_volume['high'], output_controlled_volume['high'])
rule4 = ctrl.Rule(input_current_volume['medium'] & input_desired_volume['low'], output_controlled_volume['low'])
rule5 = ctrl.Rule(input_current_volume['medium'] & input_desired_volume['medium'], output_controlled_volume['medium'])
rule6 = ctrl.Rule(input_current_volume['medium'] & input_desired_volume['high'], output_controlled_volume['high'])
rule7 = ctrl.Rule(input_current_volume['high'] & input_desired_volume['low'], output_controlled_volume['low'])
rule8 = ctrl.Rule(input_current_volume['high'] & input_desired_volume['medium'], output_controlled_volume['medium'])
rule9 = ctrl.Rule(input_current_volume['high'] & input_desired_volume['high'], output_controlled_volume['high'])

# สร้างระบบควบคุม
volume_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])  
volume_simulator = ctrl.ControlSystemSimulation(volume_ctrl)

# 1. ต้อนรับผู้ใช้
print("\033[92mWelcome to Smart Home!\033[0m")  # สีเขียว

# เลือกเปิดหรือปิดเพลง
while True:
    choice = input("\033[93mPress 'o' to open the music, 'c' to close: \033[0m")  # สีเหลือง
    if choice == 'o':
        break
    elif choice == 'c':
        print("\033[91mGoodbye!\033[0m")  # สีแดง
        exit()
    else:
        print("\033[91mInvalid choice. Please try again.\033[0m")  # สีแดง

# สุ่มระดับเสียงและแสดงค่า
random_volume = np.random.randint(0, 101)
volume_level = None
if random_volume >= 1 and random_volume <= 33:
    volume_level = "\033[92mLow\033[0m"  # สีเขียว
elif random_volume >= 34 and random_volume <= 66:
    volume_level = "\033[93mMedium\033[0m"  # สีเหลือง
elif random_volume >= 67 and random_volume <= 100:
    volume_level = "\033[91mHigh\033[0m"  # สีแดง
print(f"The SMART home is currently playing music at volume level {random_volume}. ({volume_level})")

# รับอารมณ์ (emotional) จากผู้ใช้
emotional = input("Enter your emotional state (chill, angry, happy, sad, e.g.): ")

# แปลงอารมณ์เป็นระดับเสียง
if emotional == 'e.g.':
    random_volume = np.random.randint(0, 101)  # สุ่มค่าระหว่าง 0 ถึง 100
elif emotional == 'chill':
    random_volume = np.random.randint(34, 67)  # Medium
elif emotional == 'angry':
    random_volume = np.random.randint(0, 34)   # Low
elif emotional == 'happy':
    random_volume = np.random.randint(67, 101)  # High
elif emotional == 'sad':
    random_volume = np.random.randint(0, 34)   # Low

# แสดงระดับเสียงที่สุ่มได้
volume_level = None
if random_volume >= 1 and random_volume <= 33:
    volume_level = "\033[92mLow\033[0m"
elif random_volume >= 34 and random_volume <= 66:
    volume_level = "\033[93mMedium\033[0m"
elif random_volume >= 67 and random_volume <= 100:
    volume_level = "\033[91mHigh\033[0m"

print(f"The house is currently playing music at volume level {random_volume}. ({volume_level})")

# ปรับระดับเสียงแบบ Manual(Not Emotional and Automatics)
desired_volume = int(input("Enter the desired volume (0-100): "))

# คำนวณผลลัพธ์
volume_simulator.input['current_volume'] = random_volume
volume_simulator.input['desired_volume'] = desired_volume
volume_simulator.compute()

controlled_volume_label = np.argmax(volume_simulator.output['controlled_volume'])
controlled_volume_name = list(output_controlled_volume.terms.keys())[controlled_volume_label]

print(f"\033[93mControlled Volume: {volume_simulator.output['controlled_volume']} ({controlled_volume_name})\033[93m")
print("\033[95mGood to see you guys\033")
