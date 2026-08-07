# 🧬⚙️ Biological, Cybernetic and Cognitive candidates — notes v0.1

```text
Статус:                       CAPTURED · RESEARCH_NOTES · NON_CANONICAL · DOCS_ONLY
Версия:                       0.1
Дата:                         2026-08-07
Область:                      Biological / cybernetic / cognitive-science inspiration for
                              future Mentaury research directions
Runtime authority:            NONE
Truth authority:              NONE
Capability authority:         NONE
Canon modification authority: NONE
Selection authority:          NONE — no candidate selected here
P0 scope authority:           NONE
Прямая запись в M3:           FORBIDDEN
Implementation in src/:       NOT AUTHORIZED
P1-001 priority impact:       NONE
```

> Этот документ фиксирует биологические, кибернетические и когнитивно-научные
> идеи как **research candidates**, а не как архитектурное решение. Он не
> меняет Canon, `AuthorityRef`, P1-001 contract, roadmap priority или runtime
> dependencies и не авторизует ни одной строки кода в `src/`.

```text
Metaphor ≠ mechanism
Biological inspiration ≠ implementation
Historical lesson ≠ architectural proof
Scientific plausibility ≠ engineering benefit
Candidate captured ≠ candidate selected
```

---

## 1. 🎯 Зачем эта заметка

Владелец задал прямой инженерный вопрос: можно ли сделать Mentaury «умнее»,
взяв что-то от человека, машины, животного и растительного мира, а также из
идей XX века, которые не были доведены до конца. Первый черновой ответ был
каталогом красивых аналогий. Этого недостаточно: без явного перехода

```text
биологическое явление
→ вычислительный принцип
→ граница применимости
→ существующий модуль Mentaury
→ проверяемая гипотеза
→ минимальный эксперимент
→ критерий провала
```

любая биомимикрия рискует стать декоративной, а не инженерной. Эта заметка
обязывает каждый кандидат пройти именно такую цепочку, прежде чем он вообще
может рассматриваться для будущей promotion gate.

---

## 2. 🏷️ Классификация кандидатов

Каждый кандидат помечается ровно одним классом:

```text
M — METAPHOR ONLY
    Полезна для объяснения человеку, не должна попадать в алгоритмы
    или в код напрямую.

P — ENGINEERING PRINCIPLE
    Общий проектный принцип (например, "координация через видимый след"),
    не готовый алгоритм.

A — ALGORITHM CANDIDATE
    Достаточно конкретен, чтобы проверить экспериментом с baseline
    и критерием провала.

C — CONTROL PATTERN
    Обратная связь, пороги, регулирование ресурсов; требует явного
    sensed variable / target range / actuator.

W — HISTORICAL WARNING
    Антипаттерн или governance-урок; не источник алгоритма, а
    предупреждение о том, чего избегать.
```

```text
Class M кандидат в коде
→ ЗАПРЕЩЕНО без явного computational transfer

Class W кандидат
→ никогда не становится algorithm candidate
→ используется только как проверка "не повторяем ли мы это"
```

---

## 3. 🃏 Формат карточки кандидата

Каждый кандидат ниже описан одинаковыми полями:

```text
Research ID:
Source phenomenon:
Scientific confidence:
Transfer class:
Existing Mentaury analogue:
Computational transfer hypothesis:
Expected benefit:
Minimal experiment:
Baseline:
Failure / falsification criterion:
Governance risk:
Non-claims:
Promotion gate:
```

---

## 4. 🔴 HIGH priority candidates

### 4.1. ⚡🧠 Complementary Learning Systems (CLS)

