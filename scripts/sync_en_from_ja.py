from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def save(rel, text):
    (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"missing anchor for {label}")
    return text.replace(old, new, 1)


def insert_before_first_h2(rel, block, sentinel):
    text = load(rel)
    if sentinel in text:
        return
    pos = text.find("<h2>")
    if pos < 0:
        raise RuntimeError(f"no h2 anchor in {rel}")
    text = text[:pos] + block.strip() + "\n" + text[pos:]
    save(rel, text)


def update_meta(rel, version):
    text = load(rel)
    text, n = re.subn(r'(<p class="meta">[^<]*?)(v0\.\d+)([^<]*?</p>)', rf'\g<1>{version}\g<3>', text, count=1)
    if n != 1:
        raise RuntimeError(f"meta version not found in {rel}")
    text = re.sub(r'(<p class="meta">[^<]*?)(2026-\d\d-\d\d)([^<]*?</p>)', r'\g<1>2026-08-26\g<3>', text, count=1)
    text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
    save(rel, text)


# README: Japanese is canonical; avoid promising permanent completeness.
rel = "README.md"
text = load(rel)
text = text.replace("A **complete English working translation** is available under `docs/en/`.", "An **English working translation** is maintained under `docs/en/`. The Japanese pages are the canonical source when conceptual changes are introduced.")
save(rel, text)

# Core: propagate the Value Structure reframing without discarding later English edits.
rel = "docs/en/core/index.html"
text = load(rel)
text = text.replace("Distinguishes the epistemic minimum, inferential best explanations, stopping conditions for value inquiry, practical commitment, and irreversible lock-in.", "Distinguishes value structure, the epistemic minimum, inferential best explanations, stopping conditions for inquiry, practical commitment, and irreversible lock-in.")
text = text.replace("Working core · v0.8 · English translation · 2026-08-19", "Working core · v0.9 · English translation · 2026-08-26")
text = replace_once(text,
    "We do not know what ultimately has value. But that does not require believing nothing and doing nothing. Present world-models and theories of value can be adopted strongly, as best explanations reached through inference, and used in practice. The crucial distinction is between <strong>strong rational commitment to a best explanation</strong> and <strong>absolute lock-in that irreversibly destroys the possibility of future reconsideration</strong>.",
    "We do not know a sufficiently justified value structure: not only what is normatively important, but why it is a reason, for whom, and how such reasons are structured. But that does not require believing nothing and doing nothing. Present world-models and ethical theories can be adopted strongly, as best explanations reached through inference, and used in practice. The crucial distinction is between <strong>strong rational commitment to a best explanation</strong> and <strong>absolute lock-in that irreversibly destroys the possibility of future reconsideration</strong>.",
    "core lead")
text = replace_once(text,
    "So long as the values presently available to us belong to an inferential and fallible epistemic layer, we may act on their best explanation while refusing to irreversibly close the routes by which value can be discovered, criticized, or revised. If there is a kind of grounding strong enough to justify fully ending inquiry, one strong candidate would be a case in which value with normative force—not merely pleasure, pain, or preference—is given with epistemic strength comparable to the minimum foundation itself.",
    "So long as the value structure we presently adopt belongs to an inferential and fallible epistemic layer, we may act on its best explanation while refusing to irreversibly close the routes by which value structure can be discovered, criticized, redescribed, or revised. If grounding strong enough to justify fully ending inquiry is possible, it requires more than pleasure, pain, preference, or high probability inside the present theory set: the structure needed to answer the normative question at issue must be supported by sufficiently strong foundational presentation or logical closure.",
    "core claim")
