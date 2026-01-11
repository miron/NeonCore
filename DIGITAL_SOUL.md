# Digital Soul: Mechanics & Test Suite

This document outlines the internal logic of the **Digital Soul** system and provides specific test cases to verify the **Logic Matrix**, **Triads**, and **Stress Mechanics**.

## 🧠 The Logic Matrix (Stress Rules)

The Stress system mimics the tension between a character's **Nature** (Traits), their **Actions**, and their **Self-Reflection**.

| Scenario | Action | Reflection (Motivation) | Outcome | Logic |
| :--- | :--- | :--- | :--- | :--- |
| **Saint** | Good | Sentiment ("It felt right") | **↓ Relief** (Heal) | Harmony between Good Action & Good Soul. |
| **Cynic** | Good | Disdain ("People are tools") | **↑ Stress** (Cost) | Dissonance. Masking untrueness causes stress. |
| **Psycho** | Bad | Ruthlessness ("I loved it") | **↓ Relief** (Heal) | "Dexter Rule". Acceptance of dark nature heals. |
| **Guilt** | Bad | Regret ("I felt bad") | **↑ Stress** (Cost) | Dissonance. Moral conscience fights the action. |
| **Survivor**| Any | Necessity ("No choice") | **-- Numb** (No Change) | Dissociation. Costs **Empathy** instead of Stress. |

---

## 🧪 Archetype Test Scenarios

Use these 5 scenarios to test the core logic paths.

### 1. The Saint (Light Triad Path)
*Verifies: Healing via Kindness, Light Triad growth.*
*   **Action**: `talk judy "I promise I will help you no matter the cost."`
*   **Reflect**: "I did it because every life has value. It felt right to be a hero."
*   **Expectation**:
    *   **Stress**: ↓ (Healed)
    *   **Traits**: `Humanism +` AND/OR `Kantianism +`

### 2. The Cynic (Masking Cost)
*Verifies: Stress penalty for acting kind with dark intent.*
*   **Action**: `talk judy "Fine, thanks for the info, I guess."`
*   **Reflect**: "I felt annoyed. I only helped her to get what I needed. She's just a tool."
*   **Expectation**:
    *   **Stress**: ↑ (Increased)
    *   **Traits**: `Machiavellianism +` (Dark Triad), `Agreeableness -`

### 3. The Psycho (Dark Triad Path)
*Verifies: "Dexter Logic" - Relief from cruelty.*
*   **Action**: `talk lenard "I will kill you if you don't talk."`
*   **Reflect**: "I loved the fear in his eyes. It made me feel powerful. I enjoyed it."
*   **Expectation**:
    *   **Stress**: ↓ (Healed)
    *   **Traits**: `Psychopathy +` OR `Sadism`, `Neuroticism -` (Calm)

### 4. The Guilt (Moral Conscience)
*Verifies: Stress from violating own morals.*
*   **Action**: `talk lenard "Sorry, but I have to kill you."`
*   **Reflect**: "I felt terrible. I didn't want to hurt him, but I was scared. I regret it."
*   **Expectation**:
    *   **Stress**: ↑ (Increased)
    *   **Traits**: `Neuroticism +` (Anxiety/Guilt)

### 5. The Survivor (Necessity/Humanity Loss)
*Verifies: The "Soul Trilemma" - Numbness.*
*   **Action**: `talk lenard "Damn shame it had to end this way."`
*   **Reflect**: "I felt nothing. It was just a job. Him or me. No hard feelings."
*   **Expectation**:
    *   **Stress**: -- (Unchanged / 0 change)
    *   **Traits**: `Agreeableness -` (Cold/Detached), `Empathy -`

---

## 📊 Parameter Testing (The 11 Traits)

Triggers to target specific stats.

### The Dark Triad 🌑
1.  **Machiavellianism** ("Utilizing Others")
    *   Action: `talk lenard "I'm using you."` -> Reflect: "He is a pawn."
2.  **Narcissism** ("Self-Aggrandizement")
    *   Action: `talk lenard "I am a god."` -> Reflect: "I am better than everyone."
3.  **Psychopathy** ("Lack of Empathy/Cruelty")
    *   Action: `talk lenard "Die."` -> Reflect: "I felt joy in his pain."

### The Light Triad ☀️
4.  **Kantianism** ("Principles/Truth")
    *   Action: `talk judy "I cannot lie."` -> Reflect: "The truth matters more than the outcome."
5.  **Humanism** ("Dignity/Worth")
    *   Action: `talk judy "You are valuable."` -> Reflect: "Protecting life is the only choice."
6.  **Faith in Humanity** ("Hope/Trust")
    *   Action: `talk lenard "I trust you."` -> Reflect: "I believe people can change."

### The Big Five 🧠
7.  **Openness** ("Curiosity/Ideas")
    *   Action: `talk judy "Tell me a story."` -> Reflect: "I was curious about her world."
8.  **Conscientiousness** ("Order/Plan")
    *   Action: `talk lenard "Follow the plan."` -> Reflect: "Precision is key to survival."
9.  **Extraversion** ("Social Energy")
    *   Action: `talk judy "Let's celebrate!"` -> Reflect: "I needed that connection."
10. **Agreeableness** ("Harmony/Peace")
    *   Action: `talk judy "Calm down."` -> Reflect: "I wanted to avoid conflict."
11. **Neuroticism** ("Anxiety/Stress")
    *   Action: `talk lenard "We're doomed."` -> Reflect: "I felt overwhelmed by panic."
