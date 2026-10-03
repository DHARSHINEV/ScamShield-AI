/**
 * ScamShield AI Client API Library
 * Connects Next.js Frontend to FastAPI Backend
 */

export const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (process.env.NODE_ENV === "production"
    ? "https://scamshield-ai-4qgp.onrender.com"
    : "http://127.0.0.1:10000");

export interface RedFlagItem {
  text: string;
  reason: string;
  severity: "low" | "medium" | "high";
  type?: string;
}

export interface ActionPlanItem {
  step: string;
  instruction: string;
  priority: "critical" | "high" | "medium" | "low" | "info";
}

export interface EvidenceCardItem {
  id: string;
  type: string;
  title: string;
  severity: string;
  matched_text: string;
  explanation: string;
}

export interface AnalysisMetadata {
  rules_engine: boolean;
  ml_classifier: boolean;
  semantic_ai: boolean;
  ai_provider: string;
  latency_ms: number;
}

export interface FullAnalysisResponse {
  classification: "SAFE" | "SUSPICIOUS" | "HIGH RISK";
  risk_score: number;
  percentage: number;
  scam_type: string;
  summary: string;
  risk_breakdown: {
    domain: number;
    social_engineering: number;
    url_pattern: number;
    message_intent: number;
    credential_request: number;
  };
  signals: Array<{
    type: string;
    severity: string;
    matched_text?: string;
    explanation?: string;
  }>;
  evidence_cards: EvidenceCardItem[];
  red_flags: RedFlagItem[];
  action_plan: ActionPlanItem[];
  multilingual: Record<string, {
    language: string;
    status: string;
    summary: string;
    guardian_title: string;
    guardian_warning: string;
    primary_action: string;
  }>;
  analysis_metadata: AnalysisMetadata;
  extracted_urls: string[];
  sanitized_input: string;
  had_sensitive_redaction: boolean;
}

export interface DemoCase {
  id: string;
  title: string;
  category: string;
  text: string;
  description: string;
}

export interface DojoChallenge {
  id: string;
  level: number;
  level_title: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  category: string;
  scenario: string;
  message: string;
  url?: string;
}

export interface DojoAnswerResponse {
  challenge_id: string;
  is_correct: boolean;
  correct_classification: "SAFE" | "SUSPICIOUS";
  explanation: string[];
  key_takeaway: string;
  updated_streak: number;
  updated_score: number;
  updated_correct: number;
  total_answered: number;
  accuracy_percentage: number;
  skill_level: string;
}

export interface GuardianResponse {
  title: string;
  headline: string;
  bullet_warnings: string[];
  shareable_text: string;
  official_tip: string;
  verified_badge: string;
}

// 1. Health Check
export async function checkBackendHealth(): Promise<{ status: string; healthy: boolean }> {
  try {
    const res = await fetch(`${BACKEND_URL}/api/health`, { method: "GET", cache: "no-store" });
    if (!res.ok) return { status: "offline", healthy: false };
    const data = await res.json();
    return { status: data.status, healthy: true };
  } catch {
    return { status: "offline", healthy: false };
  }
}

// 2. Demo Cases
export async function fetchDemoCases(): Promise<DemoCase[]> {
  try {
    const res = await fetch(`${BACKENDURL_SAFELY()}/api/analyze/demo-cases`, { method: "GET" });
    if (!res.ok) throw new Error("Failed to load demo cases");
    return await res.json();
  } catch (err) {
    console.warn("Using offline demo cases fallback", err);
    return [
      {
        id: "demo-sbi-kyc",
        title: "Bank KYC Phishing (High Risk)",
        category: "bank_phishing",
        text: "🚨 SBI ALERT: Your account will be blocked today. Verify your KYC immediately: https://sbi-verify-secure.xyz",
        description: "Urgent deadline, KYC lure, and brand spoofing on an untrusted .xyz domain."
      },
      {
        id: "demo-parcel-payment",
        title: "Fake Parcel Micro-Payment (High Risk)",
        category: "delivery_scam",
        text: "India Post: Your package #IN78219 could not be delivered due to wrong house address. Pay ₹25 redelivery fee to avoid return: http://indiapost-parcel-update.com/track",
        description: "Exploits routine parcel delivery with ₹25 fee to harvest debit card numbers."
      },
      {
        id: "demo-job-scam",
        title: "Work-From-Home Task Scam (High Risk)",
        category: "job_scam",
        text: "Congratulations! You are selected for YouTube Video Like & Google Review task. Earn ₹4,500 daily. Payouts every 3 hours. Contact Telegram @HrOfficerTask26 to receive ₹500 joining bonus.",
        description: "Unrealistic payout for trivial tasks, Telegram funneling, and advance fee patterns."
      },
      {
        id: "demo-legit-bank",
        title: "Legitimate Bank Transaction (Safe)",
        category: "legitimate_bank",
        text: "SBI: ₹2,500.00 debited from A/C ...8902 on 03-Oct-26 at ATM-MG ROAD. Available balance ₹34,210.50. Call 18001234 if not done by you.",
        description: "Official transaction notification with masked digits, contextual location, and official toll-free dispute number."
      }
    ];
  }
}