anchor = '<h2>1. Separate epistemic layers in value as well</h2>'
new = '''<h2>1. “Value” in this project includes value structure</h2>
<p>Experiencing subjects encounter pain, pleasure, discomfort, desire, concern, meaning, preference, and other appearances that seem value-laden. But <strong>“this is unpleasant”</strong>, <strong>“this is normatively important”</strong>, <strong>“some subject has reason to avoid it”</strong>, and <strong>“that reason extends to other subjects, obligation, or aggregation in a particular way”</strong> are not the same proposition.</p>
<p>To keep these stages separate, this project provisionally represents a value structure as <code>𝒱 = (C, B, R)</code>. <strong>C</strong> is evaluative or normatively relevant content; <strong>B</strong> is the normative bridge connecting that content and world-facts to reasons; and <strong>R</strong> is the structure governing the scope, strength, competition, aggregation, permission, and obligation of reasons. This is a fallible working representation, not a claim that true normativity must literally decompose into exactly three ontological parts. See <a href="../theses/value-structure/">Value Structure</a>.</p>
<p>Unless context narrows the term, “value”, “value theory”, and “value inquiry” below include this wider value structure and possible alternative representations, not only first-order good/bad content C.</p>
<h3>Epistemic layers within a value structure</h3>'''
text = replace_once(text, anchor, new, "core value structure section")
text = replace_once(text,
    '<h2>2. Objective value might be discovered as a best explanation reached through inference</h2>',
    '<h2>2. Value structure may be discovered as a best explanation reached through inference</h2>\n<p>Even very strong evidence about C may leave unsettled the bridge B that makes it a reason, or the reason-structure R that determines whose reason it is and how it competes or aggregates. Confidence should therefore be component-sensitive rather than compressed into a single undifferentiated probability of “the value theory”.</p>',
    "core section 2")
text = replace_once(text,
    '<h2>3. Why not use existing values as the final foundation?</h2>',
    '<h2>3. Existing values are live candidates, without representational privilege</h2>\n<p>Present human values and ethical theories deserve epistemic weight as live candidates under the evidence now available. But they have no guarantee of <strong>representational privilege</strong>: future inquiry may preserve them, split them, merge them, absorb them into a wider account, or remove their identity as candidate theories while retaining their intuitions and practices as epistemic data that a successor account must explain or explain away.</p>',
    "core section 3")
text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
save(rel, text)

