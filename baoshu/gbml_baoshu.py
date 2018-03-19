import requests


def getGbmlAll():

    url = 'http://manager.starb168.com/fn/data/report?gameCode=mthxtw'
    res = requests.get(url)
    print res


if __name__ == '__main__':
    getGbmlAll
