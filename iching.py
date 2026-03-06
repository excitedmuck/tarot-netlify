"""I Ching — 64 hexagrams with meanings, trigrams, and casting logic."""
import random

# Trigram definitions: (bottom, middle, top) — True=solid(yang), False=broken(yin)
TRIGRAMS = {
    "Heaven":   (True,  True,  True),
    "Earth":    (False, False, False),
    "Thunder":  (True,  False, False),
    "Water":    (False, True,  False),
    "Mountain": (False, False, True),
    "Wind":     (False, True,  True),
    "Fire":     (True,  False, True),
    "Lake":     (True,  True,  False),
}

TRIGRAM_SYMBOLS = {
    "Heaven": "☰", "Earth": "☷", "Thunder": "☳", "Water": "☵",
    "Mountain": "☶", "Wind": "☴", "Fire": "☲", "Lake": "☱",
}

# All 64 hexagrams in King Wen sequence:
# (number, chinese_name, english_name, lower_trigram, upper_trigram, judgment, image)
HEXAGRAMS = [
    (1,  "乾", "The Creative",           "Heaven",   "Heaven",
     "Heaven moves with persisting power. The creative force initiates all things. Through strength and perseverance, great achievement is possible. Act with clear intent and pure motivation.",
     "Heaven in its course gives the image of strength. Thus the superior person makes themselves strong and untiring."),

    (2,  "坤", "The Receptive",          "Earth",    "Earth",
     "Earth yields, supports, and nourishes. Supreme success through gentleness and nurturing. Receptivity brings its own power — holding space for things to unfold in their proper time.",
     "The earth's condition is receptive devotion. Thus the superior person nurtures all things with broad virtue."),

    (3,  "屯", "Difficult Beginnings",   "Thunder",  "Water",
     "Chaos precedes creation. A seedling breaking through hard soil — growth is real but labored. Do not attempt everything at once; seek helpers and proceed with care through the tangle.",
     "Clouds and thunder — Difficult Beginnings. The superior person brings order out of confusion."),

    (4,  "蒙", "Youthful Folly",         "Water",    "Mountain",
     "A spring gushing at the base of a mountain — youth full of energy but needing direction. Seek guidance with humility; the oracle speaks once clearly. Persistence in learning brings clarity.",
     "A spring wells up at the base of the mountain. The superior person fosters character through decisive action."),

    (5,  "需", "Waiting",                "Heaven",   "Water",
     "Clouds gather but rain has not yet fallen. Success lies in patient waiting rather than forcing. Nourish yourself and those around you; the right moment approaches. Sincerity brings good fortune.",
     "Clouds in the sky — Waiting. The superior person eats, drinks, and maintains joyful composure."),

    (6,  "訟", "Conflict",               "Water",    "Heaven",
     "Water strains upward while heaven moves downward — opposition at the core. Conflict arises from blocked communication. Seek a mediator; do not pursue the dispute to its bitter end.",
     "Heaven and water move in opposite directions — Conflict. The superior person carefully considers all undertakings."),

    (7,  "師", "The Army",               "Water",    "Earth",
     "A mass of people must be led with discipline and justice. Authority requires wisdom, not mere force. In conflict, seek a just leader. Unity of purpose under righteous command brings victory.",
     "Water in the earth — The Army. The superior person treats the people generously and provides for the multitude."),

    (8,  "比", "Holding Together",       "Earth",    "Water",
     "Water flows over the earth, gathering together. Union and alliance bring strength. Consider carefully who you bind yourself to — sincerity is essential. Late arrivals bring misfortune.",
     "On earth, water — Holding Together. Ancient kings established states and cultivated relationships."),

    (9,  "小畜", "Small Taming",         "Heaven",   "Wind",
     "Wind drives across heaven — gentle restraint, not forceful opposition. Small victories are possible; grand objectives must wait. Accumulate virtue quietly; conditions will shift favorably.",
     "The wind drives across heaven — Small Taming. The superior person refines the outward aspects of virtue."),

    (10, "履", "Treading",               "Lake",     "Heaven",
     "Treading on a tiger's tail — proceeding with awareness and respect in a potentially dangerous situation. Conduct yourself with joy and sincerity; respectful awareness brings success.",
     "Heaven above, lake below — Treading. The superior person discriminates between high and low and fortifies the will of the people."),

    (11, "泰", "Peace",                  "Heaven",   "Earth",
     "Heaven and earth unite — the small departs, the great approaches. A time of flourishing harmony. Embrace the flow of natural cycles; support and nourish what is good. Great good fortune.",
     "Heaven and earth unite — Peace. The ruler completes and regulates the gifts of heaven and earth."),

    (12, "否", "Standstill",             "Earth",    "Heaven",
     "Heaven and earth are estranged. The great departs, the small comes. Stagnation in communication and progress. Do not try to force movement; preserve your inner truth through the standstill.",
     "Heaven and earth are out of communion — Standstill. The superior person retreats into inner virtue to avoid difficulties."),

    (13, "同人", "Fellowship",           "Fire",     "Heaven",
     "Fire blazes toward heaven — people uniting around shared purpose. Fellowship in the open brings success. Seek common ground; partisan alliances lead to regret. Shared vision triumphs.",
     "Heaven together with fire — Fellowship. The superior person distinguishes things according to kind and class."),

    (14, "大有", "Great Possession",     "Heaven",   "Fire",
     "Fire in heaven illuminates all. Abundance through virtue and skill, not selfishness. Suppress what is evil, further what is good. The more magnanimously you share, the greater the growth.",
     "Fire in heaven above — Great Possession. The superior person suppresses evil and furthers the good."),

    (15, "謙", "Modesty",               "Mountain", "Earth",
     "A mountain hidden within the earth — genuine modesty lifts the low and levels the high. Those who diminish their excess and increase their insufficiency are loved by the universe. Carry on!",
     "Within the earth, a mountain — Modesty. The superior person reduces what is too much, augments what is too little."),

    (16, "豫", "Enthusiasm",            "Earth",    "Thunder",
     "Thunder bursts from the earth — resounding movement that resonates with hearts. Enthusiasm mobilizes people. Appoint helpers and set things in motion; strike while energy is high. Move!",
     "Thunder comes resounding out of the earth — Enthusiasm. The kings of old made music to honor merit."),

    (17, "隨", "Following",             "Thunder",  "Lake",
     "Thunder in the lake — joy following movement. Adapt to the time and follow what is right without servility. Genuine following requires inner freedom. Go with the tide of the moment.",
     "Thunder in the middle of the lake — Following. The superior person at nightfall goes indoors for rest and recuperation."),

    (18, "蠱", "Work on Decay",         "Wind",     "Mountain",
     "Wind at the foot of the mountain — what has stagnated must be renovated. Corruption or neglect requires work to correct. Three days before and after the turning: prepare carefully, act decisively.",
     "The wind blows low on the mountain — Work on Decay. The superior person stirs up the people and strengthens their spirit."),

    (19, "臨", "Approach",              "Lake",     "Earth",
     "Earth above the lake — the great approaches. Authority exercises gentle oversight. The eighth month brings a reversal; enjoy the flourishing season but prepare for change. Educate with love.",
     "The earth stands high above the lake — Approach. The superior person teaches and considers the people inexhaustibly."),

    (20, "觀", "Contemplation",         "Earth",    "Wind",
     "Wind roams over the earth — surveying all. The great one who contemplates deeply is an example to all. Examine yourself and the world before acting. Insight through observation.",
     "The wind blows over the earth — Contemplation. The ancient kings visited the regions of the world to examine the people."),

    (21, "噬嗑", "Biting Through",      "Thunder",  "Fire",
     "Lightning and thunder — forceful correction of obstacles. Remove whatever stands between union. Penalties applied with clarity and fairness restore order. Justice served with discernment.",
     "Thunder and lightning — Biting Through. The kings of old made firm the laws by clearly defining penalties."),

    (22, "賁", "Grace",                 "Fire",     "Mountain",
     "Fire illuminates the mountain — outward grace beautifying form. Attend to small matters with care; do not let ornament replace substance. True grace is simple and sincere.",
     "Fire at the foot of the mountain — Grace. The superior person proceeds with clarity in everyday affairs."),

    (23, "剝", "Splitting Apart",       "Earth",    "Mountain",
     "Mountain rests on earth — erosion from below. A time of dissolution when it is not advantageous to move. The strong position is being eaten away. Rest, nourish others, wait for renewal.",
     "The mountain rests on the earth — Splitting Apart. Those above can make their position secure only by giving to those below."),

    (24, "復", "Return",               "Thunder",  "Earth",
     "Thunder within the earth — the light returns. The solstice point; energy reverses and growth begins again. A single yang line begins its ascent. Do not force movement — natural return unfolds.",
     "Thunder within the earth — Return. In correspondence with this, the ancient kings closed passes at solstice."),

    (25, "無妄", "Innocence",           "Thunder",  "Heaven",
     "Thunder rolls under heaven — unexpected happenings. Act only from natural sincerity, not calculation. Only the truly innocent can receive the blessings of heaven. Trust what is spontaneous.",
     "Under heaven thunder rolls — Innocence. Kings nurtured all things in the richness of nature."),

    (26, "大畜", "Great Taming",        "Heaven",   "Mountain",
     "Heaven within the mountain — great creative powers held in reserve. Accumulate virtue and talent; the time for great undertakings is approaching. Study the wisdom of those who came before.",
     "Heaven within the mountain — Great Taming. The superior person acquaints themselves with many sayings of antiquity."),

    (27, "頤", "Nourishment",          "Thunder",  "Mountain",
     "Thunder at the foot of the mountain — the jaws. Attend to what you nourish in yourself and others. Words proceed from the mouth; food enters it. Be mindful of what you take in and give out.",
     "Thunder at the foot of the mountain — Nourishment. The superior person is careful of words and temperate in eating and drinking."),

    (28, "大過", "Great Excess",        "Wind",     "Lake",
     "The lake rises above the trees — the ridgepole is sagging. Extraordinary times require extraordinary measures. The great must shoulder what is overwhelming. Act alone if necessary; the time is critical.",
     "The lake rises above the trees — Great Excess. The superior person stands alone without fear and retires from the world without distress."),

    (29, "坎", "The Abyss",            "Water",    "Water",
     "Water flowing continuously into a chasm — danger repeated, yet water persists through faith. Do not be afraid of peril; maintain sincere virtue. Flow like water — find the way through.",
     "Water flows on — The Abyss. The superior person walks in lasting virtue and carries on the work of teaching."),

    (30, "離", "The Clinging",         "Fire",     "Fire",
     "Fire clings to wood; brightness doubled. Awareness and clarity illuminating the world. Tend the flame of consciousness persistently. Care for what sustains you; let inner light radiate outward.",
     "Brightness rises twice — The Clinging. The great person illuminates the four quarters of the world."),

    (31, "咸", "Influence",            "Mountain", "Lake",
     "Lake above mountain — the trigrams of the youngest son and daughter in embrace. Mutual attraction and influence between open hearts. Take a partner; receptivity draws all to you. Marriage.",
     "A lake on the mountain top — Influence. The superior person is open to influence from those who come."),

    (32, "恆", "Duration",             "Wind",     "Thunder",
     "Thunder and wind work together — duration through consistent change within consistent form. That which endures is not rigid but persists through flowing adaptation. Stand firm in purpose.",
     "Thunder and wind — Duration. The superior person stands firm and does not change direction."),

    (33, "遯", "Retreat",              "Mountain", "Heaven",
     "Heaven above the mountain — strategic retreat. The superior person withdraws from inferior influences not in defeat but with dignity. Timing is mastery. A graceful withdrawal preserves strength.",
     "Mountain under heaven — Retreat. The superior person keeps inferior people at a distance by being dignified."),

    (34, "大壯", "Great Power",         "Heaven",   "Thunder",
     "Thunder in heaven — great power. Energy at its peak; perseverance keeps power righteous. Do not exhaust yourself in futile opposition. The goat butts the fence — find the wise path forward.",
     "Thunder in heaven above — Great Power. The superior person does not tread paths that are not in accordance with established order."),

    (35, "晉", "Progress",             "Earth",    "Fire",
     "The sun rises over the earth — progress and advancement. Those who shine with inner clarity are recognized and rewarded. Give and receive gifts freely. Positive momentum carries you forward.",
     "The sun rises over the earth — Progress. The superior person brightens their bright virtue."),

    (36, "明夷", "Darkening of Light",  "Fire",     "Earth",
     "The sun sinks into the earth — the light is wounded. A time of oppression when intelligence must hide. Protect your inner light; do not surrender your true nature to external pressure. Endure.",
     "The light has sunk into the earth — Darkening of Light. The superior person lives among the masses while veiling their light."),

    (37, "家人", "The Family",          "Fire",     "Wind",
     "Wind rises from fire — the family. Proper roles and sincere relationships within the household create harmony. Words must be supported by actions. The woman in the home, the man in the world.",
     "Wind comes forth from fire — The Family. The superior person has substance in words and duration in ways of life."),

    (38, "睽", "Opposition",           "Lake",     "Fire",
     "Fire above, lake below — opposed in nature yet both serving their purpose. In small matters opposition can bring good. Do not demand uniformity; opposites illuminate each other.",
     "Above fire, below lake — Opposition. The superior person retains their individuality among others."),

    (39, "蹇", "Obstruction",          "Mountain", "Water",
     "Water on the mountain — danger ahead. Acknowledge the obstacle honestly. Retreat and gather resources; seek capable helpers. Self-examination reveals what contributed to the blockage.",
     "Water on top of the mountain — Obstruction. The superior person turns within and molds their character."),

    (40, "解", "Deliverance",          "Water",    "Thunder",
     "Thunder and rain dissolve tension — the rains have come, the crisis passes. Return to normal conditions swiftly; do not linger in the aftermath. Forgive transgressions; clear the decks.",
     "Thunder and rain set in — Deliverance. The superior person pardons mistakes and forgives misdeeds."),

    (41, "損", "Decrease",             "Lake",     "Mountain",
     "Lake at the foot of the mountain — voluntary decrease. Reducing the lower to increase the higher; inner development through outer simplification. Sacrifice sincerely; two small bowls suffice.",
     "At the foot of the mountain, the lake — Decrease. The superior person controls anger and restrains instincts."),

    (42, "益", "Increase",             "Thunder",  "Wind",
     "Wind and thunder reinforce each other — increase. A time of gain and abundance. Move in great undertakings; cross the great water. When you see goodness, imitate it; when you have faults, abandon them.",
     "Wind and thunder — Increase. The superior person when good sees it, imitates it; if there are faults, abandons them."),

    (43, "夬", "Breakthrough",         "Heaven",   "Lake",
     "Lake rises toward heaven — the moment of decision. The inferior must be exposed openly, resolutely. Do not use force alone; make clear what is at stake. Notify all before acting. No compromise.",
     "The lake has risen up to heaven — Breakthrough. The superior person dispenses wealth downward and refrains from resting on virtue."),

    (44, "姤", "Coming to Meet",        "Wind",     "Heaven",
     "Heaven above wind — a powerful encounter. The inferior comes on its own; do not accommodate it. Alert leadership prevents small weaknesses from gaining power. Do not marry this woman.",
     "Under heaven, wind — Coming to Meet. The prince of state publishes commands and makes known to the four quarters."),

    (45, "萃", "Gathering Together",    "Earth",    "Lake",
     "Lake above earth — the gathering. Unity around a worthy center brings extraordinary achievement. Make offerings and strengthen the center of gathering. Prepare for the unexpected.",
     "Over the earth, the lake — Gathering Together. The superior person renews weapons and is alert to the unforeseen."),

    (46, "升", "Rising",               "Wind",     "Earth",
     "Wood grows within the earth — rising upward. Quiet, steady advance through diligence and perseverance. Seek out those who can confirm your direction. Gain ground without anxiety.",
     "Within the earth, wood grows — Rising. The superior person accumulates small things to achieve something high and great."),

    (47, "困", "Oppression",           "Water",    "Lake",
     "The lake is drained — exhaustion and constriction. Words fall on deaf ears; the lake is empty. The superior person stakes their life on following their will in hardship. Joyful trust persists.",
     "There is no water in the lake — Oppression. The superior person stakes their life on following their will."),

    (48, "井", "The Well",             "Wind",     "Water",
     "Water over wood — the well. The source nourishes all without being exhausted. The structure matters; a muddy rope or cracked jug waste the water. Maintain the vessel of wisdom and give freely.",
     "Water over wood — The Well. The superior person encourages people at their work and exhorts them to help one another."),

    (49, "革", "Revolution",           "Fire",     "Lake",
     "Fire within the lake — inevitable change. Transformation at the proper time is correct and great. On your own day you are believed. Heaven and earth bring about the seasons by transformation.",
     "Fire in the lake — Revolution. The superior person sets the calendar in order and makes the seasons clear."),

    (50, "鼎", "The Cauldron",         "Wind",     "Fire",
     "Wood feeds fire — the sacred vessel. Supreme good fortune and success. The cauldron nourishes great persons and supports transformative work. Receive what nourishment the moment offers.",
     "Fire over wood — The Cauldron. The superior person consolidates fate by making their position correct."),

    (51, "震", "The Arousing",         "Thunder",  "Thunder",
     "Thunder redoubled — the shock. Terrifying thunder shocks all into alertness, yet the sacred vessels are not spilled. Fear and trembling lead to examination of the self. Inner peace through shock.",
     "Reiterated thunder — The Arousing. With fear and trembling the superior person sets their life in order and examines themselves."),

    (52, "艮", "Keeping Still",        "Mountain", "Mountain",
     "Mountains standing together — keep still. The back (spine) keeps still; the wandering self dissolves. When resting, rest; when moving, move. Act at the right time and stop at the right time.",
     "Mountains standing close together — Keeping Still. The superior person does not permit thoughts to go beyond their situation."),

    (53, "漸", "Gradual Progress",     "Mountain", "Wind",
     "A tree on the mountain growing slowly — gradual development. The wild goose progresses step by step to its resting place. Marriage is auspicious; perseverance furthers. Trust the process.",
     "On the mountain, a tree — Gradual Progress. The superior person abides in diginity and virtue in order to improve the mores."),

    (54, "歸妹", "The Marrying Maiden", "Lake",    "Thunder",
     "Thunder over the lake — undertakings that require one to accept a subordinate role. Action taken without full authority brings misfortune. Understand your position. Constancy of purpose matters.",
     "Thunder over the lake — The Marrying Maiden. The superior person understands the transitory and the abiding."),

    (55, "豐", "Abundance",            "Fire",     "Thunder",
     "Thunder and lightning together — abundance at its zenith. The king reaches the capital; be not sad — be as the sun at midday. In times of abundance, be magnanimous and clarify justice.",
     "Both thunder and lightning come — Abundance. The superior person decides lawsuits and carries out punishments."),

    (56, "旅", "The Wanderer",         "Mountain", "Fire",
     "Fire on the mountain — the stranger. Traveling through foreign lands, without permanent home. The wanderer's success is small but genuine. Move on quickly; do not linger or overstay welcome.",
     "Fire on the mountain — The Wanderer. The superior person is clear-minded and cautious in imposing penalties."),

    (57, "巽", "The Gentle",           "Wind",     "Wind",
     "Wind following upon wind — gentle penetration. Success through repeated, gentle influence rather than force. A clear direction and a skilled helper bring results. Ask the oracle twice.",
     "Winds following one upon the other — The Gentle. The superior person re-examines their decisions and carries out their undertakings."),

    (58, "兌", "The Joyous",           "Lake",     "Lake",
     "Lakes joined together — joy shared is joy doubled. True joy arises from inner sincerity, not from outer pleasure. Discussing and practicing with friends nourishes virtue and multiplies delight.",
     "Lakes resting one on the other — The Joyous. The superior person joins with friends for discussion and practice."),

    (59, "渙", "Dispersion",           "Water",    "Wind",
     "Wind drives across water — dispersion of rigidity and separation. A hard heart melts; boundaries dissolve in a good cause. Cross the great water; visit the ancestral temple. Reunification.",
     "The wind drives over the water — Dispersion. The ancient kings made offerings to the Lord and built temples."),

    (60, "節", "Limitation",           "Lake",     "Water",
     "Water above the lake — limitation brings order and joy. Not all restrictions are burdensome — those that arise from one's own nature are sweetly endured. Galling limitations are not sustainable.",
     "Water above the lake — Limitation. The superior person creates number and measure and examines the nature of virtue and correct conduct."),

    (61, "中孚", "Inner Truth",         "Lake",     "Wind",
     "Wind over the lake — inner truth rippling outward. Even pigs and fishes can be moved by sincere inner truth. Cross the great water; perseverance furthers. True trust requires no outer proof.",
     "Wind over lake — Inner Truth. The superior person discusses criminal cases to delay executions."),

    (62, "小過", "Small Excess",        "Mountain", "Thunder",
     "Thunder on the mountain — a bird in flight. Small matters can be attended to; great undertakings should not be attempted now. Stay close to the ground. Do not reach too high; humble action fits.",
     "Thunder on the mountain — Small Excess. The superior person's conduct exceeds in reverence, mourning exceeds in grief."),

    (63, "既濟", "After Completion",    "Fire",     "Water",
     "Water above fire — everything in its place, all in order. Yet completion contains the seeds of disintegration — vigilance is essential. Small fox gets its tail wet crossing. Be cautious at the end.",
     "Water over fire — After Completion. The superior person thinks of misfortune and guards against it in advance."),

    (64, "未濟", "Before Completion",   "Water",    "Fire",
     "Fire above water — not yet completed. The young fox crosses and wets its tail just before the end. So close yet so far — maintain awareness throughout. Completion lies just ahead.",
     "Fire over water — Before Completion. The superior person carefully discriminates among things so each finds its place."),
]