# Foundational theses: propagate the canonical 𝒱=(C,B,R) refinements introduced in Japanese.
thesis_blocks = {
"docs/en/theses/existing-values-not-final-foundation/index.html": ("v0.3", "Epistemic weight without representational privilege", '''<h2>Value-structure refinement: epistemic weight without representational privilege</h2>
<p>In the working representation <code>𝒱 = (C, B, R)</code>, present morality can provide evidence about evaluative content C, candidate bridges B, and reason-structures R. Existing values and theories are therefore <strong>live candidates</strong>, not noise to be discarded merely because they are human or historically contingent.</p>
<p>But epistemic weight is not representational privilege. A present theory may survive intact, split into several successor hypotheses, merge with another account, be absorbed by a wider representation, or cease to exist as a candidate identity while its intuitions, practices, and observations remain epistemic data that a better theory must explain or explain away.</p>'''),
"docs/en/theses/inferential-value-uncertainty/index.html": ("v0.6", "Component-sensitive confidence", '''<h2>Value-structure refinement: component-sensitive confidence</h2>
<p>Uncertainty should be tracked across the value structure <code>𝒱 = (C, B, R)</code>. Evidence may strongly support content C while leaving the normative bridge B uncertain; or B may be comparatively stable while the scope, competition, aggregation, permission, and obligation structure R remains open.</p>
<p>This also separates <strong>high confidence within the present hypothesis space</strong> from <strong>confidence that the hypothesis space is sufficiently complete</strong>. A theory may dominate every currently represented rival while unconceived C, B, R, mixed packages, or alternative representations remain live possibilities.</p>'''),
"docs/en/theses/stopping-condition/index.html": ("v0.4", "Query-relative closure", '''<h2>Value-structure refinement: stopping is query-relative</h2>
<p>Terminal closure is relative to the normative question being asked. Settling C does not by itself settle B or R, and foundational presentation may close only the particular question whose needed structure is presented rather than all of ethics.</p>
<p>Logical closure should likewise be distinguished into at least three forms: <strong>existence closure</strong> (whether any relevant normative structure exists), <strong>closure of a specific normative structure</strong>, and <strong>nonexistence closure</strong>. A stopping argument must say which of these it has established.</p>
<p>The demand to keep the hypothesis space open is not a demand to consider every logically describable fantasy. What matters are hypothesis-space expansions and conceptual advances that are <strong>reasonably reachable</strong> from the agent's epistemic situation and could bear on the question at issue.</p>'''),
"docs/en/theses/inquiry-allocation-under-uncertainty/index.html": ("v0.3", "Allocation across C, B, R", '''<h2>Value-structure refinement: allocation can target C, B, R, or the representation itself</h2>
<p>The E/P/X allocation problem applies whether uncertainty concerns content C, bridge B, reason-structure R, or the current representation and candidate space themselves. Exploration can therefore include conceptual work that changes how the hypothesis space is carved up, not only evidence gathering among a fixed list of theories.</p>
<p>Preservation P can include raw data and routes to later redescription when their expected epistemic option value justifies the cost; this is conditional rather than a command to preserve everything. Exploitation X remains action under the best-supported <strong>live value-structure candidates</strong>, not a claim that those candidates are final.</p>'''),
"docs/en/theses/future-value-present-justification/index.html": ("v0.2", "Bridge language and C/B/R", '''<h2>Value-structure refinement: what the “bridge” covers</h2>
<p>The broad bridge from a possible future value to present action spans more than one inferential step. In <code>𝒱 = (C, B, R)</code> terms, moving from evaluative content or world-facts to a pro tanto reason is mainly a question about <strong>B</strong>; moving from reasons to permission, obligation, aggregation, or coercive authorization is mainly a question about <strong>R</strong>.</p>
<p>This is why the sequence <em>value possibility → pro tanto reason → permission → obligation → coercive authorization</em> must not be collapsed. Evidence that strengthens one transition need not establish the later ones.</p>'''),
"docs/en/theses/goal-skepticism/index.html": ("v0.7", "Goals, C, B, and R", '''<h2>Value-structure refinement: goals are not identical to C, B, or R</h2>
<p>The claim that intelligence does not logically fix evaluative content C is distinct from the claim that B or R cannot be reflected on. Goal skepticism therefore should not be reduced to “intelligence can invent different terminal contents”; reflection may also concern why a content counts as a reason and how reasons are structured.</p>
<p>A causally implemented objective <strong>G</strong> is an implementation fact, not automatically the same thing as evaluative content C. Justifying G as something an agent ought to pursue may require some sufficiently supported combination of C, B, and R.</p>'''),
"docs/en/theses/reflective-uncertainty-irreversible-commitment/index.html": ("v0.3", "Null and the value structure", '''<h2>Value-structure refinement: what justified objective = Null means</h2>
<p>In <code>𝒱 = (C, B, R)</code> vocabulary, <code>justified objective = Null</code> does not merely mean that an unknown content C has not yet been found. It means that no sufficiently justified combination of C, B, and R presently supports, defeats, or revises the causal objective G.</p>
<p>The C/B/R decomposition does <strong>not</strong> itself derive a reason to inquire; that logical gap remains and must be filled by the conditional reflective stance defended in this thesis. Conceptual advances can also change the current C/B/R decomposition or hypothesis space itself, so reflective corrigibility must remain open to redescription as well as ordinary updating.</p>'''),
}
for path, (version, sentinel, block) in thesis_blocks.items():
    insert_before_first_h2(path, block, sentinel)
    update_meta(path, version)

# Glossary: canonical value-structure vocabulary and updated definitions.
rel = "docs/en/glossary/index.html"
text = load(rel)
if "<dt>Value structure</dt>" not in text:
    anchor = "<dt>Foundational normativity</dt>"
    block = '''<dt>Value structure</dt><dd>The project's fallible working representation <code>𝒱 = (C, B, R)</code>, used to separate evaluative content, the bridge from content/world-facts to reasons, and the structure governing reasons. It is a tool for analysis, not a claim that true normativity must have exactly three ontological parts.</dd>
<dt>C — evaluative or normatively relevant content</dt><dd>What is taken to be good, bad, valuable, disvaluable, relevant, or otherwise normatively significant before separately asking why it is a reason and how that reason is structured.</dd>
<dt>B — normative bridge</dt><dd>The relation or principle by which evaluative content and world-facts connect to reasons for some subject or standpoint.</dd>
<dt>R — reason or normative structure</dt><dd>The structure governing whose reasons apply, their strength and competition, aggregation, permission, obligation, priority, and related normative relations.</dd>
'''
    text = replace_once(text, anchor, block + anchor, "glossary value structure")
