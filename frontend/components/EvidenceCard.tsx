"use client";

import React from "react";
import { Eye, AlertOctagon, CheckCircle2 } from "lucide-react";
import { EvidenceCardItem } from "@/lib/api";

interface EvidenceSectionProps {
  cards: EvidenceCardItem[];
  classification: string;
}

export const EvidenceCard: React.FC<EvidenceSectionProps> = ({ cards, classification }) => {
  if (!cards || cards.length === 0) {
    return (
      <div className="glass-card p-6 rounded-2xl border border-slate-800 text-center">
        <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
        <h4 className="text-base font-bold text-white">TrustLens: No Security Anomalies</h4>
        <p className="text-xs text-slate-400 mt-1">
          ScamShield&apos;s rule engine and ML models detected no manipulative pressure, domain mismatch, or credential harvesting triggers.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <Eye className="w-5 h-5 text-cyan-400" />
        <h3 className="text-lg font-bold text-white tracking-tight">
          TrustLens Evidence Engine
        </h3>
        <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold">
          Why was this flagged?
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {cards.map((card) => {
          const isHigh = card.severity === "high";
          const borderClass = isHigh ? "border-red-500/30 hover:border-red-500/50" : "border-slate-800 hover:border-amber-500/40";
          const badgeClass = isHigh ? "bg-red-500/15 text-red-300 border-red-500/30" : "bg-amber-500/15 text-amber-300 border-amber-500/30";

          return (
            <div
              key={card.id}
              className={`glass-card p-5 rounded-2xl border ${borderClass} transition-all duration-200 flex flex-col justify-between`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-xs font-bold text-slate-300 tracking-wider">
                    {card.title}
                  </span>
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${badgeClass}`}>
                    {card.severity} severity
                  </span>
                </div>

                <p className="text-xs text-slate-300 font-normal leading-relaxed mt-2">
                  {card.explanation}
                </p>
              </div>

              {card.matched_text && (
                <div className="mt-3 pt-2.5 border-t border-slate-800/80">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Triggered By:</div>
                  <div className="font-mono text-[11px] text-slate-300 truncate bg-slate-900/80 px-2 py-1 rounded border border-slate-800 mt-1">
                    {card.matched_text}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
