# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    if isinstance(circuit, pq.QCircuit):
        prog = pq.QProg()
        prog.insert(circuit)
    else:
        prog = circuit

    try:
        qubits = pq.get_all_used_qubits_to_vector(prog)
    except AttributeError:
        try:
            qubits = pq.get_all_used_qubits(prog)
        except AttributeError:
            qubits = []

    max_idx = 0
    for q in qubits:
        try:
            addr = q.get_phy_addr()
        except AttributeError:
            addr = 0
        if addr > max_idx:
            max_idx = addr

    num_qubits = max_idx + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.qAlloc_many(num_qubits)
    machine.directly_run(prog)
    state = machine.get_qstate()
    return state
