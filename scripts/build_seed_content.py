#!/usr/bin/env python3
"""Build the reviewed seed corpus into one YAML file per knowledge point."""
from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


MATH = [
    ("required-1", "必修第一册", [
        ("sets-logic", "集合与常用逻辑用语", "集合、命题和充分必要条件", "用元素与集合的关系、集合运算和逻辑联结词准确表达数学对象", "混淆元素与集合、充分条件与必要条件"),
        ("inequality", "一元二次函数、方程和不等式", "二次关系与不等式", "结合函数图象、方程根与不等式解集研究二次关系", "忽略二次项系数符号或端点取值"),
        ("function", "函数的概念与性质", "函数概念及基本性质", "从对应关系、定义域、值域理解函数并判断单调性、奇偶性和最值", "只看解析式而忽略定义域"),
        ("exp-log", "幂函数、指数函数和对数函数", "幂、指数与对数函数", "利用运算规则和图象性质研究增长变化并解决实际问题", "忽略底数范围和真数大于零的条件"),
        ("trigonometry", "三角函数", "任意角三角函数", "用单位圆理解三角函数，掌握图象、性质和基本恒等变换", "角度制与弧度制混用或漏写周期"),
    ]),
    ("required-2", "必修第二册", [
        ("vector", "平面向量及其应用", "平面向量及运算", "从方向和大小理解向量，使用线性运算、数量积解决几何问题", "把向量相等误认为起点和终点都相同"),
        ("complex", "复数", "复数概念与运算", "理解复数的代数形式及几何意义，正确完成四则运算", "把虚数单位当作普通未知数而错误处理平方"),
        ("solid-geometry", "立体几何初步", "空间点线面关系", "借助空间图形、公理和判定定理研究平行与垂直", "仅凭直观图形下结论而缺少条件"),
        ("statistics", "统计", "数据分析与统计量", "根据数据特征选择抽样和统计图表，用数字特征解释总体", "用样本结论替代总体结论而不说明随机性"),
        ("probability", "概率", "随机事件与概率", "识别样本空间和事件关系，运用概率规则刻画随机现象", "把互斥事件与独立事件混为一谈"),
    ]),
    ("selective-1", "选择性必修第一册", [
        ("space-vector", "空间向量与立体几何", "空间向量及坐标方法", "建立空间直角坐标系，用向量表示位置关系并计算角与距离", "法向量方向选取错误或忽略夹角范围"),
        ("line-circle", "直线和圆的方程", "直线与圆的解析表示", "在平面直角坐标系中用方程研究直线、圆及其位置关系", "斜率不存在时仍套用斜截式"),
        ("conic", "圆锥曲线与方程", "椭圆、双曲线和抛物线", "从定义建立标准方程，并结合几何性质解决轨迹和最值问题", "未先判断焦点位置就套用标准方程"),
    ]),
    ("selective-2", "选择性必修第二册", [
        ("sequence", "数列", "数列及递推关系", "从函数观点研究数列，掌握等差、等比数列和常见求和方法", "混淆项数、末项和下标"),
        ("derivative", "一元函数的导数及其应用", "导数与函数变化", "理解导数的几何意义，用导数研究单调性、极值和实际优化", "把导数为零直接等同于取得极值"),
        ("counting", "计数原理", "分类、分步与排列组合", "根据事件过程选择分类或分步计数，并正确处理排列组合", "重复计数或遗漏互斥分类"),
        ("random-variable", "随机变量及其分布", "离散型随机变量", "建立随机变量分布列并计算数字特征，理解常见概率模型", "概率之和不为一或忽略随机变量取值范围"),
    ]),
]


