# EVAL_META: task_id=24, framework=qpanda, class=1
from collections.abc import Mapping
from pyqpanda3 import core as pq


def dj_algorithm(oracle):
    n = None
    for name in ("num_qubits", "qubit_num", "get_qubit_num", "get_qubit_count"):
        member = getattr(oracle, name, None)
        if member is not None:
            value = member() if callable(member) else member
            try:
                n = int(value)
                break
            except (TypeError, ValueError):
                pass

    if n is None:
        for name in ("get_used_qubits", "get_qubits", "qubits"):
            member = getattr(oracle, name, None)
            if member is None:
                continue
            qubits = member() if callable(member) else member
            indices = []
            for qubit in qubits:
                try:
                    indices.append(int(qubit))
                except (TypeError, ValueError):
                    indices.append(int(qubit.get_phy_addr()))
            if indices:
                n = max(indices) + 1
                break

    if n is None or n < 1:
        raise ValueError("The oracle must expose its qubit register.")

    program = pq.QProg()
    program << pq.X(n - 1)
    for qubit in range(n):
        program << pq.H(qubit)
    program << oracle
    for qubit in range(n):
        program << pq.H(qubit)

    measure = getattr(pq, "measure", None)
    if measure is None:
        measure = pq.Measure
    for qubit in range(n - 1):
        program << measure(qubit, qubit)

    simulator = pq.CPUQVM()
    result = simulator.run(program, 1024)

    if n == 1:
        return {"": 1.0}

    if result is None or (
        not isinstance(result, Mapping) and not hasattr(result, "get_counts")
    ):
        result = simulator.result()

    counts = result if isinstance(result, Mapping) else result.get_counts()
    total = sum(counts.values())
    probabilities = {}
    for key, count in counts.items():
        if isinstance(key, str):
            key = key.replace(" ", "")
            if key.startswith(("0x", "0X")):
                key = format(int(key, 16), f"0{n - 1}b")
            elif key.startswith(("0b", "0B")):
                key = key[2:].zfill(n - 1)
            else:
                key = key.zfill(n - 1)
        else:
            key = format(int(key), f"0{n - 1}b")
        probabilities[key] = probabilities.get(key, 0.0) + count / total
    return probabilities
