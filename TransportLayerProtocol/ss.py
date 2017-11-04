from . import udt
from . import util
from . import config
import time


# Stop-And-Wait reliable transport protocol.
class StopAndWait:
  # "msg_handler" is used to deliver messages to application layer
  # when it's ready.
  def __init__(self, local_port, remote_port, msg_handler):
    self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
    self.msg_handler = msg_handler
    # seq is the sequence sent, ack_seq is the sequence acked by receiver.
    self.seq = config.MSG_SEQ_ONE
    self.ack_seq = config.MSG_SEQ_ONE
    
  # "send" is called by application. Return true on success, false
  # otherwise.
  def send(self, msg):
    # TODO: impl protocol to send packet from application layer.
    # call self.network_layer.send() to send to network layer.
    self.seq ^= 1             
    packed_msg = util.make_packet(config.MSG_TYPE_DATA, self.seq, msg)
    self.network_layer.send(packed_msg)
    start_time = time.time()
    while self.seq != self.ack_seq:
      if time.time() > start_time + (config.TIMEOUT_MSEC / 1000.0):
        print("Resending packet seq: ", self.seq)
        self.network_layer.send(packed_msg)
        start_time = time.time()
    return True

  # "handler" to be called by network layer when packet is ready.
  def handle_arrival_msg(self):
    packet = self.network_layer.recv()
    # TODO: impl protocol to handle arrived packet from network layer.
    # call self.msg_handler() to deliver to application layer.
    packet_type = util.get_packet_type(packet)
    if packet_type == config.MSG_TYPE_DATA:
      seq_to_expect = self.ack_seq ^ 1
      if not util.is_original_packet(packet) or seq_to_expect != util.get_packet_seq(packet):
        print("GOT Packet: ", repr(packet))
        ack_packet = util.make_packet(config.MSG_TYPE_ACK, self.ack_seq, "Not right packet to receive.")
        self.network_layer.send(ack_packet)
        return
      self.ack_seq ^= 1
      ack_packet = util.make_packet(config.MSG_TYPE_ACK, self.ack_seq, "OK")
      msg = util.get_packet_msg(packet)
      self.msg_handler(msg)
      self.network_layer.send(ack_packet)
      
    elif packet_type == config.MSG_TYPE_ACK:
      packet_seq = util.get_packet_seq(packet)
      expect_ack_seq = self.seq
      if not util.is_original_packet(packet) or expect_ack_seq != packet_seq:
        return
      self.ack_seq ^= 1
      
      
  # Cleanup resources.
  def shutdown(self):
    # TODO: cleanup anything else you may have when implementing this
    # class.
    self.network_layer.shutdown()
