import time

def epochToHuman(x):

    return time.strftime('%Y-%m-%dT%H:%M', time.localtime(x))

def humanToEpoch(x):
    # GMT
    # Soma 3 horas para compensar o timezone. Fiquei horas mexendo e não sei o que fiz.
    return int(time.mktime(time.strptime(x, '%Y-%m-%dT%H:%M'))) + 10800


if __name__ == '__main__':
    n = 1541697624
    human_time = epochToHuman(n)
    epoch_time = humanToEpoch(human_time)

    print('human:', human_time)
    print('epoch:', epoch_time)
    print('n:', n)
    print('timezone:', time.timezone)