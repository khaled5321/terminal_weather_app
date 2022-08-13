import os
import requests
import sys
from dotenv import load_dotenv
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.console import Console
from rich.table import Table


class ApiClient:
    def __init__(self, apikey):
        self.api_key=apikey
    
    def get_current_temperature(self,city):
        URL = f'https://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}'
        response = requests.get(URL)
        data=response.json()
        current_temp=data['current']['temp_c']
        console.print(f'[bold red]current tempretaure is:[/bold red] {current_temp}')
    
    def get_temperature_after(self, city, days, hour=None):
        URL = f'https://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&days={days}'
        response = requests.get(URL)
        data=response.json()

        table = Table(title="Forecast")
        table.add_column("Temperature", justify="center", style="cyan", no_wrap=True)
        table.add_column("time", style="magenta", justify="center")

        if days==1:
            temp=data['current']['temp_c']
            time=data['current']['last_updated']
            table.add_row(str(temp), str(time))
        else:
            forecast=data['forecast']['forecastday']
            for i in forecast:
                day=i['day']
                hours=i['hour']
                if hour:
                    _hour=hours[hour]
                    time=_hour['time']
                    temp=_hour['temp_c']
                else:
                    temp=day['maxtemp_c']
                    time=i["date"]
                table.add_row(str(temp), str(time))

        console.print(table, justify="center")
    

def main():
    console.print("--Weather API--", style="bold yellow", justify="center")

    city = Prompt.ask("Enter city name")

    option = Prompt.ask("choose option", choices=options, default="current temp")

    if option=="current temp":
        api.get_current_temperature(city)
    
    else:
        days=IntPrompt.ask("Enter Number of days of weather forecast. Value ranges from 1 to 10")
        if days>10 or days<1:
            console.print_exception("invalid number of days")
            main()

        hour=IntPrompt.ask("You can Enter hour of day. valuse range from 0 to 24", default=None)
        if hour and (hour>24 or hour<0):
            console.print_exception("invalid hour")
            main()

        api.get_temperature_after(city, days, hour)

    is_continue = Confirm.ask("Do you want to continue?")
    if(not is_continue):
        sys.exit()

    main() 

if __name__=="__main__":
    load_dotenv()
    key=os.environ["key"]

    api= ApiClient(key)

    console = Console(width=100)

    options=['current temp','forecast']

    main()