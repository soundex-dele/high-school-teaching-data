"""Reviewed atomic knowledge-item seeds used by ``build_seed_content.py``.

These are original factual outlines. They intentionally avoid textbook prose,
worked examples and illustrations.
"""

from __future__ import annotations


def math_item(
    item_id: str,
    item_type: str,
    name: str,
    content: str,
    formulas: list[str] | None = None,
    conditions: list[str] | None = None,
    conclusion: str = "",
):
    item = {
        "id": item_id,
        "type": item_type,
        "name": name,
        "content": content,
        "review_status": "self_checked",
    }
    if formulas:
        item["formulas"] = formulas
    if conditions is not None:
        item["conditions"] = conditions
    if conclusion:
        item["conclusion"] = conclusion
    return item


MATH_ITEMS = {
    "sets-logic": [
        math_item("membership", "definition", "元素与集合的关系", "用属于和不属于描述对象与集合之间的关系。", [r"a\in A", r"a\notin A"]),
        math_item("set-operations", "formula", "集合的交、并、补运算", "交集取公共元素，并集汇总元素，补集依赖给定全集。", [r"A\cap B", r"A\cup B", r"\complement_U A"]),
        math_item("subset", "definition", "子集与集合相等", "若 A 的每个元素都属于 B，则 A 是 B 的子集；互为子集的集合相等。", [r"A\subseteq B", r"A=B\iff A\subseteq B\land B\subseteq A"]),
        math_item("implication", "definition", "充分条件与必要条件", "用命题间的推出关系判断充分性、必要性和充要性。", [r"p\Rightarrow q", r"p\Leftrightarrow q"]),
        math_item("demorgan", "theorem", "集合的德摩根定律", "取补会把并集与交集相互转换。", [r"\complement_U(A\cup B)=(\complement_U A)\cap(\complement_U B)", r"\complement_U(A\cap B)=(\complement_U A)\cup(\complement_U B)"], ["全集 U 已确定"], "并集的补等于补集的交，交集的补等于补集的并。"),
    ],
    "inequality": [
        math_item("quadratic", "formula", "一元二次函数的一般式", "二次项系数不为零时，函数图象是抛物线。", [r"y=ax^2+bx+c\quad(a\ne0)"]),
        math_item("discriminant", "theorem", "判别式与实根个数", "判别式的符号决定一元二次方程实根的个数。", [r"\Delta=b^2-4ac"], [r"a\ne0"], "Δ>0 有两个不等实根，Δ=0 有两个相等实根，Δ<0 没有实根。"),
        math_item("quadratic-formula", "formula", "一元二次方程求根公式", "在有实根时可由系数直接计算方程的根。", [r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}"], [r"a\ne0", r"\Delta\ge0"]),
        math_item("sign-chart", "method", "一元二次不等式解法", "结合二次函数开口方向、零点与图象在横轴上下的位置确定解集。"),
        math_item("am-gm", "theorem", "基本不等式", "两个正数的算术平均数不小于几何平均数，等号在两数相等时成立。", [r"\frac{a+b}{2}\ge\sqrt{ab}"], [r"a>0", r"b>0"], "当且仅当 a=b 时等号成立。"),
    ],
    "function": [
        math_item("definition-domain", "definition", "函数、定义域和值域", "函数要求定义域中的每个自变量都有唯一确定的函数值。", [r"y=f(x),\ x\in D"]),
        math_item("monotonicity", "definition", "函数的单调性", "在给定区间内比较自变量与函数值的同向或反向变化。"),
        math_item("parity", "theorem", "奇函数与偶函数", "奇偶性必须在关于原点对称的定义域上讨论。", [r"f(-x)=-f(x)", r"f(-x)=f(x)"], ["定义域关于原点对称"], "分别对应奇函数和偶函数。"),
        math_item("max-min", "concept", "函数的最大值与最小值", "最值是函数在指定定义域或区间内能够取得的最大或最小函数值。"),
        math_item("piecewise", "method", "分段函数分析", "先按自变量所属区间选择解析式，再分别研究图象、性质与取值。"),
    ],
    "exp-log": [
        math_item("power-laws", "formula", "实数指数幂运算", "同底数幂相乘指数相加，乘方时指数相乘。", [r"a^ma^n=a^{m+n}", r"(a^m)^n=a^{mn}"], [r"a>0"]),
        math_item("exponential", "definition", "指数函数", "底数大于 1 时递增，底数在 0 与 1 之间时递减。", [r"y=a^x"], [r"a>0", r"a\ne1"]),
        math_item("log-definition", "definition", "对数的定义", "对数表示指数运算的逆运算。", [r"a^x=N\iff\log_aN=x"], [r"a>0", r"a\ne1", r"N>0"]),
        math_item("log-laws", "formula", "对数运算法则", "积、商和幂的对数可分别转化为和、差与倍数。", [r"\log_a(MN)=\log_aM+\log_aN", r"\log_a\frac{M}{N}=\log_aM-\log_aN", r"\log_aM^n=n\log_aM"], [r"M>0", r"N>0"]),
        math_item("change-base", "formula", "换底公式", "可借助任意合法的新底数计算对数。", [r"\log_aN=\frac{\log_bN}{\log_ba}"], [r"a,b>0", r"a,b\ne1", r"N>0"]),
    ],
    "trigonometry": [
        math_item("radian", "definition", "弧度制", "圆心角的弧度数等于所对弧长与半径之比。", [r"\alpha=\frac lr"]),
        math_item("unit-circle", "definition", "任意角三角函数", "单位圆上终边交点的坐标给出余弦和正弦。", [r"\cos\alpha=x", r"\sin\alpha=y", r"\tan\alpha=\frac yx"]),
        math_item("basic-identity", "theorem", "同角三角函数基本关系", "正弦平方与余弦平方之和恒为 1。", [r"\sin^2\alpha+\cos^2\alpha=1"], [], "恒等式对任意有定义的角成立。"),
        math_item("periodicity", "property", "三角函数的周期性", "正弦和余弦的最小正周期为 2π，正切的最小正周期为 π。", [r"\sin(x+2\pi)=\sin x", r"\tan(x+\pi)=\tan x"]),
        math_item("addition", "formula", "两角和与差公式", "把复合角的三角函数转化为单角三角函数。", [r"\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta", r"\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta"]),
    ],
    "vector": [
        math_item("linear", "formula", "向量的线性运算", "向量加减和数乘同时反映大小与方向的变化。", [r"\lambda\vec a+\mu\vec b"]),
        math_item("coordinates", "formula", "平面向量坐标运算", "对应坐标分别相加、相减或数乘。", [r"(x_1,y_1)+(x_2,y_2)=(x_1+x_2,y_1+y_2)"]),
        math_item("dot-product", "definition", "向量数量积", "数量积联系向量夹角、长度与垂直关系。", [r"\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta"]),
        math_item("perpendicular", "theorem", "向量垂直判定", "两个非零向量的数量积为零等价于它们垂直。", [r"\vec a\cdot\vec b=0"], ["a、b 均为非零向量"], "a 与 b 垂直。"),
        math_item("sine-cosine-laws", "theorem", "正弦定理与余弦定理", "利用边角关系求解一般三角形。", [r"\frac a{\sin A}=\frac b{\sin B}=\frac c{\sin C}=2R", r"a^2=b^2+c^2-2bc\cos A"], ["A、B、C 为三角形内角"], "可由已知边角计算其余边角。"),
    ],
    "complex": [
        math_item("algebraic-form", "definition", "复数的代数形式", "实部与虚部共同确定复数。", [r"z=a+bi", r"i^2=-1"]),
        math_item("equality", "theorem", "复数相等", "两个复数相等当且仅当其实部与虚部分别相等。", [r"a+bi=c+di\iff a=c,\ b=d"], [], "实部、虚部分别相等。"),
        math_item("operations", "formula", "复数四则运算", "加减按实部、虚部分别运算，乘除利用 i²=-1 和共轭复数化简。"),
        math_item("conjugate-modulus", "formula", "共轭复数与复数模", "共轭复数改变虚部符号，模表示复平面中点到原点的距离。", [r"\bar z=a-bi", r"|z|=\sqrt{a^2+b^2}", r"z\bar z=|z|^2"]),
        math_item("complex-plane", "model", "复数的几何意义", "复数 a+bi 与复平面上的点 (a,b) 或从原点出发的向量对应。"),
    ],
    "solid-geometry": [
        math_item("line-plane-parallel", "theorem", "直线与平面平行判定", "平面外一直线若平行于平面内一直线，则该直线平行于此平面。", [], ["直线不在平面内", "平面内存在与之平行的直线"], "直线与平面平行。"),
        math_item("planes-parallel", "theorem", "平面与平面平行判定", "一个平面内两条相交直线分别平行于另一平面，则两平面平行。", [], ["两条直线相交", "两直线均平行于另一平面"], "两个平面平行。"),
        math_item("line-plane-perpendicular", "theorem", "直线与平面垂直判定", "一直线若垂直于平面内两条相交直线，则垂直于此平面。", [], ["平面内两条直线相交", "给定直线分别与二者垂直"], "直线与平面垂直。"),
        math_item("volume", "formula", "柱、锥体积", "柱体体积等于底面积乘高，锥体体积是同底等高柱体的三分之一。", [r"V_{柱}=Sh", r"V_{锥}=\frac13Sh"]),
        math_item("sphere", "formula", "球的表面积与体积", "球的度量只由半径决定。", [r"S=4\pi R^2", r"V=\frac43\pi R^3"]),
    ],
    "statistics": [
        math_item("sampling", "method", "随机抽样", "简单随机抽样、分层随机抽样等方法用于获得具有代表性的样本。"),
        math_item("mean", "formula", "平均数", "平均数刻画一组数据的集中位置。", [r"\bar x=\frac1n\sum_{i=1}^n x_i"]),
        math_item("variance", "formula", "方差与标准差", "方差和标准差刻画数据相对平均数的离散程度。", [r"s^2=\frac1n\sum_{i=1}^n(x_i-\bar x)^2", r"s=\sqrt{s^2}"]),
        math_item("percentile", "definition", "百分位数", "第 p 百分位数把按大小排列的数据划分，使约 p% 的数据不超过该值。"),
        math_item("correlation", "concept", "相关关系", "散点图和相关系数描述两个变量线性相关的方向与强弱，但相关不等于因果。", [r"-1\le r\le1"]),
    ],
    "probability": [
        math_item("events", "definition", "样本空间与随机事件", "样本空间由全部可能结果构成，事件是样本空间的子集。"),
        math_item("addition", "theorem", "概率加法公式", "两个事件并集的概率需要扣除重复计算的交集。", [r"P(A\cup B)=P(A)+P(B)-P(A\cap B)"], [], "给出任意两个事件并集的概率。"),
        math_item("conditional", "definition", "条件概率", "在事件 B 已发生条件下重新计算事件 A 的概率。", [r"P(A\mid B)=\frac{P(A\cap B)}{P(B)}"], [r"P(B)>0"]),
        math_item("independence", "theorem", "事件独立性", "独立事件同时发生的概率等于各自概率之积。", [r"P(A\cap B)=P(A)P(B)"], ["A 与 B 相互独立"], "A、B 同时发生的概率可相乘。"),
        math_item("total-probability", "formula", "全概率公式", "把复杂事件按互斥且完备的条件分解后求概率。", [r"P(A)=\sum_iP(B_i)P(A\mid B_i)"], [r"\{B_i\}\text{ 构成样本空间的一个划分}"]),
    ],
    "space-vector": [
        math_item("coordinates", "formula", "空间向量坐标", "在空间直角坐标系中用三个坐标表示向量。", [r"\vec a=(x,y,z)"]),
        math_item("dot-product", "formula", "空间向量数量积", "坐标乘积之和等于向量数量积。", [r"\vec a\cdot\vec b=x_1x_2+y_1y_2+z_1z_2"]),
        math_item("direction-normal", "method", "方向向量与法向量", "用直线方向向量和平面法向量把空间位置关系转化为向量关系。"),
        math_item("line-plane-angle", "formula", "直线与平面所成角", "直线方向向量与平面法向量的夹角可求线面角。", [r"\sin\theta=\frac{|\vec a\cdot\vec n|}{|\vec a||\vec n|}"]),
        math_item("point-plane-distance", "formula", "点到平面的距离", "点到平面的距离可由平面一般方程直接计算。", [r"d=\frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}"]),
    ],
    "line-circle": [
        math_item("line-equations", "formula", "直线方程", "根据已知条件选择点斜式、斜截式或一般式。", [r"y-y_0=k(x-x_0)", r"Ax+By+C=0"]),
        math_item("distance", "formula", "点到直线的距离", "代入点坐标并除以法向量长度。", [r"d=\frac{|Ax_0+By_0+C|}{\sqrt{A^2+B^2}}"]),
        math_item("circle-equation", "formula", "圆的标准方程", "圆心和半径唯一确定一个圆。", [r"(x-a)^2+(y-b)^2=r^2"]),
        math_item("position", "method", "直线与圆的位置关系", "比较圆心到直线的距离 d 与半径 r，判断相交、相切或相离。", [r"d<r", r"d=r", r"d>r"]),
        math_item("tangent", "theorem", "圆的切线性质", "圆的切线垂直于经过切点的半径。", [], ["直线与圆相切"], "切线与切点半径垂直。"),
    ],
    "conic": [
        math_item("ellipse", "formula", "椭圆定义与标准方程", "到两个定点距离之和为常数的点的轨迹是椭圆。", [r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1", r"a^2=b^2+c^2"], [r"a>b>0"]),
        math_item("hyperbola", "formula", "双曲线定义与标准方程", "到两个定点距离之差的绝对值为常数的点的轨迹是双曲线。", [r"\frac{x^2}{a^2}-\frac{y^2}{b^2}=1", r"c^2=a^2+b^2"]),
        math_item("parabola", "formula", "抛物线定义与标准方程", "到定点与到定直线距离相等的点的轨迹是抛物线。", [r"y^2=2px\quad(p>0)"]),
        math_item("eccentricity", "formula", "圆锥曲线离心率", "离心率刻画圆锥曲线的形状。", [r"e=\frac ca", r"0<e<1\text{（椭圆）}", r"e>1\text{（双曲线）}"]),
        math_item("locus", "method", "轨迹方程求法", "设动点坐标，根据几何条件列等式，化简后检查范围与特殊点。"),
    ],
    "sequence": [
        math_item("general-term", "concept", "数列与通项公式", "数列可看作定义在正整数集或其有限子集上的函数。", [r"a_n=f(n)"]),
        math_item("arithmetic", "formula", "等差数列通项", "相邻两项之差为同一常数。", [r"a_n=a_1+(n-1)d"]),
        math_item("arithmetic-sum", "formula", "等差数列前 n 项和", "首末项平均数乘项数得到前 n 项和。", [r"S_n=\frac{n(a_1+a_n)}2=na_1+\frac{n(n-1)}2d"]),
        math_item("geometric", "formula", "等比数列通项", "从第二项起后一项与前一项之比为同一非零常数。", [r"a_n=a_1q^{n-1}"]),
        math_item("geometric-sum", "formula", "等比数列前 n 项和", "公比不为 1 时使用等比求和公式。", [r"S_n=\frac{a_1(1-q^n)}{1-q}"], [r"q\ne1"]),
    ],
    "derivative": [
        math_item("definition", "definition", "导数的定义", "导数是函数增量与自变量增量之比的极限。", [r"f'(x_0)=\lim_{\Delta x\to0}\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}"]),
        math_item("basic", "formula", "基本初等函数的导数", "掌握幂函数、指数函数、对数函数和三角函数的常用导数。", [r"(x^n)'=nx^{n-1}", r"(e^x)'=e^x", r"(\ln x)'=\frac1x"]),
        math_item("rules", "formula", "导数运算法则", "和差、积、商与复合函数按相应法则求导。", [r"(uv)'=u'v+uv'", r"(\frac uv)'=\frac{u'v-uv'}{v^2}"]),
        math_item("monotonicity", "theorem", "导数与单调性", "在区间内导数保持正或负可判定函数递增或递减。", [r"f'(x)>0", r"f'(x)<0"], ["函数在区间内可导"], "导数为正时递增，导数为负时递减。"),
        math_item("extrema", "method", "用导数求极值与最值", "先找临界点，再检查导数符号变化，并结合端点比较函数值。"),
    ],
    "counting": [
        math_item("addition", "theorem", "分类加法计数原理", "完成一件事的各类办法互斥时，总方法数为各类方法数之和。", [r"N=m_1+m_2+\cdots+m_k"], ["分类完整且互斥"], "各类方法数相加。"),
        math_item("multiplication", "theorem", "分步乘法计数原理", "完成一件事需要依次完成各步骤时，总方法数为各步方法数之积。", [r"N=m_1m_2\cdots m_k"], ["每个方案必须完成全部步骤"], "各步方法数相乘。"),
        math_item("permutation", "formula", "排列数", "从 n 个不同元素中取出 m 个并按顺序排列。", [r"A_n^m=\frac{n!}{(n-m)!}"]),
        math_item("combination", "formula", "组合数", "从 n 个不同元素中取出 m 个组成一组，不计顺序。", [r"C_n^m=\frac{n!}{m!(n-m)!}"]),
        math_item("binomial", "theorem", "二项式定理", "二项式 n 次幂按组合数展开。", [r"(a+b)^n=\sum_{k=0}^nC_n^ka^{n-k}b^k"], [r"n\in\mathbb N^*"], "展开式共有 n+1 项。"),
    ],
    "random-variable": [
        math_item("distribution", "definition", "离散型随机变量分布列", "分布列列出随机变量所有可能取值及相应概率。", [r"P(X=x_i)=p_i", r"\sum_ip_i=1"]),
        math_item("expectation", "formula", "数学期望", "期望是随机变量取值按概率加权的平均。", [r"E(X)=\sum_ix_ip_i"]),
        math_item("variance", "formula", "随机变量的方差", "方差刻画随机变量取值相对期望的波动程度。", [r"D(X)=\sum_i(x_i-E(X))^2p_i"]),
        math_item("binomial", "formula", "二项分布", "n 次独立重复试验中成功次数服从二项分布。", [r"P(X=k)=C_n^kp^k(1-p)^{n-k}", r"E(X)=np", r"D(X)=np(1-p)"]),
        math_item("normal", "model", "正态分布", "正态密度曲线关于均值对称，标准差控制数据分散程度。", [r"X\sim N(\mu,\sigma^2)"]),
    ],
}


HISTORY_TOPICS = {
    "origins-qin-han": ["中华文明多元一体起源", "夏商周早期国家", "春秋战国社会变革", "秦朝统一与中央集权", "汉代大一统巩固"],
    "three-kingdoms-sui-tang": ["三国两晋南北朝政权更替", "北方民族交融", "隋朝统一与制度建设", "唐朝政治与经济发展", "隋唐中外文化交流"],
    "song-yuan": ["辽宋夏金政权并立", "宋代中央集权强化", "宋元经济与社会变化", "宋元科技文化", "元朝统一与行省制度"],
    "ming-qing": ["明朝政治制度变化", "清朝统一版图奠定", "明清商品经济发展", "明清思想文化", "海禁闭关与外部挑战"],
    "late-qing": ["鸦片战争与不平等条约", "太平天国运动", "洋务运动", "甲午战争与瓜分危机", "戊戌变法与义和团运动"],
    "republic": ["清末新政与革命形势", "辛亥革命进程", "中华民国建立", "《中华民国临时约法》", "北洋军阀统治与护国运动"],
    "cpc-revolution": ["五四运动", "中国共产党成立", "国共合作与国民革命", "南昌起义与秋收起义", "工农武装割据道路"],
    "anti-japanese-liberation": ["九一八事变与局部抗战", "全民族抗战形成", "正面战场与敌后战场", "抗日战争胜利及意义", "人民解放战争进程"],
    "prc-socialism": ["中华人民共和国成立", "人民政权巩固", "社会主义基本制度建立", "全面建设社会主义探索", "社会主义建设成就与经验"],
    "reform-opening": ["十一届三中全会", "农村与城市经济体制改革", "对外开放格局", "社会主义市场经济体制", "新时代中国特色社会主义"],
    "ancient-civilizations": ["西亚与埃及文明", "古代印度文明", "古代希腊文明", "古代帝国扩张", "文明交流与区域联系"],
    "medieval-world": ["西欧封建社会", "拜占庭与俄罗斯", "阿拉伯帝国与伊斯兰文化", "中古时期的亚洲国家", "古代非洲与美洲文明"],
    "global-world": ["新航路开辟动因", "主要航海活动", "人口迁移与物种交换", "早期殖民扩张", "世界市场初步形成"],
    "capitalist-system": ["文艺复兴与宗教改革", "近代科学与启蒙运动", "英国资产阶级革命", "美国独立与共和制度", "法国大革命与拿破仑时代"],
    "industrial-marxism": ["第一次工业革命", "第二次工业革命", "工业社会生活变化", "工人运动发展", "马克思主义诞生"],
    "colonial-resistance": ["拉丁美洲独立运动", "亚洲殖民体系形成", "非洲被瓜分", "亚洲觉醒", "世界殖民体系形成与反抗"],
    "world-wars": ["第一次世界大战", "凡尔赛—华盛顿体系", "俄国十月革命", "第二次世界大战", "雅尔塔体系与联合国"],
    "twentieth-century": ["冷战与两极格局", "社会主义国家发展与改革", "殖民体系瓦解", "资本主义国家新变化", "社会运动与科技文化"],
    "contemporary-world": ["世界多极化趋势", "经济全球化", "社会信息化与文化多样性", "全球治理体系", "人类面临的共同挑战"],
    "political-systems": ["先秦到秦汉政治制度", "隋唐到明清政治制度", "古希腊罗马政治制度", "近代西方政治制度", "近现代中国政治制度"],
    "official-selection": ["察举制与九品中正制", "科举制", "古代官员考核监察", "西方文官制度", "近现代中国公务员制度"],
    "law-education": ["先秦秦汉法律与教化", "魏晋隋唐法律体系", "宋元明清法律教化", "近代西方法律制度", "当代中国法治与精神文明"],
    "ethnic-diplomacy": ["中国古代民族关系", "中国古代边疆治理", "中国古代对外交往", "近代国际法与外交制度", "当代中国民族与外交政策"],
    "currency-tax": ["中国古代货币演进", "世界货币体系", "中国古代赋役制度", "近代关税与个人所得税", "货币赋税与国家治理"],
    "grassroots-social": ["中国古代基层组织", "中国古代社会救济", "西方基层治理", "现代社会保障制度", "当代中国基层治理"],
    "food-production": ["农业与畜牧业起源", "不同区域食物生产", "美洲作物全球传播", "现代农业与食品工业", "食物生产的社会影响"],
    "production-tools": ["古代农业工具", "手工业工具与分工", "机器大生产", "自动化与人工智能", "劳作方式和生产关系"],
    "commerce-trade": ["古代商业贸易", "世界市场形成", "货币信贷与金融", "现代商业经营", "商业贸易与日常生活"],
    "village-city": ["村落形成", "古代城市发展", "近代城市化", "居住条件改善", "城市治理与环境问题"],
    "transport": ["古代陆路交通", "古代水路与海路", "铁路与轮船", "汽车航空与高速交通", "交通对社会变迁的影响"],
    "medicine-health": ["传统医学成就", "近代西医发展", "疫病与社会", "公共卫生体系", "现代医疗保障"],
    "civilization-origins": ["中华文化的起源", "儒家思想发展", "中华文化的多民族交融", "中外文化交流", "中华文化的连续性与包容性"],
    "culture-world": ["西亚北非文化", "欧洲文化", "南亚文化", "东亚文化", "美洲文化"],
    "population-culture": ["古代人口迁徙", "印欧人迁徙", "近代跨洲人口迁徙", "华工与华人社会", "文化交融与身份认同"],
    "commerce-culture": ["丝绸之路", "欧亚草原商路", "海上丝绸之路", "近代世界贸易网络", "商品与文化传播"],
    "war-culture": ["古代战争与区域文化", "蒙古西征", "近代殖民战争", "两次世界大战中的文化", "战争后的文化重构"],
    "heritage": ["学校教育与文化传承", "印刷书籍与图书馆", "博物馆发展", "世界文化遗产保护", "非物质文化遗产传承"],
}


def history_item_type(topic: str) -> str:
    if any(keyword in topic for keyword in ("制度", "体系", "法律", "约法", "政策")):
        return "institution"
    if any(keyword in topic for keyword in ("战争", "革命", "运动", "事变", "起义")):
        return "event"
    if any(keyword in topic for keyword in ("影响", "意义", "作用", "变化", "成就", "挑战", "问题")):
        return "impact"
    if any(keyword in topic for keyword in ("形成", "发展", "建立", "演进", "传播", "扩张", "迁徙", "交融", "变迁", "改革", "建设", "巩固", "瓦解")):
        return "process"
    return "concept"


def history_items(chapter_slug: str, chapter_name: str):
    topics = HISTORY_TOPICS[chapter_slug]
    return [
        {
            "id": f"topic-{index}",
            "type": history_item_type(topic),
            "name": topic,
            "content": f"围绕“{topic}”梳理其时空背景、核心内容及其在“{chapter_name}”历史进程中的作用。",
            "review_status": "self_checked",
        }
        for index, topic in enumerate(topics, 1)
    ]
