# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq


def rx_gate(value=None):
    program = pq.QProg()
    if value is not None:
        program << pq.RX(0, float(value))
        return program

    names = ["Parameter", "QParameter", "Param", "QParam", "Symbol"]
    names.extend(
        name
        for name in dir(pq)
        if name not in names
        and any(part in name.lower() for part in ("param", "symbol", "expression"))
    )

    for name in names:
        factory = getattr(pq, name, None)
        if not callable(factory):
            continue
        try:
            theta = factory("theta")
            gate = pq.RX(0, theta)
        except (TypeError, ValueError, RuntimeError):
            continue
        program << gate
        return program

    program << pq.RX(0, "theta")
    return program
