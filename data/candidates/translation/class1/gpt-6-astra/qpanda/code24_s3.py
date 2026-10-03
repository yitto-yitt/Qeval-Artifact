# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, measure


def dj_algorithm(oracle):
    oracle_prog = QProg()
    oracle_prog << oracle

    n = None
    for obj in (oracle, oracle_prog):
        for name in (
            "num_qubits",
            "qubit_num",
            "get_qubit_num",
            "get_qubit_count",
            "num_qubit",
        ):
            value = getattr(obj, name, None)
            if value is not None:
                value = value() if callable(value) else value
                n = int(value)
                break
        if n is not None:
            break

    if n is None:
        for obj in (oracle, oracle_prog):
            value = getattr(obj, "get_max_qubit_index", None)
            if value is not None:
                n = int(value() if callable(value) else value) + 1
                break

    if n is None:
        for obj in (oracle, oracle_prog):
            for name in ("get_used_qubits", "get_qubits", "qubits"):
                value = getattr(obj, name, None)
                if value is None:
                    continue
                qubits = value() if callable(value) else value
                indices = []
                for qubit in qubits:
                    address = getattr(qubit, "get_phy_addr", None)
                    indices.append(int(address() if address else qubit))
                if indices:
                    n = max(indices) + 1
                    break
            if n is not None:
                break

    if n is None or n < 1:
        raise ValueError("The oracle must expose a nonempty qubit register.")

    prog = QProg()
    prog << X(n - 1)
    for qubit in range(n):
        prog << H(qubit)
    prog << oracle_prog
    for qubit in range(n):
        prog << H(qubit)

    for qubit in range(n):
        prog << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(prog, 1024)
    counts = simulator.result().get_counts()

    distribution = {}
    total = sum(counts.values())
    for outcome, count in counts.items():
        if isinstance(outcome, str):
            bits = outcome.replace(" ", "")
            if bits.startswith("0b"):
                bits = bits[2:]
            bits = bits.zfill(n)
        else:
            bits = format(int(outcome), "0{}b".format(n))
        inputs = bits[1:]
        distribution[inputs] = distribution.get(inputs, 0.0) + count / total
    return distribution