```text
Research ID:                       R-CLS-001
Source phenomenon:                 Complementary Learning Systems theory
                                    (fast hippocampal episodic encoding +
                                    slow neocortical semantic integration)
Scientific confidence:             established theory in cognitive
                                    neuroscience; not a metaphor-only claim
Transfer class:                    A — ALGORITHM CANDIDATE
Existing Mentaury analogue:        event capture (P0-001…P0-013) +
                                    minimal belief lifecycle (P0-014/015)
Computational transfer hypothesis: разделить (1) быстрый, детальный,
                                    малообобщающий episodic capture и (2) более
                                    медленную, интерливинговую semantic
                                    integration, которая объединяет новое
                                    знание со старым постепенно, чтобы не
                                    разрушать уже усвоенную структуру
                                    (protection against catastrophic
                                    interference) и сохраняет pattern
                                    separation между похожими эпизодами
Expected benefit:                  меньше конфликтов между новым и старым
                                    знанием; более устойчивые belief updates;
                                    явная граница между "что произошло" и
                                    "что мы теперь думаем"
Minimal experiment:                на синтетическом наборе похожих и
                                    противоречащих событий сравнить (a) прямую
                                    немедленную запись в belief state и
                                    (b) episodic capture → interleaved replay →
                                    governed integration по числу вызванных
                                    contradiction/rejection событий и по
                                    устойчивости старых beliefs после серии
                                    новых похожих эпизодов
Baseline:                          текущий прямой belief lifecycle (P0-014)
                                    без отдельного episodic buffer
Failure / falsification criterion: если interleaved integration не снижает
                                    число regressions/contradictions
                                    по сравнению с baseline на тех же
                                    входных данных — гипотеза отклоняется
Governance risk:                   средний — "медленная интеграция" не должна
                                    стать скрытым обходом Evidence Gate
Non-claims:                        CLS ≠ доказательство, что Mentaury обучается
                                    как мозг; это архитектурный паттерн, а не
                                    биологическое утверждение
Promotion gate:                    отдельный RFC внутри Mentaury + independent
                                    review + прохождение эксперимента выше;
                                    без этого — остаётся CAPTURED
```

### 4.2. 😴🔁 Offline and awake replay

```text
Research ID:                       R-REPLAY-001
Source phenomenon:                 нейронный replay, наблюдаемый не только во
                                    сне, но и во время пауз и спокойного
                                    бодрствования; связан с консолидацией и
                                    извлечением воспоминаний
Scientific confidence:             хорошо документировано в нейронауке;
                                    перенос в software — гипотеза, не факт
Transfer class:                    A — ALGORITHM CANDIDATE
Existing Mentaury analogue:        R1 deterministic replay (P0-013);
                                    Evidence Gate (P0-015); R-MM-001 Memory
                                    Metabolism (captured backlog item)
Computational transfer hypothesis: фоновая обработка накопленного опыта может
                                    выполняться не только в буквальном
                                    "sleep window", а в любые периоды простоя
                                    или низкой нагрузки; результат такой
                                    обработки — это ТОЛЬКО кандидат, который
                                    обязан пройти evidence, contradiction и
                                    authority gates, прежде чем что-либо
                                    изменится в belief state
Expected benefit:                  более качественная консолидация без
                                    отдельного дорогостоящего "sleep worker";
                                    лучше научно обоснованная схема, чем
                                    буквальный SleepTimeWorker
Minimal experiment:                сравнить belief-lifecycle outcome при (a)
                                    немедленной интеграции каждого события и
                                    (b) отложенной batched переоценке в
                                    периоды простоя, на identical replay traces
Baseline:                          немедленная посистемная обработка каждого
                                    события без отложенного batching
Failure / falsification criterion: если отложенная обработка не снижает
                                    число дублирующихся/противоречивых belief
                                    revisions и не даёт измеримой экономии
                                    ресурсов — гипотеза отклоняется
Governance risk:                   высокий, если не зафиксировать явно —
                                    "replay result" не может писать в belief
                                    state в обход Evidence Gate
Non-claims:                        replay ≠ automatic truth promotion;
                                    idle-time processing ≠ автономный goal;
                                    "как во сне" — метафора расписания, а не
                                    доказательство психологического сна
Promotion gate:                    формальная спецификация "replay pipeline"
                                    внутри существующих Evidence Gate/lifecycle
                                    контрактов + independent review
```

### 4.3. 🌡️🔧 Homeostasis / allostasis as a resource-control pattern

