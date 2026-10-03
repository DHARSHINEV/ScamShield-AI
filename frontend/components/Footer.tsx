"use client";

import React from "react";
import { Shield, ExternalLink, Heart } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="mt-20 border-t border-slate-800/80 bg-slate-950/80 backdrop-blur-md py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
        
        {/* Brand & Tagline */}
        <div className="space-y-2 max-w-md">
          <div className="flex items-center space-x-2">
            <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              <Shield className="w-4 h-4" />
            </div>
            <span className="text-base font-bold text-white tracking-tight">
              ScamShield AI
            </span>
          </div>
          <p className="text-xs text-slate-300">
            Detect it. Understand it. Practice it. Prevent it.
          </p>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Built for <span className="text-slate-300 font-semibold">HackNowa Global Hackathon 2026</span>. Primary Track: Digital Safety & Cybersecurity. Secondary Fit: AI for Everyday Life.
          </p>
        </div>

        {/* Resources & Disclaimers */}
        <div className="space-y-3 text-xs text-slate-400">
          <div className="font-semibold text-slate-300 uppercase tracking-wider text-[11px]">
            Official Resources & Support
          </div>
          <div className="flex flex-wrap gap-4">
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-cyan-400 transition-colors flex items-center space-x-1"
            >
              <span>National Cyber Crime Portal (India)</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <a
              href="tel:1930"
              className="text-red-400 hover:text-red-300 font-semibold transition-colors"
            >
              Emergency Helpline: 1930
            </a>
          </div>
          <p className="text-[10px] text-slate-400 max-w-lg leading-normal">
            Disclaimer: ScamShield provides risk assessment estimates based on deterministic security rules, lexical URL analysis, local ML models, and heuristic classification. It does not provide legal advice or guarantee detection of all emerging threats.
          </p>
        </div>

      </div>
    </footer>
  );
};
