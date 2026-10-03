"use client";

import React from "react";
import { Globe, Users, Link2, MessageSquareWarning, KeyRound } from "lucide-react";

interface RiskBreakdownProps {
  breakdown: {
    domain: number; // 0.0 to 1.0
    social_engineering: number;
    url_pattern: number;
    message_intent: number;
    credential_request: number;
  };
}

const FACTORS = [
  {
    key: "domain",
    label: "Domain Reputation & Spoofing",
    icon: Globe,
    description: "Evaluates punycode, TLD abuse, brand mismatches, and IP hosts"
  },
  {
    key: "social_engineering",
    label: "Social Engineering & Pressure",
    icon: Users,
    description: "Psychological manipulation, threat coercion, and manufactured urgency"
  },
  {
    key: "url_pattern",
    label: "URL Lexical & Structural Risk",
    icon: Link2,
    description: "Path entropy, excessive nesting, query obfuscation, and shorteners"
  },
  {
    key: "message_intent",
    label: "Deceptive Message Intent",
    icon: MessageSquareWarning,
    description: "Fake courier lures, lottery prizes, task jobs, and authority impersonation"
  },
  {
    key: "credential_request",
    label: "Credential & OTP Solicitation",
    icon: KeyRound,
    description: "Direct harvesting of passwords, UPI PINs, OTP tokens, and bank details"
  }
];

export const RiskBreakdown: React.FC<RiskBreakdownProps> = ({ breakdown }) => {
  const getSeverityColor = (val: number) => {
    if (val >= 0.7) return "bg-red-500 text-red-400";
    if (val >= 0.35) return "bg-amber-500 text-amber-400";
    return "bg-emerald-500 text-emerald-400";
  };

  const getSeverityLabel = (val: number) => {
    if (val >= 0.7) return "High";
    if (val >= 0.35) return "Moderate";
    return "Low";
  };

  return (
    <div className="glass-card p-6 rounded-2xl border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-white tracking-wide">
            Multi-Vector Risk Breakdown
          </h3>
          <p className="text-xs text-slate-400">
            Granular analysis across 5 independent cybersecurity signal dimensions
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {FACTORS.map((factor) => {
          const val = breakdown[factor.key as keyof typeof breakdown] || 0.0;
          const pct = Math.min(100, Math.round(val * 100));
          const colorClass = getSeverityColor(val);
          const Icon = factor.icon;

          return (
            <div key={factor.key} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <div className="p-1 rounded bg-slate-800 text-slate-300">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <span className="font-semibold text-slate-200">{factor.label}</span>
                </div>
                <div className="flex items-center space-x-2 font-mono">
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${colorClass.split(" ")[1]} bg-slate-800/80`}>
                    {getSeverityLabel(val)}
                  </span>
                  <span className="font-bold text-slate-300 w-8 text-right">{pct}%</span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-full h-2 rounded-full bg-slate-800/80 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ease-out ${colorClass.split(" ")[0]}`}
                  style={{ width: `${Math.max(4, pct)}%` }}
                />
              </div>

              <p className="text-[11px] text-slate-400 leading-tight">
                {factor.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
