import requests
from datetime import datetime, timedelta
import itertools
from operator import itemgetter


class Data():

    countries_list = []
    COUNTRIES_NAME = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                      'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    base_url = 'https://api.covid19api.com/'

    def get_countries_list(self):
        countries_json = requests.get(self.base_url+'countries').json()
        self.countries_list = [
            {'label': item['Country'], 'value':item['Country']} for item in countries_json]
        return self.countries_list

    def get_data_wrt_date(self, value, status, start_date, end_date, is_daily):
    
        tmp = []
        end_date_obj = datetime.strptime(end_date[:10], '%Y-%m-%d')

        start = str(datetime.strptime(start_date[:10], '%Y-%m-%d'))
        end = str(datetime.strptime(end_date[:10], '%Y-%m-%d'))

        if not (type(value) == list):
            tmp = value
            value = []
            value.append(tmp)

        tmp = []

        for country in value:

            response_json = requests.get(
                self.base_url+'country/'+country+'/status/'+status+'?from='+start+'&to='+end).json()

            response_list = []

            for key, val in itertools.groupby(response_json, key=itemgetter('Date')):

                sum = 0
                for i in val:
                    sum += i.get('Cases')
                response_list.append(sum)

            if(is_daily):
                response_list = [y-x for x,
                                 y in zip(response_list, response_list[1:])]

            date_list = [end_date_obj -
                         timedelta(days=x) for x in range(len(response_list))]
            date_list = [str(i.day)+'-'+(self.COUNTRIES_NAME[i.month-1])
                         for i in date_list]
            (date_list.reverse())

            tmp.append({"x": date_list, 'y': response_list,
                        'name': country, 'hover_name': 'country'})

        return tmp
