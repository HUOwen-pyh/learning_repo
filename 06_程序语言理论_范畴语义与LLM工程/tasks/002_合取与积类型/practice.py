"""第 002 晚：合取与积类型——可分阶段批改的形式化练习。

这份练习不是让你“操作几个 Python 元组”就结束，而是让你亲手实现三条
自然演绎规则，并看见它们如何对应积类型的构造与解构：

    合取引入：  Γ ⊢ p : A      Γ ⊢ q : B
                ---------------------------  ∧I
                     Γ ⊢ (p, q) : A ∧ B

    左投影：          Γ ⊢ r : A ∧ B
                     ----------------  ∧E₁
                         Γ ⊢ π₁ r : A

    右投影：          Γ ⊢ r : A ∧ B
                     ----------------  ∧E₂
                         Γ ⊢ π₂ r : B

这里：

* ``A``、``B`` 是命题；按 Curry–Howard 对应，它们也是类型。
* ``p``、``q``、``r`` 是证明；按 Curry–Howard 对应，它们也是程序。
* ``Γ`` 是当前可用假设组成的上下文。
* ``A ∧ B`` 对应积类型；它的值同时保存一个 ``A`` 和一个 ``B``。

你要完成的内容只有三个 TODO，并按以下顺序完成：

1. ``infer_conjunction``：实现 ∧I、∧E₁、∧E₂ 三条推导规则。
2. ``build_swap_proof``：构造 ``(A ∧ B) → (B ∧ A)`` 的证明对象。
3. ``build_associativity_proofs``：构造合取结合律两个方向的证明对象。

严格性提醒：当前小语言只检查“某个证明项具有某个命题”，还没有定义
证明项的归约与 βη 等式。因此两个方向都可证明，只建立了双向可推导；
若要在语言内部正式称为同构，还须证明两个方向的复合分别等于恒等项。
后面的 Python tuple 往返测试只展示这一等式的计算直觉，不冒充内部证明。

批改方法：

1. 第一次运行时保留 ``RUN_EXERCISE_TESTS = False``，先确认基线为 PASS。
2. 完成 TODO 1 后，把开关改成 ``True``，应通过第 2 阶段。
3. 再完成 TODO 2；批改才会进入并通过第 3 阶段。
4. 最后完成 TODO 3；四阶段全 PASS 才算完成今晚练习。

每一阶段的测试既有正例，也有反例和边界例。请不要删除测试来制造 PASS；
真正的目标是让同一个 ``infer`` 能检查所有给定证明树。
"""

from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import Callable, TypeAlias


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# =============================================================================
# 一、命题语法：我们究竟允许谈论哪些命题？
# =============================================================================


@dataclass(frozen=True)
class Atom:
    """原子命题，例如 P、Q；本练习不分析它的内部结构。"""

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
class And:
    """合取命题 ``left ∧ right``，对应积类型。左右位置有意义。"""

    left: Proposition
    right: Proposition


Proposition: TypeAlias = Atom | Imp | And


def is_proposition(value: object) -> bool:
    """运行时检查一个值是否真由本练习的命题语法构成。"""

    if isinstance(value, Atom):
        return True
    if isinstance(value, (Imp, And)):
        return is_proposition(value.left) and is_proposition(value.right)
    return False


def require_proposition(value: object, where: str) -> Proposition:
    """拒绝把字符串、Python 类型或证明对象误当成命题。"""

    if not is_proposition(value):
        raise TypeError(f"{where} 不是合法命题：{value!r}")
    return value


# =============================================================================
# 二、证明语法：一棵证明树允许使用哪些构造？
# =============================================================================


@dataclass(frozen=True)
class VarProof:
    """使用上下文中的一个假设。

    使用 de Bruijn 索引：0 指最新引入的假设，1 指再外一层，依此类推。
    它不是在“证明任意命题”；它只是在引用当前确实可用的假设。
    """

    index: int


@dataclass(frozen=True)
class ImpIntro:
    """蕴含引入。

    若在额外假设 A 下，body 能推出 B，那么退出这个局部假设后，整棵
    证明树得到 A → B。这里的 assumption 是 A，body 是局部推导。
    """

    assumption: Proposition
    body: Proof


@dataclass(frozen=True)
class AndIntro:
    """合取引入 ∧I：把 A 的证明和 B 的证明配成 A ∧ B 的证明。"""

    left: Proof
    right: Proof


