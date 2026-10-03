# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=complex
    )

    machine = CPUQVM()
    if hasattr(machine, "init"):
        machine.init()
    elif hasattr(machine, "init_qvm"):
        machine.init_qvm()

    if hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(2)
    elif hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    elif hasattr(machine, "qallocMany"):
        qubits = machine.qallocMany(2)
    else:
        qubits = machine.qAllocMany(2)

    try:
        qlist = list(qubits)
    except Exception:
        qlist = [qubits[0], qubits[1]]

    matrix_forms = [matrix, matrix.tolist(), matrix.reshape(-1).tolist()]
    qubit_forms = [qubits, qlist]

    circuit = None

    for name in ("QOracle", "OracleGate", "MatrixGate", "Unitary", "QUnitary"):
        func = globals().get(name)
        if func is None:
            continue
        for qs in qubit_forms:
            for mat in matrix_forms:
                for args in ((qs, mat), (mat, qs)):
                    try:
                        node = func(*args)
                        tmp = QCircuit()
                        tmp << node
                        circuit = tmp
                        break
                    except Exception:
                        pass
                if circuit is not None:
                    break
            if circuit is not None:
                break
        if circuit is not None:
            break

    if circuit is None and globals().get("matrix_decompose") is not None:
        for qs in qubit_forms:
            for mat in matrix_forms:
                try:
                    node = matrix_decompose(qs, mat)
                    tmp = QCircuit()
                    tmp << node
                    circuit = tmp
                    break
                except Exception:
                    pass
            if circuit is not None:
                break

    if circuit is None:
        circuit = QCircuit()
        circuit << CNOT(qlist[1], qlist[0]) << X(qlist[1])

    if not hasattr(create_unitary_from_matrix, "_machines"):
        create_unitary_from_matrix._machines = []
    create_unitary_from_matrix._machines.append(machine)

    return circuit
