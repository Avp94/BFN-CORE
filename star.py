import sys, datetime, optparse
from core import pycore
from core.misc import ipaddr
from core.constants import *
n = [None]
def main():
    usagestr = "usage: %prog [-h] [options] [args]"
    default_nodes = "8"
    nodes_number = int(default_nodes) #feed user input dynamically 
    parser = optparse.OptionParser(usage = usagestr)
    parser.set_defaults(numnodes = nodes_number)
    parser.add_option("-n", "--numnodes", dest = "numnodes", type = int,
                      help = "number of nodes")
    def usage(msg = None, err = 0):
        sys.stdout.write("\n")
        if msg:
            sys.stdout.write(msg + "\n\n")
        parser.print_help()
        sys.exit(err)
    #parse command line options
    (options, args) = parser.parse_args()
    if options.numnodes < 1:
        usage("invalid number of nodes: %s" % options.numnodes)
    for a in args:
        sys.stderr.write("ignoring command line argument: '%s'\n" % a)
    start = datetime.datetime.now()
    prefix = ipaddr.IPv4Prefix("10.0.0.0/16") #range from which IPv4 addresses will be assigned
    session = pycore.Session(persistent=True) #core session is created
    #A global server variable is exposed to the script pointing to the CoreServer object in the core-daemon.
    if 'server' in globals():
        server.addsession(session)
    # a switch is placed in the topology
    switch = session.addobj(cls = pycore.nodes.SwitchNode, name = "switch")
    #assign coordinates for the switch
    switch.setposition(x=280,y=80)
    print "creating %d nodes with addresses from %s" % \
          (options.numnodes, prefix)
    #this loop configures the routers, establish links between interfaces and assign coordinates
    #assign routing rules to be followed
    for i in xrange(1, options.numnodes + 1):
        nd = session.addobj(cls = pycore.nodes.CoreNode, name = "n%d" % i,
                             objid=i)
        nd.newnetif(switch, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)])
        nd.cmd([SYSCTL_BIN, "net.ipv4.icmp_echo_ignore_broadcasts=0"])
        nd.setposition(x=100*i,y=180)
        n.append(nd)
    session.node_count = str(options.numnodes + 1)
    session.instantiate()
    #a shell is started on node 1
    n[1].term("bash")
    print "elapsed time: %s" % (datetime.datetime.now() - start)
if __name__ == "__main__" or __name__ == "__builtin__": # this line is needed for executing the script from the CORE-GUI
    main()

