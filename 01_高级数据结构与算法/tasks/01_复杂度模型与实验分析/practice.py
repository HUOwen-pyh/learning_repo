"""第 01 晚：复杂度模型与实验分析——可分阶段批改的形式化练习。

这份练习不是让你"跑一下排序看看快不快"就结束，而是让你搭建三层
可验证的复杂度分析框架，并理解每一层为什么不可省略：

    操作计数：      在输入 x 上，算法执行 C(x) 次比较。
                    计数只取决于算法结构和输入，不受 CPU、缓存、
                    调度器影响。一次 wall-clock 计时什么也证明不了。

    循环不变量：    P(lo, hi) ≡ 若 target 存在于 a 中，
                            则 target ∈ a[lo..hi)。
                    每次循环开始时 P 成立，循环体维持 P，
                    终止时 P ∧ (lo ≥ hi) 蕴含后置条件。

    倍增比值：      r(n) = C(2n) / C(n)。
                    r → 2  ⟹  Θ(n)
                    r → 4  ⟹  Θ(n²)
                    r → 1  ⟹  O(log n)
                    单次测量无法确定增长阶；倍增序列才能给出
                    可重复的机器无关证据。

你需要按顺序完成三个 TODO：

1. ``binary_search_with_invariant``：实现二分查找，每次循环检查
   不变量，并返回正确的比较次数。
2. ``expected_comparisons_experiment``：通过随机实验验证线性查找
   的期望比较次数公式 (n+1)/2。
3. ``analyze_growth_order``：对任意计数函数执行倍增实验，分类增长阶。

批改方法：

1. 保持 ``RUN_EXERCISE_TESTS = False`` 运行，确认第 1 阶段基线通过。
2. 完成 TODO 1 后改为 ``True``，应通过第 2 阶段。
3. 依次完成 TODO 2 和 TODO 3；四阶段全 PASS 才算今晚练习完成。

每一阶段的测试既有正例（合法输入通过），也有反例（非法输入被拒绝）
和边界例。请不要删除测试来制造 PASS。
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math
import random
import statistics
import sys
from typing import TypeAlias

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# =============================================================================
# 一、数据类型：搜索结果、不变量异常与增长阶分析
# =============================================================================


@dataclass(frozen=True)
class SearchResult:
    """搜索算法的返回值：找到的索引（-1 表示未找到）和比较次数。

    比较次数是机器无关的成本指标：它只取决于算法逻辑和输入，不受
    CPU 频率、缓存命中率或操作系统调度影响。
    """

    index: int
    comparisons: int

    def __post_init__(self) -> None:
        if not isinstance(self.comparisons, int) or self.comparisons < 0:
            raise ValueError(
                f"比较次数必须为非负整数，收到 {self.comparisons!r}"
            )


class InvariantViolation(Exception):
    """当循环不变量被破坏时抛出。

    不变量不是注释或文档，而是可执行的断言。它在每次循环迭代开始
    时被检查；如果某次迭代破坏了不变量，算法的正确性论证就失效了。
    """


@dataclass(frozen=True)
class GrowthAnalysis:
    """倍增实验的完整分析结果。

    ``sizes``        测试的输入规模序列（倍增关系）。
    ``counts``       对应规模下的操作计数。
    ``ratios``       相邻规模的计数比值 counts[i+1] / counts[i]。
    ``median_ratio`` 比值的中位数，用于分类增长阶。
    ``growth_class`` 分类结果：``"logarithmic"``、``"linear"`` 或
                     ``"quadratic"``。
    """

    sizes: tuple[int, ...]
    counts: tuple[int, ...]
    ratios: tuple[float, ...]
    median_ratio: float
    growth_class: str


# =============================================================================
# 二、已提供的算法：线性查找与插入排序（带比较计数）
# =============================================================================


def linear_search_counted(a: list[int], target: int) -> SearchResult:
    """线性查找：从头到尾逐一比较，返回索引和比较次数。

    最坏情况（target 不在数组中或在末尾）：比较 n 次。
    最好情况（target 在开头）：比较 1 次。
    空数组：比较 0 次，返回 index = -1。
    """

    comparisons = 0
    for i, value in enumerate(a):
        comparisons += 1
        if value == target:
            return SearchResult(i, comparisons)
    return SearchResult(-1, comparisons)


def insertion_sort_counted(a: list[int]) -> int:
    """对 a 原地插入排序，返回比较次数。调用方负责传入可变副本。

    最坏情况（逆序输入）：比较 n(n-1)/2 次，即 Θ(n²)。
    最好情况（已排序输入）：比较 n-1 次，即 Θ(n)。
    """

    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key
    return comparisons


# =============================================================================
# 三、TODO 1：带循环不变量断言的二分查找
# =============================================================================


def binary_search_with_invariant(
    a: list[int],
    target: int,
) -> SearchResult:
    """TODO 1：实现带不变量检查的二分查找，返回 SearchResult。

    输入保证：``a`` 已按升序排列，元素互不重复。

    循环不变量 P(lo, hi)：
        若 target 存在于 a 中，则 target 的实际位置 k 满足
        lo ≤ k < hi。换言之，target 一定在半开区间 a[lo..hi) 内。

    你需要实现：

    1. 初始化 ``lo = 0``、``hi = len(a)``、``comparisons = 0``。
    2. 在 ``while lo < hi`` 循环的每次迭代 **开始处** 检查不变量：
       如果 target 确实在 a 中（用 ``target in a`` 判断），
       找到它的实际位置 ``k = a.index(target)``，
       断言 ``lo <= k < hi``，否则抛出 ``InvariantViolation``。
       如果 target 不在 a 中，不变量自动成立（前件为假）。
    3. 计算 ``mid = (lo + hi) // 2``。
    4. 将 ``a[mid]`` 与 ``target`` 做三路比较，``comparisons += 1``：
       - 若 ``a[mid] < target``：``lo = mid + 1``
       - 若 ``a[mid] > target``：``hi = mid``
       - 若 ``a[mid] == target``：返回 ``SearchResult(mid, comparisons)``
    5. 循环结束后 ``lo >= hi``，target 不在数组中，
       返回 ``SearchResult(-1, comparisons)``。

    比较计数规则：每次循环迭代中对 ``a[mid]`` 与 ``target`` 的
    三路比较计为 1 次。这是算法分析的标准约定：一次比较操作揭示
    两个元素的完整顺序关系。

    比较次数上界：⌈log₂(n+1)⌉，因为每次比较将搜索区间长度至少减半。
    """
    l, r, cnt = 0, len(a), 0
    while r > l:
        mid = (l + r) >> 1
        cnt += 1
        if a[mid] == target:
            return SearchResult(mid, cnt)
        if a[mid] < target:
            l = mid + 1
        if a[mid] > target:
            r = mid
    return SearchResult(-1, cnt)
    


# =============================================================================
# 四、TODO 2：期望比较次数的实验验证
# =============================================================================


def expected_comparisons_experiment(
    n: int,
    num_trials: int,
    rng: random.Random,
) -> float:
    """TODO 2：用随机实验测量线性查找的期望比较次数，返回平均值。

    理论公式：对于 ``a = [0, 1, ..., n-1]``，若 target 均匀随机
    取自 ``{0, 1, ..., n-1}``（保证能找到），则期望比较次数 =
    ``(n+1)/2``。

    推导：找到位置 i 的元素需要 ``i + 1`` 次比较（从头扫描）。
    若每个位置等概率 ``1/n``，则
    ``E = (1/n) * Σ_{i=0}^{n-1} (i+1) = (n+1)/2``。

    你需要实现：

    1. 构造数组 ``a = list(range(n))``。
    2. 重复 ``num_trials`` 次：
       a. 用 ``rng.randrange(n)`` 生成均匀随机的 target。
       b. 调用 ``linear_search_counted(a, target)``，记录比较次数。
    3. 返回所有试验的比较次数的 **算术平均值** （``float``）。

    关键理解：
    - "期望"不是"总是"：单次实验可能比较 1 次或 n 次。
    - 必须用均匀分布：偏向某些位置会改变期望。
    - 如果你把 target 固定为 ``n - 1``，测量的是最坏情况，不是期望。
    - "平均复杂度"必须附带输入分布，否则没有含义。
    """

    cnt = 0
    a = list(range(n))
    for _ in range(num_trials):
        target = rng.randrange(n)
        cnt += linear_search_counted(a, target).comparisons
    return cnt / num_trials


# =============================================================================
# 五、TODO 3：倍增增长阶分析
# =============================================================================


def analyze_growth_order(
    count_fn: Callable[[int], int],
    base_size: int,
    num_doublings: int,
) -> GrowthAnalysis:
    """TODO 3：对 count_fn 执行倍增实验，返回 GrowthAnalysis。

    ``count_fn(n)`` 接受规模 n，在内部构造输入、运行算法，返回操作
    计数。这个计数是机器无关的——你不需要也不应该使用 ``time`` 模块。

    你需要实现：

    1. 生成规模序列 ``sizes``：从 ``base_size`` 开始，每次翻倍，
       共 ``num_doublings + 1`` 个元素。
       例如 ``base_size=100, num_doublings=3`` → ``[100, 200, 400, 800]``。
    2. 对每个 n 调用 ``count_fn(n)``，收集 ``counts`` 列表。
    3. 若任何 count 为 0，抛出 ``ValueError``（无法计算比值）。
    4. 计算相邻计数的比值：``ratios[i] = counts[i+1] / counts[i]``。
    5. 用 ``statistics.median`` 计算 ratios 的中位数。
    6. 根据中位数分类增长阶：
       - ``median < 1.5``        → ``"logarithmic"``
       - ``1.5 ≤ median < 3.0``  → ``"linear"``
       - ``median ≥ 3.0``        → ``"quadratic"``
    7. 返回 ``GrowthAnalysis``，其中 ``sizes``、``counts``、``ratios``
       必须是 ``tuple``（用 ``tuple(your_list)`` 转换）。

    为什么用比较计数而不是 wall-clock 时间：
    - 计数不受 CPU 频率影响，在任何机器上结果完全相同。
    - 计时受预热、缓存、GC、OS 调度影响，重复运行结果不同。
    - 计数直接反映算法结构，是"模型无关证据"。
    - 计时是"模型相关证据"，只有在计数验证后才有参考价值。

    注意：O(n log n) 的理论比值为 ``2 + 2/log n``，在实际规模下与
    线性算法难以区分。这是方法的固有局限，不是你的实现错误。
    """
    sizes = [base_size]
    for _ in range(num_doublings):
        sizes.append(sizes[-1] * 2)
    counts = [count_fn(size) for size in sizes]
    ratios = []
    for  i in range(len(counts) - 1):
        if counts[i] == 0:
            raise ValueError(f"ValueError")
        ratios.append(counts[i+1] / counts[i])
    median = statistics.median(ratios)
    growth = "linear"
    if median < 1.5:
        growth = "logarithmic"
    if median >= 3.0:
        growth = "quadratic"
    g = GrowthAnalysis(tuple(sizes), tuple(counts), tuple(ratios), median, growth)
    print(g)
    return g


# =============================================================================
# 六、测试辅助函数
# =============================================================================


def assert_search_correct(
    result: SearchResult,
    a: list[int],
    target: int,
    label: str,
) -> None:
    """断言搜索结果的索引与 Python 标准行为一致。"""

    if target in a:
        expected_index = a.index(target)
        if result.index != expected_index:
            raise AssertionError(
                f"{label}：期望索引 {expected_index}，实际 {result.index}"
            )
    else:
        if result.index != -1:
            raise AssertionError(
                f"{label}：target 不在数组中，期望 -1，实际 {result.index}"
            )


def assert_count_at_most(
    result: SearchResult,
    upper_bound: int,
    label: str,
) -> None:
    """断言比较次数不超过理论上界。"""

    if result.comparisons > upper_bound:
        raise AssertionError(
            f"{label}：比较 {result.comparisons} 次，超过上界 {upper_bound}"
        )


def assert_close(
    actual: float,
    expected: float,
    tolerance: float,
    label: str,
) -> None:
    """断言两个数值在 tolerance 范围内相等。"""

    if abs(actual - expected) > tolerance:
        raise AssertionError(
            f"{label}：期望 {expected:.3f}（±{tolerance:.3f}），"
            f"实际 {actual:.3f}"
        )


def assert_raises(
    expected_error: type[Exception],
    action: Callable[[], object],
    explanation: str,
) -> None:
    """断言非法操作确实被指定异常拒绝。"""

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
    """基线：确认线性查找和插入排序的计数正确工作。"""

    # 正例：找到第一个元素，比较 1 次。
    a = list(range(100))
    result = linear_search_counted(a, 0)
    assert_search_correct(result, a, 0, "线性查找首元素")
    if result.comparisons != 1:
        raise AssertionError(
            f"首元素应比较 1 次，实际 {result.comparisons}"
        )

    # 正例：找到最后一个元素，比较 n 次。
    result = linear_search_counted(a, 99)
    assert_search_correct(result, a, 99, "线性查找末元素")
    if result.comparisons != 100:
        raise AssertionError(
            f"末元素应比较 {len(a)} 次，实际 {result.comparisons}"
        )

    # 正例：找不到，比较 n 次。
    result = linear_search_counted(a, 200)
    assert_search_correct(result, a, 200, "线性查找不存在的元素")
    if result.comparisons != 100:
        raise AssertionError(
            f"不存在元素应比较 {len(a)} 次，实际 {result.comparisons}"
        )

    # 边界：空数组，比较 0 次。
    result = linear_search_counted([], 42)
    if result.index != -1 or result.comparisons != 0:
        raise AssertionError("空数组应返回 SearchResult(-1, 0)")

    # 插入排序：已排序输入 → 最好情况 n-1 次比较。
    best_comps = insertion_sort_counted(list(range(10)))
    if best_comps != 9:
        raise AssertionError(
            f"已排序输入应比较 9 次（n-1），实际 {best_comps}"
        )

    # 插入排序：逆序输入 → 最坏情况 n(n-1)/2 次比较。
    worst_data = list(range(10, 0, -1))
    worst_comps = insertion_sort_counted(worst_data)
    if worst_comps != 45:
        raise AssertionError(
            f"逆序输入应比较 45 次（n(n-1)/2），实际 {worst_comps}"
        )
    if worst_data != list(range(1, 11)):
        raise AssertionError("插入排序后数组应有序")

    # 反例：SearchResult 不接受负比较次数。
    assert_raises(
        ValueError,
        lambda: SearchResult(0, -1),
        "比较次数不能为负",
    )


def test_stage_2_binary_search() -> None:
    """批改 TODO 1：二分查找的正确性、计数上界和不变量。"""

    n = 1000
    a = list(range(n))
    max_comps = math.ceil(math.log2(n + 1))

    # 正例：找到各位置的元素，比较次数不超过 ⌈log₂(n+1)⌉。
    for target in [0, 1, n // 2, n - 2, n - 1]:
        result = binary_search_with_invariant(a, target)
        assert_search_correct(result, a, target, f"二分查找 {target}")
        assert_count_at_most(
            result, max_comps, f"二分查找 {target} 的比较上界"
        )

    # 正例：查找不存在的元素。
    for target in [-1, n, n + 100]:
        result = binary_search_with_invariant(a, target)
        assert_search_correct(
            result, a, target, f"二分查找不存在 {target}"
        )
        assert_count_at_most(
            result, max_comps, f"二分查找不存在 {target} 的比较上界"
        )

    # 边界：空数组。
    result = binary_search_with_invariant([], 42)
    if result.index != -1 or result.comparisons != 0:
        raise AssertionError("空数组应返回 SearchResult(-1, 0)")

    # 边界：单元素，找到与找不到。
    result = binary_search_with_invariant([5], 5)
    assert_search_correct(result, [5], 5, "单元素找到")
    assert_count_at_most(result, 1, "单元素找到")

    result = binary_search_with_invariant([5], 3)
    assert_search_correct(result, [5], 3, "单元素找不到")
    assert_count_at_most(result, 1, "单元素找不到")

    # 差分测试：50 组随机数据与 Python ``in`` 对比。
    rng = random.Random(42)
    for _ in range(50):
        size = rng.randint(1, 500)
        data = sorted(rng.sample(range(10000), size))
        t = rng.randrange(10000)
        result = binary_search_with_invariant(data, t)
        expected_found = t in data
        if (result.index != -1) != expected_found:
            raise AssertionError(
                f"差分测试失败：size={size}, target={t}, "
                f"found={result.index != -1}, expected={expected_found}"
            )
        if expected_found and data[result.index] != t:
            raise AssertionError("找到的索引处的值不等于 target")

    # 反例：非空数组的二分查找比较次数不应为 0。
    result = binary_search_with_invariant(a, 500)
    if result.comparisons == 0:
        raise AssertionError(
            "在 1000 元素数组中查找，比较次数不应为 0"
        )


def test_stage_3_expected_comparisons() -> None:
    """批改 TODO 2：期望比较次数的统计验证。"""

    # 正例：n=100, 10000 次试验，平均应接近 (100+1)/2 = 50.5。
    rng = random.Random(12345)
    avg = expected_comparisons_experiment(100, 10000, rng)
    assert_close(avg, 50.5, 2.0, "n=100 的期望比较次数")

    # 正例：n=1000, 10000 次试验，平均应接近 500.5。
    rng = random.Random(67890)
    avg = expected_comparisons_experiment(1000, 10000, rng)
    assert_close(avg, 500.5, 15.0, "n=1000 的期望比较次数")

    # 边界：n=1，唯一位置总是比较 1 次。
    rng = random.Random(11111)
    avg = expected_comparisons_experiment(1, 1000, rng)
    assert_close(avg, 1.0, 0.01, "n=1 的期望比较次数必须恰好为 1")

    # 正例：相同种子 → 相同结果（可复现性）。
    rng1 = random.Random(99)
    rng2 = random.Random(99)
    avg1 = expected_comparisons_experiment(10, 500, rng1)
    avg2 = expected_comparisons_experiment(10, 500, rng2)
    if avg1 != avg2:
        raise AssertionError("相同种子应产生完全相同的实验结果")

    # 返回值必须是数值类型。
    if not isinstance(avg1, (int, float)):
        raise AssertionError(
            f"返回值应为数值类型，实际为 {type(avg1).__name__}"
        )


def test_stage_4_growth_order() -> None:
    """批改 TODO 3：倍增比值的正确计算和增长阶分类。"""

    # --- 线性查找最坏情况：C(n) = n → 比值 = 2.0 ---
    def linear_worst(n: int) -> int:
        return linear_search_counted(list(range(n)), n).comparisons

    result = analyze_growth_order(linear_worst, 500, 4)
    if result.growth_class != "linear":
        raise AssertionError(
            f"线性查找应分类为 'linear'，实际 '{result.growth_class}'"
            f"（中位比值 {result.median_ratio:.3f}）"
        )
    for r in result.ratios:
        assert_close(r, 2.0, 0.01, "线性查找倍增比值")

    # --- 二分查找最坏情况：C(n) ≈ log₂ n → 比值 ≈ 1.1 ---
    def binary_worst(n: int) -> int:
        return binary_search_with_invariant(list(range(n)), n).comparisons

    result = analyze_growth_order(binary_worst, 500, 4)
    if result.growth_class != "logarithmic":
        raise AssertionError(
            f"二分查找应分类为 'logarithmic'，实际 '{result.growth_class}'"
            f"（中位比值 {result.median_ratio:.3f}）"
        )

    # --- 插入排序最坏情况：C(n) = n(n-1)/2 → 比值 ≈ 4.0 ---
    def isort_worst(n: int) -> int:
        return insertion_sort_counted(list(range(n, 0, -1)))

    result = analyze_growth_order(isort_worst, 100, 4)
    if result.growth_class != "quadratic":
        raise AssertionError(
            f"插入排序应分类为 'quadratic'，实际 '{result.growth_class}'"
            f"（中位比值 {result.median_ratio:.3f}）"
        )
    for r in result.ratios:
        assert_close(r, 4.0, 0.15, "插入排序倍增比值")

    # 验证返回值结构：sizes 长度 = num_doublings + 1。
    result = analyze_growth_order(linear_worst, 100, 3)
    if len(result.sizes) != 4:
        raise AssertionError(
            f"3 次倍增应有 4 个规模，实际 {len(result.sizes)}"
        )
    if len(result.ratios) != 3:
        raise AssertionError(
            f"3 次倍增应有 3 个比值，实际 {len(result.ratios)}"
        )

    # 验证 sizes 确实是倍增序列。
    for i in range(len(result.sizes) - 1):
        if result.sizes[i + 1] != result.sizes[i] * 2:
            raise AssertionError("sizes 应是严格倍增序列")

    # 反例：count_fn 返回 0 → 无法计算比值 → ValueError。
    assert_raises(
        ValueError,
        lambda: analyze_growth_order(lambda n: 0, 100, 3),
        "操作计数为 0 时无法计算比值",
    )

    # 反例：分类必须基于比值，不能基于函数名称或其他外部信息。
    def tricky_linear(n: int) -> int:
        return n

    result = analyze_growth_order(tricky_linear, 100, 4)
    if result.growth_class != "linear":
        raise AssertionError(
            "增长阶分类必须基于比值，不能基于函数名称"
        )


# =============================================================================
# 八、清晰的分阶段批改器
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
        ("基线：线性查找计数与插入排序计数", test_stage_1_baseline),
        ("TODO 1：带不变量的二分查找", test_stage_2_binary_search),
        ("TODO 2：期望比较次数实验", test_stage_3_expected_comparisons),
        ("TODO 3：倍增增长阶分析", test_stage_4_growth_order),
    )

    if not grade_stage(1, stages[0][0], stages[0][1]):
        print_blocked(2, stages)
        return 1

    if not RUN_EXERCISE_TESTS:
        for number, (label, _) in enumerate(stages[1:], start=2):
            print(f"[PENDING {number}/4] {label}")
        print("\n下一步：实现 binary_search_with_invariant（TODO 1），然后把")
        print("RUN_EXERCISE_TESTS 改成 True 并重新运行本文件。")
        return 0

    for number, (label, test) in enumerate(stages[1:], start=2):
        if not grade_stage(number, label, test):
            print_blocked(number + 1, stages)
            return 1

    print("\n全部验收通过：你已实现带不变量的二分查找、期望比较实验")
    print("和倍增增长阶分析，并能区分模型无关证据与机器相关测量。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# 完成四阶段后的可选改造：实现 exponential_search（先指数步进确定
# 范围，再二分查找），并用 analyze_growth_order 验证其增长阶与
# binary_search 相同。记录 target 靠近开头时的比较次数差异。
