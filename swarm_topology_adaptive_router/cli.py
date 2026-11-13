"""CLI for swarm-topology-adaptive-router."""
import sys
import argparse
from .router import TopologyRouter, RoutePacket

def main():
    parser = argparse.ArgumentParser(description="Swarm Topology Adaptive Router CLI")
    parser.add_argument("--demo", action="store_true", help="Run adaptive topology routing demo")
    args = parser.parse_args()

    if args.demo:
        router = TopologyRouter()
        router.add_edge("AgentA", "Hub1", 1.0)
        router.add_edge("Hub1", "Hub2", 2.0)
        router.add_edge("Hub2", "AgentB", 1.0)
        pkt = RoutePacket("AgentA", "AgentB", {"action": "sync_cache"})
        router.route_packet(pkt)
        print(f"[+] Initial routing path: {' -> '.join(pkt.hops)}")
        # Simulate traffic burst triggering direct peering optimization
        for _ in range(6):
            router.record_traffic("AgentA", "AgentB")
        pkt2 = RoutePacket("AgentA", "AgentB", {"action": "sync_cache_2"})
        router.route_packet(pkt2)
        print(f"[+] Re-routed path after adaptive optimization: {' -> '.join(pkt2.hops)}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
