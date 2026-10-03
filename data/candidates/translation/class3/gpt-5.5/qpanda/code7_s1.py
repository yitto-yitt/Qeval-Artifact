# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_parametrized_gate():
    if not hasattr(create_parametrized_gate, "_machine"):
        machine = pq.CPUQVM()
        if hasattr(machine, "init"):
            machine.init()
        elif hasattr(machine, "init_qvm"):
            machine.init_qvm()
        create_parametrized_gate._machine = machine

    machine = create_parametrized_gate._machine
    qubits = machine.qAlloc_many(1)

    theta = None
    for name in ("Parameter", "QParameter", "ParameterExpression", "QParameterExpression"):
        if hasattr(pq, name):
            try:
                theta = getattr(pq, name)("theta")
                break
            except TypeError:
                pass

    if theta is None and hasattr(pq, "var"):
        try:
            theta = pq.var(0.0, True)
        except TypeError:
            theta = pq.var(0.0)

    if theta is None:
        theta = "theta"

    circuit = pq.QCircuit()
    try:
        gate = pq.RX(qubits[0], theta)
        try:
            circuit << gate
        except TypeError:
            circuit.insert(gate)
        return circuit
    except Exception:
        if hasattr(pq, "VariationalQuantumCircuit") and hasattr(pq, "VariationalQuantumGate_RX") and hasattr(pq, "var"):
            theta_var = pq.var(0.0, True)
            vcircuit = pq.VariationalQuantumCircuit()
            vcircuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta_var))
            return vcircuit
        raise