# Build lookup by number
HEXAGRAM_BY_NUMBER = {h[0]: h for h in HEXAGRAMS}


def cast_hexagram() -> dict:
    """Cast a hexagram using the three-coin method (simplified).
    Returns hexagram dict with lines and any changing lines."""
    lines = []
    changing = []
    for i in range(6):
        # Three coins: heads=3, tails=2; sum 6-9
        coins = sum(random.choice([2, 3]) for _ in range(3))
        # 6=old yin (changing), 7=young yang, 8=young yin, 9=old yang (changing)
        is_yang = coins % 2 != 0  # odd=yang, even=yin (but 6&9 are changing)
        is_changing = coins in (6, 9)
        lines.append(is_yang)
        if is_changing:
            changing.append(i)

    # Find matching hexagram
    hexagram = _find_hexagram(lines)

    result = {
        "lines": lines,
        "changing": changing,
        "hexagram": hexagram,
    }

    # If there are changing lines, calculate the relating hexagram
    if changing:
        changed_lines = lines.copy()
        for i in changing:
            changed_lines[i] = not changed_lines[i]
        result["relating_hexagram"] = _find_hexagram(changed_lines)

    return result


def _find_hexagram(lines: list) -> dict:
    """Find hexagram matching given lines (bottom to top, True=yang)."""
    lower = tuple(lines[0:3])
    upper = tuple(lines[3:6])

    # Find trigram names
    lower_name = _trigram_name(lower)
    upper_name = _trigram_name(upper)

    for h in HEXAGRAMS:
        if h[3] == lower_name and h[4] == upper_name:
            return _hexagram_to_dict(h, lines)

    # Fallback: find by closest match
    return _hexagram_to_dict(HEXAGRAMS[0], lines)


