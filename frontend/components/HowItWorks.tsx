"use client";

import React from "react";
import { 
  Scan, 
  Cpu, 
  Binary, 
  Sliders, 
  FileSearch, 
  ShieldCheck, 
  GraduationCap, 
  ArrowDown, 
  ArrowRight, 
  CheckCircle2, 
  Camera, 
  QrCode, 
  Mic, 
  Globe, 
  MessageSquare,
  Layers,
  Lock,
  Zap,
  Server
} from "lucide-react";

export const HowItWorks: React.FC = () => {
  return (
    <section className="space-y-12 py-4">
      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold">
          <Layers className="w-3.5 h-3.5" />
          <span>System Architecture & Pipeline</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          How ScamShield AI Works
        </h2>
        <p className="text-sm text-slate-400 leading-relaxed">
          From multimodal ingestion to deterministic evidence synthesis. ScamShield combines 
          heuristic rule vectors, machine learning classification, and zero-knowledge explainability 
          with sub-millisecond local inference.
        </p>
      </div>

      {/* Part 1: Visual 7-Step Pipeline */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-slate-800 bg-slate-900/60 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-8">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-cyan-400">Step-by-Step Pipeline</span>
            <h3 className="text-lg font-bold text-white">Multimodal Detection Flow</h3>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 font-mono">
            ~0.72 ms avg latency
          </span>
        </div>

        {/* 7 Pipeline Cards in Responsive Grid / Flow */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-3">
          
          {/* Step 1: Input */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-cyan-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">01</span>
                <Scan className="w-4 h-4 text-cyan-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">INPUT</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Message, URL, Screenshot, QR code, or Voice transcript.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>Multimodal Ingest</span>
            </div>
          </div>

          {/* Step 2: Signal Extraction */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-sky-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">02</span>
                <Cpu className="w-4 h-4 text-sky-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">EXTRACTION</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                OCR text extraction, 18 URL lexical features, behavioral regex.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>RapidOCR + OpenCV</span>
            </div>
          </div>

          {/* Step 3: AI / ML Analysis */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-indigo-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">03</span>
                <Binary className="w-4 h-4 text-indigo-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">AI / ML</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                RandomForest classifier + optional LLM semantic analysis layer.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>Supervised + Semantic</span>
            </div>
          </div>

          {/* Step 4: Risk Fusion */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-purple-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">04</span>
                <Sliders className="w-4 h-4 text-purple-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">RISK FUSION</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Calibrated 5-vector synthesis (Domain, Social Eng, Urgency, Intent, OTP).
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>Dynamic Weighting</span>
            </div>
          </div>

          {/* Step 5: Explainability */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-amber-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">05</span>
                <FileSearch className="w-4 h-4 text-amber-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">EVIDENCE</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                TrustLens evidence cards & highlighted in-context red flag tokens.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>Why Is It Risky?</span>
            </div>
          </div>

          {/* Step 6: Protection */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-emerald-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">06</span>
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">PROTECTION</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Action plan (Helpline 1930) + 1-Click Family Guardian card.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>Immediate Defense</span>
            </div>
          </div>

          {/* Step 7: Education */}
          <div className="relative glass-card p-4 rounded-xl border border-slate-800 hover:border-rose-500/30 transition-all flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">07</span>
                <GraduationCap className="w-4 h-4 text-rose-400" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">EDUCATION</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Scam Dojo interactive challenges for proactive cyber resilience.
              </p>
            </div>
            <div className="mt-4 pt-2 border-t border-slate-800 text-[10px] text-slate-500 flex items-center space-x-1">
              <span>12 Realistic Scenarios</span>
            </div>
          </div>

        </div>
      </div>

      {/* Part 2: Technical Architecture Diagram */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-slate-800 bg-slate-900/60 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-6">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-indigo-400">System Blueprint</span>
            <h3 className="text-lg font-bold text-white">Full-Stack Technical Architecture</h3>
          </div>
          <div className="flex items-center space-x-2 text-xs text-slate-400">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>REST API v1.0.0</span>
          </div>
        </div>

        {/* System Diagram Grid */}
        <div className="space-y-6">
          
          {/* Top Layer: Frontend UI */}
          <div className="p-4 rounded-xl border border-cyan-500/30 bg-cyan-950/20">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <Globe className="w-4 h-4 text-cyan-400" />
                <span className="text-xs font-bold text-cyan-300 uppercase tracking-wide">Frontend Layer (Client)</span>
              </div>
              <span className="text-[11px] font-mono text-cyan-400/80">Next.js 16 (App Router) + React 19 + Tailwind CSS</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs text-center">
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200">Multimodal Input (Text/URL/Image/QR/Voice)</div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200">Dynamic RiskGauge & 5-Vector Breakdown</div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200">TrustLens Evidence Cards</div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200">Family Guardian Share Generator</div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200">Scam Dojo Simulation Gym</div>
            </div>
          </div>

          {/* Connector */}
          <div className="flex justify-center -my-2 text-slate-600">
            <ArrowDown className="w-5 h-5 animate-bounce" />
          </div>

          {/* Gateway Layer: FastAPI */}
          <div className="p-4 rounded-xl border border-indigo-500/30 bg-indigo-950/20">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <Server className="w-4 h-4 text-indigo-400" />
                <span className="text-xs font-bold text-indigo-300 uppercase tracking-wide">API Gateway (Backend)</span>
              </div>
              <span className="text-[11px] font-mono text-indigo-400/80">FastAPI + Uvicorn Async Runtime (Python 3.10+)</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-center">
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                <span className="font-mono text-indigo-400">POST /analyze/text</span>
              </div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                <span className="font-mono text-indigo-400">POST /analyze/url</span>
              </div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                <span className="font-mono text-indigo-400">POST /image/ocr</span> + <span className="font-mono text-indigo-400">/image/qr</span>
              </div>
              <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                <span className="font-mono text-indigo-400">POST /voice/analyze</span>
              </div>
            </div>
          </div>

          {/* Connector */}
          <div className="flex justify-center -my-2 text-slate-600">
            <ArrowDown className="w-5 h-5" />
          </div>

          {/* Specialized Ingestion Processors */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/90 text-left">
              <div className="flex items-center space-x-2 text-sky-400 mb-1.5">
                <Camera className="w-4 h-4" />
                <span className="text-xs font-bold">Screenshot Pipeline</span>
              </div>
              <p className="text-[11px] text-slate-400">
                Image Upload → Preprocessing → RapidOCR ONNX Engine → Normalized Text Extraction → Detector.
              </p>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/90 text-left">
              <div className="flex items-center space-x-2 text-purple-400 mb-1.5">
                <QrCode className="w-4 h-4" />
                <span className="text-xs font-bold">QR Security Pipeline</span>
              </div>
              <p className="text-[11px] text-slate-400">
                QR Image → OpenCV QRCodeDetector → Destination URL Decoded → Safe Link Inspection (No auto-visit).
              </p>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/90 text-left">
              <div className="flex items-center space-x-2 text-amber-400 mb-1.5">
                <Mic className="w-4 h-4" />
                <span className="text-xs font-bold">Voice Pipeline</span>
              </div>
              <p className="text-[11px] text-slate-400">
                Audio Note → Acoustic duration/sampling validation + Transcript-assisted speech analysis.
              </p>
            </div>
          </div>

          {/* Connector */}
          <div className="flex justify-center -my-2 text-slate-600">
            <ArrowDown className="w-5 h-5" />
          </div>

          {/* Core Decision Engine: Rules, ML, Fusion */}
          <div className="p-5 rounded-xl border border-emerald-500/30 bg-emerald-950/15">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-bold text-emerald-300 uppercase tracking-wide">Multi-Signal Intelligence Core</span>
              </div>
              <span className="text-[11px] font-mono text-emerald-400/80">92.86% Out-of-Fold Prototype Accuracy</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* Box 1: Rule Engine */}
              <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
                <div className="text-xs font-bold text-white mb-1 flex items-center space-x-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Deterministic Rule Engine</span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  Urgency patterns, credential/OTP demands, impersonation regex, toll-free 1800 whitelisting, negative prefix context.
                </p>
              </div>

              {/* Box 2: ML Engine */}
              <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
                <div className="text-xs font-bold text-white mb-1 flex items-center space-x-1.5">
                  <Binary className="w-3.5 h-3.5 text-indigo-400" />
                  <span>RandomForest ML Model</span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  18 engineered URL lexical features (entropy, IP, subdomains) + message TF-IDF n-grams trained without in-sample leakage.
                </p>
              </div>

              {/* Box 3: Optional LLM Layer */}
              <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800">
                <div className="text-xs font-bold text-white mb-1 flex items-center space-x-1.5">
                  <Lock className="w-3.5 h-3.5 text-purple-400" />
                  <span>AI Semantic Layer</span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  Optional Gemini / OpenAI key integration with full fallback to deterministic local rules when keys are unconfigured.
                </p>
              </div>
            </div>

            {/* Fusion & Explainability output */}
            <div className="mt-4 pt-3 border-t border-emerald-500/20 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-300 gap-2">
              <span className="font-semibold text-emerald-300">
                FUSED RISK SCORE: (0.35 * Rules) + (0.30 * URL) + (0.35 * ML)
              </span>
              <span className="text-slate-400 text-[11px]">
                Outputs: Classification (SAFE / SUSPICIOUS / HIGH RISK) + TrustLens Cards + Action Plan + Family Warning
              </span>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};
