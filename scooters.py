#usage: ./scooters.py [json_file]

import dateutil.parser, json, datetime, sys

journeysDict = {}
shortJourneys = []
totalCost = 0
totalTime = datetime.timedelta(0,0)

with open(sys.argv[1], 'r') as json_file:
    data = json.load(json_file)
for journey in data:
    totalCost +=  journey['cost']
    time = dateutil.parser.parse(journey['endTime']) - dateutil.parser.parse(journey['startTime'])
    totalTime += time
    if time > datetime.timedelta(hours=1, minutes=30):
        shortJourneys.append(journey)
    if journey['bikeId'] in journeysDict:
        journeysDict[journey['bikeId']]['nb'] += 1
        journeysDict[journey['bikeId']]['cost'] += journey['cost']
        journeysDict[journey['bikeId']]['revenue'] += journey['revenue']
        journeysDict[journey['bikeId']]['totalTime'] += time
    else:
        journeysDict[journey['bikeId']] = {}
        journeysDict[journey['bikeId']]['nb'] = 1
        journeysDict[journey['bikeId']]['cost'] = journey['cost']
        journeysDict[journey['bikeId']]['revenue'] = journey['revenue']
        journeysDict[journey['bikeId']]['totalTime'] = time
for key, value in journeysDict.items():
    journeysDict[key]['averageCost'] = journeysDict[key]['cost'] / journeysDict[key]['nb']
    journeysDict[key]['averageTime'] =  journeysDict[key]['totalTime'] / journeysDict[key]['nb']

ret = {}
ret['dataPerScooter'] = journeysDict
ret['averageJourneyTime'] = totalTime / len(data)
ret['shortJourneys'] = shortJourneys

print("id".ljust(10), "#journeys".ljust(10), "Cost".ljust(10), \
"Revenue".ljust(10), "Avg time".ljust(10,), )
for key, value in ret['dataPerScooter'].items():
    print(key.ljust(10), \
    str(ret['dataPerScooter'][key]['nb']).ljust(10), \
    str(round((ret['dataPerScooter'][key]['cost'])/ 100, 2)).ljust(10), \
    str(round(ret['dataPerScooter'][key]['revenue'], 2)).ljust(10),\
    str(ret['dataPerScooter'][key]['averageTime']).ljust(10))

print("Average journey time for all scooters:", ret['averageJourneyTime'])
print("Journeys that lasted for longer than 1:30h:", ret['shortJourneys'])