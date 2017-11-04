from . import dummy
from . import gbn
from . import ss
import struct


def get_transport_layer_by_name(name, local_port, remote_port, msg_handler):
  assert name == 'dummy' or name == 'ss' or name == 'gbn'
  if name == 'dummy':
    return dummy.DummyTransportLayer(local_port, remote_port, msg_handler)
  if name == 'ss':
    return ss.StopAndWait(local_port, remote_port, msg_handler)
  if name == 'gbn':
    return gbn.GoBackN(local_port, remote_port, msg_handler)


def make_packet(msg_type, seq, msg):
  type_string = encode_int16(msg_type)
  seq_string = encode_int16(seq)
  check_sum = get_check_sum(type_string + seq_string + msg)
  check_sum_string = encode_int16(check_sum)
  packed_msg = type_string + seq_string + check_sum_string + msg
  return packed_msg
  
def get_check_sum(msg):
  asc_num = [ord(c) for c in msg]    
  if len(asc_num)%2 > 0 : asc_num.append(0)
  check_sum = 0
  for d in range(0,len(asc_num)-1, 2):
    check_sum += asc_num[d]*256 + asc_num[d+1] 
  return check_sum & 0x7fff
  
def is_original_packet(packet):
  type_string = packet[:2]
  seq_string = packet[2:4]
  check_sum_string = packet[4:6]
  data = packet[6:]
  msg_to_check = type_string + seq_string + data
  if (check_sum_string == encode_int16(get_check_sum(msg_to_check))):
    return True
  return False
  
def get_packet_seq(packet):
  seq_string = packet[2:4]
  return decode_int16(seq_string)
  
def get_packet_type(packet):
  type_string = packet[:2]
  return decode_int16(type_string)


def get_packet_msg(packet):
  return packet[6:]

# Encode a short int to byte code using network endianess.
#
# x: int
# return: string (of length 2)
def encode_int16(x):
  return struct.pack('!h', x)
  
  
# Decode a short int from its byte encoding.
#
# x: byte encoding of int (of length 2)
# return: int
def decode_int16(x):
  return struct.unpack('!h', x)[0]