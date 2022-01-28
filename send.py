import requests
import datetime as dt
import os


nowDate = dt.date.today()


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def data(loc="", date=""):
    summaryParam = {
        "loc": loc,
        "date": date

    }
    response = requests.get(
        url="https://api.opencovid.ca/summary", params=summaryParam)
    response.raise_for_status()
    data = response.json()["summary"][0]
    return data


def getNews(province):
    apiUrl = "https://newsapi.org/v2/everything"
    parameters = {
        "apiKey": os.environ.get("api_key"),
        "q": f"(Coronavirus OR COVID) AND {province}",
        "qInTitle": province,
        "from": nowDate - dt.timedelta(days=1),
        "to": nowDate,
        "sortBy": "relevancy"

    }

    print(province)
    print(parameters["q"])

    responseNews = requests.get(url=apiUrl, params=parameters)
    newsArtic = responseNews.json()
    return newsArtic["articles"][:3]


def sumDataReg(dataCity):
    city = dataCity["health_region"]
    prov = dataCity["province"]
    dateReg = dataCity["date"]
    casesReg = dataCity["cases"]
    deathsReg = dataCity["deaths"]

    messageRegData = f"""
    City: {city}
    Province: {prov}
    Date: {dateReg}
    Cases: {casesReg}
    Deaths: {deathsReg}
    ___________________________
    """

    return messageRegData


def sumDataPro(dataPro):
    datePro = dataPro["date"]
    activeCasesPro = dataPro["active_cases"]
    casesPro = dataPro["cases"]
    activeCasesChange = dataPro["active_cases_change"]
    deathsPro = dataPro["deaths"]
    recoveryPro = dataPro["recovered"]
    testingPro = dataPro["testing"]
    prov = dataPro["province"]

    messageQCData = f"""
    Province: {prov}
    Date: {datePro}
    Cases: {casesPro}
    Acive cases: {activeCasesPro}
    Active case change: {activeCasesChange}
    Deaths: {deathsPro}
    Recoveries: {recoveryPro}
    Testing: {testingPro}

    __________________________
    """

    messagePro = messageQCData
    return messagePro


def newsDataMsg(province):
    newsProv = getNews(province)

    messageNews = f""""""

    for i in range(len(newsProv)):
        article = newsProv[i]
        descr = remove_html_tags(article["description"]).encode(
            "ascii", "ignore").decode("ascii")
        temp_text = f"""
Article {i + 1} - {article["author"]}

Title: {article["title"]}
Description: {descr}...
URL: {article["url"]}

                    """
        messageNews += temp_text
    return messageNews


def combineMsgOne(dataSum, province):
    return f"""
    ```
    Searching for {province}
    {sumDataPro(dataSum)}
    ```
    """


def combineMsgProvCity(province, dataSumOne, dataSumTwo=""):
    return f"""
    ```
    {sumDataPro(dataSumOne)}
    {sumDataReg(dataSumTwo)}
    ```
    """