HISTORY = [
    ("outline-1", "中外历史纲要（上）", [
        ("origins-qin-han", "从中华文明起源到秦汉统一多民族封建国家的建立与巩固", "早期国家到秦汉统一", "从多元一体文明起源、制度演进和统一国家形成理解中华文明早期发展", "只记年代而忽视统一多民族国家形成的历史联系"),
        ("three-kingdoms-sui-tang", "三国两晋南北朝的民族交融与隋唐统一多民族封建国家的发展", "分裂交融与隋唐发展", "分析政权更替、民族交融、制度创新和开放交流对隋唐发展的影响", "把分裂时期简单理解为社会完全停滞"),
        ("song-yuan", "辽宋夏金多民族政权的并立与元朝的统一", "多民族政权并立与统一", "从政治、经济和文化互动理解宋元时期统一趋势与社会变化", "只用单一政权视角解释多民族互动"),
        ("ming-qing", "明清中国版图的奠定与面临的挑战", "明清治理、经济与挑战", "认识统一版图巩固、社会经济变化及传统体制面临的内外挑战", "把明清经济发展等同于已完成近代转型"),
        ("late-qing", "晚清时期的内忧外患与救亡图存", "民族危机与近代探索", "结合列强侵略、社会变动和救亡实践理解近代中国转型的艰难", "孤立评价某次探索而忽略时代条件和连续性"),
        ("republic", "辛亥革命与中华民国的建立", "共和革命与民国初建", "评价辛亥革命的历史意义与局限，理解民国初年政治变迁", "用是否立即改变社会性质作为唯一评价标准"),
        ("cpc-revolution", "中国共产党成立与新民主主义革命兴起", "中国共产党与革命道路探索", "理解中国共产党成立、国民革命和革命道路探索之间的联系", "把革命道路形成看成一次性完成"),
        ("anti-japanese-liberation", "中华民族的抗日战争和人民解放战争", "民族抗战与人民解放", "从全民族抗战和中国共产党作用理解民族独立与人民解放进程", "忽视正面战场和敌后战场的相互配合"),
        ("prc-socialism", "中华人民共和国成立和社会主义革命与建设", "新中国建立与社会主义建设", "认识政权巩固、制度建立和建设探索的成就、曲折及经验", "割裂成就、曲折与探索背景"),
        ("reform-opening", "改革开放与社会主义现代化建设新时期", "改革开放与现代化", "从制度创新、对外开放和社会发展理解中国特色社会主义道路", "把改革理解为单一领域或一次性政策调整"),
    ]),
    ("outline-2", "中外历史纲要（下）", [
        ("ancient-civilizations", "古代文明的产生与发展", "多元古代文明", "比较不同自然和社会条件下古代文明及帝国的发展", "用单线进化模式评价所有文明"),
        ("medieval-world", "中古时期的世界", "中古世界的区域发展", "比较欧洲、亚洲和非洲、美洲不同区域的政治经济文化", "把中古世界等同于欧洲历史"),
        ("global-world", "走向整体的世界", "新航路与全球联系", "分析新航路开辟、早期殖民扩张和世界联系增强的多重影响", "只从欧洲受益角度评价全球联系"),
        ("capitalist-system", "资本主义制度的确立", "思想解放与制度变革", "理解思想解放、资产阶级革命和资本主义制度建立之间的联系", "把不同国家制度确立道路视为完全相同"),
        ("industrial-marxism", "工业革命与马克思主义的诞生", "工业化、社会转型与马克思主义", "分析工业革命对生产、阶级和世界格局的影响及马克思主义产生背景", "只关注技术发明而忽略社会关系变化"),
        ("colonial-resistance", "世界殖民体系与亚非拉民族独立运动", "殖民扩张与民族抗争", "理解世界殖民体系形成及亚非拉人民争取民族独立的实践", "把各地民族运动视为同一模式"),
        ("world-wars", "两次世界大战与国际秩序的演变", "世界大战与国际秩序", "从矛盾演变、战争进程和战后安排理解国际秩序变化", "只用单一事件解释战争爆发"),
        ("twentieth-century", "20世纪下半叶世界的新变化", "冷战、民族解放与社会变革", "理解冷战格局、社会主义发展、民族独立和资本主义调整", "把冷战理解为美苏直接全面战争"),
        ("contemporary-world", "当代世界发展的特点与主要趋势", "多极化与全球化", "从和平发展、全球治理和人类共同挑战认识当代世界趋势", "把趋势等同于已经完成的固定格局"),
    ]),
    ("selective-1", "选择性必修1 国家制度与社会治理", [
        ("political-systems", "政治制度", "中外政治制度演进", "比较政治制度形成、运行和变革，认识制度与国情的关系", "脱离时代背景简单比较制度优劣"),
        ("official-selection", "官员的选拔与管理", "选官与官员管理", "梳理中外官员选拔、考核和监察制度的演进与影响", "把制度规定等同于实际执行效果"),
        ("law-education", "法律与教化", "法律体系与社会教化", "比较法律和教化在国家治理中的作用及互动", "把法律与教化理解为彼此排斥"),
        ("ethnic-diplomacy", "民族关系与国家关系", "民族治理与对外交往", "认识民族关系、边疆治理和外交制度与统一国家发展的联系", "以现代国界观念机械解释古代关系"),
        ("currency-tax", "货币与赋税制度", "货币、财政与国家治理", "分析货币形态和赋税制度变化对经济社会及国家治理的影响", "只记税种名称而忽略征收基础变化"),
        ("grassroots-social", "基层治理与社会保障", "基层组织与社会保障", "比较基层治理和社会救济、保障制度的历史演进", "把传统救济与现代社会保障完全等同"),
    ]),
    ("selective-2", "选择性必修2 经济与社会生活", [
        ("food-production", "食物生产与社会生活", "农业起源与食物体系", "理解食物生产方式演变对人类社会结构和生活的影响", "把农业出现理解为各地区同时发生"),
        ("production-tools", "生产工具与劳作方式", "工具进步与劳作变迁", "分析生产工具、能源和组织方式变化对生产关系的影响", "用技术进步单因素解释全部社会变化"),
        ("commerce-trade", "商业贸易与日常生活", "商业网络与生活变化", "理解商业、金融和世界市场发展如何改变社会生活", "只关注商品数量而忽略制度与网络"),
        ("village-city", "村落、城镇与居住环境", "聚落与城市发展", "从生产、交通和治理分析村落城镇及居住环境演变", "用现代城市标准评价所有古代聚落"),
        ("transport", "交通与社会变迁", "交通网络与社会联系", "认识交通工具和道路网络对经济、政治与文化交流的影响", "只讨论速度而忽略空间联系重组"),
        ("medicine-health", "医疗与公共卫生", "医学、疫病与公共卫生", "比较医学发展和公共卫生体系对人类健康及社会治理的作用", "用今天的医学知识苛求历史医疗实践"),
    ]),
    ("selective-3", "选择性必修3 文化交流与传播", [
        ("civilization-origins", "源远流长的中华文化", "中华文化的形成与特征", "从连续性、包容性和多民族互动理解中华文化发展", "把中华文化理解为封闭不变的单一传统"),
        ("culture-world", "丰富多样的世界文化", "世界文化的多样性", "比较不同区域文化形成条件、主要成就和历史影响", "用单一文化尺度评价所有文明"),
        ("population-culture", "人口迁徙、文化交融与认同", "迁徙、交融与文化认同", "分析人口迁徙对文化传播、族群交融和认同建构的影响", "把文化交融理解为原有文化完全消失"),
        ("commerce-culture", "商路、贸易与文化交流", "贸易网络与文化传播", "理解陆海商路和贸易活动在跨区域文化交流中的作用", "只关注商品交换而忽略人员与观念流动"),
        ("war-culture", "战争与文化交锋", "战争中的文化互动", "辩证分析战争对文化破坏、传播和重构的复杂影响", "把战争影响简单概括为单向传播"),
        ("heritage", "文化传承的多种载体及其发展", "教育、书籍、博物馆与遗产", "认识文化传承载体演变及文化遗产保护的公共意义", "把文化遗产保护等同于拒绝合理利用"),
    ]),
]