```text
Research ID:                       R-HOMEO-001
Source phenomenon:                 гомеостаз (Cannon) и его развитие —
                                    allostasis: поддержание переменной в
                                    допустимом диапазоне через постоянный
                                    цикл измерения и коррекции, а не через
                                    статичный лимит
Scientific confidence:             установленный физиологический механизм;
                                    инженерный аналог (feedback control) —
                                    отдельная, проверяемая абстракция
Transfer class:                    C — CONTROL PATTERN
Existing Mentaury analogue:        `VerificationBudget` (P0-009)
Computational transfer hypothesis: полноценный homeostatic loop требует ВСЕХ
                                    элементов: sensed variable → target range
                                    → measured error → regulating actuator →
                                    re-measurement. `VerificationBudget`
                                    сегодня — это статичное ограничение
                                    (constraint/actuator), а НЕ полный
                                    контур: он не измеряет текущее давление
                                    на ресурсы и не адаптирует сам себя.
                                    Пример полного контура:
                                    memory pressure → превышение порога →
                                    снижение глубины фонового анализа →
                                    освобождение ресурсов → повторная оценка
Expected benefit:                  предсказуемая деградация под нагрузкой
                                    вместо жёсткого отказа или неограниченного
                                    потребления ресурсов
Minimal experiment:                смоделировать нарастающую нагрузку
                                    (объём событий/replay work) и сравнить
                                    (a) фиксированный `VerificationBudget` без
                                    обратной связи и (b) explicit control loop
                                    с sensed variable и adaptive actuator по
                                    метрикам задержки и отказов
Baseline:                          текущий статичный `VerificationBudget`
                                    без адаптивного контура
Failure / falsification criterion: если adaptive loop не снижает частоту
                                    жёстких отказов/budget exhaustion при той
                                    же нагрузке — гипотеза отклоняется
Governance risk:                   низкий при условии, что actuator не
                                    получает право менять authority/consent
                                    decisions, только вычислительный бюджет
Non-claims:                        `VerificationBudget` = возможный
                                    actuator/constraint;
                                    `VerificationBudget` ≠ полный homeostatic
                                    controller;
                                    гомеостаз ≠ доказательство "живости" системы
Promotion gate:                    явная спецификация sensed variable, target
                                    range, actuator и remeasurement cycle как
                                    отдельного P0/post-P0 control-module RFC
                                    + independent review
```

### 4.4. 👁️🎯 Active perception / active inference (candidate, handled with caution)

```text
Research ID:                       R-ACTINF-001
Source phenomenon:                 active inference: восприятие, планирование
                                    и действие как единый процесс
                                    вероятностного вывода, направленный на
                                    уменьшение значимой неопределённости, а
                                    не только на реакцию на входные данные
Scientific confidence:             активная область исследований в
                                    computational neuroscience; влиятельная,
                                    но не единственная теория; инженерный
                                    перенос требует осторожности
Transfer class:                    A — ALGORITHM CANDIDATE (высокий governance
                                    risk; не путать с "готовым принципом")
Existing Mentaury analogue:        Evidence Gate (P0-015) — уже есть понятие
                                    evidence, необходимого для смены статуса
Computational transfer hypothesis: система может явно выбирать, какое
                                    наблюдение или уточняющий запрос
                                    максимально снижает релевантную
                                    неопределённость, вместо пассивного
                                    ожидания входных данных — НО без
                                    превращения этого в единственную
                                    монолитную цель ("минимизировать
                                    surprise"); goals, consent и bounded
                                    authority остаются внешними ограничениями,
                                    а не частью одной оптимизируемой функции
Expected benefit:                  более целенаправленный сбор evidence перед
                                    belief revision вместо пассивного
                                    накопления
Minimal experiment:                сравнить (a) пассивный порядок обработки
                                    evidence "как пришло" и (b) активный выбор
                                    "какое evidence запросить/приоритизировать
                                    следующим" по числу шагов до устойчивого
                                    belief resolution
Baseline:                          текущая пассивная последовательная
                                    обработка evidence без явного uncertainty
                                    targeting
Failure / falsification criterion: если активный выбор не снижает число
                                    шагов/времени до устойчивого разрешения
                                    неопределённости — гипотеза отклоняется
Governance risk:                   высокий — легко скатиться в единый
                                    "surprise-minimizing" objective, который
                                    конфликтует с bounded authority и consent
Non-claims:                        active inference ≠ единственная цель
                                    системы; ≠ автономный goal-seeking behavior;
                                    ≠ замена явного human-authorized scope
Promotion gate:                    отдельный RFC с явным перечнем того, что
                                    НЕ оптимизируется этим механизмом
                                    (authority, consent, external actions) +
                                    independent review + узкий bounded
                                    эксперимент до любого расширения
```

