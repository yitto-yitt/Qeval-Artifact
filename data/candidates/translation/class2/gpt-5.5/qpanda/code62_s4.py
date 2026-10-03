# EVAL_META: task_id=62, framework=qpanda, class=2
import pyqpanda3.core as pq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)

    def _new_circuit(n):
        try:
            return pq.QCircuit(n)
        except Exception:
            return pq.QCircuit()

    def _append_gate(circuit, gate):
        try:
            circuit << gate
        except Exception:
            circuit.insert(gate)

    circuit = _new_circuit(num_qubits)

    try:
        for i in range(len(basis)):
            if state[i] == 1:
                _append_gate(circuit, pq.X(i))
            if basis[i] == 1:
                _append_gate(circuit, pq.H(i))
        return circuit
    except Exception:
        pass

    qvm = None
    qubits = None

    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(qvm, init_name):
                getattr(qvm, init_name)()
                break

        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
            if hasattr(qvm, alloc_name):
                qubits = getattr(qvm, alloc_name)(num_qubits)
                break

        if qubits is None:
            qubits = [qvm.qAlloc() for _ in range(num_qubits)]

        if not hasattr(bb84_senders_circuit, "_qvms"):
            bb84_senders_circuit._qvms = []
        bb84_senders_circuit._qvms.append(qvm)
    else:
        if hasattr(pq, "init") and hasattr(pq, "QMachineType"):
            pq.init(pq.QMachineType.CPU)
        if hasattr(pq, "qAlloc_many"):
            qubits = pq.qAlloc_many(num_qubits)
        elif hasattr(pq, "qAllocMany"):
            qubits = pq.qAllocMany(num_qubits)
        else:
            qubits = [pq.qAlloc() for _ in range(num_qubits)]

    circuit = _new_circuit(num_qubits)
    for i in range(len(basis)):
        if state[i] == 1:
            _append_gate(circuit, pq.X(qubits[i]))
        if basis[i] == 1:
            _append_gate(circuit, pq.H(qubits[i]))

    return circuit
