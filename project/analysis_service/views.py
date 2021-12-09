from rest_framework.views import APIView

from main_service.serializers import  VgSalesSerialier
from django.db.models import Sum
from main_service.models import vgSales
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
class ComparisonTwoGames(APIView):
    serializer_class = VgSalesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, name_game1, name_game2):
        game1 = vgSales.objects.filter(Name=name_game1)
        game2 = vgSales.objects.filter(Name=name_game2)
        na1 = 0
        eu1 = 0
        jp1 = 0
        other1 = 0
        global1 = 0
        
        if len(game1) != 1:
            for game in game1:
                na1 = na1 + game.NA_Sales
                eu1 = eu1 + game.EU_Sales
                jp1 = jp1 + game.JP_Sales
                other1 = other1 + game.Other_Sales
                global1 = global1 + game.Global_Sales
        else:
                na1 = game1.get().NA_Sales
                eu1 = game1.get().EU_Sales
                jp1 = game1.get().JP_Sales
                other1 = game1.get().Other_Sales
                global1 = game1.get().Global_Sales
        
        game1_np = np.array([na1, eu1, jp1, other1, global1])

        na1 = 0
        eu1 = 0
        jp1 = 0
        other1 = 0
        global1 = 0

        if len(game2) != 1:
            for game in game2:
                na1 = na1 + game.NA_Sales
                eu1 = eu1 + game.EU_Sales
                jp1 = jp1 + game.JP_Sales
                other1 = other1 + game.Other_Sales
                global1 = global1 + game.Global_Sales
        else:
                na1 = game2.get().NA_Sales
                eu1 = game2.get().EU_Sales
                jp1 = game2.get().JP_Sales
                other1 = game2.get().Other_Sales
                global1 = game2.get().Global_Sales


        game2_np = np.array([na1, eu1, jp1, other1, global1])

        figure, axis = plt.subplots(1, 2, constrained_layout=True, figsize=(15,15))

        axis[0].bar(['NA', 'EU', 'JP', 'Other', 'Global'], game1_np)
        axis[0].set_title(f"{name_game1}")

        axis[1].bar(['NA', 'EU', 'JP', 'Other', 'Global'], game2_np)
        axis[1].set_title(f"{name_game2}")
        
        plt.savefig(f"comparison_{name_game1}_with_{name_game2}.png")


        return Response(data={
            'game1_NA': game1_np[0],
            'game1_EU': game1_np[1],
            'game1_JP': game1_np[2],
            'game1_Other': game1_np[3],
            'game1_Global': game1_np[4], 
            'game2_NA': game2_np[0],
            'game2_EU': game2_np[1],
            'game2_JP': game2_np[2],
            'game2_Other': game2_np[3],
            'game2_Global': game2_np[4], 
        })


class TotalSalesEachYear(APIView):
    serializer_class = VgSalesSerialier
    permission_classes = (IsAuthenticated,)


    def get(self, request, yearOne, yearTwo):

        yearTemp = yearOne
        total_sales = []

        while(yearTemp != (yearTwo+1)):
            # games = vgSales.objects.filter(Year=yearTemp)
            games_sum = vgSales.objects.filter(Year=yearTemp).aggregate(
                    sum=Sum('EU_Sales') + Sum('NA_Sales') + Sum('JP_Sales') + Sum('Other_Sales') + Sum('Global_Sales')).get('sum')   
            if games_sum == None: games_sum = 0 
            
            total_sales.append(f"{yearTemp}:{games_sum}")

            yearTemp = yearTemp + 1
        
        year = []
        sales = []
        for ts in total_sales:
            year.append(ts.split(":")[0])
            sales.append(float(ts.split(":")[1]))
        
        sales_np = np.array(sales)
        
        fig = plt.figure(figsize = (10, 5))

        plt.bar(year, sales_np)

        plt.title(f"Total Sales in {yearOne} until {yearTwo}")
        
        plt.savefig(f"Total Sales in {yearOne} until {yearTwo}.png")

        return Response(data={
            'year': year,
            'sales': sales_np,
        })


class TotalSalesBetweenPublisherEachYear(APIView):
    serializer_class = VgSalesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, yearOne, yearTwo, publisherOne, publisherTwo):
        yearTemp = yearOne
        total_sales = []
        while(yearTemp != (yearTwo+1)):
            games_sum = vgSales.objects.filter(Year=yearTemp, Publisher=publisherOne).aggregate(
                    sum=Sum('EU_Sales') + Sum('NA_Sales') + Sum('JP_Sales') + Sum('Other_Sales') + Sum('Global_Sales')).get('sum')
            
            if games_sum == None: games_sum = 0
            
            total_sales.append(f"{yearTemp}:{games_sum}")

            yearTemp = yearTemp + 1
        
        year = []
        sales = []
        for ts in total_sales:
            year.append(ts.split(":")[0])
            sales.append(float(ts.split(":")[1]))
        
        sales_np_publisher1 = np.array(sales)
        
        
        yearTemp = yearOne
        total_sales = []

        while(yearTemp != (yearTwo+1)):
            games = vgSales.objects.filter(Year=yearTemp, Publisher=publisherTwo)
            sum = 0

            for game in games:
                sum = sum + game.NA_Sales + game.EU_Sales + game.JP_Sales + game.Other_Sales + game.Global_Sales
            
            total_sales.append(f"{yearTemp}:{sum}")

            yearTemp = yearTemp + 1
        
        year = []
        sales = []
        for ts in total_sales:
            year.append(ts.split(":")[0])
            sales.append(float(ts.split(":")[1]))
        
        sales_np_publisher2 = np.array(sales)


        figure, axis = plt.subplots(1, 2, constrained_layout=True, figsize=(15,15))

        axis[0].bar(year, sales_np_publisher1)
        axis[0].set_title(f"{publisherOne}")

        axis[1].bar(year, sales_np_publisher2)
        axis[1].set_title(f"{publisherTwo}")
        
        plt.savefig(f"comparison_{publisherOne}_with_{publisherTwo}_EachYear.png")


        return Response(data={
            f"save image as comparison_{publisherOne}_with_{publisherTwo}_EachYear.png",
        })
