# EVAL_META: task_id=24, framework=qpanda, class=1
import pyqpanda3.core as pq


def dj_algorithm(oracle):
    wrapped = pq.QProg()
    wrapped << oracle

    n = None
    for obj in (oracle, wrapped):
        for name in ("num_qubits", "get_qubit_num", "qubit_num", "get_qubit_count"):
            value = getattr(obj, name, None)
            if value is not None:
                value = value() if callable(value) else value
                n = int(value)
                break
        if n is not None:
            break
        for name in ("qubits", "get_qubits", "get_used_qubits"):
            value = getattr(obj, name, None)
            if value is not None:
                qubits = list(value() if callable(value) else value)
                addresses = []
                for qubit in qubits:
                    if hasattr(qubit, "get_phy_addr"):
                        addresses.append(int(qubit.get_phy_addr()))
                    elif hasattr(qubit, "getPhysicalQubitPtr"):
                        addresses.append(
                            int(qubit.getPhysicalQubitPtr().getQubitAddr())
                        )
                    else:
                        addresses.append(int(qubit))
                n = max(addresses) + 1 if addresses else 0
                break
        if n is not None:
            break

    if n is None or n < 1:
        raise ValueError("The oracle must expose a nonempty qubit register.")

    prog = pq.QProg()
    prog << pq.X(n - 1)
    for qubit in range(n):
        prog << pq.H(qubit)
    prog << oracle
    for qubit in range(n):
        prog << pq.H(qubit)

    measure = getattr(pq, "measure", None)
    if measure is None:
        measure = pq.Measure
    for qubit in range(n - 1):
        prog << measure(qubit, qubit)

    qvm = pq.CPUQVM()
    qvm.run(prog, 1024)
    if n == 1:
        return {"": 1.0}

    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {
        (format(key, f"0{n - 1}b") if isinstance(key, int)
         else str(key).replace(" ", "").zfill(n - 1)): value / total
        for key, value in counts.items()
    }