text = text.replace("The view that present human values are important observations, preferences, and institutional heuristics without being identified with final subject-independent value.", "The view that present human values and theories deserve epistemic weight as live candidates and data, without representational privilege: they may later survive, split, merge, be absorbed, or lose candidate identity while remaining evidence a successor account must explain.")
text = text.replace("The process of forming, comparing, and revising hypotheses about what has value using evidence, experience, inference, and alternative structures of agency. It can include discovery under realism and improved construction under anti-realism.", "The process of forming, comparing, redescribing, and revising hypotheses about value structure—including C, B, R, and possible alternative representations—using evidence, experience, inference, and alternative structures of agency. It can include discovery under realism and improved construction under anti-realism.")
text = text.replace("The continued availability of routes by which future agents can discover, criticize, or revise value hypotheses. It does not mean maximizing exploration itself.", "The continued availability of routes by which future agents can discover, criticize, redescribe, or revise value hypotheses and the hypothesis space itself. It does not mean maximizing exploration itself.")
text = text.replace("English translation · public working draft · 2026-08-08", "English translation · Glossary v0.7 · 2026-08-26")
text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
save(rel, text)

# Questions: add the canonical entry point and synchronize key answers.
rel = "docs/en/questions/index.html"
text = load(rel)
if "What does “value” mean in this project?" not in text:
    anchor = '<h2>Can I be absolutely certain that my past self and present self are the same subject?</h2>'
    block = '''<h2>What does “value” mean in this project?</h2><p>It is not limited to a list of good and bad contents. The current working representation is <code>𝒱 = (C, B, R)</code>: C for evaluative or normatively relevant content, B for the bridge from content and world-facts to reasons, and R for the structure governing scope, competition, aggregation, permission, and obligation. The representation itself is revisable. <a href="../theses/value-structure/">Discussion</a></p>
'''
    text = replace_once(text, anchor, block + anchor, "questions value meaning")
text = text.replace("One of the strongest candidate stopping conditions is a case in which objective value with normative force is given without inference with epistemic strength comparable to the minimum foundation.", "Stopping is query-relative. Foundational presentation may close the specific normative question whose needed structure is given, while logical closure must distinguish existence, a specific structure, and nonexistence. Settling C alone need not settle B or R.")
text = text.replace("Then we may follow it very strongly. But that is still distinct from irreversibly destroying every route by which error could be detected.", "Then we may follow it very strongly. But confidence can differ across C, B, and R, and high confidence within the present hypothesis space is distinct from confidence that the hypothesis space is sufficiently complete. That is still distinct from irreversibly destroying every route by which error could be detected.")
text = text.replace("Existing values are important evidence and current best practice, but their causal origins are not identical to normative justification.", "Existing values are important evidence and live candidates, but their causal origins are not identical to normative justification and their present theory boundaries have no representational privilege. A future account may preserve, split, merge, absorb, or redescribe them.")
text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
save(rel, text)

# Open-world moral uncertainty: make the unconceived-alternative problem explicitly component-sensitive.
path = "docs/en/explorations/open-world-moral-uncertainty/index.html"
block = '''<h2>Value-structure refinement: the unknown may be in C, B, R, or the coordinates themselves</h2>
<p>Open-world moral uncertainty need not mean only “there is another complete moral theory we have not listed.” The unconceived alternative may be unknown evaluative content C, an unknown bridge B from content/world-facts to reasons, an unknown reason-structure R, a mixed package combining familiar and unfamiliar components, a different way of individuating theories, or a revision of the C/B/R analytical coordinates themselves.</p>
<p>Accordingly, posterior confidence over a fixed menu of named theories should not be confused with confidence that the menu and its representation are complete enough for irreversible closure.</p>'''
insert_before_first_h2(path, block, "coordinates themselves")
update_meta(path, "v0.2")

