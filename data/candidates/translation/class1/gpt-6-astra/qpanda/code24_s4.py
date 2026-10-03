# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, measure


def dj_algorithm(oracle):
    oracle_prog = QProg()
    oracle_prog << oracle

    n = None
    for obj in (oracle, oracle_prog):
        for name in (
            "num_qubits", "qubit_num", "get_qubit_num",
            "get_qubit_count", "get_used_qubit_num",
        ):
            member = getattr(obj, name, None)
            if member is not None:
                value = member() if callable(member) else member
                try:
                    n = int(value)
                except (TypeError, ValueError):
                    continue
                break
        if n is not None:
            break

    if n is None:
        for obj in (oracle, oracle_prog):
            for name in ("qubits", "get_qubits", "get_used_qubits"):
                member = getattr(obj, name, None)
                if member is None:
                    continue
                qubits = member() if callable(member) else member
                addresses = []
                for qubit in qubits:
                    try:
                        addresses.append(int(qubit))
                        continue
                    except (TypeError, ValueError):
                        pass
                    for address_name in (
                        "get_phy_addr", "get_phy_address",
                        "getPhysicalQubitPtr", "index",
                    ):
                        address = getattr(qubit, address_name, None)
                        if address is None:
                            continue
                        address = address() if callable(address) else address
                        if hasattr(address, "getQubitAddr"):
                            address = address.getQubitAddr()
                        addresses.append(int(address))
                        break
                    else:
                        raise TypeError("Cannot determine the oracle qubit indices.")
                if addresses:
                    n = max(addresses) + 1
                    break
            if n is not None:
                break

    if n is None or n < 2:
        raise ValueError("The oracle must expose its input and output qubits.")

    prog = QProg()
    prog << X(n - 1)
    for qubit in range(n):
        prog << H(qubit)
    prog << oracle_prog
    for qubit in range(n):
        prog << H(qubit)
    for qubit in range(n - 1):
        prog << measure(qubit, qubit)

    qvm = CPUQVM()
    run_result = qvm.run(prog, 1024)
    result_member = getattr(qvm, "result", None)
    result = (
        result_member() if callable(result_member)
        else result_member if result_member is not None
        else run_result
    )
    counts = result if isinstance(result, dict) else result.get_counts()
    total = sum(counts.values())
    return {
        (format(key, f"0{n - 1}b") if isinstance(key, int) else key): value / total
        for key, value in counts.items()
    }
