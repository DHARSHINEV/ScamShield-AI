# HackNowa Global Hackathon 2026 Submission Material

**Project Title:**  
ScamShield AI – Detect It. Understand It. Prevent It.

**Track:**  
Digital Safety & Cybersecurity

**Secondary Fit:**  
AI for Everyday Life

**One-Line Description:**  
An explainable multimodal AI cybersecurity assistant that detects scams, explains the evidence, recommends protective actions, protects families, and trains users through interactive scam simulations.

---

## 100-Word Description (Executive Summary)

ScamShield AI is an explainable cybersecurity assistant protecting everyday users from evolving digital fraud. Beyond binary blocking, ScamShield ingests messages, links, screenshots, QR codes, and voice notes. It synthesizes heuristic rules, lexical feature extraction, and trained machine learning into a calibrated risk score with sub-millisecond latency. Through TrustLens, ScamShield answers *why* an input is dangerous, highlighting psychological manipulation triggers and providing verified incident response steps (Helpline 1930). With 1-click share-ready Family Guardian alerts and the gamified Scam Dojo simulation gym, ScamShield transforms everyday citizens from vulnerable targets into proactive, resilient defenders. *(96 words)*

---

## 250-Word Description (Comprehensive Overview)

Cyber fraud across emerging economies has evolved from obvious malware into hyper-targeted social engineering—including fake bank KYC updates, courier reschedule micro-payments, and coercive digital arrests. Traditional security tools fail ordinary citizens because they operate as opaque black boxes, checking static blacklists without explaining *why* an interaction is fraudulent or *what* immediate protective action should be taken.

ScamShield AI bridges the gap between complex threat intelligence and human intuition. Operating on a transparent multi-signal architecture, ScamShield analyzes multimodal inputs—text SMS, URLs, screenshot OCR (RapidOCR ONNX), QR codes (OpenCV), and voice notes—without relying on mandatory paid cloud APIs. Incoming signals are evaluated across 18 lexical URL dimensions, behavioral regex vectors, and a scikit-learn RandomForest model to produce a calibrated 5-vector risk score.

Critically, ScamShield prioritizes explainability and family defense. Its TrustLens engine deconstructs attacks into numbered evidence cards and highlights manipulative red-flag tokens in context. The system provides immediate incident guidance, linking directly to India's national cybercrime portal (`cybercrime.gov.in`) and helpline `1930`. Through Family Guardian, users generate jargon-free warning cards to safeguard elderly relatives via messaging apps. Finally, ScamShield builds long-term human immunity through the Scam Dojo, an interactive training gym featuring 12 realistic scenarios across 6 difficulty tiers.

Evaluated on a curated 70-sample prototype benchmark using strict 5-fold cross-validation with out-of-fold holdouts, ScamShield's combined multi-signal pipeline achieved 92.86% accuracy with zero false positives on routine transaction alerts. *(242 words)*

---

## 500-Word Description (Full Hackathon Narrative)

As digital payments and instant messaging penetrate every tier of society, social engineering scams have exploded. Every day, millions of citizens receive deceptive SMS alerts claiming their bank accounts are blocked, courier deliveries have failed, or tax refunds await verification. Victims do not lose money because their operating systems lack encryption; they lose money because human trust and panic are manipulated. Current cybersecurity solutions offer either enterprise endpoint protection or silent URL filtering. When a user asks: "Is this message safe, why is it suspicious, and what should I tell my parents?", traditional antivirus offers no answers.

ScamShield AI was designed from first principles to solve this fundamental human vulnerability. It is an explainable, multimodal cybersecurity assistant that empowers ordinary users through five coordinated pillars: Detection, Explainability, Protective Action, Family Defense, and Proactive Education.

ScamShield accepts five input modalities: raw message text, standalone URLs, screenshot images, QR codes, and voice notes. To ensure accessibility, the core system operates entirely on local compute:
1. **Multimodal Ingestion**: Screenshots undergo local OCR via RapidOCR (ONNX runtime) to extract text while masking sensitive credentials. QR codes are decoded via computer vision into destination endpoints without dangerous automatic redirection.
2. **Multi-Signal Intelligence Core**: The engine extracts 18 lexical and Shannon-entropy features from URLs and applies contextual heuristic rules. It uses negative-prefix detection ("never share OTP") and toll-free whitelisting to eliminate false alarms on legitimate banking notifications. These features feed a trained RandomForest model, and an optional semantic AI layer can be activated if cloud LLM keys are supplied.
3. **Calibrated Risk Fusion**: Signal scores are fused into a normalized risk score (0.00 to 1.00) classified into SAFE, SUSPICIOUS, or HIGH RISK.
4. **TrustLens Explainability**: Rather than displaying an arbitrary percentage, TrustLens details the exact evidence found—such as brand domain mismatches, artificial urgency, and deceptive credential harvesting—while dynamically highlighting suspicious tokens within the original message.
5. **Actionable Protection & Family Guardian**: Users receive prioritized guidance, direct one-click dials to India's National Cyber Crime Helpline (1930), and official links to `cybercrime.gov.in`. With the "Protect My Family" feature, users generate clean, shareable warning cards to alert family messaging groups before scammers can strike relatives.
6. **Gamified Resilience (Scam Dojo)**: Real defense requires active practice. The built-in Scam Dojo offers 12 realistic challenges across 6 progressive tiers (from fake lotteries to UPI debit requests). Users earn points, build streaks, and review in-depth explanations for why benign transactions differ from deceptive fraud.

