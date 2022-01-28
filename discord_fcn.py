import json
from difflib import SequenceMatcher, get_close_matches
from send import *
import requests
import datetime as dt

now = dt.date.today()

def correct_word(prov, date=""):

    with open("provinces.json", "r") as data_file:
        fp = json.load(data_file)
        lstfp = list(fp)
        if prov not in lstfp:
            suggestion = get_close_matches(prov, lstfp, n=1, cutoff=0.3)
            if len(suggestion) == 0:
                return "Please re-write province with the command $Province {Province Name}"
            else:
                province = fp[suggestion[0]]["Dataset"]
                dataProv = data(province, date)
                msgData = combineMsgOne(dataProv, suggestion[0])
                return msgData

        else:
            province = fp[prov]["Dataset"]
            dataProv = data(province, date)
            msgData = combineMsgOne(dataProv, province)
            return msgData


def ranking(date, sortBy="active_cases"):
    param = {
        "date": date
    }

    response = requests.get(
        url="https://api.opencovid.ca/summary", params=param)
    response.raise_for_status()
    data = response.json()["summary"]
    active_cases = {

    }

    sortBypossiblity = ["active_cases", "active_cases_change", "avaccine", "cases", "cumulative_avaccine",
                        "cumulative_cases", "cumulative_cvaccine", "cumulative_deaths", "cumulative_dvaccine", "cumulative_recovered", "cumulative_testing", "recovered", "testing", "deaths"]
    sortByCheck = ""
    sortByCheck = sortBy
    print(sortBy)
    if sortBy in sortBypossiblity:
        sortByCheck = sortBy
    elif sortBy not in sortBypossiblity:
        sortBy = sortBy.lower()
        sortByCheck = get_close_matches(
            sortBy, sortBypossiblity, n=1, cutoff=0.1)[0]
    for i in data:
        province = i["province"]
        active = i[sortByCheck]
        active_cases[province] = active

    sortedActiveCases = sorted(active_cases, key=active_cases.get)[::-1]

    sorted_dict = {}

    for j in sortedActiveCases:
        sorted_dict[j] = active_cases[j]
    dates = data[0]["date"]
    formatted = f"""```Sort by {sortByCheck} on {dates}\n"""
    count = 1
    for k in sorted_dict.keys():
        string_ranking = f"{count}. {k}: {sorted_dict[k]}\n"
        formatted += string_ranking
        count += 1
    formatted += "```"

    return formatted
