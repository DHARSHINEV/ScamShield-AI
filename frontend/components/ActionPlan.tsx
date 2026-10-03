"use client";

import React from "react";
import { ShieldAlert, CheckSquare2, ExternalLink, PhoneCall, AlertTriangle } from "lucide-react";
import { ActionPlanItem } from "@/lib/api";

interface ActionPlanProps {
  actionPlan: ActionPlanItem[];
  classification: string;
}

export const ActionPlan: React.FC<ActionPlanProps> = ({ actionPlan, classification }) => {
  const isSafe = classification === "SAFE";

  return (
    <div className="glass-card p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <CheckSquare2 className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-bold text-white tracking-tight">
            Action Plan: What Should You Do?
          </h3>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
          Priority Guidance
        </span>
      </div>

      <p className="text-xs text-slate-400">
        Concrete protective actions recommended by ScamShield AI based on specific threats detected.
      </p>

      <div className="space-y-3">
        {actionPlan.map((item, idx) => {
          const isCritical = item.priority === "critical";
          const isHigh = item.priority === "high";

          const badgeClass = isCritical
            ? "bg-red-500/15 text-red-300 border-red-500/30"
            : isHigh
            ? "bg-amber-500/15 text-amber-300 border-amber-500/30"
            : "bg-slate-800 text-slate-300 border-slate-700";

          return (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border flex items-start space-x-3 transition-colors ${
                isCritical
                  ? "bg-red-950/20 border-red-500/30"
                  : isHigh
                  ? "bg-amber-950/15 border-amber-500/25"
                  : "bg-slate-900/50 border-slate-800"
              }`}
            >
              <div className="mt-0.5 shrink-0">
                {isCritical ? (
                  <ShieldAlert className="w-4 h-4 text-red-400" />
                ) : isHigh ? (
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                ) : (
                  <CheckSquare2 className="w-4 h-4 text-cyan-400" />
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <h4 className="text-xs font-bold text-slate-100">{item.step}</h4>
                  <span className={`text-[9px] uppercase font-bold px-1.5 py-0.2 rounded border ${badgeClass}`}>
                    {item.priority}
                  </span>
                </div>
                <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                  {item.instruction}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Official Government Cybercrime Reporting Box */}
      <div className="mt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <div className="text-xs font-bold text-white flex items-center space-x-1.5">
            <span>🇮🇳</span>
            <span>Official Cybercrime Incident Reporting (India)</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-0.5">
            National Cyber Crime Reporting Portal under Ministry of Home Affairs
          </p>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-600 transition-colors"
          >
            <span>cybercrime.gov.in</span>
            <ExternalLink className="w-3 h-3 ml-0.5" />
          </a>
          <a
            href="tel:1930"
            className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-red-600 hover:bg-red-500 text-white shadow transition-colors"
          >
            <PhoneCall className="w-3 h-3" />
            <span>Call 1930</span>
          </a>
        </div>
      </div>
    </div>
  );
};
