# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict

from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure


def sampler_qiskit() -> Dict[str, float]:
    circuit = QCircuit()
    circuit << H(0)
    circuit << CNOT(0, 1)
    circuit << measure(0, 0)
    circuit << measure(1, 1)

    prog = QProg()
    prog << circuit

    qvm = CPUQVM()
    shots = 8192
    obj = qvm.run(prog, shots)

    result = obj
    if result is None or not hasattr(result, "get_counts"):
        try:
            result = qvm.result()
        except Exception:
            result = obj

    counts = None
    for name in ("get_counts", "get_probabilities", "get_prob_dict"):
        if hasattr(result, name):
            counts = getattr(result, name)()
            break
    if counts is None:
        try:
            counts = qvm.result().get_counts()
        except Exception:
            counts = {}
    if counts is None:
        counts = {}

    dist: Dict[str, float] = {}
    for key, value in dict(counts).items():
        if isinstance(key, int):
            key = format(key, "02b")
        else:
            key = str(key)
        dist[key] = dist.get(key, 0.0) + float(value)

    total = float(sum(dist.values()))
    if total > 0.0:
        dist = {k: v / total for k, v in dist.items()}
    return dist
