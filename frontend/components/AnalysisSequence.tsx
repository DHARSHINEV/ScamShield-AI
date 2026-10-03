"use client";

import React, { useState, useEffect } from "react";
import { CheckCircle2, Loader2, ShieldAlert } from "lucide-react";

interface AnalysisSequenceProps {
  onComplete?: () => void;
}

const STEPS = [
  "Extracting indicators & sanitizing content...",
  "Checking URL structure & domain consistency...",
  "Detecting social-engineering & urgency signals...",
  "Running transparent cybersecurity rule engine...",
  "Running trained ML inference pipeline...",
  "Synthesizing TrustLens evidence & breakdown...",
  "Building customized action & protection plan..."
];

export const AnalysisSequence: React.FC<AnalysisSequenceProps> = () => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 250);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="glass-panel p-8 rounded-2xl border border-cyan-500/30 max-w-xl mx-auto my-8 relative overflow-hidden shadow-2xl">
      {/* Scanner beam */}
      <div className="scanner-beam" />

      <div className="flex items-center space-x-3 mb-6">
        <div className="w-8 h-8 rounded-lg bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center">
          <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white tracking-wide">
            Analyzing Threat Indicators
          </h3>
          <p className="text-xs text-slate-400 font-mono">
            ScamShield Multi-Signal Intelligence Engine
          </p>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {STEPS.map((step, idx) => {
          const isDone = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;
          return (
            <div
              key={idx}
              className={`flex items-center space-x-3 transition-opacity duration-200 ${
                isDone
                  ? "text-slate-300"
                  : isCurrent
                  ? "text-cyan-300 font-semibold"
                  : "text-slate-600 opacity-50"
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-cyan-400 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-700 shrink-0" />
              )}
              <span>{step}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
