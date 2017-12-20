import sys, datetime, optparse
from core import pycore
from core.misc import ipaddr
from core.constants import *
n = [None]
def main():
    default_nodes = "8"
    nodes_number = int(default_nodes) # feed user input dynamically 
    usagestr = "usage: %prog [-h] [options] [args]"
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
    #command line options are parsed
    (options, args) = parser.parse_args()
    if options.numnodes < 1:
        usage("invalid number of nodes: %s" % options.numnodes)
    # upto 255 nodes can be generated for a single emulation
    if options.numnodes >= 255:
        usage("invalid number of nodes: %s" % options.numnodes)
    for a in args:
        sys.stderr.write("ignoring command line argument: '%s'\n" % a)
    start = datetime.datetime.now()
    session = pycore.Session(persistent=True)
    if 'server' in globals():#A global server variable is exposed to the script pointing to the CoreServer object in the core-daemon.
        server.addsession(session)
    print "creating %d nodes"  % options.numnodes
    left = None
    prefix = None
    #this loop configures the routers, establish links between interfaces and assign coordinates
    for i in xrange(1, options.numnodes + 1):
        nd = session.addobj(cls = pycore.nodes.CoreNode, name = "n%d" % i,
                             objid=i)
        if left:
            tmp.newnetif(left, ["%s/%s" % (prefix.addr(2), prefix.prefixlen)])
        prefix = ipaddr.IPv4Prefix("10.0.%d.0/24" % i) # assign IPv4 address to the node
        right = session.addobj(cls = pycore.nodes.PtpNet)
        nd.newnetif(right, ["%s/%s" % (prefix.addr(1), prefix.prefixlen)])
        # routing rules to be followed are set
        nd.cmd([SYSCTL_BIN, "net.ipv4.icmp_echo_ignore_broadcasts=0"])
        nd.cmd([SYSCTL_BIN, "net.ipv4.conf.all.forwarding=1"])
        nd.cmd([SYSCTL_BIN, "net.ipv4.conf.default.rp_filter=0"])
        nd.setposition(x=90*i,y=170)
        n.append(nd)
        left = right
    prefixes = map(lambda(x): ipaddr.IPv4Prefix("10.0.%d.0/24" % x),
                   xrange(1, options.numnodes + 1))
    # static route is set up
    for i in xrange(1, options.numnodes + 1):
        for j in xrange(1, options.numnodes + 1):
            if j < i - 1:
                g = prefixes[i-2].addr(1)
            elif j > i:
                if i > len(prefixes) - 1:
                    continue
                g = prefixes[i-1].addr(2)
            else:
                continue
            net = prefixes[j-1]
            n[i].cmd([IP_BIN, "route", "add", str(net), "via", str(g)])
    print "elapsed time: %s" % (datetime.datetime.now() - start)
if __name__ == "__main__" or __name__ == "__builtin__": # this line is needed for executing the script from the CORE-GUI
    main()
    


