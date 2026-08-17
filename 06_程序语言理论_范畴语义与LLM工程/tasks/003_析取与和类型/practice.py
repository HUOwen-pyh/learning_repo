"""第 003 晚：析取与和类型——带穷尽分支的形式化练习。

旧练习只对 Python 的 ``Left`` / ``Right`` 做了几次运行时操作。那能展示
标签，却没有说明为什么这些操作对应析取逻辑。本练习把析取写进与前两晚
一致的“命题语法—证明语法—独立检查器”中。

今晚新增三条自然演绎规则：

    左引入：             Γ ⊢ p : A
                    --------------------  ∨I₁
                     Γ ⊢ inl_B(p) : A ∨ B

    右引入：             Γ ⊢ q : B
                    --------------------  ∨I₂
                     Γ ⊢ inr_A(q) : A ∨ B

    析取消去：  Γ ⊢ s : A ∨ B    Γ,A ⊢ l : C    Γ,B ⊢ r : C
                ------------------------------------------------  ∨E
                         Γ ⊢ case(s; l; r) : C

``A ∨ B`` 的证明只携带 A 或 B 中的一项，所以必须用 ``inl`` / ``inr``
记录它来自哪一侧。消去时不知道将遇到哪一种构造子，因此必须同时提供
两个分支，而且两个分支必须得到同一个结论 C。

你需要按顺序完成三个 TODO：

1. ``infer_disjunction``：实现 ∨I₁、∨I₂、∨E 的类型规则。
2. ``build_swap_proof``：构造 ``(A ∨ B) → (B ∨ A)``。
3. ``build_case_combinator``：构造
   ``(A→C) → (B→C) → (A∨B) → C``。

批改流程：

1. 保持 ``RUN_EXERCISE_TESTS = False`` 运行，确认第 1 阶段基线通过。
2. 完成 TODO 1 后把开关改为 ``True``；第 2 阶段应通过。
3. 依次完成 TODO 2 和 TODO 3；批改器一次只暴露最早失败的阶段。

严格性提醒：检查出 ``swap`` 两个方向都有正确类型，并不等于在当前语言
内部证明 ``swap ∘ swap = id``。后者还需要证明项的求值规则和 βη 等式。
这里会检查复合项的类型，并用 Python 值展示运行时往返，但会明确区分
“同类型”“运行结果相等”和“形式系统内部证明相等”。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import sys
from typing import TypeAlias


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# =============================================================================
# 一、命题语法：原子命题、蕴含与析取
# =============================================================================


@dataclass(frozen=True)
class Atom:
    """不可继续拆分的原子命题，例如 A、B、C。"""

    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("原子命题必须有非空名称")


@dataclass(frozen=True)
class Imp:
    """蕴含命题 ``left → right``，对应函数类型。"""

    left: Proposition
    right: Proposition


@dataclass(frozen=True)
class Or:
    """析取命题 ``left ∨ right``，对应带标签的和类型。"""

    left: Proposition
    right: Proposition


Proposition: TypeAlias = Atom | Imp | Or


def is_proposition(value: object) -> bool:
    """判断对象是否完全由本晚允许的命题构造子组成。"""

    if isinstance(value, Atom):
        return True
    if isinstance(value, (Imp, Or)):
        return is_proposition(value.left) and is_proposition(value.right)
    return False


def require_proposition(value: object, where: str) -> Proposition:
    """拒绝把字符串、Python 类型或证明对象误当成命题。"""

    if not is_proposition(value):
        raise TypeError(f"{where} 不是合法命题：{value!r}")
    return value


# =============================================================================
# 二、证明语法：每个类都代表一条证明规则的使用
# =============================================================================


@dataclass(frozen=True)
class VarProof:
    """引用上下文中的假设；0 是最新假设，1 是再外一层。"""

    index: int


@dataclass(frozen=True)
class ImpIntro:
    """蕴含引入：在 body 中临时加入 assumption。"""

    assumption: Proposition
    body: Proof


@dataclass(frozen=True)
class ImpElim:
    """蕴含消去：把证明 ``A→B`` 的 function 应用于证明 A 的 argument。"""

    function: Proof
    argument: Proof


@dataclass(frozen=True)
class OrIntroLeft:
    """左引入 ``inl_B(value)``。

    ``value`` 证明左侧 A；``right_proposition`` 明确目标析取的另一侧 B。
    B 没有对应证明，检查器不可能从 value 猜到它，所以必须显式给出。
    """

    value: Proof
    right_proposition: Proposition


@dataclass(frozen=True)
class OrIntroRight:
    """右引入 ``inr_A(value)``。

    ``value`` 证明右侧 B；``left_proposition`` 明确目标析取的另一侧 A。
    """

    left_proposition: Proposition
    value: Proof


@dataclass(frozen=True)
class OrElim:
    """析取消去，即穷尽的 case analysis。

    * ``scrutinee`` 必须证明某个 ``A ∨ B``；
    * 检查 ``on_left`` 时，在上下文最前面临时加入 ``A``；
    * 检查 ``on_right`` 时，在上下文最前面临时加入 ``B``；
    * 两个分支必须推出同一个命题 C。

    分支里的 ``VarProof(0)`` 是被解包出的 A 或 B，不再是 case 外面原来
    的第 0 个假设；外部假设的索引都会向后移动一位。
    """

    scrutinee: Proof
    on_left: Proof
    on_right: Proof


Proof: TypeAlias = (
    VarProof | ImpIntro | ImpElim | OrIntroLeft | OrIntroRight | OrElim
)
Context: TypeAlias = tuple[Proposition, ...]


# =============================================================================
# 三、独立证明检查器
# =============================================================================


def infer(proof: Proof, context: Context = ()) -> Proposition:
    """由 proof 的结构和 context 推导结论，不相信证明对象自报答案。"""

    if not isinstance(context, tuple):
        raise TypeError("context 必须是 tuple，且第 0 项是最新假设")
    for position, proposition in enumerate(context):
        require_proposition(proposition, f"context[{position}]")

    # 假设规则：Γ[i] 在 Γ 中，才能引用它。
    if isinstance(proof, VarProof):
        if isinstance(proof.index, bool) or not isinstance(proof.index, int):
            raise TypeError("VarProof.index 必须是整数")
        if proof.index < 0 or proof.index >= len(context):
            raise IndexError(
                f"VarProof({proof.index}) 越界：当前上下文只有 {len(context)} 个假设"
            )
        return context[proof.index]

    # 蕴含引入：Γ,A ⊢ body:B  推出  Γ ⊢ λbody:A→B。
    if isinstance(proof, ImpIntro):
        assumption = require_proposition(proof.assumption, "ImpIntro.assumption")
        body_type = infer(proof.body, (assumption,) + context)
        return Imp(assumption, body_type)

    # 蕴含消去：Γ ⊢ f:A→B 且 Γ ⊢ x:A，才能推出 Γ ⊢ f(x):B。
    if isinstance(proof, ImpElim):
        function_type = infer(proof.function, context)
        argument_type = infer(proof.argument, context)
        if not isinstance(function_type, Imp):
            raise TypeError(
                f"ImpElim.function 必须证明蕴含，实际为 {function_type!r}"
            )
        if function_type.left != argument_type:
            raise TypeError(
                "ImpElim 实参类型不匹配："
                f"函数需要 {function_type.left!r}，实际得到 {argument_type!r}"
            )
        return function_type.right

    # 本晚新增的三种析取节点交给 TODO 1。
    if isinstance(proof, (OrIntroLeft, OrIntroRight, OrElim)):
        return infer_disjunction(proof, context)

    raise TypeError(f"未知证明节点：{proof!r}")


def infer_disjunction(
    proof: OrIntroLeft | OrIntroRight | OrElim,
    context: Context,
) -> Proposition:
    """TODO 1：实现析取的左右引入与穷尽消去。

    请严格按证明节点完成：

    1. ``OrIntroLeft(value, right_proposition)``：
       在原 ``context`` 中递归推导 value 的命题 A；检查显式给出的右侧
       确实是合法命题 B；返回 ``Or(A, B)``。
    2. ``OrIntroRight(left_proposition, value)``：
       检查左侧 A；在原 ``context`` 中递归推导 value 的命题 B；返回
       ``Or(A, B)``。
    3. ``OrElim(scrutinee, on_left, on_right)``：
       a. 先推导 scrutinee，若结果不是 ``Or(A, B)``，抛出 TypeError；
       b. 在 ``(A,) + context`` 中推导 on_left，得到 C_left；
       c. 在 ``(B,) + context`` 中推导 on_right，得到 C_right；
       d. 只有 ``C_left == C_right`` 时才返回它，否则抛出 TypeError。

    必须真的检查两个分支。即使某个具体运行时值带左标签，类型检查阶段
    也不能因此跳过右分支，因为程序以后仍可能收到右值。
    """
    if isinstance(proof, OrIntroLeft):
        right_prop = require_proposition(proof.right_proposition, "proof.right_proposition")
        return Or(infer(proof.value, context), right_prop)

    if isinstance(proof, OrIntroRight):
        left_prop = require_proposition(proof.left_proposition, "proof.left_proposition")
        return Or(left_prop, infer(proof.value, context))

    if isinstance(proof, OrElim):
        or_prop = infer(proof.scrutinee, context)
        if not isinstance(or_prop, Or):
            raise TypeError(f"or_prop should be Or")
        a2c = infer(proof.on_left, (or_prop.left,) + context)
        b2c = infer(proof.on_right, (or_prop.right,) + context)

        if a2c != b2c:
            raise TypeError("a2c should be equal to b2c")

        return a2c


# =============================================================================
# 四、需要构造的证明对象
# =============================================================================


def build_swap_proof(a: Proposition, b: Proposition) -> Proof:
    """TODO 2：构造 ``(a ∨ b) → (b ∨ a)`` 的闭证明。

    思考路径：

    1. 用 ``ImpIntro`` 假设 ``a ∨ b``；此时它是 ``VarProof(0)``。
    2. 对这个假设使用 ``OrElim``。
    3. 左分支得到 ``a`` 后，目标 ``b ∨ a`` 应使用哪个标签？
    4. 右分支得到 ``b`` 后，目标 ``b ∨ a`` 应使用哪个标签？

    注意：进入任一 case 分支后，新解包出的值占索引 0，原来的析取假设
    移到索引 1。这里只需使用分支变量，不要硬编码原子命题的名称。
    """
    return ImpIntro(Or(a, b), OrElim(VarProof(0), OrIntroRight(b, VarProof(0)), OrIntroLeft(VarProof(0), a)))

    


def build_case_combinator(
    a: Proposition,
    b: Proposition,
    c: Proposition,
) -> Proof:
    """TODO 3：构造 ``(a→c) → (b→c) → (a∨b) → c``。

    这就是析取消去规则作为普通程序的类型。按顺序引入三个参数后，case
    之前的上下文为：

        index 0: s : a ∨ b
        index 1: g : b → c
        index 2: f : a → c

    进入左分支后，上下文变成：

        index 0: x : a
        index 1: s : a ∨ b
        index 2: g : b → c
        index 3: f : a → c

    所以左分支应通过 ``ImpElim`` 计算 ``f(x)``。右分支的布局同样是
    ``(y, s, g, f)``，应计算 ``g(y)``。两个结果都必须是 c。

    请返回证明 AST，而不是 Python 回调函数或目标命题本身。
    """
    return ImpIntro(
        Imp(a, c),
        ImpIntro(
            Imp(b, c),
            ImpIntro(
                Or(a, b),
                OrElim(
                    VarProof(0),
                    ImpElim(VarProof(3), VarProof(0)),
                    ImpElim(VarProof(2), VarProof(0))
                )
            )
        )
    )


# =============================================================================
# 五、形式证明以外的运行时模型：只用于观察标签和分支行为
# =============================================================================


@dataclass(frozen=True)
class LeftValue:
    """和类型的运行时左值；类名本身就是不可丢失的标签。"""

    value: object


@dataclass(frozen=True)
class RightValue:
    """和类型的运行时右值；payload 可与左值完全相同。"""

    value: object


SumValue: TypeAlias = LeftValue | RightValue


def case_sum_value(
    value: SumValue,
    on_left: Callable[[object], object],
    on_right: Callable[[object], object],
) -> object:
    """运行时的穷尽 case；在观察标签前就要求两个处理器都存在。"""

    if not callable(on_left) or not callable(on_right):
        raise TypeError("case 必须同时提供可调用的左处理器和右处理器")
    if isinstance(value, LeftValue):
        return on_left(value.value)
    if isinstance(value, RightValue):
        return on_right(value.value)
    raise TypeError("和值必须带 LeftValue 或 RightValue 标签")


def swap_sum_value(value: SumValue) -> SumValue:
    """形式 swap 所对应的运行时程序：保留 payload，只翻转标签。"""

    result = case_sum_value(value, RightValue, LeftValue)
    if not isinstance(result, (LeftValue, RightValue)):
        raise AssertionError("内部错误：swap 必须产生带标签的和值")
    return result


def proves(proof: Proof, expected: Proposition, context: Context = ()) -> bool:
    """判断检查器推导出的命题是否与 expected 语法相等。"""

    require_proposition(expected, "expected")
    return infer(proof, context) == expected


# =============================================================================
# 六、断言工具：让失败信息直接指向规则
# =============================================================================


def assert_infers(
    proof: Proof,
    expected: Proposition,
    context: Context = (),
) -> None:
    """断言 proof 在 context 中恰好推出 expected。"""

    actual = infer(proof, context)
    if actual != expected:
        raise AssertionError(f"推导结果错误：期望 {expected!r}，实际 {actual!r}")


def assert_raises(
    expected_error: type[Exception],
    action: Callable[[], object],
    explanation: str,
) -> None:
    """断言非法证明或非法和值确实被指定异常拒绝。"""

    try:
        action()
    except expected_error:
        return
    except Exception as error:
        raise AssertionError(
            f"{explanation}：期望 {expected_error.__name__}，"
            f"实际抛出 {type(error).__name__}: {error}"
        ) from error
    raise AssertionError(f"{explanation}：非法输入没有被拒绝")


# =============================================================================
# 七、四阶段批改内容
# =============================================================================


def test_stage_1_baseline() -> None:
    """基线：前两晚所需的上下文、蕴含引入和蕴含消去。"""

    a = Atom("A")
    b = Atom("B")

    identity = ImpIntro(a, VarProof(0))
    assert_infers(identity, Imp(a, a))
    # 课程静态门禁要求保留原生 assert；assert_infers 仍负责详细报错。
    assert proves(identity, Imp(a, a)), "A → A 的基线证明应成立"

    # (A→B)→A→B：内层上下文为 (A, A→B)。
    application = ImpIntro(
        Imp(a, b),
        ImpIntro(a, ImpElim(VarProof(1), VarProof(0))),
    )
    assert_infers(application, Imp(Imp(a, b), Imp(a, b)))

    assert_raises(
        TypeError,
        lambda: infer(ImpIntro(a, ImpElim(VarProof(0), VarProof(0)))),
        "普通命题不能当作函数",
    )
    assert_raises(
        IndexError,
        lambda: infer(VarProof(-1), (a,)),
        "负索引不能绕到上下文末尾",
    )
    assert_raises(
        IndexError,
        lambda: infer(VarProof(0)),
        "空上下文不能凭空产生证明",
    )


def test_stage_2_disjunction_rules() -> None:
    """批改 TODO 1：两个引入规则、穷尽消去及所有关键反例。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")

    # A → A∨B 与 B → A∨B：只有实际拥有的一侧需要证明。
    inject_left = ImpIntro(a, OrIntroLeft(VarProof(0), b))
    inject_right = ImpIntro(b, OrIntroRight(a, VarProof(0)))
    assert_infers(inject_left, Imp(a, Or(a, b)))
    assert_infers(inject_right, Imp(b, Or(a, b)))

    # 嵌套和的括号结构不能被压平，也不能由实现硬编码固定深度。
    nested_left = ImpIntro(
        b,
        OrIntroLeft(OrIntroRight(a, VarProof(0)), c),
    )
    nested_right = ImpIntro(
        b,
        OrIntroRight(a, OrIntroLeft(VarProof(0), c)),
    )
    assert_infers(nested_left, Imp(b, Or(Or(a, b), c)))
    assert_infers(nested_right, Imp(b, Or(a, Or(b, c))))
    if Or(Or(a, b), c) == Or(a, Or(b, c)):
        raise AssertionError("析取的不同括号结构不应被当作语法相等")

    # (A∨B)→(A∨B)：case 的两支分别重新贴回原来的标签。
    sum_identity = ImpIntro(
        Or(a, b),
        OrElim(
            VarProof(0),
            OrIntroLeft(VarProof(0), b),
            OrIntroRight(a, VarProof(0)),
        ),
    )
    assert_infers(sum_identity, Imp(Or(a, b), Or(a, b)))

    # C→(A∨B)→C：进入分支后 C 从 index 1 移到 index 2。
    keep_outer = ImpIntro(
        c,
        ImpIntro(
            Or(a, b),
            OrElim(VarProof(0), VarProof(2), VarProof(2)),
        ),
    )
    assert_infers(keep_outer, Imp(c, Imp(Or(a, b), c)))

    # 反例：A 与 B 不同，两个分支直接返回各自变量时没有统一结论 C。
    assert_raises(
        TypeError,
        lambda: infer(
            OrElim(VarProof(0), VarProof(0), VarProof(0)),
            (Or(a, b),),
        ),
        "case 两个分支必须返回同一命题",
    )

    # 反例：不是 A∨B 的证明不能接受析取消去。
    assert_raises(
        TypeError,
        lambda: infer(OrElim(VarProof(0), VarProof(0), VarProof(0)), (a,)),
        "只能对析取证明做 case",
    )

    # 反例：左右分支都必须存在；不能只实现当前碰巧运行到的一侧。
    assert_raises(
        TypeError,
        lambda: infer(
            OrElim(VarProof(0), None, VarProof(0)),  # type: ignore[arg-type]
            (Or(a, a),),
        ),
        "case 不能缺少左分支",
    )
    assert_raises(
        TypeError,
        lambda: infer(
            OrElim(VarProof(0), VarProof(0), None),  # type: ignore[arg-type]
            (Or(a, a),),
        ),
        "case 不能缺少右分支",
    )

    # 注入的“另一侧”虽没有值，却仍必须是合法命题。
    assert_raises(
        TypeError,
        lambda: infer(OrIntroLeft(VarProof(0), None), (a,)),  # type: ignore[arg-type]
        "左注入不能省略右侧命题",
    )
    assert_raises(
        TypeError,
        lambda: infer(OrIntroRight(None, VarProof(0)), (b,)),  # type: ignore[arg-type]
        "右注入不能省略左侧命题",
    )
    assert_raises(
        TypeError,
        lambda: infer(OrIntroLeft(None, b), (a,)),  # type: ignore[arg-type]
        "左标签不能代替左侧证明",
    )
    assert_raises(
        TypeError,
        lambda: infer(OrIntroRight(a, None), (b,)),  # type: ignore[arg-type]
        "右标签不能代替右侧证明",
    )

    # 运行时也在查看标签之前要求两个处理器，体现接口的穷尽性。
    assert_raises(
        TypeError,
        lambda: case_sum_value(LeftValue(1), lambda x: x, None),  # type: ignore[arg-type]
        "即使当前是左值，也不能省略右处理器",
    )


