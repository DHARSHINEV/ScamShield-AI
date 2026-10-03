"use client";

import React, { useState, useEffect } from "react";
import { 
  BarChart3, 
  Clock, 
  ShieldCheck, 
  ShieldAlert, 
  AlertTriangle, 
  Trophy, 
  Flame, 
  Layers, 
  Trash2,
  ExternalLink
} from "lucide-react";

export interface HistoryItem {
  id: string;
  timestamp: string;
  snippet: string;
  classification: "SAFE" | "SUSPICIOUS" | "HIGH RISK";
  percentage: number;
  scamType: string;
}

export const Dashboard: React.FC = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [dojoScore, setDojoScore] = useState<number>(0);
  const [dojoStreak, setDojoStreak] = useState<number>(0);

  useEffect(() => {
    const raw = localStorage.getItem("scamshield_history");
    if (raw) {
      try {
        setHistory(JSON.parse(raw));
      } catch (e) {
        console.error(e);
      }
    }

    const score = localStorage.getItem("scamshield_dojo_score");
    const streak = localStorage.getItem("scamshield_dojo_streak");
    if (score) setDojoScore(parseInt(score, 10));
    if (streak) setDojoStreak(parseInt(streak, 10));
  }, []);

  const clearHistory = () => {
    localStorage.removeItem("scamshield_history");
    setHistory([]);
  };

  const highRiskCount = history.filter((h) => h.classification === "HIGH RISK").length;
  const suspiciousCount = history.filter((h) => h.classification === "SUSPICIOUS").length;
  const safeCount = history.filter((h) => h.classification === "SAFE").length;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      
      {/* Overview Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-indigo-500/30 shadow-2xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <BarChart3 className="w-6 h-6 text-indigo-400" />
              <h2 className="text-xl font-bold text-white tracking-tight">
                Threat Intelligence & User Audit Dashboard
              </h2>
            </div>
            <p className="text-xs text-slate-300 mt-1">
              Local, privacy-preserving threat audit metrics and prevention readiness score
            </p>
          </div>

          {/* Dojo Stats Badge */}
          <div className="flex items-center space-x-3 bg-slate-900/80 px-4 py-2 rounded-2xl border border-slate-800">
            <div className="flex items-center space-x-1.5 text-amber-400">
              <Trophy className="w-4 h-4" />
              <span className="font-mono font-bold text-sm">{dojoScore} pts</span>
            </div>
            <div className="h-4 w-px bg-slate-800" />
            <div className="flex items-center space-x-1.5 text-orange-400">
              <Flame className="w-4 h-4" />
              <span className="font-mono font-bold text-sm">{dojoStreak} streak</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-card p-5 rounded-2xl border border-red-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase text-red-400">High Risk Blocked</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="mt-2 text-3xl font-extrabold font-mono text-white">
            {highRiskCount}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Immediate malicious action plans served</p>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-amber-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase text-amber-400">Suspicious Flagged</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-2 text-3xl font-extrabold font-mono text-white">
            {suspiciousCount}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Social engineering & pressure anomalies</p>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-emerald-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase text-emerald-400">Verified Safe</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-2 text-3xl font-extrabold font-mono text-white">
            {safeCount}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Official bank alerts & clean communications</p>
        </div>
      </div>

      {/* Recent Scan History */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              Recent Scans (Stored in Local Browser Sandbox)
            </h3>
          </div>
          {history.length > 0 && (
            <button
              onClick={clearHistory}
              className="text-xs text-slate-400 hover:text-red-400 flex items-center space-x-1"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          )}
        </div>

        {history.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-400 font-mono">
            No previous scans recorded. Analyze a message above to populate your personal threat log.
          </div>
        ) : (
          <div className="space-y-2.5">
            {history.slice(0, 8).map((item) => {
              const isHigh = item.classification === "HIGH RISK";
              const isSafe = item.classification === "SAFE";
              const badgeClass = isHigh
                ? "bg-red-500/20 text-red-300 border-red-500/40"
                : isSafe
                ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
                : "bg-amber-500/20 text-amber-300 border-amber-500/40";

              return (
                <div
                  key={item.id}
                  className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between gap-4 text-xs font-mono"
                >
                  <div className="flex-1 truncate">
                    <span className="text-slate-200 font-sans truncate block">
                      {item.snippet}
                    </span>
                    <span className="text-[10px] text-slate-400">
                      {item.timestamp} • {item.scamType.replace(/_/g, " ")}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 shrink-0">
                    <span className={`px-2 py-0.5 rounded-full font-bold uppercase text-[10px] border ${badgeClass}`}>
                      {item.classification}
                    </span>
                    <span className="font-bold text-slate-300 w-10 text-right">
                      {item.percentage}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Cyber Threat Landscape Intel */}
      <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold text-white flex items-center space-x-1.5">
            <Layers className="w-4 h-4 text-cyan-400" />
            <span>Active Cyber Threat Landscape: India & Asia-Pacific 2026</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Dominant attack vectors: Fake KYC deactivation SMS, micro-fee courier links (₹25), fake YouTube review task job scams, and &apos;Digital Arrest&apos; impersonation extortion calls.
          </p>
        </div>

        <a
          href="https://cybercrime.gov.in"
          target="_blank"
          rel="noopener noreferrer"
          className="shrink-0 text-xs px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition-colors"
        >
          <span>Cyber Crime Portal</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

    </div>
  );
};