def slug_label(value: str) -> str:
    return value.replace("-", " ")


def questions(point_id: str, name: str, core: str, objective: str, mistake: str, subject: str):
    method = "结合定义、图象和条件逐步推理" if subject == "math" else "结合时空背景、史料和因果关系综合分析"
    unrelated = ["只背结论，不检查适用条件", "只凭直觉，不使用证据", "把局部现象直接推广为普遍规律"]
    data = [
        ("q1", f"学习“{name}”时，最需要把握的核心内容是（ ）。", core, ["孤立记忆章节标题", "只关注书写格式", "回避概念之间的联系"], "basic", f"该知识点的核心是“{core}”，其余选项都没有触及主要学习对象。"),
        ("q2", f"研究“{name}”时，下列学习方法最恰当的是（ ）。", method, unrelated, "basic", f"{method}能够同时关注概念、条件与论证，是本知识点的有效学习方法。"),
        ("q3", f"关于“{name}”的学习，下列做法最需要避免的是（ ）。", mistake, ["先明确问题所处情境", "用证据检验初步判断", "完成后复核结论与条件"], "medium", f"“{mistake}”会造成典型理解偏差，其他做法都有助于形成可靠结论。"),
        ("q4", f"要达成“{name}”的学习目标，较合理的步骤是（ ）。", f"先明确关键概念，再分析关系，最后用新情境检验结论", ["先猜答案，再寻找支持猜测的片段", "跳过条件，直接套用记忆中的结论", "只完成一道例题，不总结方法"], "medium", f"由概念到关系再到迁移检验，符合“{objective}”所要求的认知过程。"),
        ("q5", f"把“{name}”迁移到新问题时，最可靠的判断依据是（ ）。", "结论能够由明确条件和完整证据链支持", ["结论与熟悉题目的答案相同", "表述中出现了本章关键词", "多数同学选择了同一选项"], "advanced", "迁移不是套用表面特征；只有条件明确、证据链完整，结论才具有可靠性。"),
    ]
    result = []
    for suffix, stem, correct, distractors, difficulty, explanation in data:
        option_texts = [correct, *distractors]
        # Rotate the answer position deterministically to avoid a fixed answer pattern.
        rotation = (sum(ord(char) for char in point_id + suffix) % 4)
        option_texts = option_texts[rotation:] + option_texts[:rotation]
        option_ids = ["A", "B", "C", "D"]
        correct_id = option_ids[option_texts.index(correct)]
        result.append({
            "id": f"{point_id}.{suffix}",
            "stem": stem,
            "options": [
                {"id": option_id, "text": text}
                for option_id, text in zip(option_ids, option_texts, strict=True)
            ],
            "correct_option_id": correct_id,
            "explanation": explanation,
            "difficulty": difficulty,
            "tags": [name, core],
            "source_type": "original",
        })
    return result


