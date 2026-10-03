# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubit = machine.qAlloc_many(1)[0]
    elif hasattr(machine, "qalloc_many"):
        qubit = machine.qalloc_many(1)[0]
    elif hasattr(machine, "qAlloc"):
        qubit = machine.qAlloc()
    else:
        qubit = machine.qalloc()

    if not hasattr(rx_gate, "_machines"):
        rx_gate._machines = []
    rx_gate._machines.append(machine)

    circuit = pq.QCircuit()

    if value is not None:
        circuit << pq.RX(qubit, value)
        return circuit

    theta = None
    for ctor_name in ("Parameter", "QParameter", "CircuitParameter", "ParameterExpression"):
        ctor = getattr(pq, ctor_name, None)
        if ctor is None:
            continue
        for args in (("theta",), ("theta", 0.0), (0.0, "theta")):
            try:
                theta = ctor(*args)
                break
            except TypeError:
                continue
        if theta is not None:
            break

    if theta is None:
        theta = "theta"

    try:
        circuit << pq.RX(qubit, theta)
        return circuit
    except TypeError:
        var_func = getattr(pq, "var", None)
        vqc_cls = getattr(pq, "VariationalQuantumCircuit", None)
        vrx_cls = getattr(pq, "VariationalQuantumGate_RX", None)
        if var_func is not None and vqc_cls is not None and vrx_cls is not None:
            try:
                theta_var = var_func(0.0, True)
            except TypeError:
                theta_var = var_func(0.0)
            if hasattr(theta_var, "set_name"):
                theta_var.set_name("theta")
            vqc = vqc_cls()
            vqc.insert(vrx_cls(qubit, theta_var))
            return vqc
        raise
