"""
 @author Marildo Cesar 25/04/2023
"""

from src.services.status_invest import StatusInvest

statusI = StatusInvest()
data = statusI.find_by_name('BANCO INTER')
#statusI.download_images(245)
for i in data:
    print(i)

