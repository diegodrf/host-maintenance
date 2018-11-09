import time

def epochToHuman(x):

    return time.strftime('%Y-%m-%dT%H:%M', time.localtime(x))

def humanToEpoch(x):
    # GMT
    # Soma 3 horas para compensar o timezone. Fiquei horas mexendo e não sei o que fiz.
    timestamp = int(time.mktime(time.strptime(x, '%Y-%m-%dT%H:%M')))
    return timestamp


if __name__ == '__main__':
    n = 1541764800
    human_time = epochToHuman(n)
    epoch_time = humanToEpoch(human_time)

    print('human:\t\t', human_time)
    print('epoch:\t\t', epoch_time)
    print('    n:\t\t', n)
    #print('timezone:', time.timezone)