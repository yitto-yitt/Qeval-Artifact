# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3.core as pq

def controlled_custom_unitary_circuit():
    machine = pq.CPUQVM()
    if hasattr(machine, "init"):
        machine.init()
    elif hasattr(machine, "init_qvm"):
        machine.init_qvm()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(2)
    else:
        qubits = machine.qAllocMany(2)

    prog = pq.QProg()
    custom_gate = pq.U3(qubits[1], 0.3, 0.2, 0.1)

    if hasattr(custom_gate, "control"):
        controlled_gate = custom_gate.control([qubits[0]])
        if controlled_gate is None:
            controlled_gate = custom_gate
    else:
        custom_gate.set_control([qubits[0]])
        controlled_gate = custom_gate

    prog << controlled_gate

    if not hasattr(controlled_custom_unitary_circuit, "_machines"):
        controlled_custom_unitary_circuit._machines = []
    controlled_custom_unitary_circuit._machines.append(machine)

    return prog
