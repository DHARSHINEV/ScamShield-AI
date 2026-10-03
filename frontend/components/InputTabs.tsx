"use client";

import React, { useState, useRef } from "react";
import { 
  MessageSquare, 
  Link2, 
  Image as ImageIcon, 
  QrCode, 
  Mic, 
  Upload, 
  X, 
  Zap, 
  ShieldCheck, 
  Info,
  Play
} from "lucide-react";
import { DemoCase } from "@/lib/api";

export type AnalysisMode = "message" | "url" | "screenshot" | "qr" | "voice";

interface InputTabsProps {
  mode: AnalysisMode;
  setMode: (mode: AnalysisMode) => void;
  textInput: string;
  setTextInput: (text: string) => void;
  urlInput: string;
  setUrlInput: (url: string) => void;
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  voiceTranscript: string;
  setVoiceTranscript: (t: string) => void;
  demoCases: DemoCase[];
  onSelectDemo: (demo: DemoCase) => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

export const InputTabs: React.FC<InputTabsProps> = ({
  mode,
  setMode,
  textInput,
  setTextInput,
  urlInput,
  setUrlInput,
  selectedFile,
  setSelectedFile,
  voiceTranscript,
  setVoiceTranscript,
  demoCases,
  onSelectDemo,
  onAnalyze,
  isLoading
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setSelectedFile(f);
      if (f.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = () => setFilePreview(reader.result as string);
        reader.readAsDataURL(f);
      } else {
        setFilePreview(null);
      }
    }
  };

  const clearCurrentInput = () => {
    setTextInput("");
    setUrlInput("");
    setSelectedFile(null);
    setFilePreview(null);
    setVoiceTranscript("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const isAnalyzeDisabled = () => {
    if (isLoading) return true;
    if (mode === "message") return textInput.trim().length < 3;
    if (mode === "url") return urlInput.trim().length < 3;
    if (mode === "screenshot" || mode === "qr") return !selectedFile;
    if (mode === "voice") return !selectedFile && voiceTranscript.trim().length < 3;
    return false;
  };

  return (
    <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl relative">
      
      {/* Tab Navigation */}
      <div className="flex flex-wrap items-center gap-2 pb-5 border-b border-slate-800">
        <button
          onClick={() => { setMode("message"); clearCurrentInput(); }}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            mode === "message"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
              : "text-slate-400 hover:text-white hover:bg-slate-800/60"
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Message / SMS</span>
        </button>

        <button
          onClick={() => { setMode("url"); clearCurrentInput(); }}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            mode === "url"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
              : "text-slate-400 hover:text-white hover:bg-slate-800/60"
          }`}
        >
          <Link2 className="w-4 h-4" />
          <span>URL / Link</span>
        </button>

        <button
          onClick={() => { setMode("screenshot"); clearCurrentInput(); }}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            mode === "screenshot"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
              : "text-slate-400 hover:text-white hover:bg-slate-800/60"
          }`}
        >
          <ImageIcon className="w-4 h-4" />
          <span>Screenshot (OCR)</span>
        </button>

