"use client";

import React, { useState } from "react";
import { AlertCircle, HelpCircle, ShieldAlert } from "lucide-react";
import { RedFlagItem } from "@/lib/api";

interface RedFlagTextProps {
  originalText: string;
  redFlags: RedFlagItem[];
}

export const RedFlagText: React.FC<RedFlagTextProps> = ({ originalText, redFlags }) => {
  const [activeTooltip, setActiveTooltip] = useState<RedFlagItem | null>(null);

  if (!redFlags || redFlags.length === 0) {
    return (
      <div className="glass-card p-5 rounded-2xl border border-slate-800">
        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
          Sanitized Target Content
        </h4>
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-sm text-slate-300 font-mono leading-relaxed whitespace-pre-wrap">
          {originalText}
        </div>
        <p className="text-xs text-emerald-400 mt-2 flex items-center space-x-1.5">
          <span>✓</span>
          <span>No highlighted high-risk lure phrases detected in this sample.</span>
        </p>
      </div>
    );
  }

  // Find occurrences of red flag texts
  // Sort red flags by longest match first to avoid partial conflicts
  const sortedFlags = [...redFlags].sort((a, b) => b.text.length - a.text.length);

  // Build segmented elements
  const renderHighlightedSegments = () => {
    let segments: Array<{ text: string; flag?: RedFlagItem }> = [{ text: originalText }];

    for (const rf of sortedFlags) {
      const newSegments: Array<{ text: string; flag?: RedFlagItem }> = [];
      for (const seg of segments) {
        if (seg.flag) {
          newSegments.push(seg);
          continue;
        }
        const lowerSeg = seg.text.toLowerCase();
        const lowerTarget = rf.text.toLowerCase();
        let startIndex = lowerSeg.indexOf(lowerTarget);

        if (startIndex === -1) {
          newSegments.push(seg);
        } else {
          let currText = seg.text;
          while (startIndex !== -1) {
            const before = currText.substring(0, startIndex);
            const matched = currText.substring(startIndex, startIndex + rf.text.length);
            currText = currText.substring(startIndex + rf.text.length);

            if (before) newSegments.push({ text: before });
            newSegments.push({ text: matched, flag: rf });

            startIndex = currText.toLowerCase().indexOf(lowerTarget);
          }
          if (currText) newSegments.push({ text: currText });
        }
      }
      segments = newSegments;
    }

    return segments.map((seg, idx) => {
      if (!seg.flag) {
        return <span key={idx}>{seg.text}</span>;
      }

      const isHigh = seg.flag.severity === "high";
      const highlightClasses = isHigh
        ? "bg-red-500/25 text-red-200 border-b-2 border-red-500 px-1 py-0.5 rounded cursor-pointer hover:bg-red-500/40 transition-colors"
        : "bg-amber-500/20 text-amber-200 border-b-2 border-amber-500 px-1 py-0.5 rounded cursor-pointer hover:bg-amber-500/35 transition-colors";

      return (
        <mark
          key={idx}
          onClick={() => setActiveTooltip(seg.flag || null)}
          onMouseEnter={() => setActiveTooltip(seg.flag || null)}
          className={highlightClasses}
          title={`${seg.flag.reason} (${seg.flag.severity} severity)`}
        >
          {seg.text}
        </mark>
      );
    });
  };

  return (
    <div className="glass-card p-6 rounded-2xl border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-red-400" />
          <h3 className="text-base font-bold text-white tracking-wide">
            Deconstructive Red-Flag Highlight
          </h3>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 font-semibold">
          {redFlags.length} Flagged Snippet{redFlags.length > 1 ? "s" : ""}
        </span>
      </div>

      <p className="text-xs text-slate-400 mb-3">
        Hover or click on highlighted snippets to inspect the psychological or technical deception trigger.
      </p>

      {/* Main highlighted text box */}
      <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/80 text-sm text-slate-200 font-mono leading-relaxed whitespace-pre-wrap">
        {renderHighlightedSegments()}
      </div>

      {/* Tooltip / Explanation Inspector */}
      {activeTooltip && (
        <div className="mt-4 p-3.5 rounded-xl bg-slate-800/90 border border-slate-700 text-xs flex items-start space-x-3 transition-all animate-fadeIn">
          <AlertCircle className={`w-4 h-4 mt-0.5 shrink-0 ${activeTooltip.severity === 'high' ? 'text-red-400' : 'text-amber-400'}`} />
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <span className="font-mono font-bold text-white bg-slate-700 px-1.5 py-0.5 rounded">
                &ldquo;{activeTooltip.text}&rdquo;
              </span>
              <span className={`text-[10px] font-bold uppercase px-1.5 py-0.2 rounded ${activeTooltip.severity === 'high' ? 'bg-red-500/20 text-red-300' : 'bg-amber-500/20 text-amber-300'}`}>
                {activeTooltip.severity} risk
              </span>
            </div>
            <p className="text-slate-300 mt-1 font-sans">{activeTooltip.reason}</p>
          </div>
        </div>
      )}
    </div>
  );
};