def build(subject: str, curriculum_id: str, prefix: str, publisher: str, volumes):
    target = ROOT / "curricula" / subject / ("xj-current" if subject == "math" else "pep-current")
    points_dir = target / "knowledge_points"
    points_dir.mkdir(parents=True, exist_ok=True)
    for old in points_dir.glob("*.yaml"):
        old.unlink()
    catalog = {"curriculum_id": curriculum_id, "subject": subject, "volumes": []}
    for volume_id, volume_name, chapters in volumes:
        volume = {"id": f"{prefix}.{volume_id}", "name": volume_name, "chapters": []}
        for order, (slug, chapter_name, core, objective, mistake) in enumerate(chapters, 1):
            point_id = f"{prefix}.{volume_id}.{slug}"
            chapter_id = f"{prefix}.{volume_id}.chapter-{order}"
            section_id = f"{chapter_id}.section-1"
            volume["chapters"].append({
                "id": chapter_id,
                "name": chapter_name,
                "sections": [{
                    "id": section_id,
                    "name": f"{chapter_name}核心知识",
                    "knowledge_points": [point_id],
                }],
            })
            point = {
                "id": point_id,
                "subject": subject,
                "curriculum_id": curriculum_id,
                "name": chapter_name,
                "summary": f"本知识点围绕{core}展开，重点是{objective}，并能在新的问题情境中说明条件、过程与结论之间的联系。",
                "objectives": [objective, "能够识别典型条件并用规范语言说明判断依据"],
                "prerequisites": ["初中阶段相关基础知识", "基本阅读、表达与推理能力"],
                "common_mistakes": [mistake],
                "keywords": [core, chapter_name],
                "competency_tags": ["数学抽象", "逻辑推理"] if subject == "math" else ["时空观念", "史料实证", "历史解释"],
                "review_status": "self_checked",
                "reference": {
                    "publisher": publisher,
                    "edition_scope": "现行普通高中教科书",
                    "chapter": f"{volume_name}·{chapter_name}",
                },
                "questions": questions(point_id, chapter_name, core, objective, mistake, subject),
            }
            (points_dir / f"{point_id}.yaml").write_text(
                yaml.safe_dump(point, allow_unicode=True, sort_keys=False, width=120),
                encoding="utf-8",
            )
        catalog["volumes"].append(volume)
    (target / "catalog.yaml").write_text(
        yaml.safe_dump(catalog, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def main():
    build("math", "xj-math-current", "math.xj", "湖南教育出版社", MATH)
    build("history", "pep-history-current", "history.pep", "人民教育出版社", HISTORY)


if __name__ == "__main__":
    main()
