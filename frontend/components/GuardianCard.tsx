"use client";

import React, { useState } from "react";
import { Users, Copy, Check, Download, Share2, ShieldAlert, Sparkles } from "lucide-react";
import { generateGuardianCard, GuardianResponse } from "@/lib/api";

interface GuardianCardProps {
  messageSnippet: string;
  riskLevel: string;
  scamType: string;
  language: string;
}

export const GuardianCard: React.FC<GuardianCardProps> = ({
  messageSnippet,
  riskLevel,
  scamType,
  language
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [guardianData, setGuardianData] = useState<GuardianResponse | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const handleOpenGuardian = async () => {
    setIsOpen(true);
    if (!guardianData) {
      setLoading(true);
      try {
        const data = await generateGuardianCard(messageSnippet, riskLevel, scamType, language);
        setGuardianData(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleCopy = () => {
    if (!guardianData) return;
    navigator.clipboard.writeText(guardianData.shareable_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleDownload = () => {
    if (!guardianData) return;
    const blob = new Blob([guardianData.shareable_text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ScamShield_Family_Alert_${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mt-4">
      {/* Trigger Button */}
      <button
        onClick={handleOpenGuardian}
        className="w-full sm:w-auto px-5 py-2.5 rounded-xl font-semibold text-xs bg-gradient-to-r from-red-600 via-rose-600 to-pink-600 hover:from-red-500 hover:to-pink-500 text-white shadow-lg shadow-red-500/20 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
      >
        <Users className="w-4 h-4" />
        <span>Protect My Family — Share Warning</span>
        <Sparkles className="w-3.5 h-3.5 text-amber-300" />
      </button>

      {/* Warning Card Modal / Panel */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
          <div className="relative w-full max-w-lg glass-panel rounded-2xl border border-red-500/40 p-6 shadow-2xl bg-slate-900 overflow-hidden">
            
            {/* Header */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 rounded-lg bg-red-500/20 text-red-400">
                  <ShieldAlert className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white tracking-wide">
                    Family Guardian Alert Card
                  </h3>
                  <p className="text-[11px] text-slate-400">
                    Share-ready warning formatted for WhatsApp, Telegram & SMS
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
              >
                ✕
              </button>
            </div>

            {loading ? (
              <div className="py-12 text-center text-xs text-slate-400 font-mono">
                Generating protective alert card...
              </div>
            ) : guardianData ? (
              <div className="py-4 space-y-4">
                {/* Visual Preview Card */}
                <div className="p-4 rounded-xl bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border border-red-500/30 font-sans shadow-inner">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-red-400 uppercase tracking-wider flex items-center space-x-1.5">
                      <span>🚨</span>
                      <span>{guardianData.headline}</span>
                    </span>
                    <span className="text-[10px] bg-red-500/20 text-red-300 px-2 py-0.5 rounded font-mono font-semibold">
                      VERIFIED
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 italic mb-3 bg-slate-950/50 p-2.5 rounded border border-slate-800/80 font-mono">
                    &ldquo;{messageSnippet.slice(0, 140)}...&rdquo;
                  </p>

                  <div className="space-y-1.5">
                    {guardianData.bullet_warnings.map((bullet, idx) => (
                      <div key={idx} className="text-xs font-semibold text-slate-200 flex items-center space-x-2">
                        <span>{bullet}</span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400">
                    <span>🛡️ Checked by ScamShield AI</span>
                    <span>Helpline: 1930</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-2 pt-2">
                  <button
                    onClick={handleCopy}
                    className="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 flex items-center justify-center space-x-2 transition-colors shadow-md"
                  >
                    {copied ? <Check className="w-4 h-4 text-emerald-950" /> : <Copy className="w-4 h-4" />}
                    <span>{copied ? "Copied to Clipboard!" : "Copy for WhatsApp / SMS"}</span>
                  </button>

                  <button
                    onClick={handleDownload}
                    className="py-2.5 px-4 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center justify-center space-x-2 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span>Save Text</span>
                  </button>
                </div>
              </div>
            ) : null}

          </div>
        </div>
      )}
    </div>
  );
};