### 4.5. 🐜📜 Stigmergic event coordination

```text
Research ID:                       R-STIG-001
Source phenomenon:                 стигмергия у муравьёв и других
                                    насекомых — координация через изменения,
                                    оставленные в общей среде, а не через
                                    прямую коммуникацию между агентами
Scientific confidence:             хорошо документированное явление в
                                    биологии и multi-agent systems research
Transfer class:                    P / A — ENGINEERING PRINCIPLE, частично
                                    ALGORITHM CANDIDATE
Existing Mentaury analogue:        immutable event history (P0-004),
                                    Evidence Ledger / Evidence Gate (P0-015)
Computational transfer hypothesis: процессы/модули Mentaury не обязаны
                                    координироваться напрямую — они оставляют
                                    проверяемые изменения в immutable event
                                    history, а другие процессы реагируют на
                                    эти следы асинхронно
Expected benefit:                  меньше связности между модулями; легче
                                    воспроизводимость (replay уже доказывает
                                    детерминизм); естественное согласование с
                                    существующей event-substrate архитектурой
Minimal experiment:                сравнить прямое межмодульное вызовное
                                    взаимодействие и event-trace-based
                                    реакцию по количеству связей/зависимостей
                                    и по устойчивости к добавлению нового
                                    независимого потребителя событий
Baseline:                          текущая прямая интеграция между
                                    компонентами belief lifecycle
Failure / falsification criterion: если event-trace-координация не снижает
                                    связность и не упрощает добавление нового
                                    независимого consumer — гипотеза
                                    отклоняется как не дающая измеримой пользы
Governance risk:                   низкий при строгом соблюдении границы ниже
Non-claims:                        event history = координационный след;
                                    event history ≠ команда;
                                    event history ≠ authority
Promotion gate:                    формальное описание, какие модули могут
                                    "читать след" и какие инварианты они
                                    обязаны сохранять + independent review
```

---

## 5. 🟠 MEDIUM priority candidates

### 5.1. 🦠🛡️ Immune danger/tolerance model (not self/non-self)

```text
Research ID:                       R-DANGER-001
Source phenomenon:                 danger-модель иммунитета: реакция
                                    определяется не просто "чужеродностью"
                                    (self/non-self), а повреждением, стрессом
                                    ткани и контекстом; многие чужеродные
                                    элементы переносимы, а собственные могут
                                    вызывать реакцию при повреждении
Scientific confidence:             признанная, более современная модель по
                                    сравнению с упрощённым self/non-self
Transfer class:                    P / C — ENGINEERING PRINCIPLE + CONTROL
                                    PATTERN (quarantine/threshold logic)
Existing Mentaury analogue:        belief contradiction handling (P0-014),
                                    Evidence Gate rejection paths (P0-015)
Computational transfer hypothesis: заменить упрощённую пару "известный
                                    источник / неизвестный источник" на явные
                                    независимые оси: known/unknown,
                                    safe/potentially-dangerous,
                                    damage/conflict/anomaly,
                                    trusted/tolerated; новый источник не
                                    равен угрозе, знакомый источник не равен
                                    безопасности, аномалия не равна лжи,
                                    конфликт не означает автоматическое
                                    удаление
Expected benefit:                  более точная quarantine-логика для
                                    подозрительного evidence без чрезмерного
                                    отбрасывания легитимных новых источников
Minimal experiment:                на синтетическом наборе evidence с
                                    размеченными комбинациями
                                    known/unknown × safe/damaging сравнить
                                    текущую бинарную обработку и
                                    multi-axis danger-модель по числу
                                    ложных quarantine и пропущенных аномалий
Baseline:                          текущая обработка evidence без явной
                                    danger-таксономии
Failure / falsification criterion: если multi-axis модель не снижает
                                    одновременно false-quarantine и
                                    missed-anomaly rate — гипотеза отклоняется
Governance risk:                   средний — quarantine логика не должна
                                    получить право на permanent deletion
Non-claims:                        danger-модель ≠ self/non-self;
                                    anomaly ≠ falsehood;
                                    quarantine ≠ deletion
Promotion gate:                    явная схема осей + связь с существующими
                                    reason codes Evidence Gate + independent
                                    review
```

