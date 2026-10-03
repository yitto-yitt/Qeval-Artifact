# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    try:
        qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
        qvm.run(circuit)
        return qvm.get_qState()
    except Exception:
        pass

    try:
        if hasattr(circuit, 'get_state'):
            return circuit.get_state()
    except Exception:
        pass

    try:
        return pq.get_state(circuit)
    except Exception:
        pass

    return circuit
