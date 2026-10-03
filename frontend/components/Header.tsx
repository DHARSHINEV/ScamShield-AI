"use client";

import React, { useState, useEffect } from "react";
import { Shield, ShieldAlert, Globe, Activity, PhoneCall, ChevronDown } from "lucide-react";
import { checkBackendHealth } from "@/lib/api";

interface HeaderProps {
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "ta", label: "தமிழ் (Tamil)" },
  { code: "hi", label: "हिन्दी (Hindi)" },
  { code: "te", label: "తెలుగు (Telugu)" },
  { code: "ml", label: "മലയാളം (Malayalam)" },
  { code: "kn", label: "ಕನ್ನಡ (Kannada)" }
];

export const Header: React.FC<HeaderProps> = ({
  currentLanguage,
  onLanguageChange,
  activeTab,
  setActiveTab
}) => {
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(true);
  const [langMenuOpen, setLangMenuOpen] = useState<boolean>(false);
  const [copiedHelpline, setCopiedHelpline] = useState<boolean>(false);

  useEffect(() => {
    checkBackendHealth().then((res) => setIsBackendHealthy(res.healthy));
    const interval = setInterval(() => {
      checkBackendHealth().then((res) => setIsBackendHealthy(res.healthy));
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const copyHelpline = () => {
    navigator.clipboard.writeText("1930");
    setCopiedHelpline(true);
    setTimeout(() => setCopiedHelpline(false), 2500);
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("analyzer")}>
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-sky-500 to-indigo-600 shadow-lg shadow-cyan-500/20">
            <Shield className="w-5 h-5 text-white" />
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isBackendHealthy ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
              <span className={`relative inline-flex rounded-full h-3 w-3 ${isBackendHealthy ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
            </span>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">
                ScamShield
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                AI 2026
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase">
              HackNowa Digital Safety
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center space-x-1 bg-slate-900/60 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab("analyzer")}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "analyzer"
                ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-300 hover:text-white hover:bg-slate-800/50"
            }`}
          >
            Detector & Evidence
          </button>
          <button
            onClick={() => setActiveTab("how-it-works")}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center space-x-1.5 ${
              activeTab === "how-it-works"
                ? "bg-sky-500/20 text-sky-300 border border-sky-500/30 shadow-sm"
                : "text-slate-300 hover:text-white hover:bg-slate-800/50"
            }`}
          >
            <span>⚡</span>
            <span>How It Works</span>
          </button>
          <button
            onClick={() => setActiveTab("dojo")}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center space-x-1.5 ${
              activeTab === "dojo"
                ? "bg-purple-500/20 text-purple-300 border border-purple-500/30 shadow-sm"
                : "text-slate-300 hover:text-white hover:bg-slate-800/50"
            }`}
          >
            <span>🥋</span>
            <span>Scam Dojo</span>
          </button>
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "dashboard"
                ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 shadow-sm"
                : "text-slate-300 hover:text-white hover:bg-slate-800/50"
            }`}
          >
            Threat Intel
          </button>
          <button
            onClick={() => setActiveTab("privacy")}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "privacy"
                ? "bg-slate-700/50 text-white"
                : "text-slate-400 hover:text-white hover:bg-slate-800/50"
            }`}
          >
            Privacy
          </button>
        </nav>

        {/* Actions: Helpline & Language */}
        <div className="flex items-center space-x-3">
          
          {/* Emergency Helpline Pill */}
          <button
            onClick={copyHelpline}
            title="National Cyber Crime Reporting Helpline (India) - Click to copy 1930"
            className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/25 hover:bg-red-500/20 transition-colors"
          >
            <PhoneCall className="w-3.5 h-3.5 text-red-400" />
            <span className="hidden sm:inline font-mono">1930</span>
            <span className="text-[10px] text-red-300/80">{copiedHelpline ? "Copied!" : "Helpline"}</span>
          </button>

          {/* Language Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setLangMenuOpen(!langMenuOpen)}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900/90 text-slate-200 border border-slate-700 hover:border-cyan-500/50 transition-colors"
            >
              <Globe className="w-3.5 h-3.5 text-cyan-400" />
              <span>{LANGUAGES.find(l => l.code === currentLanguage)?.label.split(" ")[0]}</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            {langMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 rounded-xl bg-slate-900 border border-slate-700 shadow-2xl py-1 z-50">
                {LANGUAGES.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => {
                      onLanguageChange(lang.code);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full text-left px-3 py-2 text-xs transition-colors flex items-center justify-between ${
                      currentLanguage === lang.code
                        ? "bg-cyan-500/20 text-cyan-300 font-semibold"
                        : "text-slate-300 hover:bg-slate-800 hover:text-white"
                    }`}
                  >
                    <span>{lang.label}</span>
                    {currentLanguage === lang.code && <span className="text-cyan-400">✓</span>}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Engine Status indicator */}
          <div 
            title={isBackendHealthy ? "Multi-Signal Backend Active (Rules, ML, OCR, QR)" : "Backend Fallback Active"}
            className="flex items-center space-x-1.5 px-2 py-1 rounded-md bg-slate-900/50 border border-slate-800 text-[11px]"
          >
            <Activity className={`w-3.5 h-3.5 ${isBackendHealthy ? 'text-emerald-400' : 'text-amber-400'}`} />
            <span className="hidden lg:inline text-slate-400 font-mono">
              {isBackendHealthy ? "SYS OK" : "LOCAL"}
            </span>
          </div>

        </div>
      </div>
    </header>
  );
};