### 5.2. 🕸️⚖️ Distributed local/global control

```text
Research ID:                       R-DISTCTRL-001
Source phenomenon:                 биологические и инженерные системы, где
                                    локальные узлы принимают решения
                                    самостоятельно, а глобальный уровень
                                    осуществляет только ограниченный арбитраж
                                    (например, гомеостатические подсистемы
                                    тела, децентрализованные control systems)
Scientific confidence:             общий инженерный/биологический принцип,
                                    не единая теория
Transfer class:                    P — ENGINEERING PRINCIPLE
Existing Mentaury analogue:        разделение P0 модулей (storage, integrity,
                                    lifecycle, evidence gate) с чёткими
                                    границами ответственности
Computational transfer hypothesis: каждый модуль Mentaury принимает локальные
                                    решения в своей узкой границе (schema
                                    admission, redaction, evidence
                                    evaluation), а global arbitration
                                    (authority, governance policy) остаётся
                                    ограниченным и explicit, а не растворяется
                                    по модулям
Expected benefit:                  меньше скрытых implicit global decisions;
                                    легче аудировать, какой модуль отвечает
                                    за какое решение
Minimal experiment:                архитектурный review существующих module
                                    boundaries на предмет случаев, где
                                    локальный модуль неявно принимает
                                    global-level решение (например, authority
                                    check внутри storage layer)
Baseline:                          текущее распределение ответственности без
                                    формализованного local/global различения
Failure / falsification criterion: если формализация не находит ни одного
                                    реального case неявного global decision
                                    внутри local module — принцип остаётся
                                    декларативным, не даёт измеримой пользы
                                    сейчас
Governance risk:                   низкий — это в основном принцип для
                                    документации существующих границ, не
                                    новый механизм
Non-claims:                        принцип ≠ новый runtime slice;
                                    ≠ распределённая multi-node система
Promotion gate:                    architecture-review note; не требует
                                    отдельного эксперимента для документации,
                                    но требует independent review перед
                                    ссылкой как на "принятый принцип"
```

### 5.3. 🍄🛤️ Physarum-inspired resource-aware routing

```text
Research ID:                       R-PHYSARUM-001
Source phenomenon:                 Physarum polycephalum (слизевик) находит и
                                    укрепляет эффективные пути в сети ресурсов
                                    через положительную обратную связь
Scientific confidence:             хорошо задокументированный биологический
                                    эксперимент; уже исследуется как external
                                    research input соседним проектом
                                    Native Kernel (`PHYSARUM_ROUTING_EXPERIMENT`)
Transfer class:                    A — ALGORITHM CANDIDATE (экспериментальный)
Existing Mentaury analogue:        нет прямого аналога; потенциально —
                                    будущая маршрутизация проверки/обработки
                                    ресурсов при масштабировании R0/R1
Computational transfer hypothesis: гипотеза resource-aware маршрутизации:
                                    пути обработки, которые чаще оказываются
                                    полезными (например, порядок verification
                                    при ограниченном budget), могут получать
                                    усиление по аналогии с укреплением путей
                                    Physarum
Expected benefit:                  потенциально более эффективное
                                    распределение ограниченного
                                    verification/processing budget под
                                    нагрузкой
Minimal experiment:                сравнить Physarum-inspired маршрутизацию
                                    с простыми baseline: shortest-path,
                                    priority queue, round-robin load
                                    balancing — на синтетической нагрузке
                                    verification requests
Baseline:                          shortest-path / priority queue / simple
                                    load balancing
Failure / falsification criterion: если Physarum-inspired подход не даёт
                                    измеримого преимущества над простыми
                                    baseline — кандидат отклоняется
                                    ("reject it if it gives no measurable
                                    benefit")
Governance risk:                   низкий — это чисто scheduling/routing
                                    эксперимент без доступа к authority или
                                    identity state
Non-claims:                        биологическая аналогия ≠ доказанное
                                    инженерное преимущество до эксперимента
Promotion gate:                    результаты эксперимента выше + independent
                                    review; без измеримой пользы остаётся
                                    CAPTURED / REJECTED
```

