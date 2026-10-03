# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    n_qubits = circuit.n_qubits
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(n_qubits)
    prog = pq.QProg()
    prog.insert(circuit)
    state = pq.get_qstate(prog, machine)
    pq.destroy_quantum_machine(machine)
    return state