        <button
          onClick={() => { setMode("qr"); clearCurrentInput(); }}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            mode === "qr"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
              : "text-slate-400 hover:text-white hover:bg-slate-800/60"
          }`}
        >
          <QrCode className="w-4 h-4" />
          <span>QR Code</span>
        </button>

        <button
          onClick={() => { setMode("voice"); clearCurrentInput(); }}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            mode === "voice"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
              : "text-slate-400 hover:text-white hover:bg-slate-800/60"
          }`}
        >
          <Mic className="w-4 h-4" />
          <span>Voice / Transcript</span>
        </button>
      </div>

      {/* Quick Demo Preloads */}
      <div className="pt-4 pb-3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1">
            <Zap className="w-3 h-3 text-amber-400 fill-current" />
            <span>Judge Demo Cases (Simulated Scenarios — Click to Test)</span>
          </span>
          <span className="text-[10px] text-amber-300/80 font-mono">Simulated Examples</span>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {demoCases.map((dc) => (
            <button
              key={dc.id}
              onClick={() => onSelectDemo(dc)}
              className="text-xs px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-colors flex items-center space-x-1"
            >
              <span>{dc.title.includes("Safe") ? "🛡️" : "🚨"}</span>
              <span>{dc.title.split("(")[0]}</span>
              <span className="text-[9px] text-slate-400 uppercase tracking-tight">[Simulated]</span>
            </button>
          ))}
        </div>
      </div>

      {/* Input Area by Mode */}
      <div className="mt-2">
        {mode === "message" && (
          <div className="relative">
            <textarea
              rows={4}
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Paste suspicious SMS, WhatsApp message, email excerpt, or job offer here...&#10;e.g. 🚨 SBI ALERT: Your account will be blocked today. Verify your KYC immediately: https://sbi-verify-secure.xyz"
              className="w-full p-4 rounded-2xl bg-slate-900/90 border border-slate-700/80 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono leading-relaxed resize-none shadow-inner"
            />
            {textInput && (
              <button
                onClick={clearCurrentInput}
                className="absolute top-3 right-3 p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800/80 hover:bg-slate-700"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        )}

        {mode === "url" && (
          <div className="relative">
            <input
              type="text"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              placeholder="Paste suspicious website or link... e.g. https://sbi-verify-secure.xyz or http://192.168.1.100/login"
              className="w-full p-4 rounded-2xl bg-slate-900/90 border border-slate-700/80 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono shadow-inner"
            />
            {urlInput && (
              <button
                onClick={clearCurrentInput}
                className="absolute top-3.5 right-3 p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800/80 hover:bg-slate-700"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        )}

        {(mode === "screenshot" || mode === "qr") && (
          <div className="space-y-3">
            <div
              onClick={() => fileInputRef.current?.click()}
              className="cursor-pointer border-2 border-dashed border-slate-700 hover:border-cyan-500/60 rounded-2xl p-6 text-center bg-slate-900/60 transition-all hover:bg-slate-900/80 flex flex-col items-center justify-center min-h-[140px]"
            >
              <Upload className="w-8 h-8 text-cyan-400 mb-2" />
              <div className="text-xs font-semibold text-slate-200">
                {selectedFile ? selectedFile.name : `Click to select or drop ${mode === "qr" ? "QR Code" : "Screenshot"} image`}
              </div>
              <p className="text-[11px] text-slate-400 mt-1">
                Supported formats: PNG, JPG, JPEG, WEBP (Max 10 MB)
              </p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
            />

            {filePreview && (
              <div className="relative inline-block mt-2 rounded-xl overflow-hidden border border-slate-700 max-h-40">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={filePreview} alt="Preview" className="h-40 object-contain rounded-xl" />
                <button
                  onClick={clearCurrentInput}
                  className="absolute top-2 right-2 p-1 rounded-full bg-slate-900/90 text-white hover:bg-red-600"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            )}
          </div>
        )}

        {mode === "voice" && (
          <div className="space-y-3">
            <div
              onClick={() => fileInputRef.current?.click()}
              className="cursor-pointer border-2 border-dashed border-slate-700 hover:border-cyan-500/60 rounded-2xl p-5 text-center bg-slate-900/60 transition-all flex flex-col items-center justify-center"
            >
              <Mic className="w-7 h-7 text-cyan-400 mb-1.5" />
              <div className="text-xs font-semibold text-slate-200">
                {selectedFile ? selectedFile.name : "Select or Drop Audio Note (.wav, .mp3, .ogg)"}
              </div>
              <p className="text-[11px] text-slate-400 mt-0.5">
                Local Speech Pipeline with graceful acoustic fallback
              </p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              onChange={handleFileChange}
              className="hidden"
            />

            {/* Transcript input fallback for demo reliability */}
            <div>
              <label className="text-[11px] text-slate-400 font-semibold block mb-1">
                Audio Transcript (Demo Fallback / Manual Input):
              </label>
              <textarea
                rows={2}
                value={voiceTranscript}
                onChange={(e) => setVoiceTranscript(e.target.value)}
                placeholder="Or paste speech transcript here (e.g. 'Hello sir, this is Delhi Airport customs. You are placed under digital arrest...')"
                className="w-full p-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>
        )}
      </div>

      {/* Bottom Action Bar */}
      <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-800/80">
        
        {/* Safety Notice */}
        <div className="flex items-center space-x-2 text-[11px] text-slate-400">
          <Info className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
          <span>Never submit real passwords, OTPs, recovery codes, or banking PINs.</span>
        </div>

        {/* CTA Analyze Button */}
        <button
          onClick={onAnalyze}
          disabled={isAnalyzeDisabled()}
          className="w-full sm:w-auto px-8 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-cyan-500 via-sky-400 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 shadow-lg shadow-cyan-500/25 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:pointer-events-none"
        >
          <ShieldCheck className="w-4 h-4 text-slate-950" />
          <span>Analyze with ScamShield</span>
        </button>

      </div>
    </div>
  );
};
