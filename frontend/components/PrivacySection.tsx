"use client";

import React from "react";
import { Lock, ShieldCheck, Database, EyeOff, FileText, CheckCircle2 } from "lucide-react";

export const PrivacySection: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="glass-panel p-8 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
        
        {/* Title */}
        <div className="flex items-center space-x-3 pb-4 border-b border-slate-800">
          <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <Lock className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              Privacy, Data Handling & Ethics Architecture
            </h2>
            <p className="text-xs text-slate-400">
              Clear, transparent cybersecurity policies — no hidden data aggregation
            </p>
          </div>
        </div>

        {/* Core Declarations */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold uppercase tracking-wider">
              <EyeOff className="w-4 h-4" />
              <span>Minimization of Data Retention</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              ScamShield is designed to minimize unnecessary data retention. Submitted messages, URLs, and screenshots are processed in transient memory for inspection and are discarded immediately.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4" />
              <span>Credential Redaction & Warning</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Do not submit passwords, OTPs, banking credentials, or other sensitive secrets. Our safety layer actively scrubs and masks detected 16-digit card patterns and OTPs prior to analysis.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider">
              <Database className="w-4 h-4" />
              <span>No Server Database Required</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              No tracking database or user accounts are required. Your scan audit history and Scam Dojo training points are stored exclusively within your local browser sandbox (localStorage).
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
              <FileText className="w-4 h-4" />
              <span>External AI Provider Disclosure</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              If an external AI API key (OpenAI or Gemini) is configured in your backend environment, sanitized message content may be sent to that provider for semantic evaluation. Otherwise, the system operates completely offline on local rules, OpenCV, and scikit-learn models.
            </p>
          </div>
        </div>

        {/* Security Commitments */}
        <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 text-xs space-y-2">
          <div className="font-bold text-slate-200">Our Cyber Safety Guarantees:</div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-400">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
              <span>Never automatically navigates to suspicious links</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
              <span>Never executes uploaded files or binaries</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
              <span>No API keys exposed in frontend client bundle</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
              <span>Strict 10 MB upload limits & MIME validation</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
