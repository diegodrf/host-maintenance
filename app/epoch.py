import time

def epochToHuman(x):

    return time.strftime('%Y-%m-%dT%H:%M', time.localtime(x))

def humanToEpoch(x):
    # GMT
    return int(time.mktime(time.strptime(x, '%Y-%m-%dT%H:%M')))


if __name__ == '__main__':
    n = 1541616000
    human_time = epochToHuman(n)
    epoch_time = humanToEpoch(human_time)

    print(human_time)
    print(epoch_time)
    print(n)