"use client";

import React from "react";
import { ShieldCheck, Eye, Lock, GraduationCap, ArrowRight, Zap } from "lucide-react";

interface HeroProps {
  onAnalyzeClick: () => void;
  onDojoClick: () => void;
  onHowItWorksClick?: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onAnalyzeClick, onDojoClick, onHowItWorksClick }) => {
  return (
    <section className="relative pt-10 pb-8 px-4 sm:px-6 lg:px-8 text-center overflow-hidden">
      {/* Background glow orb */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[300px] bg-gradient-to-tr from-cyan-500/10 via-sky-500/10 to-indigo-500/10 blur-[100px] -z-10 pointer-events-none rounded-full" />

      {/* Hackathon Badge */}
      <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-slate-700/80 mb-6 shadow-sm">
        <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
        <span className="text-xs font-semibold text-slate-300">
          HackNowa Global Hackathon 2026
        </span>
        <span className="text-slate-600">|</span>
        <span className="text-xs text-cyan-400 font-medium">Digital Safety & Cybersecurity</span>
      </div>

      {/* Main Title & Hero Tagline */}
      <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
        SCAMSHIELD{" "}
        <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
          AI
        </span>
      </h1>
      
      <p className="mt-3 text-lg sm:text-xl font-medium tracking-wide text-cyan-300 max-w-2xl mx-auto">
        Detect it. Understand it. Practice it. Prevent it.
      </p>

      {/* Subtitle */}
      <p className="mt-4 text-sm sm:text-base text-slate-300/90 max-w-3xl mx-auto leading-relaxed">
        An AI-powered scam guardian that analyzes suspicious messages, links, screenshots,
        QR codes, and voice notes — then explains the evidence, tells you what to do next,
        and empowers you to spot scams before they strike.
      </p>

      {/* CTAs */}
      <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
        <button
          onClick={onAnalyzeClick}
          className="w-full sm:w-auto px-6 py-3 rounded-xl font-semibold text-sm bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 shadow-lg shadow-cyan-500/25 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
        >
          <Zap className="w-4 h-4 text-slate-950 fill-current" />
          <span>Analyze a Scam</span>
          <ArrowRight className="w-4 h-4 text-slate-950" />
        </button>

        <button
          onClick={onDojoClick}
          className="w-full sm:w-auto px-5 py-3 rounded-xl font-semibold text-sm bg-purple-500/15 hover:bg-purple-500/25 text-purple-300 border border-purple-500/30 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
        >
          <span>🥋</span>
          <span>Try Scam Dojo</span>
        </button>

        {onHowItWorksClick && (
          <button
            onClick={onHowItWorksClick}
            className="w-full sm:w-auto px-5 py-3 rounded-xl font-semibold text-sm bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <span>⚡</span>
            <span>How It Works</span>
          </button>
        )}
      </div>

      {/* 4 Trust & Value Pillars */}
      <div className="mt-12 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-4xl mx-auto">
        <div className="glass-card p-3 rounded-xl flex items-center space-x-3 text-left">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-white">Multimodal</div>
            <div className="text-[11px] text-slate-400">Text, URL, Image, QR, Voice</div>
          </div>
        </div>

        <div className="glass-card p-3 rounded-xl flex items-center space-x-3 text-left">
          <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <Eye className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-white">Explainable</div>
            <div className="text-[11px] text-slate-400">TrustLens evidence breakdown</div>
          </div>
        </div>

        <div className="glass-card p-3 rounded-xl flex items-center space-x-3 text-left">
          <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            <Lock className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-white">Privacy-First</div>
            <div className="text-[11px] text-slate-400">Zero credential retention</div>
          </div>
        </div>

        <div className="glass-card p-3 rounded-xl flex items-center space-x-3 text-left">
          <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
            <GraduationCap className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-white">Educational</div>
            <div className="text-[11px] text-slate-400">Interactive prevention training</div>
          </div>
        </div>
      </div>
    </section>
  );
};
