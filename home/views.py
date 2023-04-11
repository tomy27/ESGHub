from django.shortcuts import render
from .models import DataExt, DataDetails, Database
import json
from django.http import JsonResponse
import requests
# import csv


def index(request):
    return render(request, "index.html")


def what(request):
    return render(request, "what_is_esg.html")


def search(request):
    query = request.GET.get('term', '')
    results = Database.objects.filter(company__icontains=query)
    suggestions = [result.company for result in results]
    return JsonResponse(suggestions, safe=False)


def chartdata(request, id):
    try:
        query = DataDetails.objects.get(cid=id)
        flags = json.loads(str(query))
    except:
        # Get detailed ESG data from API
        url = f"https://apis.esganalytics.io/7b2f6v3xevs7t3f2/company/nlp/?company_id={id}&feed_type=flags"
        headers = {
            "X-BLOBR-KEY": "!!! PUT YOUR API KEY HERE !!!"
        }
        response = requests.get(url, headers=headers)
        DataDetails.objects.create(cid=id, data=response.text)
        flags = json.loads(str(response.text))

    # Define dict
    data = {}

    # Fill up dict with topic and company data
    for i in flags["data"]["company_ai_flags"]:
        data[i["topic"]] = [i["sentiment_avg"]]

    # Fill up dict with industry data
    for i in flags["industry_data"]["industry_ai_flags"]:
        if i["topic"] in data:
            s = data[i["topic"]]
            s.append(i["sentiment_avg"])

    return JsonResponse({'data': data})


def query(request):
    q = request.GET.get('q')
    query = Database.objects.filter(company=q)

    # Load csv into database
    """
    with open('home/static/stocks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_data = list(csv_reader)

        length = len(csv_data) - 1
        batch_size = 200
        bucket = []
        for i in range(1, length):
            bucket.append(Database(cid=csv_data[i][0], company=csv_data[i][1]))
        Database.objects.bulk_create(bucket, batch_size)
        print("Successfully uploaded!")
    """

    cid = query[0].cid
    rawCompany = query[0].company
    company = rawCompany.replace(",", "").replace(".", "")

    try:
        # Define dict
        stockData = {}

        # Get company symbol
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company}&apikey=!!! PUT YOUR API KEY HERE !!!'
        r = requests.get(url)
        d = r.json()
        for i in d["bestMatches"]:
            if i["4. region"] == "United States" and i["3. type"] == "Equity":
                symbol = i["1. symbol"]
                stockData["symbol"] = symbol
                break

        # Get price data
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&datatype=json&apikey=!!! PUT YOUR API KEY HERE !!!'
        r = requests.get(url)
        d = r.json()
        stockData["close"] = float(list(d["Time Series (Daily)"].values())[0]["4. close"])
        stockData["open"] = float(list(d["Time Series (Daily)"].values())[0]["1. open"])
        stockData["change"] = round(stockData["close"] - stockData["open"], 2)

        # Get market cap data
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=!!! PUT YOUR API KEY HERE !!!'
        r = requests.get(url)
        d = r.json()
        stockData["marketcap"] = round((float(d["MarketCapitalization"])) / 10**9, 2)

        try:
            query = DataExt.objects.get(cid=cid)
            data = json.loads(str(query))
        except:
            # Get external ESG data from API
            url = f"https://apis.esganalytics.io/7b2f6v3xevs7t3f2/company/external/?company_id={cid}"
            headers = {
                "X-BLOBR-KEY": "!!! PUT YOUR API KEY HERE !!!"
            }
            response = requests.get(url, headers=headers)
            DataExt.objects.create(cid=cid, data=response.text)
            data = json.loads(str(response.text))

        return render(request, "result.html", {
            "company": company,
            "cid": cid,
            "update": str(data["details"][0]["update_date"]),
            "snp": str(data["details"][0]["snp"]),
            "snp_link": str(data["details"][0]["snp_link"]),
            "msci": str(data["details"][0]["msci"]),
            "msci_link": str(data["details"][0]["msci_link"]),
            "stockData": stockData,
        })
    except KeyError:
        return render(request, "index.html", {
            "message": "ERROR: Too many attempts, try again later!",
        })
    except UnboundLocalError:
        return render(request, "index.html", {
            "message": "ERROR: Company not found, try another one!",
        })
    except:
        return render(request, "index.html", {
            "message": "ERROR: something went wrong!",
        })