On our 70-sample prototype benchmark (40 URLs, 30 messages, 50% scam / 50% legitimate), ScamShield achieved 92.86% out-of-fold accuracy, 96.88% precision, and 0.72 ms inference latency under strict 5-fold stratified cross-validation with zero data leakage. With multilingual support in English, Tamil, Hindi, Telugu, Malayalam, and Kannada, ScamShield AI turns cybersecurity from an intimidating technical warning into accessible everyday protection. *(462 words)*

---

## Key Innovation Points

1. **Deterministic Explainability Over Black-Box AI**:  
   Unlike generic wrapper bots that hallucinate risk scores, ScamShield generates evidence cards and red-flag token highlights directly from extracted signals.
2. **Context-Aware Rule Refinement**:  
   Differentiates between legitimate bank debits ("₹2,500 debited from your account") and urgent phishing demands ("₹2,500 debited. Call unofficial number immediately").
3. **Zero Mandatory Cloud Dependency**:  
   FastAPI backend runs RapidOCR, OpenCV QR decoding, URL entropy extraction, and RandomForest inference locally without requiring paid API tokens.
4. **Action-Oriented Human Protection (Family Guardian)**:  
   Translates machine telemetry into share-ready warning cards to protect non-technical family members.
5. **Gamified Behavioral Training (Scam Dojo)**:  
   Transforms reactive antivirus scanning into proactive cyber hygiene with 12 interactive scenarios, immediate feedback, and scoring streaks.
6. **Vernacular Multilingual Delivery**:  
   Adapts technical warnings into clear, jargon-free explanations in 6 Indian languages.

---

## Real-World Impact

- **Financial Loss Mitigation**: Empowers citizens to halt transactions and report incidents to Helpline 1930 within the critical "golden hour".
- **Bridging the Digital Divide**: Brings accessible threat intelligence to non-technical users, elderly demographics, and vernacular speakers.
- **De-escalating Panic**: Explains psychological manipulation tactics (artificial urgency, fear of account suspension) so users pause before clicking.

---

## Technical Architecture Blueprint

```
[ USER INTERACTION: Text / URL / Screenshot / QR / Voice ]
                           │
                           ▼
          [ Next.js 16 + React 19 Frontend ]
      (RiskGauge, TrustLens, Family Guardian, Dojo)
                           │  HTTP REST (FastAPI)
                           ▼
          [ FastAPI Ingestion & Sanitization ]
      (Credential Masking, No-SSRF Validation, CORS)
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
[RapidOCR ONNX]     [OpenCV QR Engine]   [Lexical Extractor]
 (Screenshot Text)   (Safe Destination)   (18 URL Features)
     └─────────────────────┬─────────────────────┘
                           │
                           ▼
          [ Multi-Signal Detection Engine ]
   ├── Deterministic Heuristic Rules (Urgency, Impersonation)
   ├── scikit-learn RandomForest Classifier (Holdout-Validated)
   └── Optional Cloud LLM Semantic Layer (Local Fallback)
                           │
                           ▼
               [ Calibrated Score Fusion ]
         Risk = 0.35*Rules + 0.30*URL + 0.35*ML
                           │
                           ▼
      [ TrustLens Evidence & Action Plan Synthesizer ]
```

---

## Prototype Limitations & Scientific Honesty

- **Benchmark Scope**: Evaluated on an internal prototype dataset of 70 curated samples (40 URLs, 30 messages). Results validate pipeline logic rather than universal real-world threat coverage.
- **Voice Ingestion**: Implemented with acoustic feature validation and transcript-assisted analysis; automated Speech-to-Text operates in fallback mode without heavy offline ASR models installed.
- **Semantic LLM**: External LLM analysis requires user-supplied Gemini or OpenAI API keys; deterministic local rules and RandomForest serve as the primary active engine.
- **Family Sharing**: Generates pre-formatted share-ready text cards for WhatsApp/SMS; does not require direct Meta Graph API business integrations.

---

## Judge Demonstration Flow (Recommended 2-Minute Walkthrough)

1. **Step 1 — Bank KYC Phishing**:
   - Click demo pill: `Bank KYC Phishing`.
   - Click `Analyze with ScamShield`.
   - Observe scanning animation, 94% HIGH RISK score, and 5-vector breakdown (Domain: 85%, Social Eng: 90%).
   - Review TrustLens Evidence cards and highlighted red flags (`"blocked today"`, `"sbi-verify-secure.xyz"`).
2. **Step 2 — Legitimate Transaction Verification (Zero False Positive)**:
   - Click demo pill: `Legitimate Transaction`.
   - Click `Analyze with ScamShield`.
   - Observe SAFE classification (low risk), verifying the system does not flag benign debits or official 1800 numbers.
3. **Step 3 — Family Guardian Alert**:
   - On the Bank KYC result, click `Protect My Family`.
   - Review the generated warning card, copy text, or view WhatsApp-ready formatting.
4. **Step 4 — Multilingual Switch**:
   - Toggle language dropdown to `தமிழ் (Tamil)` or `हिन्दी (Hindi)` to inspect vernacular action recommendations.
5. **Step 5 — Architecture & How It Works**:
   - Click `⚡ How It Works` in the header to view the 7-step pipeline and system blueprint.
6. **Step 6 — Scam Dojo Practice**:
   - Navigate to `🥋 Scam Dojo`.
   - Complete Level 1 (Courier Reschedule challenge) to view instant feedback, points, and score streak tracking.
