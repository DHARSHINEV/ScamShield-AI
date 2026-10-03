"use client";

import React, { useEffect, useState } from "react";
import { ShieldCheck, AlertTriangle, ShieldAlert } from "lucide-react";

interface RiskGaugeProps {
  score: number; // 0.0 to 1.0
  percentage: number; // 0 to 100
  classification: "SAFE" | "SUSPICIOUS" | "HIGH RISK";
  scamType: string;
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({
  score,
  percentage,
  classification,
  scamType
}) => {
  const [animatedScore, setAnimatedScore] = useState<number>(0);

  useEffect(() => {
    let current = 0;
    const target = percentage;
    const step = Math.max(1, Math.floor(target / 30));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        setAnimatedScore(target);
        clearInterval(timer);
      } else {
        setAnimatedScore(current);
      }
    }, 20);
    return () => clearInterval(timer);
  }, [percentage]);

  const isSafe = classification === "SAFE";
  const isSuspicious = classification === "SUSPICIOUS";
  const isHighRisk = classification === "HIGH RISK";

  const colorScheme = isSafe
    ? {
        stroke: "#10b981",
        text: "text-emerald-400",
        bg: "bg-emerald-500/10",
        border: "border-emerald-500/30",
        badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
        icon: ShieldCheck,
        label: "SAFE"
      }
    : isSuspicious
    ? {
        stroke: "#f59e0b",
        text: "text-amber-400",
        bg: "bg-amber-500/10",
        border: "border-amber-500/30",
        badge: "bg-amber-500/20 text-amber-300 border-amber-500/40",
        icon: AlertTriangle,
        label: "SUSPICIOUS"
      }
    : {
        stroke: "#ef4444",
        text: "text-red-500",
        bg: "bg-red-500/10",
        border: "border-red-500/30",
        badge: "bg-red-500/20 text-red-300 border-red-500/40",
        icon: ShieldAlert,
        label: "HIGH RISK"
      };

  const IconComponent = colorScheme.icon;

  // SVG circle calculation
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  return (
    <div className={`glass-card p-6 rounded-2xl border ${colorScheme.border} flex flex-col items-center justify-center text-center relative overflow-hidden shadow-xl`}>
      {/* Background ambient glow */}
      <div
        className="absolute w-40 h-40 rounded-full blur-3xl opacity-20 pointer-events-none"
        style={{ backgroundColor: colorScheme.stroke }}
      />

      {/* Classification Tag */}
      <div className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider mb-4 ${colorScheme.badge}`}>
        <IconComponent className="w-3.5 h-3.5" />
        <span>{colorScheme.label}</span>
      </div>

      {/* Circular Progress Gauge */}
      <div className="relative w-40 h-40 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
          {/* Background track */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="currentColor"
            strokeWidth="12"
            className="text-slate-800/80"
            fill="transparent"
          />
          {/* Progress stroke */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke={colorScheme.stroke}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-300 ease-out"
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-extrabold tracking-tight font-mono ${colorScheme.text}`}>
            {animatedScore}%
          </span>
          <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mt-0.5">
            Risk Score
          </span>
        </div>
      </div>

      {/* Category / Type info */}
      <div className="mt-4">
        <div className="text-xs text-slate-400 uppercase tracking-wider">Identified Vector</div>
        <div className="text-sm font-semibold text-slate-200 capitalize">
          {scamType.replace(/_/g, " ")}
        </div>
        <p className="text-[11px] text-slate-400 mt-1">
          {isSafe
            ? "No severe anomalies or coercive threats flagged."
            : "Multi-signal fusion identified significant risk indicators."}
        </p>
      </div>
    </div>
  );
};