def _trigram_name(trigram: tuple) -> str:
    for name, bits in TRIGRAMS.items():
        if bits == trigram:
            return name
    return "Heaven"


def _hexagram_to_dict(h: tuple, lines: list = None) -> dict:
    num, chinese, english, lower, upper, judgment, image = h
    return {
        "number": num,
        "chinese": chinese,
        "english": english,
        "lower_trigram": lower,
        "upper_trigram": upper,
        "lower_symbol": TRIGRAM_SYMBOLS.get(lower, "☰"),
        "upper_symbol": TRIGRAM_SYMBOLS.get(upper, "☷"),
        "judgment": judgment,
        "image": image,
        "lines": lines or list(TRIGRAMS.get(lower, (True,True,True))) + list(TRIGRAMS.get(upper, (True,True,True))),
    }


def hexagram_svg(lines: list, changing: list = None, width: int = 80) -> str:
    """Generate SVG for a hexagram."""
    changing = changing or []
    height = 120
    line_w = width - 20
    line_h = 6
    gap = 10
    start_y = 100
    cx = width // 2

    svg_lines = []
    for i, is_yang in enumerate(lines):
        y = start_y - i * (line_h + gap)
        is_ch = i in changing
        color = "#e8c98e" if is_ch else "#c9a96e"
        opacity = "1" if is_ch else "0.85"

        if is_yang:
            # Solid line
            svg_lines.append(
                f'<rect x="10" y="{y}" width="{line_w}" height="{line_h}" '
                f'fill="{color}" rx="1" opacity="{opacity}"/>'
            )
        else:
            # Broken line (two segments with gap)
            seg = (line_w - 10) // 2
            svg_lines.append(
                f'<rect x="10" y="{y}" width="{seg}" height="{line_h}" '
                f'fill="{color}" rx="1" opacity="{opacity}"/>'
                f'<rect x="{10 + seg + 10}" y="{y}" width="{seg}" height="{line_h}" '
                f'fill="{color}" rx="1" opacity="{opacity}"/>'
            )

    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        + "".join(svg_lines)
        + "</svg>"
    )
