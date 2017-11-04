from . import udt
from . import util
from . import config
import time


# Go-Back-N reliable transport protocol.
class GoBackN:
  # "msg_handler" is used to deliver messages to application layer
  # when it's ready.
  def __init__(self, local_port, remote_port, msg_handler):
    self.network_layer = udt.NetworkLayer(local_port, remote_port, self)
    self.msg_handler = msg_handler
    self.expect_seq = 0
    self.base_seq = 0
    self.next_seq = 0
    self.packets = []
    self.start_time = 0

  # "send" is called by application. Return true on success, false
  # otherwise.
  def send(self, msg):
    # TODO: impl protocol to send packet from application layer.
    # call self.network_layer.send() to send to network layer.
    if self.next_seq < self.base_seq + config.WINDOWN_SIZE:
      packet = util.make_packet(config.MSG_TYPE_DATA, self.next_seq, msg)
      self.packets.append(packet)
      self.network_layer.send(packet)
      if (self.base_seq == self.next_seq):
        self.start_time = time.time()
      self.next_seq += 1
      return True

    else:
      if time.time() > self.start_time + (config.TIMEOUT_MSEC / 1000.0):
        self.start_time = time.time()
        for i in range(self.base_seq, self.next_seq):
          print("Resenting packets: ", i)
          self.network_layer.send(self.packets[i])
      return False


  # "handler" to be called by network layer when packet is ready.
  def handle_arrival_msg(self):
    packet = self.network_layer.recv()
    # TODO: impl protocol to handle arrived packet from network layer.
    # call self.msg_handler() to deliver to application layer.
    ack_packet = util.make_packet(config.MSG_TYPE_ACK, self.expect_seq - 1, "Random stuff.")
    packet_type = util.get_packet_type(packet)
    if packet_type == config.MSG_TYPE_DATA:
      packet_seq = util.get_packet_seq(packet)
      if util.is_original_packet(packet) and self.expect_seq == packet_seq :
        msg = util.get_packet_msg(packet)
        self.msg_handler(msg)
        ack_packet = util.make_packet(config.MSG_TYPE_ACK, self.expect_seq, "OK")
        self.network_layer.send(ack_packet)
        self.expect_seq += 1
        return
      self.network_layer.send(ack_packet)
      
    elif packet_type == config.MSG_TYPE_ACK :
          if util.is_original_packet(packet):
            self.base_seq = util.get_packet_seq(packet) + 1
            if self.base_seq == self.next_seq:
              self.start_time = 0
            else:
              self.start_time = time.time()

  # Cleanup resources.
  def shutdown(self):
    # TODO: cleanup anything else you may have when implementing this
    # class.
    self.network_layer.shutdown()
