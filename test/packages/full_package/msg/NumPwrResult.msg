# Demo of a custom message definition in a ros package.
#
# This message is supposed to be a simulation for a node that is like a message
# filter. This is the response. The node has received an incoming message, and
# publishes this message in response.

# Result of raising the incoming number to a power
float64 to_power
# Result of taking the powereth_root of the number, eg to the power (1./exponent)
float64 to_root