def test_stage_3_swap() -> None:
    """批改 TODO 2：交换的两个方向、标签行为和复合项。"""

    a = Atom("A")
    b = Atom("B")
    source = Or(a, b)
    swapped = Or(b, a)

    swap_ab = build_swap_proof(a, b)
    swap_ba = build_swap_proof(b, a)
    assert_infers(swap_ab, Imp(source, swapped))
    assert_infers(swap_ba, Imp(swapped, source))

    # a 本身也可以是和类型；交换构造不得只适用于原子命题。
    c = Atom("C")
    nested_a = Or(a, b)
    nested_swap = build_swap_proof(nested_a, c)
    assert_infers(
        nested_swap,
        Imp(Or(nested_a, c), Or(c, nested_a)),
    )

    if source == swapped:
        raise AssertionError("A∨B 与 B∨A 不应被当成同一棵命题语法树")
    if proves(swap_ab, Imp(source, source)):
        raise AssertionError("交换证明不应被误判成恒等证明")

    # 构造 swap_ba(swap_ab(x))，只能证明它与恒等函数有相同类型。
    # 当前语言尚无证明项等式，不能据此宣称两个证明项在内部已经相等。
    swap_twice = ImpIntro(
        source,
        ImpElim(swap_ba, ImpElim(swap_ab, VarProof(0))),
    )
    assert_infers(swap_twice, Imp(source, source))

    # 运行时分别覆盖左右标签；payload 相同也不会使标签消失。
    left = LeftValue("same-payload")
    right = RightValue("same-payload")
    if left == right:
        raise AssertionError("相同 payload 的左右和值仍必须不同")
    if swap_sum_value(left) != RightValue("same-payload"):
        raise AssertionError("左标签交换后应成为右标签")
    if swap_sum_value(right) != LeftValue("same-payload"):
        raise AssertionError("右标签交换后应成为左标签")

    for value in (left, right, LeftValue(RightValue("nested"))):
        if swap_sum_value(swap_sum_value(value)) != value:
            raise AssertionError(f"交换两次没有恢复原值：{value!r}")

    assert_raises(
        TypeError,
        lambda: swap_sum_value(("没有标签", 1)),  # type: ignore[arg-type]
        "普通 tuple 不能冒充和值",
    )