@dataclass(frozen=True)
class AndElimLeft:
    """合取消去 ∧E₁：从 A ∧ B 的证明中取出 A 的证明。"""

    pair: Proof


@dataclass(frozen=True)
class AndElimRight:
    """合取消去 ∧E₂：从 A ∧ B 的证明中取出 B 的证明。"""

    pair: Proof


Proof: TypeAlias = VarProof | ImpIntro | AndIntro | AndElimLeft | AndElimRight
Context: TypeAlias = tuple[Proposition, ...]


# =============================================================================
# 三、推导器：给定 Γ 和 proof，计算 Γ ⊢ proof : ? 中的命题
# =============================================================================


def infer(proof: Proof, context: Context = ()) -> Proposition:
    """按照证明树的最后一条规则推导其命题。

    返回值不是“这个证明是否看起来合理”，而是该证明在 ``context`` 下
    唯一能得到的命题。证明节点与规则不匹配时必须拒绝，不能猜测。
    """

    if not isinstance(context, tuple):
        raise TypeError("context 必须是 tuple，且第 0 项是最新假设")
    for position, proposition in enumerate(context):
        require_proposition(proposition, f"context[{position}]")

    # 假设规则：若第 i 项确实在 Γ 中，就可以使用它。
    if isinstance(proof, VarProof):
        if isinstance(proof.index, bool) or not isinstance(proof.index, int):
            raise TypeError("VarProof.index 必须是整数")
        if proof.index < 0 or proof.index >= len(context):
            raise IndexError(
                f"VarProof({proof.index}) 越界：当前上下文只有 {len(context)} 个假设"
            )
        return context[proof.index]

    # 蕴含引入：Γ, A ⊢ body : B  推出  Γ ⊢ λbody : A → B。
    if isinstance(proof, ImpIntro):
        assumption = require_proposition(proof.assumption, "ImpIntro.assumption")
        body_type = infer(proof.body, (assumption,) + context)
        return Imp(assumption, body_type)

    # 第 002 晚新增的三个证明节点由你在 TODO 1 中解释。
    if isinstance(proof, (AndIntro, AndElimLeft, AndElimRight)):
        return infer_conjunction(proof, context)

    raise TypeError(f"未知证明节点：{proof!r}")


def infer_conjunction(
    proof: AndIntro | AndElimLeft | AndElimRight,
    context: Context,
) -> Proposition:
    """TODO 1：实现合取引入和两条投影规则。

    请严格按节点种类完成以下逻辑：

    1. 若 ``proof`` 是 ``AndIntro(left, right)``：
       分别递归调用 ``infer`` 得到左右证明的命题 A、B，然后返回
       ``And(A, B)``。两个子证明都必须在同一个 ``context`` 中检查。
    2. 若 ``proof`` 是 ``AndElimLeft(pair)``：
       先递归推导 ``pair`` 的命题；只有结果确实是 ``And(A, B)`` 时，
       才能返回 A，否则抛出 ``TypeError``。
    3. ``AndElimRight`` 同理，但返回 B。

    不要根据变量名、原子命题名称或预期答案硬编码结果。推导只能查看
    ``proof`` 的结构和 ``context``。
    """
    if isinstance(proof, AndIntro):
        a, b = infer(proof.left, context), infer(proof.right, context)
        return And(a, b)

    if isinstance(proof, AndElimLeft | AndElimRight):
        a = infer(proof.pair, context)
        if not isinstance(a, And):
            raise TypeError(f"AndElimLeft需证明And命题")
        return a.left if isinstance(proof, AndElimLeft) else a.right

# =============================================================================
# 四、你要构造的证明对象
# =============================================================================


def build_swap_proof(a: Proposition, b: Proposition) -> Proof:
    """TODO 2：返回 ``(a ∧ b) → (b ∧ a)`` 的闭证明。

    只需要一层 ``ImpIntro``：进入函数体后，``VarProof(0)`` 就是新假设
    ``a ∧ b``。为了构造 ``b ∧ a``：

    * 新积的左边应由原积的哪一个投影得到？
    * 新积的右边应由原积的哪一个投影得到？

    请返回证明 AST，不要返回 Python 函数，也不要直接返回命题。
    """

    require_proposition(a, "build_swap_proof.a")
    require_proposition(b, "build_swap_proof.b")

    return ImpIntro(And(a, b), AndIntro(AndElimRight(VarProof(0)), AndElimLeft(VarProof(0))))


