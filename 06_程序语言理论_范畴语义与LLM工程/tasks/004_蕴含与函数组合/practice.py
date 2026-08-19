"""第 004 晚：蕴含与函数组合——可分阶段批改的形式化练习。

这份练习把蕴含证明与函数组合连接起来。前三晚你已经见过蕴含引入
和消去规则；今晚的重点是用它们构造多步组合，并理解组合的类型
结构：

    蕴含引入 →I：    Γ, A ⊢ body : B
                     ——————————————————
                     Γ ⊢ λbody : A → B

    蕴含消去 →E：    Γ ⊢ f : A → B    Γ ⊢ x : A
                     ————————————————————————————
                           Γ ⊢ f(x) : B

    组合（传递性）：  f : A → B      g : B → C
                     ——————————————————————————
                     g ∘ f  ≡  λx. g(f(x)) : A → C

    逻辑读法：若 A 蕴含 B，且 B 蕴含 C，则 A 蕴含 C。
    这就是假言三段论；编程中对应函数组合。

关键区分（今晚反复出现）：

    * 构造证明对象并通过类型检查  →  确认命题可证。
    * 组合 Python 函数并在有限样本上比较结果  →  测试，不是证明。
    * 证明两个证明对象"相等"  →  需要求值规则和 βη 等式，
      当前系统尚未引入。

你需要按顺序完成三个 TODO：

1. ``build_compose_proof``：构造 ``(A→B) → (B→C) → (A→C)``。
2. ``build_flip_proof``：构造 ``(A→B→C) → B → A → C``。
3. ``build_chain3_proof``：构造 ``(A→B) → (B→C) → (C→D) → (A→D)``。

批改方法：

1. 保持 ``RUN_EXERCISE_TESTS = False`` 运行，确认第 1 阶段基线通过。
2. 完成 TODO 1 后改为 ``True``，应通过第 2 阶段。
3. 依次完成 TODO 2 和 TODO 3；四阶段全 PASS 才算今晚练习完成。

严格性提醒：当前小语言只检查"某个证明项具有某个命题"，还没有
定义证明项的归约或 βη 等式。我们可以说两个证明的类型相同，但
不能在语言内部证明两个证明对象"行为相等"。Python 函数组合上
的有限样本测试展示这一等式的计算直觉，不冒充内部证明。
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import sys
from typing import TypeAlias

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# =============================================================================
# 一、命题语法：原子命题与蕴含
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


Proposition: TypeAlias = Atom | Imp


def is_proposition(value: object) -> bool:
    """判断对象是否完全由本晚允许的命题构造子组成。"""

    if isinstance(value, Atom):
        return True
    if isinstance(value, Imp):
        return is_proposition(value.left) and is_proposition(value.right)
    return False


def require_proposition(value: object, where: str) -> Proposition:
    """拒绝把字符串、Python 类型或证明对象误当成命题。"""

    if not is_proposition(value):
        raise TypeError(f"{where} 不是合法命题：{value!r}")
    return value


# =============================================================================
# 二、证明语法：变量引用、蕴含引入与蕴含消去
# =============================================================================


@dataclass(frozen=True)
class VarProof:
    """引用上下文中的假设；0 是最新假设，1 是再外一层。"""

    index: int


@dataclass(frozen=True)
class ImpIntro:
    """蕴含引入：在 body 中临时加入 assumption。

    若在额外假设 A 下，body 能推出 B，那么退出这个局部假设后，
    整棵证明树得到 A → B。
    """

    assumption: Proposition
    body: Proof


@dataclass(frozen=True)
class ImpElim:
    """蕴含消去：把证明 ``A→B`` 的 function 应用于证明 A 的 argument。

    若 function 证明 A→B，argument 证明 A，则整个节点证明 B。
    这对应函数应用 ``f(x)``。
    """

    function: Proof
    argument: Proof


Proof: TypeAlias = VarProof | ImpIntro | ImpElim
Context: TypeAlias = tuple[Proposition, ...]


# =============================================================================
# 三、独立证明检查器（本晚全部提供，无须实现新规则）
# =============================================================================


def infer(proof: Proof, context: Context = ()) -> Proposition:
    """由 proof 的结构和 context 推导结论，不相信证明对象自报答案。

    本晚使用的三条规则在前几晚已经实现过；这里直接给出完整版本，
    让你可以专注于构造证明对象。
    """

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
                f"VarProof({proof.index}) 越界："
                f"当前上下文只有 {len(context)} 个假设"
            )
        return context[proof.index]

    # 蕴含引入：Γ,A ⊢ body:B  推出  Γ ⊢ λbody:A→B。
    if isinstance(proof, ImpIntro):
        assumption = require_proposition(
            proof.assumption, "ImpIntro.assumption"
        )
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
                f"函数需要 {function_type.left!r}，"
                f"实际得到 {argument_type!r}"
            )
        return function_type.right

    raise TypeError(f"未知证明节点：{proof!r}")


def proves(proof: Proof, expected: Proposition, context: Context = ()) -> bool:
    """判断检查器推导出的命题是否与 expected 语法相等。"""

    require_proposition(expected, "expected")
    return infer(proof, context) == expected


# =============================================================================
# 四、TODO 1：组合——蕴含的传递性
# =============================================================================


def build_compose_proof(
    a: Proposition, b: Proposition, c: Proposition,
) -> Proof:
    """TODO 1：构造 ``(A→B) → (B→C) → (A→C)`` 的闭证明。

    这就是假言三段论：若 A 蕴含 B 且 B 蕴含 C，则 A 蕴含 C。
    对应的程序是函数组合 ``g ∘ f = λx. g(f(x))``。

    提示（从外到内构造三层 ImpIntro）：

    1. 第一层 ImpIntro 引入 ``f : A → B``。
       此时上下文为 ``(A→B)``。
    2. 第二层 ImpIntro 引入 ``g : B → C``。
       此时上下文为 ``(B→C, A→B)``。
       ``VarProof(0)`` 是 g，``VarProof(1)`` 是 f。
    3. 第三层 ImpIntro 引入 ``x : A``。
       此时上下文为 ``(A, B→C, A→B)``。
       ``VarProof(0)`` 是 x，``VarProof(1)`` 是 g，``VarProof(2)`` 是 f。
    4. 函数体：先用 ``ImpElim(f, x)`` 得到 ``f(x) : B``；
       再用 ``ImpElim(g, f(x))`` 得到 ``g(f(x)) : C``。

    请返回证明 AST，不要返回 Python 函数或命题。
    """

    require_proposition(a, "build_compose_proof.a")
    require_proposition(b, "build_compose_proof.b")
    require_proposition(c, "build_compose_proof.c")

    return ImpIntro(Imp(a, b), ImpIntro(Imp(b, c), ImpIntro(a, ImpElim(VarProof(1), ImpElim(VarProof(2), VarProof(0))))))


# =============================================================================
# 五、TODO 2：参数翻转
# =============================================================================


def build_flip_proof(
    a: Proposition, b: Proposition, c: Proposition,
) -> Proof:
    """TODO 2：构造 ``(A→B→C) → B → A → C`` 的闭证明。

    目标：给定一个接受两个参数 ``(A, B)`` 的柯里化函数 ``f``，
    返回一个先接受 ``B`` 再接受 ``A`` 的函数。这在逻辑中表示
    假设的引入顺序可以交换，在编程中叫 ``flip``。

    提示：

    1. 第一层 ImpIntro 引入 ``f : A → B → C``。
    2. 第二层 ImpIntro 引入 ``y : B``。
    3. 第三层 ImpIntro 引入 ``x : A``。
    4. 此时上下文为 ``(A, B, A→B→C)``。
       ``VarProof(0)`` = x : A
       ``VarProof(1)`` = y : B
       ``VarProof(2)`` = f : A → B → C
    5. 先用 ``ImpElim(f, x)`` 得到 ``f(x) : B → C``；
       再用 ``ImpElim(f(x), y)`` 得到 ``f(x)(y) : C``。

    注意 f∘g 和 g∘f 不同：翻转后的函数类型是 ``B→A→C``，
    而非原始的 ``A→B→C``。请返回证明 AST。
    """

    require_proposition(a, "build_flip_proof.a")
    require_proposition(b, "build_flip_proof.b")
    require_proposition(c, "build_flip_proof.c")

    return ImpIntro(Imp(a, Imp(b,c)), ImpIntro(b, ImpIntro(a, ImpElim(ImpElim(VarProof(2), VarProof(0)), VarProof(1)))))


# =============================================================================
# 六、TODO 3：三步链式组合
# =============================================================================


def build_chain3_proof(
    a: Proposition,
    b: Proposition,
    c: Proposition,
    d: Proposition,
) -> Proof:
    """TODO 3：构造 ``(A→B) → (B→C) → (C→D) → (A→D)`` 的闭证明。

    三步组合 ``h ∘ g ∘ f``：从 A 经由 B、C 到达 D。无论先组合
    ``(h∘g)∘f`` 还是 ``h∘(g∘f)``，最终类型都是 ``A → D``。

    提示：

    1. 三层 ImpIntro 依次引入 f:A→B、g:B→C、h:C→D。
    2. 再一层 ImpIntro 引入 x:A。
    3. 此时上下文为 ``(A, C→D, B→C, A→B)``：
       ``VarProof(0)`` = x : A
       ``VarProof(1)`` = h : C → D
       ``VarProof(2)`` = g : B → C
       ``VarProof(3)`` = f : A → B
    4. 依次应用：
       ``f(x) : B`` → ``g(f(x)) : C`` → ``h(g(f(x))) : D``。

    请返回证明 AST。
    """

    require_proposition(a, "build_chain3_proof.a")
    require_proposition(b, "build_chain3_proof.b")
    require_proposition(c, "build_chain3_proof.c")
    require_proposition(d, "build_chain3_proof.d")

    return ImpIntro(Imp(a, b), ImpIntro(Imp(b, c), ImpIntro(Imp(c, d), ImpIntro(a, ImpElim(VarProof(1), ImpElim(VarProof(2), ImpElim(VarProof(3), VarProof(0))))))))


# =============================================================================
# 七、运行时组合函数：只用于观察证明对应程序的行为
# =============================================================================


A_ = object
B_ = object
C_ = object


def compose_fn(
    g: Callable[[B_], C_],
    f: Callable[[A_], B_],
) -> Callable[[A_], C_]:
    """Python 函数组合 ``g ∘ f``。

    注意参数顺序：数学上 ``(g ∘ f)(x) = g(f(x))``，所以 g 在前。
    """

    if not callable(g) or not callable(f):
        raise TypeError("compose_fn 的两个参数必须可调用")
    return lambda x: g(f(x))


def extensionally_equal(
    f: Callable[[object], object],
    g: Callable[[object], object],
    samples: tuple[object, ...],
) -> bool:
    """在给定样本上逐点比较 f 和 g 的输出。

    如果所有样本上 f(x) == g(x)，返回 True。这只是有限测试，
    不是一般性证明：两个函数可能在样本外不同。
    """

    if not isinstance(samples, tuple):
        raise TypeError("samples 必须是 tuple")
    return all(f(x) == g(x) for x in samples)


# =============================================================================
# 八、测试辅助函数
# =============================================================================


def assert_infers(
    proof: Proof,
    expected: Proposition,
    context: Context = (),
) -> None:
    """断言一棵证明树在给定上下文中推出精确的 expected。"""

    actual = infer(proof, context)
    if actual != expected:
        raise AssertionError(
            f"推导结果错误：期望 {expected!r}，实际 {actual!r}"
        )


def assert_raises(
    expected_error: type[Exception],
    action: Callable[[], object],
    explanation: str,
) -> None:
    """断言非法证明确实被指定异常拒绝。"""

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
# 九、四阶段批改内容
# =============================================================================


def test_stage_1_baseline() -> None:
    """基线：确认蕴含引入、消去和上下文边界。"""

    a = Atom("A")
    b = Atom("B")
    q = Atom("Q")

    # 恒等证明 A → A：最简单的蕴含。
    identity = ImpIntro(a, VarProof(0))
    assert_infers(identity, Imp(a, a))
    assert proves(identity, Imp(a, a)), "A → A 的基线证明应成立"

    # (A→B) → A → B：在上下文 (A, A→B) 中做一次应用。
    application = ImpIntro(
        Imp(a, b),
        ImpIntro(a, ImpElim(VarProof(1), VarProof(0))),
    )
    assert_infers(application, Imp(Imp(a, b), Imp(a, b)))

    # 进入 A 再进入 Q 后，索引 1 引用外层 A。
    assert_infers(
        ImpIntro(a, ImpIntro(q, VarProof(1))),
        Imp(a, Imp(q, a)),
    )

    # 反例：空上下文中不能凭空引用假设。
    assert_raises(
        IndexError,
        lambda: infer(VarProof(0)),
        "空上下文中不能凭空引用命题",
    )
    # 反例：负索引不合法。
    assert_raises(
        IndexError,
        lambda: infer(VarProof(-1), (a,)),
        "负索引不能绕到上下文末尾",
    )
    # 反例：普通命题不能当作函数使用。
    assert_raises(
        TypeError,
        lambda: infer(ImpIntro(a, ImpElim(VarProof(0), VarProof(0)))),
        "普通命题不能当作蕴含消去的函数",
    )
    # 反例：实参类型必须匹配蕴含左侧。
    assert_raises(
        TypeError,
        lambda: infer(
            ImpIntro(Imp(a, b), ImpIntro(q, ImpElim(VarProof(1), VarProof(0)))),
        ),
        "实参 Q 不匹配蕴含左侧 A",
    )


def test_stage_2_compose() -> None:
    """批改 TODO 1：组合证明的正确类型和关键反例。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")

    compose = build_compose_proof(a, b, c)
    expected = Imp(Imp(a, b), Imp(Imp(b, c), Imp(a, c)))
    assert_infers(compose, expected)

    # 参数本身可以是蕴含命题；实现不能只对 Atom 工作。
    nested_a = Imp(Atom("X"), Atom("Y"))
    nested_compose = build_compose_proof(nested_a, b, c)
    assert_infers(
        nested_compose,
        Imp(Imp(nested_a, b), Imp(Imp(b, c), Imp(nested_a, c))),
    )

    # 组合不是交换的：(A→B)→(B→C)→(A→C) ≠ (B→C)→(A→B)→(A→C)。
    wrong_order = Imp(Imp(b, c), Imp(Imp(a, b), Imp(a, c)))
    if proves(compose, wrong_order):
        raise AssertionError("组合证明的参数顺序不应被翻转")

    # 组合不是恒等：结果类型 A→C 不是 A→B。
    if proves(compose, Imp(Imp(a, b), Imp(Imp(b, c), Imp(a, b)))):
        raise AssertionError("组合证明不应丢弃 g 而直接返回 f")


