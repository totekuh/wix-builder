import string
import secrets
import random
from typing import List

WORDS1 = [
    "Cloud", "System", "Net", "Diag", "Win", "App", "Core", "Service", "Data", "Stream",
    "Pulse", "Echo", "Node", "Atlas", "Vector", "Nimbus", "Halo", "Orbit", "Axis", "Matrix",
    "Bridge", "Gate", "Flux", "Quantum", "Signal", "Anchor", "Forge", "Kernel", "Shard", "Slate",
    "Prism", "Horizon", "Vertex", "Sigma", "Cache", "Relay", "Field",
    "Vortex", "Cluster", "Aspect", "Glyph", "Lumen", "Quartz", "Cobalt", "Onyx", "Argon", "Nova",
    "Helix", "Cipher", "Radiant", "Marlin", "Talon", "Serris", "Sentinel", "Harbor",
    "Canoe", "Rivet", "Pixel", "Raster", "Magma", "Drift", "Falcon", "Ridge", "Summit", "Bastion",
    "Strata", "Contour", "Munit", "Ledger", "Pylon", "Anchorite", "Compass", "Cartel", "Galley",
    "Haven", "Citadel", "Tesser", "Paragon", "Mercury", "Apollo", "Orion", "Lyra", "Kodiak",
    "Nomad", "Arcadia", "Echelon", "Mirage", "Cinder", "Grove", "Boreal", "Celest", "Fathom",
    "Corsair", "Vanguard", "Helios", "Argus", "Warden", "Cachet", "Fjord", "Nebula", "Cascade",
]

WORDS2 = [
    "Manager", "Host", "Helper", "Agent", "Updater", "Module", "Daemon", "Broker", "Keeper",
    "Watcher", "Guardian", "Handler", "Driver", "Controller", "Supervisor", "Monitor", "Proxy",
    "Service", "Runner", "Launcher", "AgentPro", "DaemonSvc", "Orchestrator", "Scheduler",
    "Coordinator", "Dispatcher", "Operator", "Admin", "AgentCore", "AgentHost", "Conductor",
    "Executor", "Invoker", "Adapter", "Connector", "Shim", "ControllerX", "Pilot",
    "KeeperX", "Observer", "Registrar", "RegistrarSvc", "Binder", "RegistrarX", "Anchorman",
    "AnchorSvc", "Custodian", "Archivist", "ArchivistSvc", "Mediator", "Marshal", "Sentinel",
    "SentinelSvc", "Gatekeeper", "Pathfinder", "Navigator", "Scout", "Surveyor", "Warden",
    "Viceroy", "Overseer", "Steward", "Caretaker", "Curator", "Shepherd", "Harbinger", "Catalyst",
    "Engine", "Assembler", "Fabric", "Synth", "Composer", "Builder", "Smith", "Forge", "Foundry",
    "Smithery", "Molder", "Conflux", "Mixer", "Fluxer", "Balancer", "Regulator", "Optimizer",
    "Tuner", "Profiler", "Inspector", "Scanner", "Analyzer", "Indexer", "Collector", "Aggregator",
    "Harvester", "Miner", "Extractor", "Fetcher", "Retriever", "Packer", "Unpacker", "Serializer",
    "Deserializer", "Marshaller", "Gateway", "Endpoint", "ServiceBus", "Pipeline", "Streamlet",
    "Router", "Switch", "Mux", "Demux", "Distributor", "BalancerX", "BalancerSvc", "RelaySvc",
]

SUFFIXES = ["Svc", "Core", "Pro", "SvcX", "Agent", "Mgr", "Host", "Daemon", "SvcPro", "Net"]
PREFIXES = ["Sys", "Win", "Micro", "Neo", "Ultra", "Hyper", "Meta", "Proto", "Secure", "True"]


def _pick(seq: List[str]) -> str:
    return secrets.choice(seq)


def generate_name(
    parts: int = 2,
    joiner: str = "",
    use_prefix: bool = True,
    use_suffix: bool = True,
) -> str:
    parts_list = []
    for i in range(parts):
        if i % 2 == 0:
            parts_list.append(_pick(WORDS1))
        else:
            parts_list.append(_pick(WORDS2))

    if use_prefix and secrets.randbelow(100) < 25:
        parts_list.insert(0, _pick(PREFIXES))
    if use_suffix and secrets.randbelow(100) < 30:
        parts_list.append(_pick(SUFFIXES))

    parts_list = [p[0].upper() + p[1:] if p else p for p in parts_list]
    name = joiner.join(parts_list)

    allowed = string.ascii_letters + string.digits + "_"
    sanitized = "".join(ch if ch in allowed else "_" for ch in name)
    if sanitized and sanitized[0] in string.digits:
        sanitized = "A" + sanitized

    return sanitized


def random_version(parts: int = 3) -> str:
    parts = max(2, min(parts, 4))
    nums = [str(random.randint(0, 50)) for _ in range(parts)]
    return ".".join(nums)