def build_associativity_proofs(
    a: Proposition,
    b: Proposition,
    c: Proposition,
) -> tuple[Proof, Proof]:
    """TODO 3：返回合取结合律正向和反向的两棵闭证明树。

    返回 ``(forward, backward)``，其中：

    * ``forward`` 证明 ``((a ∧ b) ∧ c) → (a ∧ (b ∧ c))``；
    * ``backward`` 证明 ``(a ∧ (b ∧ c)) → ((a ∧ b) ∧ c)``。

    画投影路径会比盯着代码容易：

    forward 的输入 x : ((a ∧ b) ∧ c)
      a = π₁(π₁ x)，b = π₂(π₁ x)，c = π₂ x

    backward 的输入 y : (a ∧ (b ∧ c))
      a = π₁ y，b = π₁(π₂ y)，c = π₂(π₂ y)

    用这些叶子重新调用 ``AndIntro`` 组装目标形状。不要把 ``And`` 当成
    自动满足结合律的集合运算：两个括号结构是不同的语法树。
    """

    require_proposition(a, "build_associativity_proofs.a")
    require_proposition(b, "build_associativity_proofs.b")
    require_proposition(c, "build_associativity_proofs.c")

    forw_prop = And(And(a, b), c)
    back_prop = And(a, And(b, c))

    forward = ImpIntro(
        forw_prop, 
        AndIntro(
            AndElimLeft(AndElimLeft(VarProof(0))),
            AndIntro(
                AndElimRight(AndElimLeft(VarProof(0))),
                AndElimRight(VarProof(0))
            )
        )
    )

    backward = ImpIntro(
        back_prop, 
        AndIntro(
            AndIntro(
                AndElimLeft(VarProof(0)),
                AndElimLeft(AndElimRight(VarProof(0)))
            ),
            AndElimRight(AndElimRight(VarProof(0)))
        )
    )

    return (forward, backward)  


# =============================================================================
# 五、辅助函数：形式证明与普通 Python 值不要混为一谈
# =============================================================================


def proves(proof: Proof, expected: Proposition, context: Context = ()) -> bool:
    """检查 proof 推出的命题是否与 expected 语法相等。"""

    require_proposition(expected, "expected")
    return infer(proof, context) == expected


def swap_pair_value(pair: tuple[object, object]) -> tuple[object, object]:
    """交换一个 Python 二元积，用于观察证明对应程序的运行行为。"""

    if not isinstance(pair, tuple) or len(pair) != 2:
        raise TypeError("swap_pair_value 只接受长度为 2 的 tuple")
    left, right = pair
    return right, left


def associate_right_value(
    value: tuple[tuple[object, object], object],
) -> tuple[object, tuple[object, object]]:
    """把运行时值 ``((a, b), c)`` 变成 ``(a, (b, c))``。"""

    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError("外层必须是二元 tuple")
    ab, c = value
    if not isinstance(ab, tuple) or len(ab) != 2:
        raise TypeError("左侧必须是二元 tuple (a, b)")
    a, b = ab
    return a, (b, c)


def associate_left_value(
    value: tuple[object, tuple[object, object]],
) -> tuple[tuple[object, object], object]:
    """把运行时值 ``(a, (b, c))`` 变回 ``((a, b), c)``。"""

    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError("外层必须是二元 tuple")
    a, bc = value
    if not isinstance(bc, tuple) or len(bc) != 2:
        raise TypeError("右侧必须是二元 tuple (b, c)")
    b, c = bc
    return (a, b), c


# =============================================================================
# 六、测试断言：失败信息直接说明“期望什么、实际得到什么”
# =============================================================================


def assert_infers(
    proof: Proof,
    expected: Proposition,
    context: Context = (),
) -> None:
    """断言一棵证明树在给定上下文中推出精确的 expected。"""

    actual = infer(proof, context)
    if actual != expected:
        raise AssertionError(f"推导结果错误：期望 {expected!r}，实际 {actual!r}")


