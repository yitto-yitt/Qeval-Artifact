# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, H, X, measure


def dj_algorithm(oracle):
    n = None
    for name in ("num_qubits", "get_qubit_num", "qubit_num"):
        attribute = getattr(oracle, name, None)
        if attribute is not None:
            n = int(attribute() if callable(attribute) else attribute)
            break

    if n is None:
        for name in ("get_used_qubits", "get_qubits", "qubits"):
            attribute = getattr(oracle, name, None)
            if attribute is None:
                continue
            qubits = attribute() if callable(attribute) else attribute
            indices = []
            for qubit in qubits:
                if hasattr(qubit, "get_phy_addr"):
                    indices.append(int(qubit.get_phy_addr()))
                elif hasattr(qubit, "get_phy_address"):
                    indices.append(int(qubit.get_phy_address()))
                else:
                    indices.append(int(qubit))
            n = max(indices) + 1
            break

    if n is None:
        raise TypeError("Cannot determine the oracle's qubit count.")
    if n < 2:
        raise ValueError("The oracle must include an input and an output qubit.")

    program = QProg()
    program << X(n - 1)
    for qubit in range(n):
        program << H(qubit)
    program << oracle
    for qubit in range(n):
        program << H(qubit)
    for qubit in range(n - 1):
        program << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(program, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
