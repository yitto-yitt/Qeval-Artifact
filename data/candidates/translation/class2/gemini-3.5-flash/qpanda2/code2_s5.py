# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq


def create_bell_statevector():
    # Initialize the CPU Quantum Virtual Machine
    machine = pq.CPUQVM()
    machine.init_qvm()

    # Allocate 2 qubits
    q = machine.qAlloc_many(2)

    # Create a quantum program
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])

    # Run the program
    machine.directly_run(prog)

    # Get the resulting statevector
    state = machine.get_qstate()

    return state