def assert_raises(
    expected_error: type[BaseException],
    action: Callable[[], object],
    explanation: str,
) -> None:
    """断言非法证明确实被指定异常拒绝。"""

    try:
        action()
    except expected_error:
        return
    except BaseException as error:
        raise AssertionError(
            f"{explanation}：期望 {expected_error.__name__}，"
            f"实际抛出 {type(error).__name__}: {error}"
        ) from error
    raise AssertionError(f"{explanation}：非法输入没有被拒绝")


# =============================================================================
# 七、四阶段批改内容
# =============================================================================


def test_stage_1_baseline() -> None:
    """基线：确认你理解上下文、de Bruijn 索引和蕴含引入。"""

    p = Atom("P")
    q = Atom("Q")

    # 假设 P 后，VarProof(0) 引用 P；退出假设便得到 P → P。
    identity = ImpIntro(p, VarProof(0))
    assert_infers(identity, Imp(p, p))
    # 保留一条原生 assert 作为课程静态门禁；上面的 assert_infers 负责给出
    # 更具体的“期望/实际”错误信息。
    assert proves(identity, Imp(p, p)), "P → P 的基线证明应当成立"

    # 进入 P 再进入 Q 后，上下文是 (Q, P)，所以索引 1 引用外层 P。
    assert_infers(
        ImpIntro(p, ImpIntro(q, VarProof(1))),
        Imp(p, Imp(q, p)),
    )

    assert_raises(
        IndexError,
        lambda: infer(VarProof(0)),
        "空上下文中不能凭空引用命题",
    )
    assert_raises(
        IndexError,
        lambda: infer(VarProof(-1), (p,)),
        "负索引不能绕到上下文末尾",
    )
    assert_raises(
        IndexError,
        lambda: infer(VarProof(1), (p,)),
        "只有一个假设时索引 1 越界",
    )


def test_stage_2_conjunction_rules() -> None:
    """批改 TODO 1：三个推导规则及其错误边界。"""

    a = Atom("A")
    b = Atom("B")

    # A → B → A ∧ B：在上下文 (B, A) 中分别取索引 1 和 0。
    introduction = ImpIntro(
        a,
        ImpIntro(b, AndIntro(VarProof(1), VarProof(0))),
    )
    assert_infers(introduction, Imp(a, Imp(b, And(a, b))))

    # (A ∧ B) → A 与 (A ∧ B) → B。
    left_projection = ImpIntro(And(a, b), AndElimLeft(VarProof(0)))
    right_projection = ImpIntro(And(a, b), AndElimRight(VarProof(0)))
    assert_infers(left_projection, Imp(And(a, b), a))
    assert_infers(right_projection, Imp(And(a, b), b))

    # 反例：普通函数证明不是积，不能进行 π₁ 投影。
    assert_raises(
        TypeError,
        lambda: infer(AndElimLeft(ImpIntro(a, VarProof(0)))),
        "左投影只能用于合取证明",
    )
    assert_raises(
        TypeError,
        lambda: infer(AndElimRight(ImpIntro(a, VarProof(0)))),
        "右投影也只能用于合取证明",
    )

    # 反例：A ∧ B 必须同时拥有两边的证明，None 不能充当缺失的 B。
    assert_raises(
        TypeError,
        lambda: infer(AndIntro(VarProof(0), None), (a,)),  # type: ignore[arg-type]
        "合取引入不能缺少右侧证明",
    )
    assert_raises(
        TypeError,
        lambda: infer(AndIntro(None, VarProof(0)), (b,)),  # type: ignore[arg-type]
        "合取引入也不能缺少左侧证明",
    )


def test_stage_3_swap_isomorphism() -> None:
    """批改 TODO 2：交换律的两个方向及其可逆行为。"""

    a = Atom("A")
    b = Atom("B")

    forward = build_swap_proof(a, b)
    backward = build_swap_proof(b, a)
    assert_infers(forward, Imp(And(a, b), And(b, a)))
    assert_infers(backward, Imp(And(b, a), And(a, b)))

    # A ∧ B 和 B ∧ A 不是同一棵命题语法树。这里严格检查的是两个方向
    # 都可推导；若要在证明语言内部称为同构，还要加入复合及 βη 等式。
    if And(a, b) == And(b, a):
        raise AssertionError("不同原子命题的积不应被当作语法相等")
    if proves(forward, Imp(And(a, b), And(a, b))):
        raise AssertionError("交换证明不应被误判为恒等证明")

    # 这是双向证明所对应的运行时直觉，不是本语言内部的等式证明。
    original = ("proof-of-A", 42)
    if swap_pair_value(swap_pair_value(original)) != original:
        raise AssertionError("交换两次应恢复原始二元积")
    assert_raises(
        TypeError,
        lambda: swap_pair_value((1, 2, 3)),  # type: ignore[arg-type]
        "交换程序只处理二元积",
    )