---

## 6. ⚪ METAPHOR ONLY candidates

### 6.1. 🌲🍄 Mycorrhizal networks (disputed / context-dependent)

```text
Research ID:                       R-MYCO-001
Source phenomenon:                 симбиоз растений и грибов (микориза) —
                                    хорошо установленное явление; но
                                    популярные утверждения о повсеместной
                                    "лесной сети", целенаправленной передаче
                                    ресурсов и "родительской помощи" деревьев
                                    подвергаются серьёзной научной критике;
                                    часть более новых работ защищает
                                    отдельные формы передачи ресурсов, так
                                    что область остаётся спорной
Scientific confidence:             СПОРНО / контекстно-зависимо — не
                                    установленный факт в сильной
                                    интерпретации ("wood-wide web")
Transfer class:                    M — METAPHOR ONLY
Existing Mentaury analogue:        relationship/commitment research
                                    (`MENTAURY_IDENTITY_CONTINUITY_AND_
                                    RELATIONAL_ARCHITECTURE_NOTES.md`)
Computational transfer hypothesis: НЕТ точного вычислительного переноса на
                                    этом этапе; допустима только как
                                    объяснительная метафора "контекстно-
                                    зависимого обмена между связанными
                                    узлами", не как модель "интернета
                                    деревьев"
Expected benefit:                  риторическая ясность при объяснении идеи
                                    relationship-context sharing человеку;
                                    НЕ инженерное преимущество само по себе
Minimal experiment:                неприменимо, пока не будет предложен
                                    точный вычислительный transfer
                                    (если появится — кандидат переклассифи-
                                    цируется в P или A)
Baseline:                          неприменимо
Failure / falsification criterion: неприменимо на уровне M; кандидат
                                    "проваливается" в algorithm candidate,
                                    если никто не предложит точный transfer
Governance risk:                   низкий, если используется только как
                                    метафора в тексте, не в архитектуре
Non-claims:                        mycorrhizal symbiosis ≠ доказанная модель
                                    "интернета деревьев";
                                    metaphor / ecological inspiration only
Promotion gate:                    требуется отдельный точный computational
                                    transfer proposal, прежде чем этот
                                    кандидат сможет претендовать на класс P/A
```

### 6.2. 🧬🎭 Epigenetic expression

```text
Research ID:                       R-EPI-001
Source phenomenon:                 эпигенетика — контекстно-зависимая
                                    экспрессия генома без изменения самой
                                    последовательности ДНК
Scientific confidence:             установленный биологический механизм;
                                    архитектурный перенос — метафора, не
                                    доказательство
Transfer class:                    M — METAPHOR ONLY
Existing Mentaury analogue:        Character as presentation (P0-INV-7
                                    "Style ≠ Epistemic State"); Canon v0.1
                                    frozen constraints
Computational transfer hypothesis: НЕ буквальное "Canon = genome, Character =
                                    epigenetic expression". Корректная
                                    формулировка: immutable constitutional
                                    constraints (Canon) допускают
                                    контекстно-зависимое выражение поведения
                                    (Character/Presentation), не меняя сами
                                    ограничения. Это объяснительная метафора,
                                    не инженерное доказательство архитектуры
Expected benefit:                  более понятное объяснение "почему
                                    Character меняется, а Canon — нет" для
                                    человека; не даёт нового алгоритма
Minimal experiment:                неприменимо на уровне метафоры
Baseline:                          неприменимо
Failure / falsification criterion: неприменимо
Governance risk:                   низкий, но есть риск, что кто-то
                                    воспримет метафору буквально и предложит
                                    "мутируемый Canon" — явно запрещено
Non-claims:                        Canon ≠ геном в биологическом смысле;
                                    Character change ≠ Canon change;
                                    метафора ≠ инженерное доказательство
Promotion gate:                    не подлежит promotion как есть; может
                                    использоваться только как narrative
                                    explanation в документации
```

