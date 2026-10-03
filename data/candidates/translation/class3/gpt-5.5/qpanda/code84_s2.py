# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3.core as pq

def controlled_custom_unitary_circuit():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(2)
    elif hasattr(machine, "allocate_qubits"):
        qubits = machine.allocate_qubits(2)
    else:
        qubits = [machine.qAlloc(), machine.qAlloc()]

    qc = pq.QCircuit()
    gate = pq.U3(qubits[1], 0.3, 0.2, 0.1)

    try:
        controlled_gate = gate.control([qubits[0]])
    except TypeError:
        controlled_gate = gate.control(qubits[0])
    except AttributeError:
        try:
            controlled_gate = gate.ctrl([qubits[0]])
        except TypeError:
            controlled_gate = gate.ctrl(qubits[0])

    try:
        updated_qc = qc << controlled_gate
        if updated_qc is not None:
            qc = updated_qc
    except Exception:
        qc.insert(controlled_gate)

    if not hasattr(controlled_custom_unitary_circuit, "_machines"):
        controlled_custom_unitary_circuit._machines = []
    controlled_custom_unitary_circuit._machines.append(machine)

    return qc