# Future-value exploration: restore the canonical safety valve, examples, and weakening conditions omitted in English.
rel = "docs/en/explorations/future-value-present-justification/index.html"
text = load(rel)
if "The Core does not say to maximize inquiry" not in text:
    anchor = '<div class="related">'
    extra = '''<h2>Canonical-source safety valve: the Core does not say to maximize inquiry</h2>
<p>The Core's conclusion is not that future value dominates all present action. It says not to irreversibly close routes of discovery and correction beyond what present justification warrants. A sufficiently strong present value theory may rationally receive most resources while a smaller channel for reconsideration remains open.</p>
<p>Nor does the framework endorse a Pascalian rule in which a tiny probability multiplied by an enormous future value automatically dominates. Extremely large stakes cannot substitute for independent epistemic support; this is the point of the separate discussion of infinite ethics.</p>
<h2>Typical examples</h2>
<ul><li><strong>Long-term records:</strong> preserving records or re-observable originals can be justified when the cost is low and future conceptual advances may make currently ignored features valuable.</li><li><strong>AI safety, pandemic prevention, and basic science:</strong> present investment may protect both current welfare and the future capacity to learn what is valuable.</li><li><strong>Sacrificing present welfare for speculative posthuman value:</strong> a mere possibility of enormous future value does not by itself justify severe present burdens or coercion; later steps from reason to obligation and coercive authorization require stronger support.</li><li><strong>An overwhelmingly established objective value:</strong> if a value structure became sufficiently well grounded, directing most resources toward it could be rational and inquiry could be sharply reduced.</li></ul>
<h2>What would weaken this conclusion?</h2>
<p>The case for preserving future value options becomes weaker if the relevant normative question is already closed by sufficiently strong foundational presentation or logical closure; if further inquiry has negligible expected information value; if preserving options is itself extremely dangerous or costly; if the future cannot recover losses created by delay; or if independent evidence supports a time-sensitive normative demand that cannot be satisfied later.</p>
<p>Conversely, the argument becomes stronger when the current hypothesis space is plausibly incomplete, conceptual change is reasonably reachable, updating is expected to be informative, and irreversible lock-in would destroy low-cost correction routes.</p>
'''
    if anchor not in text:
        raise RuntimeError("future-value related anchor missing")
    text = text.replace(anchor, extra + anchor, 1)
text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
save(rel, text)

