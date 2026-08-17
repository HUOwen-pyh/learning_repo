"""第 001 晚：极小蕴含逻辑的证明对象与独立检查器。

今晚不是让程序判断现实中的命题 P 是否为真，而是让它检查：

1. 一个证明对象使用了哪些假设；
2. 每一步是否符合变量规则、蕴含引入或蕴含消去；
3. 整个证明对象最终能够证明哪个命题。

学习顺序：

1. 先直接运行本文件，确认“基线测试”通过；
2. 阅读 ``infer`` 中已有的变量规则与蕴含引入规则；
3. 完成 ``infer_imp_elim`` 和 ``build_application_proof`` 两个 TODO；
4. 把 ``RUN_EXERCISE_TESTS`` 改为 True，再运行全部验收测试。
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import sys
from typing import TypeAlias

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# 第一层：命题语法
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Atom:
    """不可继续拆解的原子命题，例如 P、Q。这里不判断它在现实中是否为真。"""

    name: str


@dataclass(frozen=True)
class Imp:
    """蕴含命题 left → right。"""

    left: Proposition
    right: Proposition


Proposition: TypeAlias = Atom | Imp


# ---------------------------------------------------------------------------
# 第二层：证明对象语法
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VarProof:
    """使用上下文中的一个假设。

    index=0 表示最近引入的假设，index=1 表示再外一层的假设。
    例如上下文为 (P, P→Q) 时，0 指向 P，1 指向 P→Q。
    """

    index: int


@dataclass(frozen=True)
class ImpIntro:
    """蕴含引入：临时假设 assumption，并在该假设下检查 body。

    如果 body 在扩展后的上下文中证明 Q，那么整个节点证明
    assumption → Q。它对应函数抽象 ``lambda assumption: body``。
    """

    assumption: Proposition
    body: Proof


@dataclass(frozen=True)
class ImpElim:
    """蕴含消去（函数应用）的待实现节点。

    若 function 证明 P→Q，argument 证明 P，则整个节点证明 Q。
    """

    function: Proof
    argument: Proof


Proof: TypeAlias = VarProof | ImpIntro | ImpElim
Context: TypeAlias = tuple[Proposition, ...]


# ---------------------------------------------------------------------------
# 第三层：独立证明检查器
# ---------------------------------------------------------------------------

def infer(proof: Proof, context: Context = ()) -> Proposition:
    """根据证明树和假设上下文推导结论；不相信证明对象自报结论。

    ``context[0]`` 永远是最近引入的假设。返回值是由规则计算出来的
    命题；未绑定变量、非法应用或未知节点必须抛出异常。
    """

    # 变量规则：Γ[index] : Γ[index]
    if isinstance(proof, VarProof):
        if not 0 <= proof.index < len(context):
            raise ValueError(
                f"未绑定的证明变量：index={proof.index}, context={context!r}"
            )
        return context[proof.index]

    # 蕴含引入规则：
    #   Γ, P ⊢ body : Q
    # ------------------ →I
    #   Γ ⊢ λp.body : P→Q
    if isinstance(proof, ImpIntro):
        extended_context = (proof.assumption,) + context
        body_type = infer(proof.body, extended_context)
        return Imp(proof.assumption, body_type)

    # 蕴含消去规则交给今晚的动手函数实现。
    if isinstance(proof, ImpElim):
        return infer_imp_elim(proof, context)

    raise TypeError(f"未知证明节点：{proof!r}")


def infer_imp_elim(proof: ImpElim, context: Context) -> Proposition:
    imp_prop = infer(proof.function, context)
    imp_arg = infer(proof.argument, context)

    if not isinstance(imp_prop, Imp):
        raise TypeError(f"function需要证明Imp类型命题")

    if not imp_prop.left == imp_arg:
        raise TypeError(f"实参命题不等于蕴含左侧")

    return imp_prop.right


def proves(proof: Proof, expected: Proposition, context: Context = ()) -> bool:
    """检查 proof 推导出的结论是否恰好等于 expected。

    这个函数展示“自报结论”和“检查器推导结论”的区别：expected 只是
    待核对目标，真正的结论仍由 ``infer`` 计算。
    """

    return infer(proof, context) == expected


# ---------------------------------------------------------------------------
# 第四层：测试辅助函数
# ---------------------------------------------------------------------------

def assert_infers(proof: Proof, expected: Proposition, label: str) -> None:
    """断言某个证明对象恰好推导出 expected，并显示可读错误。"""

    actual = infer(proof)
    assert actual == expected, f"{label}: expected={expected!r}, actual={actual!r}"


def assert_raises(
    expected_error: type[BaseException],
    action: Callable[[], object],
    label: str,
) -> None:
    """断言 action 必须以指定异常失败，防止负例悄悄通过。"""

    try:
        action()
    except expected_error:
        return
    except Exception as error:
        raise AssertionError(
            f"{label}: 应抛 {expected_error.__name__}，实际抛 {type(error).__name__}"
        ) from error
    raise AssertionError(f"{label}: 非法证明被检查器接受")


# ---------------------------------------------------------------------------
# 第五层：已实现规则的基线测试——直接运行就应该全部通过
# ---------------------------------------------------------------------------

def test_baseline_rules() -> None:
    """测试变量规则、蕴含引入、伪造目标和上下文边界。"""

    p = Atom("P")
    q = Atom("Q")

    # 正例：在假设 p:P 下使用 p，再解除该假设，得到 P→P。
    identity = ImpIntro(p, VarProof(0))
    assert_infers(identity, Imp(p, p), "恒等证明 P→P")

    # 正例：两层假设中 index=1 指向较外层的 P，因此得到 P→Q→P。
    keep_first = ImpIntro(p, ImpIntro(q, VarProof(1)))
    assert_infers(keep_first, Imp(p, Imp(q, p)), "外层变量索引")

    # 反例：同一个证明对象不能通过“自报目标”冒充 P→Q。
    assert not proves(identity, Imp(p, q)), "伪造的目标命题被接受"

    # 反例：空上下文里没有第 0 个假设。
    assert_raises(
        ValueError,
        lambda: infer(VarProof(0)),
        "空上下文中的自由变量",
    )

    # 边界：只引入一个假设时，index=1 仍然越界。
    assert_raises(
        ValueError,
        lambda: infer(ImpIntro(p, VarProof(1))),
        "单假设上下文中的越界变量",
    )


# ---------------------------------------------------------------------------
# 第六层：今晚要完成的代码和验收测试
# ---------------------------------------------------------------------------

def build_application_proof(p: Proposition, q: Proposition) -> Proof:
    """TODO 2：构造 ``(P→Q)→P→Q`` 的证明对象。

    提示：

    1. 外层 ``ImpIntro`` 引入 ``f : P→Q``；
    2. 内层 ``ImpIntro`` 引入 ``p : P``；
    3. 此时 ``VarProof(0)`` 是 p，``VarProof(1)`` 是 f；
    4. 用 ``ImpElim`` 表示 ``f p``。

    完成前保留下面的 NotImplementedError；完成时返回构造好的证明树。
    """
    imp_pq = Imp(p, q)

    res = ImpIntro(imp_pq, ImpIntro(p, ImpElim(VarProof(1), VarProof(0))))

    #res = ImpIntro(imp_pq, VarProof(0))

    print(infer(res))

    return res


def test_implication_elimination_exercise() -> None:
    """完成两个 TODO 后必须通过的正例、反例和边界测试。"""

    p = Atom("P")
    q = Atom("Q")

    # 正例：f:P→Q 与 p:P 可以推出 f(p):Q。
    application_proof = build_application_proof(p, q)
    assert_infers(
        application_proof,
        Imp(Imp(p, q), Imp(p, q)),
        "(P→Q)→P→Q",
    )

    # 反例：P 不是蕴含，不能把 p 当作函数应用到 p。
    non_function = ImpIntro(p, ImpElim(VarProof(0), VarProof(0)))
    assert_raises(
        TypeError,
        lambda: infer(non_function),
        "把普通命题当作函数",
    )

    # 反例：f 需要 P，但这里给了 Q。
    wrong_argument = ImpIntro(
        Imp(p, q),
        ImpIntro(q, ImpElim(VarProof(1), VarProof(0))),
    )
    assert_raises(
        TypeError,
        lambda: infer(wrong_argument),
        "蕴含左侧与实参命题不匹配",
    )

    # 边界：即使位于 ImpElim 内部，自由变量仍须被拒绝。
    unbound_argument = ImpElim(
        ImpIntro(p, VarProof(0)),
        VarProof(0),
    )
    assert_raises(
        ValueError,
        lambda: infer(unbound_argument),
        "应用节点中的自由实参",
    )


# 完成两个 TODO 后改为 True。此时运行文件会执行全部动手验收。
RUN_EXERCISE_TESTS = True


def main() -> None:
    test_baseline_rules()
    print("基线通过：变量规则、蕴含引入和上下文边界均正确。")

    if not RUN_EXERCISE_TESTS:
        print(
            "待完成：实现 infer_imp_elim 和 build_application_proof，"
            "然后把 RUN_EXERCISE_TESTS 改为 True。"
        )
        return

    test_implication_elimination_exercise()
    print("动手验收通过：蕴含消去的正例、反例和边界测试全部通过。")


if __name__ == "__main__":
    main()