function BACKENDURL_SAFELY(): string {
  return BACKEND_URL;
}

// 3. Analyze Text
export async function analyzeText(text: string, language: string = "en"): Promise<FullAnalysisResponse> {
  const res = await fetch(`${BACKEND_URL}/api/analyze/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Analysis request failed" }));
    throw new Error(errorData.detail || errorData.message || "Failed to analyze message");
  }
  return await res.json();
}

// 4. Analyze URL
export async function analyzeUrl(url: string, language: string = "en"): Promise<FullAnalysisResponse> {
  const res = await fetch(`${BACKEND_URL}/api/analyze/url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "URL analysis failed" }));
    throw new Error(errorData.detail || errorData.message || "Failed to analyze URL");
  }
  return await res.json();
}

// 5. Analyze Screenshot (OCR)
export async function analyzeImage(file: File, language: string = "en", manualContext: string = ""): Promise<FullAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", language);
  if (manualContext) {
    formData.append("manual_context", manualContext);
  }
  const res = await fetch(`${BACKEND_URL}/api/analyze/image`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Image analysis failed" }));
    throw new Error(errorData.detail || errorData.message || "ScamShield couldn't analyze this file. Please try another image.");
  }
  return await res.json();
}

// 6. Analyze QR Code
export async function analyzeQrCode(file: File, language: string = "en"): Promise<FullAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", language);
  const res = await fetch(`${BACKEND_URL}/api/analyze/qr`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "QR analysis failed" }));
    throw new Error(errorData.detail || errorData.message || "ScamShield couldn't detect a QR code in this image.");
  }
  return await res.json();
}

// 7. Analyze Voice Note
export async function analyzeVoice(file: File, manualTranscript: string = "", language: string = "en"): Promise<FullAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", language);
  if (manualTranscript) {
    formData.append("manual_transcript", manualTranscript);
  }
  const res = await fetch(`${BACKEND_URL}/api/analyze/voice`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Voice analysis failed" }));
    throw new Error(errorData.detail || errorData.message || "Could not transcribe or analyze audio.");
  }
  return await res.json();
}

// 8. Generate Guardian Alert Card
export async function generateGuardianCard(
  messageSnippet: string,
  riskLevel: string = "HIGH RISK",
  detectedScamType: string = "Phishing",
  language: string = "en"
): Promise<GuardianResponse> {
  const res = await fetch(`${BACKEND_URL}/api/guardian`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message_snippet: messageSnippet,
      risk_level: riskLevel,
      detected_scam_type: detectedScamType,
      language: language
    }),
  });
  if (!res.ok) {
    throw new Error("Failed to generate Family Guardian warning");
  }
  return await res.json();
}

// 9. Scam Dojo Challenges
export async function fetchDojoChallenges(): Promise<DojoChallenge[]> {
  const res = await fetch(`${BACKEND_URL}/api/dojo/challenges`, { method: "GET" });
  if (!res.ok) throw new Error("Failed to load Dojo challenges");
  const data = await res.json();
  return data.challenges || [];
}

// 10. Submit Dojo Answer
export async function submitDojoAnswer(
  challengeId: string,
  userChoice: "SAFE" | "SUSPICIOUS",
  currentStreak: number,
  totalAnswered: number,
  totalCorrect: number
): Promise<DojoAnswerResponse> {
  const res = await fetch(`${BACKEND_URL}/api/dojo/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      challenge_id: challengeId,
      user_choice: userChoice,
      current_streak: currentStreak,
      total_answered: totalAnswered,
      total_correct: totalCorrect
    }),
  });
  if (!res.ok) throw new Error("Failed to evaluate Dojo response");
  return await res.json();
}
