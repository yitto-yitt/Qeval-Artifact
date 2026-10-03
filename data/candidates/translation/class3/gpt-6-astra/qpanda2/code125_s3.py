# EVAL_META: task_id=125, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circ_to_gate(circ):
    prog = pq.QProg()
    prog << circ

    used_qubits = pq.QVec()
    try:
        result = prog.get_used_qubits(used_qubits)
    except TypeError:
        used_qubits = prog.get_used_qubits()

    ordered_qubits = sorted(
        used_qubits, key=lambda qubit: qubit.get_phy_addr()
    )

    last_error = None
    for name in ("get_matrix", "get_unitary", "get_circuit_matrix"):
        extractor = getattr(pq, name, None)
        if extractor is None:
            continue
        for source in (prog, circ):
            try:
                matrix = extractor(source)
            except TypeError as error:
                last_error = error
                continue
            coefficients = np.asarray(matrix, dtype=complex).reshape(-1).tolist()
            return pq.QOracle(ordered_qubits, coefficients)

    raise TypeError("The input must be a unitary pyQPanda circuit.") from last_error


machine.finalize()
