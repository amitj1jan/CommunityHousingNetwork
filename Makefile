download: content/GrossRentByBedRooms.json content/costBurden.csv

content/GrossRentByBedRooms.json:
	python downloadGrossRent.py content/ GrossRentByBedRooms.json
    
content/costBurden.csv:
	python downloadCostBurden.py content/ costBurden.csv
    