---

## 7. ⚠️ Historical warnings (class W)

Эти кандидаты — **не источники алгоритмов**, а проверка "не повторяем ли мы
чужую ошибку".

### 7.1. 📚🚫 GOFAI / Cyc — knowledge-acquisition bottleneck

```text
Research ID:      R-WARN-GOFAI-001
Source phenomenon: попытка вручную закодировать весь common sense (проект
                   Cyc и шире — GOFAI символьный подход)
Transfer class:    W — HISTORICAL WARNING
Lesson:            ручное кодирование "полного знания" упирается в
                   knowledge-acquisition и maintenance bottleneck и не
                   масштабируется
Mentaury guardrail: не пытаться построить "полный Canon на все случаи
                   жизни" — только один bounded milestone за раз
                   (текущая P1-001-first дисциплина уже соответствует
                   этому уроку)
Non-claims:        Mentaury Canon ≠ Cyc-подобная попытка тотальной базы
                   знаний
```

### 7.2. 🧩🌐 General Problem Solver — excessive universality

```text
Research ID:      R-WARN-GPS-001
Source phenomenon: General Problem Solver (Newell & Simon) — попытка создать
                   единый универсальный решатель произвольных задач
Transfer class:    W — HISTORICAL WARNING
Lesson:            чрезмерная универсальность без конкретной scoped границы
                   плохо масштабируется и плохо проверяется
Mentaury guardrail: P1-001 Capability Lease Resolution — намеренно узкий,
                   scoped resolver, а не universal problem solver; это
                   прямое инженерное следствие данного урока, а не совпадение
Non-claims:        ни один текущий или будущий Mentaury модуль не должен
                   стремиться стать "универсальным решателем"
```

### 7.3. 🏛️🔌 OGAS — institutional misalignment (nuanced)

```text
Research ID:      R-WARN-OGAS-001
Source phenomenon: советский проект ОГАС (Глушков) — общегосударственная
                   автоматизированная система управления
Transfer class:    W — HISTORICAL WARNING
Lesson:            исторические исследования описывают провал как
                   комбинацию бюрократических препятствий, институционального
                   конфликта и неспособности ведомств согласовать власть над
                   общей сетью — а не просто "не было независимой проверки".
                   Корректный урок: технически сильная система +
                   несовместимые центры власти + неясное распределение
                   полномочий = проект может не состояться
Mentaury guardrail: independent-review policy (issue #39) мотивирована этим
                   более widely, а НЕ прямым доказательством "нужен именно
                   второй GitHub reviewer"; ОГАС — иллюстрация общего риска
                   institutional misalignment, не техническая спецификация
                   review policy
Non-claims:        OGAS failure ≠ прямое доказательство конкретного правила
                   GitHub branch protection; это общий governance-урок,
                   не техническое требование
```

### 7.4. ❄️📉 AI winters — claims must not outrun evidence

```text
Research ID:      R-WARN-AIWINTER-001
Source phenomenon: циклы завышенных ожиданий и последующего разочарования в
                   истории AI (включая критику перцептронов Minsky/Papert)
Transfer class:    W — HISTORICAL WARNING
Lesson:            публичные заявления о возможностях, опережающие reale
                   evidence, приводят к потере доверия и финансирования на
                   годы вперёд
Mentaury guardrail: `DOCS_ONLY · NOT IMPLEMENTED` маркеры, freshness gate
                   (`scripts/check_doc_freshness.py`) и правило
                   "OPEN PR ≠ implemented in main" — прямая защита от
                   повторения этой ошибки
Non-claims:        ни один research candidate в этом документе не должен
                   быть представлен как уже работающая возможность Mentaury
```

---

## 8. 🧾 Related taxonomy note — forgetting is not one mechanism

Замечание к R-CLS-001/R-REPLAY-001: недопустимо объединять в одну операцию
разные механизмы с разными truth- и governance-последствиями:

