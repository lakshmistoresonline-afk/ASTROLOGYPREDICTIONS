# 🗺️ GURUKUL HINDI SOURCE-TO-UI MAPPING MATRIX

## Executive Summary
This document provides the complete mapping matrix connecting every raw field from the 5 source JSON files (`Notes(2).json`, `Master(2).json`, `Flashcards(1).json`, `Quiz(2).json`, `Mindmaps.json`) to the corresponding UI stage, accordion section, and renderer component in the running Hindi Dashboard.

---

## 1. Complete Source-to-UI Mapping Table

| Source File | Source JSON Field | Target Dashboard Tab | UI Section / Accordion Header | Renderer Component | Navigation / Reachability |
|---|---|---|---|---|---|
| `Notes(2).json` | `summary` | **OVERVIEW** | पाठ का सारांश | `SummaryRenderer` | Direct View |
| `Notes(2).json` | `centralTheme` | **OVERVIEW** | मुख्य भाव एवं सन्देश | `ThemeRenderer` | Direct View |
| `Notes(2).json` | `detailedExplanation` | **LEARN** | पाठ को समझें | `ExplanationRenderer` | Accordion Section 1 |
| `Notes(2).json` | `stanzaExplanations[]` | **LEARN** | काव्यांश व्याख्या | `StanzaRenderer` | Accordion Section 2 |
| `Notes(2).json` | `vocabulary[]` | **LEARN** | शब्दावली (शब्द-अर्थ) | `VocabularyRenderer` | Accordion Section 3 |
| `Notes(2).json` | `synonyms[]` | **LEARN** | पर्यायवाची शब्द | `SynonymRenderer` | Accordion Section 4 |
| `Notes(2).json` | `antonyms[]` | **LEARN** | विलोम शब्द | `AntonymRenderer` | Accordion Section 5 |
| `Notes(2).json` | `spelling[]` | **LEARN** | शुद्ध वर्तनी अभ्यास | `SpellingRenderer` | Accordion Section 6 |
| `Notes(2).json` | `grammar[]` | **LEARN** | भाषा-बोध एवं व्याकरण | `GrammarRenderer` | Accordion Section 7 |
| `Notes(2).json` | `activities[]` | **LEARN** | गतिविधियाँ एवं अनुभव | `ActivityRenderer` | Accordion Section 8 |
| `Mindmaps.json` | `central_node` + branches | **LEARN** | Mind Map (ज्ञान वृक्ष) | `MindmapRenderer` | Accordion Section 9 (Embedded) |
| `Master(2).json` | `questionBank.mcq[]` | **PRACTICE** | शब्द एवं व्याकरण अभ्यास | `QuestionSetRenderer` | Practice Section A |
| `Master(2).json` | `questionBank.shortAnswer[]`| **PRACTICE** | पाठ-बोध (लघु उत्तरीय) | `QuestionSetRenderer` | Practice Section B |
| `Master(2).json` | `questionBank.longAnswer[]` | **PRACTICE** | विचार एवं तर्क (दीर्घ उत्तरीय) | `QuestionSetRenderer` | Practice Section C |
| `Master(2).json` | `questionBank.extractBased[]`| **PRACTICE** | पद्यांश-बोध | `QuestionSetRenderer` | Practice Section D |
| `Master(2).json` | `modelQuestionPaper` | **PRACTICE** | आदर्श प्रश्न-पत्र (Model Paper) | `ModelPaperRenderer` | Practice Section E |
| `Flashcards(1).json`| `flashcards[]` (HN01-FC001..20) | **REVISION** | स्मरण कार्ड (20 Cards) | `FlashcardRenderer` | Card X of Y (Prev/Flip/Next) |
| `Quiz(2).json` | `questions[]` (18 Questions) | **QUIZ** | मूल्यांकन प्रश्नोत्तरी | `QuizRenderer` | Question X of N (One-at-a-time) |

---

## 2. Five-Stage Pedagogical Journey Structure
- **Stage 1: OVERVIEW (अवलोकन)**: Summary, central theme, chapter metadata.
- **Stage 2: LEARN (अध्ययन)**: Complete explanations, stanzas, vocabulary, synonyms, antonyms, spelling, grammar, activities, and embedded recursive mindmap.
- **Stage 3: PRACTICE (अभ्यास)**: Categorized accordions for Word Practice, Grammar Practice, Comprehension, Short/Long Answer questions, Creative Writing, and sectioned Model Question Paper.
- **Stage 4: REVISION (पुनरावृत्ति)**: Dynamic flashcards with category filters (Literature, Vocabulary, Grammar, Spelling), flip animations, and mastery tracking.
- **Stage 5: QUIZ (परीक्षण)**: One-question-at-a-time quiz interface with progress bar, immediate feedback, and generic fallback renderers for all question types.