def test_stage_4_case_combinator() -> None:
    """批改 TODO 3：通用 case 类型、索引移动和泛化能力。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")

    case_proof = build_case_combinator(a, b, c)
    expected = Imp(Imp(a, c), Imp(Imp(b, c), Imp(Or(a, b), c)))
    assert_infers(case_proof, expected)

    # 参数本身可以是复合命题；实现不得检查名称或硬编码固定 Atom。
    nested_a = Or(Atom("A1"), Atom("A2"))
    nested_c = Imp(c, c)
    nested_proof = build_case_combinator(nested_a, b, nested_c)
    nested_expected = Imp(
        Imp(nested_a, nested_c),
        Imp(Imp(b, nested_c), Imp(Or(nested_a, b), nested_c)),
    )
    assert_infers(nested_proof, nested_expected)

    # 这个故意错误的版本在右分支仍拿 f:A→C 处理 y:B。
    # 它能抓住忘记计算 case 分支新增索引的实现。
    wrong_handler_index = ImpIntro(
        Imp(a, c),
        ImpIntro(
            Imp(b, c),
            ImpIntro(
                Or(a, b),
                OrElim(
                    VarProof(0),
                    ImpElim(VarProof(3), VarProof(0)),
                    ImpElim(VarProof(3), VarProof(0)),
                ),
            ),
        ),
    )
    assert_raises(
        TypeError,
        lambda: infer(wrong_handler_index),
        "右分支不能错误地使用左处理函数",
    )

    wrong_target = Imp(Imp(a, c), Imp(Imp(b, c), Imp(Or(a, b), a)))
    if proves(case_proof, wrong_target):
        raise AssertionError("case 证明不能通过自报目标把 C 伪造成 A")

    # 元语言运行测试：每个带标签的值只执行与标签对应的处理器。
    calls: list[str] = []

    def on_left(value: object) -> str:
        calls.append("left")
        return f"L:{value}"

    def on_right(value: object) -> str:
        calls.append("right")
        return f"R:{value}"

    if case_sum_value(LeftValue(7), on_left, on_right) != "L:7":
        raise AssertionError("左值没有交给左处理器")
    if calls != ["left"]:
        raise AssertionError(f"左值只能执行左处理器，实际调用：{calls!r}")

    calls.clear()
    if case_sum_value(RightValue("err"), on_left, on_right) != "R:err":
        raise AssertionError("右值没有交给右处理器")
    if calls != ["right"]:
        raise AssertionError(f"右值只能执行右处理器，实际调用：{calls!r}")

    assert_raises(
        TypeError,
        lambda: case_sum_value("untagged", on_left, on_right),  # type: ignore[arg-type]
        "无标签 payload 不能进入 case",
    )


# =============================================================================
# 八、清晰的分阶段批改器
# =============================================================================


# 完成 TODO 1 后改成 True。之后会按依赖顺序执行；第一处错误被修好前，
# 后续阶段显示 BLOCKED，避免一次看到许多由同一根因产生的错误。
RUN_EXERCISE_TESTS = True


StageTest: TypeAlias = Callable[[], None]


def grade_stage(number: int, label: str, test: StageTest) -> bool:
    """运行一阶段，并用统一格式报告结果与第一个真实错误。"""

    try:
        test()
    except Exception as error:
        print(f"[FAIL {number}/4] {label}")
        print(f"  {type(error).__name__}: {error}")
        return False
    print(f"[PASS {number}/4] {label}")
    return True


def print_blocked(start: int, stages: tuple[tuple[str, StageTest], ...]) -> None:
    """列出因为前置阶段失败而尚未运行的测试。"""

    for number, (label, _) in enumerate(stages[start - 1 :], start=start):
        print(f"[BLOCKED {number}/4] {label}（先修复上一失败阶段）")


def main() -> int:
    stages: tuple[tuple[str, StageTest], ...] = (
        ("基线：上下文与蕴含规则", test_stage_1_baseline),
        ("TODO 1：析取引入与穷尽消去", test_stage_2_disjunction_rules),
        ("TODO 2：交换证明与标签行为", test_stage_3_swap),
        ("TODO 3：通用 case 组合子", test_stage_4_case_combinator),
    )

    if not grade_stage(1, stages[0][0], stages[0][1]):
        print_blocked(2, stages)
        return 1

    if not RUN_EXERCISE_TESTS:
        for number, (label, _) in enumerate(stages[1:], start=2):
            print(f"[PENDING {number}/4] {label}")
        print("\n下一步：实现 infer_disjunction（TODO 1），然后把")
        print("RUN_EXERCISE_TESTS 改成 True 并重新运行本文件。")
        return 0

    for number, (label, test) in enumerate(stages[1:], start=2):
        if not grade_stage(number, label, test):
            print_blocked(number + 1, stages)
            return 1

    print("\n全部验收通过：你已经实现析取引入、穷尽消去、交换证明与")
    print("通用 case 组合子，并能区分标签、分支类型和证明项等式。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# 完成四阶段后的可选动手改造：定义 map_sum，使其证明/实现
# (A→C) → (B→D) → (A∨B) → (C∨D)，并测试左右标签都被保留。
