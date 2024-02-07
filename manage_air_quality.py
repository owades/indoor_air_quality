import argparse
import purple_air_sensor as aqisensor
import ecobee_thermostat as thermo_stat
# In case of Nest, use this line instead:
# import nest_thermostat as thermo_stat
import datetime
import pytz

def manage_air_quality(aqi_sensor, thermostat, aqi_ceiling, fan_runtime_mins):
        
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
    thermostat.check_mode()
    thermostat.set_fan_timer(fan_runtime_mins)
    manage_air_quality(aqi_sensor, thermostat, aqi_ceiling, fan_runtime_mins)

if __name__ == '__main__':
   main()

#    Run with: python manage_air_quality.py --a [acceptable aqi threshold] --f [fan duration in minutes]
#    example: python manage_air_quality_2.py --a 50 --f 15