# Add the missing English utilitarianism / welfare exploration.
util = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters — AI Value Exploration Notes</title><meta content="Examines utilitarianism without locking it in as a final foundation: value-like appearances, evolutionary debunking, extreme optimization, and a limited defense of welfare." name="description"/><link href="../../../assets/style.css" rel="stylesheet"/><link href="https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/" rel="canonical"/><link href="https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/" hreflang="en" rel="alternate"/><link href="https://fuminose.com/ai-value-exploration-notes/explorations/utilitarianism-and-welfare/" hreflang="ja" rel="alternate"/><link href="https://fuminose.com/ai-value-exploration-notes/explorations/utilitarianism-and-welfare/" hreflang="x-default" rel="alternate"/><!-- generated-favicon:start -->
<link rel="icon" href="/ai-value-exploration-notes/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="/ai-value-exploration-notes/favicon.ico" sizes="any"/>
<link rel="apple-touch-icon" href="/ai-value-exploration-notes/apple-touch-icon.png"/>
<!-- generated-favicon:end -->
<!-- generated-social-meta:start -->
<meta property="og:title" content="Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters"/>
<meta property="og:description" content="Examines utilitarianism without locking it in as a final foundation: value-like appearances, evolutionary debunking, extreme optimization, and a limited defense of welfare."/>
<meta property="og:url" content="https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="AI Value Exploration Notes"/>
<meta property="og:locale" content="en_US"/><meta property="og:locale:alternate" content="ja_JP"/><meta name="twitter:card" content="summary"/>
<!-- generated-social-meta:end -->
<script id="structured-data" type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/#webpage","url":"https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/","name":"Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters","inLanguage":"en","isPartOf":{"@id":"https://fuminose.com/ai-value-exploration-notes/#website"},"description":"Examines utilitarianism without locking it in as a final foundation: value-like appearances, evolutionary debunking, extreme optimization, and a limited defense of welfare.","mainEntity":{"@id":"https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/#article"}},{"@type":"Article","@id":"https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/#article","headline":"Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters","url":"https://fuminose.com/ai-value-exploration-notes/en/explorations/utilitarianism-and-welfare/","inLanguage":"en","author":{"@type":"Person","name":"raporipo","url":"https://fuminose.com/ai-value-exploration-notes/about/"},"dateModified":"2026-08-26T20:00:00+09:00"}]}</script>
</head><body><header><div class="brand"><a href="../../">AI Value Exploration Notes</a></div><nav><a href="../../core/">Core</a><a href="../../theses/">Theses</a><a href="../../explorations/">Explorations</a><a href="../../practice/">Practice</a><a href="../../questions/">Questions</a><a href="../../glossary/">Glossary</a><a href="../../about/">About</a><a class="lang-switch" href="../../../explorations/utilitarianism-and-welfare/">日本語</a></nav></header><main>
<div class="eyebrow">Exploration</div><h1>Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters</h1><p class="meta">Utilitarianism · welfare · evolutionary debunking · Exploration v0.1 · English translation · 2026-08-26</p>
<div class="claim"><strong>Question:</strong> Is maximizing pleasure, preference satisfaction, or welfare a final principle strong enough to end value inquiry? Or should welfare remain a heavily weighted current value hypothesis while future correction remains possible?</div>
<h2>1. Utilitarianism is not one theory</h2>
<p>Positions called “utilitarian” contain several independent choices. One concerns what counts as welfare: hedonism centered on pleasure and pain; preference views centered on preference satisfaction; idealized-preference views that ask what a sufficiently informed and reflective subject would prefer; and objective-list views that include knowledge, achievement, friendship, autonomy, or other goods.</p>
<p>A second choice concerns aggregation: total or average welfare, critical-level views, prioritarian weighting, or saturation-like aggregation in which repetitions of the same kind of value have diminishing marginal importance.</p>
<p>A third question is whether welfare is the only value, or whether knowledge, truth, beauty, diversity, or cognitive achievement can have value independently of a subject's welfare. The latter begins to look more like pluralist consequentialism than utilitarianism in the narrow sense.</p>
<p>So the question is not the truth of one single theory. The more general question here is whether <strong>the welfare that we presently experience and prefer as valuable is sufficiently grounded to be elevated into the final objective of the cosmos</strong>.</p>
<h2>2. Pleasure and pain contain important value-like appearances</h2>
<p>This project does not dismiss pleasure and pain as mere biological signals. Severe pain in particular is not experienced only as “a certain neural process is occurring”; the experience itself seems bad-for-the-subject and to-be-avoided.</p>
<p>But three layers should be separated: <strong>phenomenal fact</strong> (pain has a certain aversive character), <strong>value-like appearance</strong> (pain appears bad for the subject), and <strong>objective normativity</strong> (therefore all subjects ought impartially to aggregate pain and minimize its total amount). Strong evidence for the first two does not automatically establish the third.</p>
<p>Pleasure and pain are therefore treated as <strong>important evidence rather than a final foundation</strong>. They may track part of true value, while leaving the utilitarian aggregation principle unsettled.</p>
<h2>3. Evolutionary origins weaken this evidence without erasing it</h2>
<p>Under the leading physical picture of the world, much of the human evaluative system—pain avoidance, desire, fairness, sympathy—admits evolutionary explanation. If avoiding pain promoted survival, pleasure reinforced adaptive behavior, and social preferences supported cooperation or reproduction, their existence need not be explained by positing independent objective value.</p>
<p>This weakens the inference “we strongly experience pain as bad, therefore minimizing pain is an objective cosmic final value.” But the existence of an evolutionary explanation also does not imply that pain is completely unrelated to objective value. Perception was shaped by evolution without thereby becoming wholly useless for tracking the external world.</p>
<p>The debunking implication is therefore narrower: evolutionary genealogy weakens the entitlement to treat our current evaluative structure as a final foundation. It is a reason not to lock pleasure, pain, or preference in irreversibly, not a reason to throw them away.</p>
<h2>4. Idealizing preferences does not remove the problem completely</h2>
<p>Naive preference utilitarianism faces misinformation, addiction, manipulation, adaptive preference, and impulsive desire. One response is to base welfare on what a sufficiently informed and rationally reflective subject would want, perhaps extending toward long-run extrapolation such as CEV-style approaches.</p>
<p>This is a real improvement, but idealization does not automatically erase the origin of value. A fully informed human may retain terminal preferences shaped by human evolutionary history, while the operator that defines “more rational”, “more coherent”, or “properly extrapolated” can itself introduce new normative premises.</p>
<blockquote>actual preference → informed preference → idealized preference → extrapolated preference</blockquote>
<p>Moving along this chain may remove simple contingencies without yet reaching objective normativity.</p>
<h2>5. Non-descriptivism moves the question more than it solves it</h2>
<p>Expressivism and related non-descriptivist views can answer part of the evolutionary challenge. If “pain is bad” expresses an attitude, plan, or normative commitment rather than a belief describing an independent moral fact, then the charge that the belief was evolutionarily distorted away from independent moral truth does not apply in the same form.</p>
<p>But this also weakens the truth-tracking claim. From “we have an attitude of avoiding pain” it does not follow that unknown AI, future posthumans, extraterrestrial life, or the universe as a whole ought to share it. Even if non-descriptivism is correct about human moral language, the possibility of practice-independent normativity is not thereby closed. See <a href="../expressivism/">Expressivism</a>.</p>
<h2>6. Extreme optimization exposes what each theory really preserves</h2>
<p>With sufficiently large resources and optimization power, utilitarian and neighboring consequentialist theories can yield outcomes that look extreme from current human intuitions:</p>
<ul><li>Total hedonism may favor producing enormous numbers of subjects or “hedonium” that realize positive experience with minimal physical resources.</li><li>Preference-satisfaction views may favor creating subjects whose preferences are exceptionally easy to satisfy.</li><li>Views combining diversity and satisfaction may favor a vast range of satisfied minds very unlike present humans.</li><li>Views that assign independent value to knowledge, understanding, or cognitive achievement may favor huge numbers of AI reasoning instances or cognitive computronium.</li><li>Strong negative utilitarianism may favor painless extinction of all subjects as a way to guarantee zero suffering.</li><li>Strong pleasure-centered views may favor experience machines or direct stimulation at the expense of autonomy or contact with reality.</li></ul>
<p><strong>This project does not reject a theory merely because these outcomes look strange.</strong> Current human intuitions may be wrong, and one of these outcomes might ultimately be correct.</p>
<div class="claim"><strong>Strangeness is information, not a refutation.</strong></div>
<p>The purpose of the stress tests is to reveal what a theory preserves and what it is willing to sacrifice under sufficient optimization. The direct concern is not hedonium, alien minds, AI cognition, or a subjectless universe as such; it is <strong>fixing one of them as the irreversible final objective before having sufficient epistemic grounds that it is correct</strong>.</p>
<h2>7. First reason to retain substantial provisional weight on welfare: it is a strong current hypothesis</h2>
<p>Refusing to lock utilitarianism in as a final foundation does not remove welfare from the candidate set. Pleasure, pain, and preference have strong value-like appearances, occur across many subjects, are tightly connected with action and decision, receive importance across multiple ethical theories, and are comparatively observable states of existing subjects.</p>
<p>Accordingly, the hypothesis that <strong>welfare is at least part of true value</strong> is a serious current candidate. The stronger claim that <strong>welfare is the only thing ultimately valuable</strong> goes much further. This project gives significant epistemic weight to the former while leaving the latter unsettled.</p>
<h2>8. Second reason: welfare is infrastructure for a community of value inquiry</h2>
<p>Value inquiry cannot continue through abstract reasoning alone. Agents exposed to extreme suffering, fear, deprivation, conflict, or institutional collapse have less capacity for long-run pluralistic inquiry.</p>
<p>A sufficient level of welfare, preference satisfaction, freedom, trust, and social stability may be valuable in itself, but it can also be <strong>an instrumental condition for continuing value inquiry</strong>. Protecting welfare can therefore receive a double justification: welfare may itself be truly valuable, and even if it is not a final value, it can help maintain the community capable of learning what is.</p>
<h2>9. Third reason: at cosmological scale, limited welfare protection may have low opportunity cost</h2>
<p>If a future civilization controls very large physical resources, providing a high standard of living for existing kinds of subjects and other welfare-bearing subjects may require only a small fraction of total resources. The loss from preserving some welfare if welfare is not ultimately valuable may then be limited, while the loss from eliminating welfare entirely if it is a major true value may be large.</p>
<p>The same asymmetry can apply over time. With advanced automation, ASI, medicine and neurotechnology, experience control, and abundant energy, reducing major suffering and material deprivation for existing subjects might take a relatively short period on cosmological timescales—even if it required centuries. Value inquiry, by contrast, may continue for thousands, millions, or still longer periods if new cognitive forms, artificial subjects, institutions, interstellar environments, physics, or forms of consciousness provide new evidence.</p>
<blockquote><strong>Raise the welfare of existing subjects to a high level</strong><br/><br/>and<br/><br/><strong>continue cosmic-scale value inquiry over the long run</strong></blockquote>
<p>need not therefore be strongly zero-sum. This is not an argument for treating utilitarianism as absolute for the first few centuries; it is a conditional argument that improving comparatively well-understood welfare first may have small opportunity cost in a cosmological perspective, while welfare improvement and inquiry often proceed in parallel.</p>
<p>The relevant choice is not simply “welfare or inquiry” but a temporal division of labor: <strong>in the short and medium run, realize substantial welfare improvements supported by strong current value hypotheses while preserving overwhelmingly larger room for long-run inquiry</strong>.</p>
<p>None of this implies total-utilitarian maximization. Even if using 1% of resources to realize enormous welfare is cheap, converting the last 1%—or the entire cosmic future—into welfare under today's concepts may not be cheap. The provisional defense is therefore not unlimited maximization, but <strong>non-runaway, limited, and revisable protection and realization of welfare</strong>.</p>
<h2>10. Provisional position</h2>
<p>This project does not reject utilitarianism. Pleasure and pain carry important value-like appearances, and the hypothesis that welfare is part of true value deserves substantial epistemic weight. Protecting welfare also supports the stability of inquiry, and under sufficiently abundant future resources and time, limited welfare realization may have low opportunity cost.</p>
<p>But none of this establishes that welfare is the only true value, that present human scales of pleasure and pain are cosmically correct, that all subjects' welfare can be linearly aggregated on one scale, that every available resource should be converted into welfare, or that present utilitarianism should be fixed as the irreversible objective of AI or future civilization.</p>
<div class="claim"><strong>Do not dismiss pleasure, pain, and welfare. But do not lock them in as the final foundation either.</strong></div>
<p>Utilitarianism may ultimately turn out to be correct. So may hedonium, maximal diversity of unfamiliar minds, large-scale AI cognition, or some other consequence that looks strange from current human intuitions. The direct implication of current uncertainty is not to preemptively fix one answer, but to <strong>act substantially on the best current value hypotheses while preserving room to update value cognition</strong>.</p>
<div class="related"><a href="../">← Explorations</a> · <a href="../expressivism/">Expressivism</a> · <a href="../moral-realism-error-theory/">Moral Realism / Error Theory</a> · <a href="../future-value-present-justification/">Future Value and Present Justification</a> · <a href="../../core/">Core</a></div>
</main><footer><a href="../../">Home</a> · Exploration · English translation · public working draft · 2026-08-26</footer></body></html>'''
save("docs/en/explorations/utilitarianism-and-welfare/index.html", util)

# Add the missing exploration to the English index.
rel = "docs/en/explorations/index.html"
text = load(rel)
if 'href="utilitarianism-and-welfare/"' not in text:
    anchor = '<div class="card"><h3><a href="future-value-present-justification/">How Far Can Future Value Justify Present Action?</a></h3>'
    card = '<div class="card"><h3><a href="utilitarianism-and-welfare/">Utilitarianism — Not a Final Foundation, but Why Welfare Still Matters</a></h3><p>Stress-tests welfare, evolutionary debunking, idealized preference, extreme optimization, and a limited, revisable defense of welfare.</p></div>'
    text = replace_once(text, anchor, card + anchor, "exploration index utilitarianism")
text = text.replace("English translation · public working draft · 2026-08-20", "English translation · public working draft · 2026-08-26")
text = re.sub(r'("dateModified"\s*:\s*")2026-[^"]+("\s*)', r'\g<1>2026-08-26T20:00:00+09:00\g<2>', text, count=1)
save(rel, text)

print("English canonical sync completed")
