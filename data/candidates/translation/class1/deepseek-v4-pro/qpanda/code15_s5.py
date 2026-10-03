# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as qp

def noisy_bell():
    Machine = getattr(qp, 'QuantumMachine', None)
    if Machine is None:
        Machine = getattr(qp, 'QVM')
    machine = Machine()
    if hasattr(machine, 'init'):
        machine.init()

    qbits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    Prog = getattr(qp, 'QProg', None)
    if Prog is None:
        Prog = getattr(qp, 'QCircuit')
    prog = Prog()

    H = getattr(qp, 'H')
    CNOT = getattr(qp, 'CNOT')
    Measure = getattr(qp, 'Measure')

    prog << H(qbits[0]) << CNOT(qbits[0], qbits[1])
    prog << Measure(qbits[0], cbits[0]) << Measure(qbits[1], cbits[1])

    shots = 1000
    if hasattr(machine, 'run_with_configuration'):
        counts = machine.run_with_configuration(prog, cbits, shots)
    elif hasattr(machine, 'runWithConfiguration'):
        counts = machine.runWithConfiguration(prog, cbits, shots)
    else:
        counts = machine.run(prog, shots)

    total = sum(counts.values())
    if total == 0:
        return {}
    return {bit: val / total for bit, val in counts.items()}