def test_stage_3_flip() -> None:
    """批改 TODO 2：参数翻转的正确类型与非恒等性。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")

    flip = build_flip_proof(a, b, c)
    expected = Imp(Imp(a, Imp(b, c)), Imp(b, Imp(a, c)))
    assert_infers(flip, expected)

    # 翻转不是恒等：B→A→C ≠ A→B→C（除非 A=B）。
    identity_type = Imp(Imp(a, Imp(b, c)), Imp(a, Imp(b, c)))
    if proves(flip, identity_type):
        raise AssertionError("翻转后的参数顺序应不同于原始顺序")

    # 翻转嵌套命题仍然有效。
    nested_b = Imp(Atom("P"), Atom("Q"))
    nested_flip = build_flip_proof(a, nested_b, c)
    assert_infers(
        nested_flip,
        Imp(Imp(a, Imp(nested_b, c)), Imp(nested_b, Imp(a, c))),
    )

    # 对 A=B 时翻转类型碰巧与原始一致，但证明的内部结构不同；
    # 这里只测类型正确。
    same_flip = build_flip_proof(a, a, c)
    assert_infers(
        same_flip,
        Imp(Imp(a, Imp(a, c)), Imp(a, Imp(a, c))),
    )

    # 反例：翻转后不能把 B 误当 A 送给 f。
    wrong_flip = ImpIntro(
        Imp(a, Imp(b, c)),
        ImpIntro(b, ImpIntro(a, ImpElim(ImpElim(VarProof(2), VarProof(1)), VarProof(0)))),
    )
    assert_raises(
        TypeError,
        lambda: infer(wrong_flip),
        "把 B 误当 A 送给 f 应被类型检查拒绝",
    )


def test_stage_4_chain3_and_runtime() -> None:
    """批改 TODO 3：三步组合、运行时组合行为和外延相等。"""

    a = Atom("A")
    b = Atom("B")
    c = Atom("C")
    d = Atom("D")

    # --- 形式证明部分 ---

    chain3 = build_chain3_proof(a, b, c, d)
    expected = Imp(
        Imp(a, b), Imp(Imp(b, c), Imp(Imp(c, d), Imp(a, d)))
    )
    assert_infers(chain3, expected)

    # 嵌套命题参数仍然有效。
    nested_chain = build_chain3_proof(Imp(a, a), b, c, d)
    nested_expected = Imp(
        Imp(Imp(a, a), b),
        Imp(Imp(b, c), Imp(Imp(c, d), Imp(Imp(a, a), d))),
    )
    assert_infers(nested_chain, nested_expected)

    # 不能跳过中间步骤：若丢掉 f 只用 g 和 h，得到的类型不对。
    if proves(chain3, Imp(Imp(a, b), Imp(Imp(b, c), Imp(Imp(c, d), Imp(b, d))))):
        raise AssertionError("三步组合不应跳过 f 直接从 B 出发")

    # --- 运行时组合部分 ---

    inc: Callable[[int], int] = lambda x: x + 1
    double: Callable[[int], int] = lambda x: 2 * x
    show: Callable[[int], str] = lambda x: f"[{x}]"

    # 基本组合。
    double_then_inc = compose_fn(inc, double)
    inc_then_double = compose_fn(double, inc)
    if double_then_inc(3) != 7:
        raise AssertionError(f"(inc ∘ double)(3) 应为 7")
    if inc_then_double(3) != 8:
        raise AssertionError(f"(double ∘ inc)(3) 应为 8")

    # 组合不是交换的。
    if double_then_inc(3) == inc_then_double(3):
        raise AssertionError("inc∘double 和 double∘inc 不应在 3 上相等")

    # 组合是结合的（在有限样本上测试）。
    left_grouped = compose_fn(show, compose_fn(double, inc))
    right_grouped = compose_fn(compose_fn(show, double), inc)
    samples = (-2, 0, 1, 5, 100)
    if not extensionally_equal(left_grouped, right_grouped, samples):
        raise AssertionError(
            "show∘(double∘inc) 与 (show∘double)∘inc 在样本上应相等"
        )

    # 恒等函数是组合的单位元（在有限样本上测试）。
    identity_fn: Callable[[int], int] = lambda x: x
    if not extensionally_equal(
        compose_fn(identity_fn, double), double, samples
    ):
        raise AssertionError("id∘double 在样本上应等于 double")
    if not extensionally_equal(
        compose_fn(double, identity_fn), double, samples
    ):
        raise AssertionError("double∘id 在样本上应等于 double")

    # 有限样本不等于证明：两个函数在样本上全部相等，但在样本外不同。
    safe_samples = (0, 1, 2, 3)
    f_real: Callable[[int], int] = lambda x: x
    f_fake: Callable[[int], int] = lambda x: x if x != 999 else -1
    if not extensionally_equal(f_real, f_fake, safe_samples):
        raise AssertionError("两个函数在安全样本上应相等")
    if f_real(999) == f_fake(999):
        raise AssertionError("两个函数在样本外应不同——有限测试的局限")

    # compose_fn 必须检查参数可调用性。
    assert_raises(
        TypeError,
        lambda: compose_fn("not-a-function", inc),  # type: ignore[arg-type]
        "compose_fn 不接受不可调用的参数",
    )

    # 空字符串边界：对单位元和 str.upper 都能正确处理。
    assert compose_fn(str.upper, lambda s: s)("") == ""


# =============================================================================
# 十、清晰的分阶段批改器
# =============================================================================


# 完成 TODO 1 后改为 True。批改器按依赖顺序逐阶段执行；前一阶段
# 失败时，后续阶段显示 BLOCKED，避免大量由同一根因产生的错误。
RUN_EXERCISE_TESTS = True


StageTest: TypeAlias = Callable[[], None]


def grade_stage(number: int, label: str, test: StageTest) -> bool:
    """运行一个批改阶段，输出统一格式的结果。"""

    try:
        test()
    except Exception as error:
        print(f"[FAIL {number}/4] {label}")
        print(f"  {type(error).__name__}: {error}")
        return False
    print(f"[PASS {number}/4] {label}")
    return True


def print_blocked(
    start: int, stages: tuple[tuple[str, StageTest], ...],
) -> None:
    """列出因前置阶段失败而尚未运行的测试。"""

    for offset, (label, _) in enumerate(stages[start - 1 :], start=start):
        print(f"[BLOCKED {offset}/4] {label}（先修复上一失败阶段）")


def main() -> int:
    stages: tuple[tuple[str, StageTest], ...] = (
        ("基线：蕴含引入、消去与上下文边界", test_stage_1_baseline),
        ("TODO 1：组合——蕴含的传递性", test_stage_2_compose),
        ("TODO 2：参数翻转", test_stage_3_flip),
        ("TODO 3：三步链式组合与运行时组合", test_stage_4_chain3_and_runtime),
    )

    if not grade_stage(1, stages[0][0], stages[0][1]):
        print_blocked(2, stages)
        return 1

    if not RUN_EXERCISE_TESTS:
        for number, (label, _) in enumerate(stages[1:], start=2):
            print(f"[PENDING {number}/4] {label}")
        print("\n下一步：实现 build_compose_proof（TODO 1），然后把")
        print("RUN_EXERCISE_TESTS 改成 True 并重新运行本文件。")
        return 0

    for number, (label, test) in enumerate(stages[1:], start=2):
        if not grade_stage(number, label, test):
            print_blocked(number + 1, stages)
            return 1

    print("\n全部验收通过：你已构造组合、翻转和三步链式证明，")
    print("并能区分类型检查、有限样本测试和形式化等式证明。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# 完成四阶段后的可选改造：实现 curry / uncurry，
# 构造 ((A∧B)→C) → A→B→C 和 (A→B→C) → (A∧B)→C 的证明对象，
# 并在 Python 值上验证两个方向的往返。需要从第 002 晚引入 And 节点。
