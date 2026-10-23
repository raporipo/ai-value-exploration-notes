"""Regenerate bilingual figures and self-contained semantics; no JS or network needed.

Edit the approved SVGs in docs/assets/diagrams and the descriptions below together.
Run from any directory: python scripts/embed_concept_diagrams.py
"""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = {
    'informs': 'Provides input to a judgment; does not determine it alone.',
    'coordinates': 'Combines functions within one plan.',
    'uses_criteria': 'Uses practical criteria in evaluation.',
    'next': 'Next procedural step, not logical entailment.',
    'revises': 'Reassesses or revises the target.',
    'requires': 'The target is necessary for the source, not necessarily sufficient.',
    'supports_or_revises': 'Supports or revises through reasons and evidence.',
    'reflectively_identifies': 'Identifies the target through reflective judgment.'
}
DATA = [
    {
        'id': 'epx-structure', 'svg': 'epx-structure',
        'page': 'theses/inquiry-allocation-under-uncertainty/index.html',
        'before': r'<h3[^>]*>4\.2\b',
        'titles': ['E・P・Xを支える判断の構造', 'The reasoning behind E / P / X'],
        'captions': ['認識的支持、意思決定上の理由、主体側の応答態度を区別し、E・P・Xを一つの計画へ組み合わせる。', 'Distinguish epistemic support, decision-theoretic reasons, and agent responsiveness when bringing E, P, and X into one plan.'],
        'descriptions': [
            ['証拠・推論、仮説空間の不完全性、未概念化の可能性は認識論的支持に関係する。比較可能性、情報価値、不可逆性、危険、機会費用、保存費用は意思決定上の検討材料となる。現在の目的・選好・関心、正当化への条件付き応答性、反省的誤り回避は主体側の前提である。', '三つの入力を照らし合わせ、E（能動探索）、P（探索可能性保存）、X（現在の実践）を組み合わせる。一つの活動が複数の機能に寄与しうる。', 'Xでは表象可能な各仮説の下で承認する実践基準を用いる。選好・関心・協力、主体の存在を条件とする福利重視、契約主義、義務論、総量功利主義、徳倫理は例示であり、排他的・網羅的な分類ではない。', '認識的支持、評価重み、資源配分率は別である。箱の面積は配分率を表さない。未概念化の可能性は具体的な行為基準を与えず、不確実性だけから探索・保存の動機は生じない。'],
            ['Evidence and reasoning, incomplete hypothesis spaces, and unconceptualized possibilities bear on epistemic support. Comparability, information value, irreversibility, risk, opportunity costs, and preservation costs inform decision-theoretic evaluation. Current goals, preferences, concerns, conditional responsiveness to justification, and avoidance of reflective error are agent-side premises.', 'These inputs inform a plan combining E (active inquiry), P (preserving explorability), and X (present practice). An activity may serve several functions.', 'X uses practical criteria endorsed under represented hypotheses. Preferences, concerns, cooperation, welfare conditional on subjects existing, contractualism, deontology, total utilitarianism, and virtue ethics are nonexclusive, nonexhaustive examples.', 'Epistemic support, evaluation weights, and resource shares are distinct. Box area encodes no allocation ratio. Unconceptualized possibilities provide no determinate action criterion; uncertainty alone supplies no motivation for inquiry or preservation.']
        ],
        'semantics': {
            'nodes': {'K':'Epistemic support: what to believe and how strongly','D':'Decision-theoretic support: which choices are justified','A':'Agent preferences and responsiveness','PLAN':'Reflective allocation and planning','E':'Active inquiry','P':'Preservation of future inquiry and revision capacities','X':'Present practice under current goals and value judgments','XC':'Practical criteria endorsed under represented hypotheses'},
            'considerations': {'K':['evidence and reasoning','incomplete hypothesis space','unconceptualized possibilities'],'D':['comparability and value of information','irreversibility and risk','opportunity and preservation costs'],'A':['current goals, preferences, and concerns','conditional responsiveness to justification','avoidance of reflective error']},
            'relations': [['K','informs','PLAN'],['D','informs','PLAN'],['A','informs','PLAN'],['PLAN','coordinates','E'],['PLAN','coordinates','P'],['PLAN','coordinates','X'],['X','uses_criteria','XC']],
            'criteria_examples': ['preferences, concerns, and cooperation','welfare conditional on subjects existing','contractualism','deontology','total utilitarianism','virtue ethics'],
            'constraints': ['E, P, and X are overlapping functions, not exclusive action classes.','Epistemic support, evaluation weights, and resource shares are distinct.','Unconceptualized possibilities supply no determinate action criterion.','Criteria examples are neither exhaustive nor mutually exclusive.','Box size encodes no allocation ratio.','Uncertainty alone does not entail motivation for inquiry or preservation.']
        }
    },
    {
        'id':'practice-cycle', 'svg':'practice-cycle', 'page':'practice/index.html',
        'before':r'<h2[^>]*>2\. ',
        'titles':['判断を、見直せる実践へ','From judgment to revisable action'],
        'captions':['現在の最善判断で行動し、観測・記録を通じて必要な前提を更新する。','Act on the best current judgment and update relevant premises through observation and records.'],
        'descriptions': [
            ['目的と応答態度、世界認識と因果仮説、選択肢・資源・制約を入力とする。E・P・Xを組み合わせた候補を、代替案と不作為の効果、費用、負担、不可逆性に照らして比較する。','計画には今すること、訂正・退出・復旧の経路、観測項目、見直し条件を含める。実行して結果を記録し、前提の変化を観測する。','関連する新しい証拠、誤り、実行可能性や価値理解の変化があれば入力を更新して比較・計画に戻る。なければ履歴を引き継いで継続する。達成済みの便益を新規の便益として数え直さない。','矢印は手続きであり論理的含意ではない。比較・数値化には正当化できる範囲を用い、共有資源では権限・参加・同意・外部性も点検する。'],
            ['Inputs are goals and responsiveness, worldviews and causal hypotheses, and options, resources, and constraints. Compare plans combining E, P, and X with alternatives and inaction in terms of effects, costs, burdens, and irreversibility.','The plan specifies present action, routes for revision, exit, and recovery, observations, and review triggers. Act, record outcomes, and monitor premises.','Relevant new evidence, errors, or changes in feasibility or value understanding trigger updated inputs and renewed comparison and planning. Otherwise continue with the existing history; do not count an achieved benefit again as new.','Arrows describe procedure, not entailment. Use justified comparisons and numerical precision. Shared decisions also require attention to authority, participation, consent, and externalities.']
        ],
        'semantics': {
            'states': {'INPUT':['goals and responsiveness','worldviews and causal hypotheses','options, resources, and constraints'],'COMPARE':['combine E, P, and X','compare alternatives and inaction','assess effects, costs, burdens, and irreversibility'],'PLAN':['select present action','preserve routes for revision, exit, and recovery','specify observations and review triggers'],'ACT':['act, record outcomes, and monitor premises','retain achievement history']},
            'transitions': [['INPUT','next','COMPARE'],['COMPARE','next','PLAN'],['PLAN','next','ACT'],['ACT','revises','INPUT','relevant evidence, error, or change'],['ACT','next','ACT','no relevant change']],
            'constraints':['Transitions describe a revisable procedure, not logical entailments.','Use only justified comparisons and numerical precision.','Do not reset history and recount an achieved benefit as new.','Shared decisions also require examination of authority, participation, consent, and externalities.']
        }
    },
    {
        'id':'epistemic-minimum', 'svg':'epistemic-minimum', 'page':'theses/epistemic-minimum/index.html',
        'before':r'<h2[^>]*>8\. ',
        'titles':['生起・関係構造・反省的な最小化','Occurrence, relations, and reflective minimization'],
        'captions':['推論に必要な関係構造と、その推論による最小点の同定を区別する。','Distinguish the relational conditions of inference from its reflective identification of the epistemic minimum.'],
        'descriptions': [
            ['中央を離した七枚の縦長フレームは瞬間の模式表現である。フレーム間の結びつきは差異・保持・相互拘束を表す。その関係構造から推論の領域へ必要条件の矢印が向く。関係構造があるだけで推論が成立するという十分条件は主張しない。','概念・推論・正当化の領域では、証拠、整合性、説明力、予測、介入成功を用いて世界像・主体像・価値像を支持・改訂する。三者は相互に改訂される。','反省的な最小化によって現在的生起を認識的限界点として捉え直す。「それが最小点である」というメタ判断も推論の領域に属し、生起そのものとは区別する。最小点だけから世界像・主体像・価値像を正当化しない。','生起のカテゴリー・実現基盤・主体境界は未指定である。左から右への時間軸は推論的モデル内の模式表現であり、最小点から時間が直接確定するとはしない。七枚は独立した最小実体の数ではなく、線の太さや距離も結びつきの強さの定量値ではない。'],
            ['Seven portrait frames with a separated central frame schematically represent moments. Their connections depict difference, retention, and mutual constraint. The arrow from this relational structure to inference marks a necessary condition, not a sufficient one.','Within concepts, inference, and justification, evidence, coherence, explanatory power, prediction, and successful intervention support or revise world, subject, and value models. These models undergo mutual revision.','Reflective minimization reidentifies present occurrence as an epistemic limit point. The meta-judgment identifying the minimum belongs within inference and is distinct from the occurrence itself. Occurrence alone does not justify the world, subject, or value models.','The occurrence’s category, substrate, and subject boundary remain unspecified. Left-to-right time is schematic within an inferential model, not directly established by the minimum. Seven frames do not assert seven independent minimal entities; distance and line thickness do not quantify relation strength.']
        ],
        'semantics': {
            'nodes':{'O':'Present occurrence or constraint','R':'Relational structure: difference, retention, mutual constraint','I':'Conceptual inference and justification','W':'World model','S':'Subject model','V':'Value model','M':'Meta-judgment identifying O as the epistemic minimum'},
            'relations':[['I','requires','R'],['I','supports_or_revises','W'],['I','supports_or_revises','S'],['I','supports_or_revises','V'],['M','reflectively_identifies','O']],
            'judgment_domain':{'M':'I'},'mutual_revision':['W','S','V'],
            'visual_encoding':{'frames':'Schematic moments; the central frame highlights O','connections':'Depict R; nearby connections are emphasized','time_arrow':'Left-to-right time within an inferential model'},
            'constraints':['R is necessary for I; sufficiency is not asserted.','O and the judgment M about O are distinct.','O alone does not justify W, S, or V.','The category, substrate, and subject boundary of O remain unspecified.','Seven frames do not assert seven independent minimal entities.','O does not directly establish the temporal model.','Visual distance and line thickness encode no quantitative strength.']
        }
    }
]

