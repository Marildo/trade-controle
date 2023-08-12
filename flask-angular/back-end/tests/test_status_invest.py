"""
 @author Marildo Cesar 25/04/2023
"""

from src.services.status_invest import StatusInvest

statusI = StatusInvest()
# data = statusI.find_by_name('Banrisul')
# #statusI.download_images(245)
# for i in data:
#     print(i)

data = statusI.load_dividendos_fiis('tord11')
print(data)
