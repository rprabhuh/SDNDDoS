# encode categorical protocol name to number
def encode_protocol(text):
  # put frequent cases to the front
  if 'tcp' in text:
    return 6
  elif 'udp' in text:
    return 17
  elif 'icmp' in text:
    return 1
  elif 'hopopt' in text:
    return 0
  elif 'igmp' in text:
    return 2
  elif 'ggp' in text:
    return 3
  elif 'ipv4' in text:
    return 4
  elif 'stp' in text:
    return 118
  elif 'st' in text:
    return 5
  elif 'cbt' in text:
    return 7
  elif 'egp' in text:
    return 8
  elif 'igp' in text:
    return 9
  elif 'bbn-rcc' in text:
    return 10
  elif 'nvp' in text:
    return 11
  elif 'pup' in text:
    return 12
  elif 'argus' in text:
    return 13
  elif 'emcon' in text:
    return 14
  elif 'xnet' in text:
    return 15
  elif 'chaos' in text:
    return 16
  elif 'mux' in text:
    return 18
  elif 'dcn' in text:
    return 19
  elif 'hmp' in text:
    return 20
  elif 'prm' in text:
    return 21
  elif 'xns-idp' in text:
    return 22
  elif 'trunk-1' in text:
    return 23
  elif 'trunk-2' in text:
    return 24
  elif 'leaf-1' in text:
    return 25
  elif 'leaf-2' in text:
    return 26
  elif 'rdp' in text:
    return 27
  elif 'irtp' in text:
    return 28
  elif 'iso-tp4' in text:
    return 29
  elif 'netblt' in text:
    return 30
  elif 'mfe-nsp' in text:
    return 31
  elif 'merit-inp' in text:
    return 32
  elif 'dccp' in text:
    return 33
  elif '3pc' in text:
    return 34
  elif 'idpr' in text:
    return 35
  elif 'xtp' in text:
    return 36
  elif 'ddp' in text:
    return 37
  elif 'idpr-cmtp' in text:
    return 38
  elif 'tp++' in text:
    return 39
  elif 'il' in text:
    return 40
  elif 'sdrp' in text:
    return 42
  elif 'ipv6-route' in text:
    return 43
  elif 'ipv6-frag' in text:
    return 44
  elif 'idrp' in text:
    return 45
  elif 'rsvp' in text:
    return 46
  elif 'gre' in text:
    return 47
  elif 'dsr' in text:
    return 48
  elif 'bna' in text:
    return 49
  elif 'esp' in text:
    return 50
  elif 'ah' in text:
    return 51
  elif 'i-nlsp' in text:
    return 52
  elif 'swipe' in text:
    return 53
  elif 'narp' in text:
    return 54
  elif 'mobile' in text:
    return 55
  elif 'tlsp' in text:
    return 56
  elif 'skip' in text:
    return 57
  elif 'ipv6-icmp' in text:
    return 58
  elif 'ipv6-nonxt' in text:
    return 59
  elif 'ipv6-opts' in text:
    return 60
  elif 'ipv6' in text:
    return 41
  elif 'internal' in text:
    return 61
  elif 'cftp' in text:
    return 62
  elif 'local' in text:
    return 63
  elif 'sat-expak' in text:
    return 64
  elif 'kryptolan' in text:
    return 65
  elif 'rvd' in text:
    return 66
  elif 'ippc' in text:
    return 67
  elif 'distributed' in text:
    return 68
  elif 'sat-mon' in text:
    return 69
  elif 'visa' in text:
    return 70
  elif 'ipcv' in text:
    return 71
  elif 'cpnx' in text:
    return 72
  elif 'cphb' in text:
    return 73
  elif 'wsn' in text:
    return 74
  elif 'pvp' in text:
    return 75
  elif 'br-sat-mon' in text:
    return 76
  elif 'sun-nd' in text:
    return 77
  elif 'wb-mon' in text:
    return 78
  elif 'wb-expak' in text:
    return 79
  elif 'iso-ip' in text:
    return 80
  elif 'secure-vmtp' in text:
    return 82
  elif 'vmtp' in text:
    return 81
  elif 'vines' in text:
    return 83
  elif 'ttp' in text:
    return 84
  elif 'iptm' in text:
    return 84
  elif 'nsfnet-igp' in text:
    return 85
  elif 'dgp' in text:
    return 86
  elif 'tcf' in text:
    return 87
  elif 'eigrp' in text:
    return 88
  elif 'ospfigp' in text:
    return 89
  elif 'sprite-rpc' in text:
    return 90
  elif 'larp' in text:
    return 91
  elif 'mtp' in text:
    return 92
  elif 'ax.25' in text:
    return 93
  elif 'ipip' in text:
    return 94
  elif 'micp' in text:
    return 95
  elif 'ssc-sp' in text:
    return 96
  elif 'etherip' in text:
    return 97
  elif 'encap' in text:
    return 98
  elif 'private-encryp' in text:
    return 99
  elif 'gmtp' in text:
    return 100
  elif 'ifmp' in text:
    return 101
  elif 'pnni' in text:
    return 102
  elif 'pim' in text:
    return 103
  elif 'aris' in text:
    return 104
  elif 'scps' in text:
    return 105
  elif 'qnx' in text:
    return 106
  elif 'a/n' in text:
    return 107
  elif 'ipcomp' in text:
    return 108
  elif 'snp' in text:
    return 109
  elif 'compaq' in text:
    return 110
  elif 'ipx-in-ip' in text:
    return 111
  elif 'vrrp' in text:
    return 112
  elif 'pgm' in text:
    return 113
  elif '0-hop' in text:
    return 114
  elif 'l2tp' in text:
    return 115
  elif 'ddx' in text:
    return 116
  elif 'iatp' in text:
    return 117
  elif 'stp' in text:
    return 118
  elif 'srp' in text:
    return 119
  elif 'uti' in text:
    return 120
  elif 'smp' in text:
    return 121
  elif 'sm' in text:
    return 122
  elif 'ptp' in text:
    return 123
  elif 'isis' in text:
    return 124
  elif 'fire' in text:
    return 125
  elif 'crtp' in text:
    return 126
  elif 'crudp' in text:
    return 127
  elif 'sscopmce' in text:
    return 128
  elif 'iplt' in text:
    return 129
  elif 'sps' in text:
    return 130
  elif 'pipe' in text:
    return 131
  elif 'sctp' in text:
    return 132
  elif 'fc' in text:
    return 133
  elif 'rsvp-e2e-ignore' in text:
    return 134
  elif 'mobility' in text:
    return 135
  elif 'udplite' in text:
    return 136
  elif 'mpls-in-ip' in text:
    return 137
  elif 'manet' in text:
    return 138
  elif 'hip' in text:
    return 139
  elif 'shim6' in text:
    return 140
  elif 'wesp' in text:
    return 141
  elif 'rohc' in text:
    return 142
  elif 'experiment' in text:
    return 143			# 253
  elif 'test' in text:
    return 144			# 254
  else:
    return 145			# 255

