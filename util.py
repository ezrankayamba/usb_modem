from smspdu import SMS_SUBMIT


def split(line, n, append=''):
    res = [line[i:i + n] for i in range(0, len(line), n)]
    lst = res[-1]
    if append and len(lst) < n:
        lst = lst.ljust(n, append)
        res[-1] = lst
    return res


def swap_hex(lst):
    return list(map(lambda x: f'{x[1]}{x[0]}', lst))


def at_cmgs(smsc_raw, sender, receiver, text_msg):
    tokens = smsc_raw.split(",")
    smsc_no = tokens[0][2:-1]
    type_int = int(tokens[1])
    pdu = SMS_SUBMIT.create(sender, receiver, text_msg)
    tpdu = pdu.toPDU()
    test = '01' + '00' + '{:02X}'.format(len(receiver[1:])) + '91' + ''.join(swap_hex(split(receiver[1:], 2, 'F'))) + '0000' + '%02X' % pdu.tp_udl + ''.join(['%02X' % ord(c) for c in pdu.tp_ud])
    print(test)
    tmp = '{:02X}'.format(type_int) + ''.join(swap_hex(split(smsc_no, 2, 'F')))
    smsc_len = int(len(tmp) / 2)
    smsc = '{:02X}'.format(smsc_len) + tmp
    tpdu_len = int(len(test) / 2)
    return (tpdu_len, smsc, test)


def test():
    print('Check ...')
    res = at_cmgs('"+85290000000",145', '+85290000000', '+85291234567', 'It is easy to send text messages.')
    pdu_len, smsc, tpdu = res
    tpdu = f'{pdu_len}\r{smsc}{tpdu}'
    print(tpdu)
    print(tpdu == '42\r07915892000000F001000B915892214365F7000021493A283D0795C3F33C88FE06CDCB6E32885EC6D341EDF27C1E3E97E72E')
    # print('Origin: ' + '42\r07915892000000F001000B915892214365F7000021493A283D0795C3F33C88FE06CDCB6E32885EC6D341EDF27C1E3E97E72E')
    print(f'Result: {res}')


test()