def payload(item):
    data=item['semantics']
    used={r[1] for r in data.get('relations',[])+data.get('transitions',[])}
    return {'format':'diagram-semantics/v1','id':item['id'],
            'notation':{'relation_tuple':['source','relation','target'],'transition_tuple':['source','relation','target','optional condition'],'omission':'Unspecified, not false.','judgment_domain':'Maps a judgment to the domain in which it is made.','mutual_revision':'Listed models are revised in relation to one another.','relation_definitions':{k:RELATIONS[k] for k in RELATIONS if k in used}},**data}

def main():
    for item in DATA:
        raw=json.dumps(payload(item),ensure_ascii=False,indent=2).replace('<','\\u003c')
        for lang,i in [('ja',0),('en',1)]:
            page=ROOT/'docs'/('en' if lang=='en' else '')/item['page']
            asset=ROOT/'docs/assets/diagrams'/f"{item['svg']}-{lang}.svg"
            svg=asset.read_text()
            # Keep HTML and SVG semantics identical; preserve approved drawing geometry.
            svg=re.sub(r'<metadata>.*?</metadata>', lambda m: '<metadata>'+escape(raw)+'</metadata>',svg,flags=re.S)
            asset.write_text(svg)
            view=ET.fromstring(svg).get('viewBox').split()
            width,height=view[2:]
            import os
            url=os.path.relpath(asset,page.parent).replace(os.sep,'/')
            ident='diagram-'+item['id']; title=item['titles'][i]; cap=item['captions'][i]
            details='図の内容を文章で読む' if lang=='ja' else 'Read a text description of the diagram'
            full='図を拡大して読む（SVG）' if lang=='ja' else 'Open the full-size diagram (SVG)'
            block=f'''<!-- {ident}:start -->
<figure class="concept-diagram" id="{ident}">
<a class="concept-diagram-image" href="{url}"><img src="{url}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{escape(title,quote=True)}" aria-describedby="{ident}-caption"/></a>
<figcaption id="{ident}-caption">{escape(cap)} <a href="{url}">{full}</a></figcaption>
<details class="concept-diagram-description"><summary>{details}</summary>
{''.join('<p>'+escape(t)+'</p>' for t in item['descriptions'][i])}
</details>
<script type="application/json" id="{ident}-semantics">
{raw}
</script>
</figure>
<!-- {ident}:end -->
'''
            content=page.read_text()
            pattern=rf'<!-- {ident}:start -->.*?<!-- {ident}:end -->\n?'
            if re.search(pattern,content,re.S):content=re.sub(pattern,lambda m:block,content,flags=re.S)
            else:
                match=re.search(item['before'],content)
                if not match:raise ValueError(f'Missing insertion point: {page}')
                content=content[:match.start()]+block+content[match.start():]
            page.write_text(content)

if __name__=='__main__':main()