```text
decay          → становится менее доступным (мягкое понижение приоритета)
compression    → сохраняется обобщённая структура, детали теряются
redaction      → payload удаляется по governed процедуре (P0-010),
                 provenance события сохраняется
suppression    → временно не используется, обратимо
consolidation  → интеграция в устойчивую semantic-структуру (см. R-CLS-001)
"forgetting"   → общий бытовой термин, НЕ одна операция
```

Любая будущая работа над R-MM-001 (Memory Metabolism, captured backlog item в
`RESEARCH_INDEX.md`) обязана использовать эти пять терминов раздельно, а не
единое слово "забывание".

---

## 9. 📊 Priority table

```text
HIGH:
  R-CLS-001      Complementary Learning Systems
  R-REPLAY-001   Offline and awake replay
  R-HOMEO-001    Homeostatic resource regulation
  R-ACTINF-001   Active perception / active inference (handled with caution)
  R-STIG-001     Stigmergic event coordination

MEDIUM:
  R-DANGER-001    Immune danger/tolerance model
  R-DISTCTRL-001  Distributed local/global control
  R-PHYSARUM-001  Physarum-inspired routing

METAPHOR ONLY:
  R-MYCO-001  Mycorrhizal networks
  R-EPI-001   Epigenetic expression

HISTORICAL WARNINGS:
  R-WARN-GOFAI-001     GOFAI / Cyc knowledge-acquisition bottleneck
  R-WARN-GPS-001       General Problem Solver excessive universality
  R-WARN-OGAS-001      OGAS institutional misalignment
  R-WARN-AIWINTER-001  AI winters — claims must not outrun evidence
```

---

## 10. 🧭 Concrete research program (mandatory sequence)

Ни один кандидат выше не может миновать эту последовательность:

```text
Candidate (M/P/A/C/W)
→ bounded experiment (для A/C) или architecture note (для P)
→ baseline comparison
→ measurable benefit demonstrated
→ falsification attempted and survived
→ governance / independent review
→ explicit repository-owner selection
→ only then implementation planning (still not this document)
```

```text
Class M кандидат
→ никогда не проходит эту последовательность как есть;
  должен сначала получить точный computational transfer proposal,
  чтобы претендовать на переклассификацию в P или A

Class W кандидат
→ никогда не проходит эту последовательность;
  используется только как guardrail-проверка
```

---

## 11. 🚫 Явные запреты для этого документа

```text
❌ изменения в src/
❌ изменения в .github/workflows
❌ изменения Canon
❌ изменения AuthorityRef
❌ изменения P1-001 contract
❌ изменения roadmap priority
❌ изменения runtime dependencies
❌ Action Gate
❌ M3 writes
❌ Identity runtime
❌ Relationship runtime
❌ Native Kernel / Titan / Crystal integration
❌ смешивание с PR #38 (P1-001 hardening) или PR #45 (status sync / storage-graph candidates)
```

---

## 12. 📌 Текущее решение

```text
Candidates captured:        14 (5 HIGH · 3 MEDIUM · 2 METAPHOR ONLY · 4 WARNING)
Candidates selected:        0
Runtime wiring:             NOT AUTHORIZED
Execution milestone created: NO
P1-001 priority:            UNCHANGED
```

См. также:

- `RESEARCH_INDEX.md` — навигационный индекс, пока существует только в открытом
  PR #38; регистрация этой заметки — отдельный шаг после merge #38 (не
  markdown-ссылка здесь, чтобы не создавать broken link на текущем `main`);
- `STORAGE_AND_GRAPH_PROFILE_CANDIDATES_V0.1.md` — тот же паттерн
  `CAPTURED · NOT SELECTED`, пока существует только в открытом PR #45
  (не markdown-ссылка здесь по той же причине);
- [`MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md`](MENTAURY_IDENTITY_CONTINUITY_AND_RELATIONAL_ARCHITECTURE_NOTES.md) —
  relationship research, релевантно для R-MYCO-001 и R-DANGER-001;
- [`../MENTAURY_P0_IMPLEMENTATION_PLAN.md`](../MENTAURY_P0_IMPLEMENTATION_PLAN.md) —
  `P0-INV-6 Implementation Profile ≠ Canon`, `P0-INV-7 Style ≠ Epistemic State`.
