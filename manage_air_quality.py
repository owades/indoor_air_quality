import argparse

import purple_air_sensor as aqisensor
import nest_thermostat as thermo_stat
import datetime

def manage_air_quality(aqi_sensor, thermostat, aqi_ceiling, fan_runtime_mins):
    
    current_hour = datetime.datetime.now().hour
    heat_off = thermostat.check_mode() == 'OFF'

    # If the heat is off at the end of the day, it automatically turns on the next day. This usecase is fairly specific.
    if heat_off and current_hour <= 7:
        print("Heat is set to OFF, turning heat on...")
        thermostat.set_mode('HEAT')

    aqi = aqi_sensor.get_aqi()
    if(aqi >= aqi_ceiling):
        print(f'Current AQI of {str(aqi)} is bad! It is above the maximum acceptable AQI of {str(aqi_ceiling)}...running fan for {str(fan_runtime_mins)} min')
        thermostat.set_fan_timer(fan_runtime_mins)
    else:
        print(f'Current AQI of {str(aqi)} is good! It is below the maximum acceptable AQI of {str(aqi_ceiling)}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', type=int, required=True)
    parser.add_argument('--f', type=int, required=True)
    args = parser.parse_args()
    aqi_ceiling = args.a
    fan_runtime_mins = args.f

    aqi_sensor = aqisensor.sensor()
    thermostat = thermo_stat.thermostat()
    manage_air_quality(aqi_sensor, thermostat, aqi_ceiling, fan_runtime_mins)

if __name__ == '__main__':
   main()

#    Run with: python manage_air_quality.py --a [acceptable aqi threshold] --f [fan duration in minutes]
#    example: python manage_air_quality.py --a 50 --f 15