def test_stage_4_associativity_isomorphism() -> None:
    """批改 TODO 3：结合律两方向、嵌套边界与运行时往返。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")
    source = And(And(a, b), c)
    target = And(a, And(b, c))

    forward, backward = build_associativity_proofs(a, b, c)
    assert_infers(forward, Imp(source, target))
    assert_infers(backward, Imp(target, source))

    if source == target:
        raise AssertionError("不同括号结构不应被当作语法相等")
    if proves(forward, Imp(source, source)):
        raise AssertionError("结合变换不应被误判为恒等证明")

    # 边界：参数本身也可以是积；实现不能硬编码 A、B、C 或固定深度。
    nested_a = And(Atom("A1"), Atom("A2"))
    nested_forward, nested_backward = build_associativity_proofs(nested_a, b, c)
    nested_source = And(And(nested_a, b), c)
    nested_target = And(nested_a, And(b, c))
    assert_infers(nested_forward, Imp(nested_source, nested_target))
    assert_infers(nested_backward, Imp(nested_target, nested_source))

    # 对具体值执行正向再反向，观察两段程序确实互逆。
    value = (("a", "b"), "c")
    moved = associate_right_value(value)
    if moved != ("a", ("b", "c")):
        raise AssertionError(f"结合变换的运行结果错误：{moved!r}")
    if associate_left_value(moved) != value:
        raise AssertionError("结合变换正向再反向应恢复原值")
    assert_raises(
        TypeError,
        lambda: associate_right_value(("not-a-pair", "c")),  # type: ignore[arg-type]
        "结合变换必须检查内层积的形状",
    )


# =============================================================================
# 八、清晰的批改流程
# =============================================================================


# 完成 TODO 1 后改为 True。之后脚本会按依赖顺序逐阶段批改；前一阶段
# 失败时，后续阶段显示 BLOCKED，避免一屏互相干扰的错误。
RUN_EXERCISE_TESTS = True


StageTest: TypeAlias = Callable[[], None]


def grade_stage(number: int, label: str, test: StageTest) -> bool:
    """运行一个批改阶段并输出唯一、可定位的结果。"""

    try:
        test()
    except Exception as error:
        print(f"[FAIL {number}/4] {label}")
        print(f"  {type(error).__name__}: {error}")
        return False
    print(f"[PASS {number}/4] {label}")
    return True


def print_blocked(start: int, stages: tuple[tuple[str, StageTest], ...]) -> None:
    """说明哪些阶段因前置阶段失败而尚未批改。"""

    for offset, (label, _) in enumerate(stages[start - 1 :], start=start):
        print(f"[BLOCKED {offset}/4] {label}（先修复上一失败阶段）")


def main() -> int:
    stages: tuple[tuple[str, StageTest], ...] = (
        ("基线：上下文与蕴含引入", test_stage_1_baseline),
        ("TODO 1：合取引入与左右投影", test_stage_2_conjunction_rules),
        ("TODO 2：交换的双向推导与同构直觉", test_stage_3_swap_isomorphism),
        ("TODO 3：结合的双向推导与同构直觉", test_stage_4_associativity_isomorphism),
    )

    if not grade_stage(1, stages[0][0], stages[0][1]):
        print_blocked(2, stages)
        return 1

    if not RUN_EXERCISE_TESTS:
        for number, (label, _) in enumerate(stages[1:], start=2):
            print(f"[PENDING {number}/4] {label}")
        print("\n下一步：实现 infer_conjunction（TODO 1），然后把")
        print("RUN_EXERCISE_TESTS 改成 True 并重新运行本文件。")
        return 0

    for number, (label, test) in enumerate(stages[1:], start=2):
        if not grade_stage(number, label, test):
            print_blocked(number + 1, stages)
            return 1

    print("\n全部验收通过：你已实现合取规则和交换/结合的双向证明，")
    print("并能区分双向可推导、运行时互逆与语言内部的正式同构证明。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
